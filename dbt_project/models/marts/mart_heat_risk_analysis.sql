-- models/marts/mart_heat_risk_analysis.sql
-- ─────────────────────────────────────────────────────────────────────────────
-- Mart: business-ready heat risk table
-- Joins state risk scores with economic impact and intervention prioritization
-- This is the table Power BI / Looker / dashboard connects to directly
-- ─────────────────────────────────────────────────────────────────────────────

WITH states AS (
    SELECT * FROM {{ ref('stg_heatpulse_states') }}
    WHERE data_quality_flag = 'VALID'
),

risk_calculations AS (
    SELECT
        state,
        region,
        peak_temp_2026_c,
        temp_anomaly_2026_c,
        heatwave_days_2024,
        heatwave_days_2025,
        heatwave_days_2026,
        -- Heatwave day trend (2024 to 2026 change)
        heatwave_days_2026 - heatwave_days_2024                 AS hw_days_increase_2yr,
        ROUND(SAFE_DIVIDE(
            heatwave_days_2026 - heatwave_days_2024,
            heatwave_days_2024
        ) * 100, 1)                                             AS hw_days_pct_increase_2yr,

        -- Economic metrics
        economic_loss_2026_usd_mn,
        labour_hours_lost_2026_mn,
        state_gdp_usd_bn_2023,
        population_mn,
        ROUND(economic_loss_2026_usd_mn / population_mn, 2)     AS loss_per_capita_usd,
        ROUND(economic_loss_2026_usd_mn /
              (state_gdp_usd_bn_2023 * 1000) * 100, 2)         AS loss_as_pct_of_state_gdp,

        -- Health metrics
        heatstroke_cases_2026,
        ROUND(SAFE_DIVIDE(
            heatstroke_cases_2026, population_mn
        ), 2)                                                   AS cases_per_million,

        -- Risk composite
        heat_risk_score,
        risk_tier,
        informal_workforce_pct,
        outdoor_workforce_pct,
        latitude,
        longitude,

        -- National ranking
        RANK() OVER (ORDER BY heat_risk_score DESC)             AS national_risk_rank,
        RANK() OVER (PARTITION BY region
                     ORDER BY heat_risk_score DESC)             AS regional_risk_rank,

        -- Cumulative economic concentration
        ROUND(SAFE_DIVIDE(
            economic_loss_2026_usd_mn,
            SUM(economic_loss_2026_usd_mn) OVER ()
        ) * 100, 2)                                             AS pct_of_national_loss,

        SUM(economic_loss_2026_usd_mn) OVER (
            ORDER BY heat_risk_score DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) / SUM(economic_loss_2026_usd_mn) OVER () * 100       AS cumulative_loss_pct,

        -- Intervention ROI proxy (higher = more impact per $ spent)
        ROUND(
            economic_loss_2026_usd_mn * informal_workforce_pct / 100
            / population_mn, 2
        )                                                       AS intervention_roi_proxy

    FROM states
)

SELECT
    national_risk_rank,
    regional_risk_rank,
    state,
    region,
    risk_tier,
    ROUND(heat_risk_score, 1)               AS heat_risk_score,
    peak_temp_2026_c,
    temp_anomaly_2026_c,
    heatwave_days_2026,
    hw_days_increase_2yr,
    hw_days_pct_increase_2yr,
    ROUND(economic_loss_2026_usd_mn, 0)     AS economic_loss_2026_usd_mn,
    ROUND(loss_per_capita_usd, 2)           AS loss_per_capita_usd,
    ROUND(loss_as_pct_of_state_gdp, 2)     AS loss_as_pct_of_state_gdp,
    labour_hours_lost_2026_mn,
    heatstroke_cases_2026,
    cases_per_million,
    population_mn,
    informal_workforce_pct,
    outdoor_workforce_pct,
    pct_of_national_loss,
    ROUND(cumulative_loss_pct, 1)           AS cumulative_loss_pct,
    intervention_roi_proxy,
    latitude,
    longitude
FROM risk_calculations
ORDER BY national_risk_rank
