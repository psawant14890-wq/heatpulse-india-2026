-- ═══════════════════════════════════════════════════════════════════════════
-- HeatPulse India 2026 — Core SQL Analysis
-- Target: PostgreSQL (local) / BigQuery (cloud migration ready)
-- ═══════════════════════════════════════════════════════════════════════════
-- BigQuery migration note: Replace EXTRACT(DOW FROM date) with 
-- EXTRACT(DAYOFWEEK FROM date). All other syntax is standard SQL.
-- ═══════════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 1: State Heat Risk Ranking (window function + composite score)
-- Business question: Which states need priority Heat Action Plan investment?
-- ─────────────────────────────────────────────────────────────────────────────
WITH risk_ranked AS (
    SELECT
        state,
        region,
        peak_temp_2026,
        temp_anomaly_2026,
        heatwave_days_2026,
        heat_risk_score,
        risk_tier,
        economic_loss_2026_usd_mn,
        heatstroke_cases_2026,
        population_mn,
        RANK() OVER (ORDER BY heat_risk_score DESC)                          AS national_risk_rank,
        RANK() OVER (PARTITION BY region ORDER BY heat_risk_score DESC)      AS regional_risk_rank,
        ROUND(heatstroke_cases_2026::NUMERIC / population_mn, 1)             AS cases_per_million,
        ROUND(economic_loss_2026_usd_mn / population_mn, 2)                 AS loss_per_capita_usd,
        SUM(economic_loss_2026_usd_mn) OVER ()                               AS national_total_loss_usd_mn,
        ROUND(economic_loss_2026_usd_mn /
              SUM(economic_loss_2026_usd_mn) OVER () * 100, 2)              AS pct_of_national_loss
    FROM heatpulse_states
),
cumulative AS (
    SELECT *,
        SUM(pct_of_national_loss) OVER (ORDER BY national_risk_rank)        AS cumulative_loss_pct
    FROM risk_ranked
)
SELECT
    national_risk_rank,
    state,
    region,
    risk_tier,
    ROUND(heat_risk_score, 1)           AS heat_risk_score,
    peak_temp_2026                      AS peak_c,
    temp_anomaly_2026                   AS anomaly_c,
    heatwave_days_2026                  AS hw_days,
    ROUND(economic_loss_2026_usd_mn)    AS econ_loss_usd_mn,
    cases_per_million,
    pct_of_national_loss,
    ROUND(cumulative_loss_pct, 1)       AS cumulative_loss_pct
FROM cumulative
ORDER BY national_risk_rank;


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 2: Year-over-Year Heatwave Escalation (trend analysis)
-- Business question: Is heat becoming structural or episodic?
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    year,
    peak_temp_india,
    heatwave_days_avg,
    national_peak_demand_gw,
    labour_hours_lost_bn,
    economic_loss_usd_bn,
    hottest_city,
    onset_month,
    -- Year-over-year growth rates
    ROUND(
        (national_peak_demand_gw - LAG(national_peak_demand_gw) OVER (ORDER BY year))
        / LAG(national_peak_demand_gw) OVER (ORDER BY year) * 100, 1
    ) AS demand_yoy_pct,
    ROUND(
        (economic_loss_usd_bn - LAG(economic_loss_usd_bn) OVER (ORDER BY year))
        / LAG(economic_loss_usd_bn) OVER (ORDER BY year) * 100, 1
    ) AS econ_loss_yoy_pct,
    ROUND(
        (labour_hours_lost_bn - LAG(labour_hours_lost_bn) OVER (ORDER BY year))
        / LAG(labour_hours_lost_bn) OVER (ORDER BY year) * 100, 1
    ) AS labour_hours_yoy_pct,
    -- 3-year rolling average (structural trend)
    ROUND(AVG(peak_temp_india) OVER (ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2)
        AS rolling_3yr_peak_temp,
    ROUND(AVG(economic_loss_usd_bn) OVER (ORDER BY year ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 1)
        AS rolling_3yr_econ_loss
FROM heatpulse_yearly
ORDER BY year;


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 3: Power Grid Demand vs Temperature Correlation
-- Business question: At what temperature does the grid enter critical stress?
-- ─────────────────────────────────────────────────────────────────────────────
WITH daily_grid AS (
    SELECT
        date,
        peak_demand_gw,
        avg_temp_c,
        solar_supply_gw,
        demand_deficit_gw,
        CASE
            WHEN peak_demand_gw >= 265 THEN 'Critical (≥265 GW)'
            WHEN peak_demand_gw >= 255 THEN 'High Stress (255–265 GW)'
            WHEN peak_demand_gw >= 240 THEN 'Elevated (240–255 GW)'
            ELSE 'Normal (<240 GW)'
        END AS stress_level,
        ROUND(avg_temp_c::NUMERIC, 0) AS temp_bucket
    FROM heatpulse_grid
),
temp_demand_agg AS (
    SELECT
        temp_bucket,
        COUNT(*) AS days_at_temp,
        ROUND(AVG(peak_demand_gw)::NUMERIC, 2) AS avg_demand_gw,
        ROUND(MAX(peak_demand_gw)::NUMERIC, 2) AS max_demand_gw,
        ROUND(AVG(demand_deficit_gw)::NUMERIC, 3) AS avg_deficit_gw,
        COUNT(CASE WHEN demand_deficit_gw > 0 THEN 1 END) AS deficit_days
    FROM daily_grid
    GROUP BY temp_bucket
)
SELECT
    temp_bucket,
    days_at_temp,
    avg_demand_gw,
    max_demand_gw,
    avg_deficit_gw,
    deficit_days,
    -- Regression-implied demand at each temp (slope from data)
    ROUND(
        180.2 + (temp_bucket * 2.14), 2
    ) AS regression_demand_gw
    -- Note: slope 2.14 GW/°C computed in Python analysis (see notebooks/)
FROM temp_demand_agg
ORDER BY temp_bucket;


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 4: Sector Economic Impact — where is money actually lost?
-- Business question: Which sectors need priority cooling/protection spend?
-- ─────────────────────────────────────────────────────────────────────────────
SELECT
    sector,
    workers_mn_india,
    share_of_outdoor_workforce_pct,
    productivity_loss_per_degree_pct,
    avg_daily_wage_inr,
    income_loss_usd_bn_2026,
    ROUND(income_loss_usd_bn_2026 / workers_mn_india, 3)
        AS loss_per_worker_usd_thousands,
    RANK() OVER (ORDER BY income_loss_usd_bn_2026 DESC)
        AS priority_rank,
    ROUND(income_loss_usd_bn_2026 / SUM(income_loss_usd_bn_2026) OVER () * 100, 1)
        AS pct_of_total_loss,
    SUM(income_loss_usd_bn_2026) OVER (ORDER BY income_loss_usd_bn_2026 DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
        AS cumulative_loss_usd_bn
FROM heatpulse_sectors
ORDER BY income_loss_usd_bn_2026 DESC;


-- ─────────────────────────────────────────────────────────────────────────────
-- QUERY 5: Top-5 Priority States for Intervention (final recommendation)
-- Business question: Where should $1B of adaptation spend go first?
-- ─────────────────────────────────────────────────────────────────────────────
WITH intervention_score AS (
    SELECT
        state,
        region,
        heat_risk_score,
        risk_tier,
        economic_loss_2026_usd_mn,
        gdp_at_risk_high_usd_mn,
        informal_workforce_pct,
        heatstroke_cases_2026,
        population_mn,
        -- ROI proxy: loss prevented per $ of intervention
        -- Higher informal workforce + higher loss = higher intervention ROI
        ROUND(
            (economic_loss_2026_usd_mn * informal_workforce_pct / 100)
            / (population_mn * 1.0), 2
        ) AS intervention_roi_proxy,
        NTILE(5) OVER (ORDER BY heat_risk_score DESC) AS risk_quintile
    FROM heatpulse_states
)
SELECT
    RANK() OVER (ORDER BY intervention_roi_proxy DESC) AS investment_priority,
    state,
    region,
    risk_tier,
    ROUND(heat_risk_score, 1) AS heat_risk_score,
    ROUND(economic_loss_2026_usd_mn) AS econ_loss_usd_mn,
    ROUND(gdp_at_risk_high_usd_mn) AS gdp_at_risk_2030_usd_mn,
    heatstroke_cases_2026,
    ROUND(intervention_roi_proxy, 2) AS roi_proxy
FROM intervention_score
WHERE risk_quintile = 1   -- Top 20% by risk
ORDER BY intervention_priority
LIMIT 5;
