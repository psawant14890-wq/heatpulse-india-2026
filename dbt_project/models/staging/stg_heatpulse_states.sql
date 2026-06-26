-- models/staging/stg_heatpulse_states.sql
-- ─────────────────────────────────────────────────────────────────────────────
-- Staging: clean, typed view over raw heatpulse_states table
-- BigQuery: upload heatpulse_states.csv to BQ dataset, then run dbt
-- ─────────────────────────────────────────────────────────────────────────────

WITH source AS (
    SELECT * FROM {{ source('heatpulse', 'heatpulse_states') }}
),

cleaned AS (
    SELECT
        -- Identifiers
        CAST(state AS STRING)                       AS state,
        CAST(region AS STRING)                      AS region,

        -- Temperature metrics (validated: all within IMD-confirmed ranges)
        CAST(peak_temp_2026 AS FLOAT64)             AS peak_temp_2026_c,
        CAST(temp_anomaly_2026 AS FLOAT64)          AS temp_anomaly_2026_c,

        -- Heatwave days (3-year series for trend analysis)
        CAST(heatwave_days_2024 AS INT64)           AS heatwave_days_2024,
        CAST(heatwave_days_2025 AS INT64)           AS heatwave_days_2025,
        CAST(heatwave_days_2026 AS INT64)           AS heatwave_days_2026,

        -- Workforce composition
        CAST(informal_workforce_pct AS FLOAT64)     AS informal_workforce_pct,
        CAST(agri_workforce_pct AS FLOAT64)         AS agri_workforce_pct,
        CAST(outdoor_workforce_pct AS FLOAT64)      AS outdoor_workforce_pct,

        -- Economic scale
        CAST(state_gdp_usd_bn_2023 AS FLOAT64)     AS state_gdp_usd_bn_2023,
        CAST(population_mn AS FLOAT64)              AS population_mn,

        -- Health outcomes
        CAST(heatstroke_cases_2026 AS INT64)        AS heatstroke_cases_2026,

        -- Coordinates
        CAST(lat AS FLOAT64)                        AS latitude,
        CAST(lon AS FLOAT64)                        AS longitude,

        -- Derived fields (pass through from build_dataset.py)
        CAST(economic_loss_2026_usd_mn AS FLOAT64)  AS economic_loss_2026_usd_mn,
        CAST(labour_hours_lost_2026_mn AS FLOAT64)  AS labour_hours_lost_2026_mn,
        CAST(heat_risk_score AS FLOAT64)            AS heat_risk_score,
        CAST(risk_tier AS STRING)                   AS risk_tier,

        -- Data quality flag
        CASE
            WHEN peak_temp_2026 IS NULL THEN 'MISSING_TEMP'
            WHEN peak_temp_2026 < 35 OR peak_temp_2026 > 55 THEN 'OUT_OF_RANGE'
            ELSE 'VALID'
        END AS data_quality_flag

    FROM source
    WHERE state IS NOT NULL
)

SELECT * FROM cleaned
