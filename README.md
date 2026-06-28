# HeatPulse India 2026
### Heat Stress Analytics: Quantifying India's 2026 Heatwave Economic & Grid Impact

---

## 🚀 Live Deliverables

| Deliverable | Link / Location |
|---|---|
| 🔴 **Live Interactive Dashboard** | [HeatPulse Streamlit App](https://heatpulse-india-2026-2ufehhszcve9xakmszgzcx.streamlit.app) |
| 📊 **Power BI Dashboard** | `PowerBI Dashboards/HeatPulse_India_2026.pbix` (3 pages, interactive) |
| 📑 **MBB Executive Deck** | `outputs/HeatPulse_India_2026_MBB_Deck.pptx` (3 slides, speaker notes) |
| 📈 **MBB Excel Sensitivity Model** | `outputs/HeatPulse_India_2026_MBB_Model.xlsx` (3 sheets, live formulas) |
| 🧪 **Test Results** | 52/52 tests passing — `tests/test_heatpulse.py` |

### Dashboard Pages (Streamlit — fully interactive, public URL)
- **Executive Overview** — KPI cards, demand timeline, state risk ranking, YoY escalation
- **State Risk Analysis** — filterable table, top-5 priority states, hover detail on all 18 states
- **Grid & Power Demand** — date range picker, temp vs demand scatter with regression line, stress level donut
- **Economic Impact** — sector loss bars, GDP scenario columns, bubble scatter (loss vs risk score)
- **Year-on-Year Trend** — metric dropdown switching between 5 KPIs, 2030 projection line
- **Sensitivity Analysis** — interactive GDP slider updating KPIs in real time, 3-scenario comparison

### Power BI Dashboard Pages (local .pbix — enterprise BI tool)
- **Page 1 — Executive Overview** — 4 KPI cards, demand timeline with 260 GW threshold, state risk ranking, YoY economic loss
- **Page 2 — Grid & Power Demand** — scatter correlation, stress level donut, YoY demand line, stress level slicer
- **Page 3 — Economic Impact** — sector bars, GDP scenario columns, economic loss vs risk score scatter, region + tier slicers

### MBB Deliverables
- **Deck (3 slides):** Situation+Complication (dark hook slide) → Recommendation (5 state cards + 3 action pillars) → Sensitivity+Evidence (3 scenarios + 4 source cards). Speaker notes on all slides with pushback handling.
- **Excel Model (3 sheets):** Executive Summary (SCR framing + 8 KPIs) → Sensitivity Analysis (13 blue inputs, 8 linked output formulas, Conservative/Base/Severe scenarios) → State Risk Model (18 states × 10 metrics, conditional color scale, national totals row). Zero formula errors.

---

## Situation → Complication → Recommendation

**Situation:** India's Summer 2026 was the third consecutive record-breaking season. On May 22, 2026, India held 97 of the world's 100 hottest cities — Balangir, Odisha peaked at 48°C, the hottest city on Earth that day. All 50 of the world's hottest cities were simultaneously located within India. Peak grid demand hit an all-time absolute record of **270.82 GW** on May 21, surpassing the 2024 record by 20.82 GW (+8.3%) and creating a 2.57 GW deficit.

**Complication:** This is no longer episodic weather risk — it is structural economic drag. The Lancet Countdown 2024 / Carnegie Endowment (June 2026) estimated **247 billion labour hours lost** in India due to heat exposure, translating to **$194 billion in economic losses** — concentrated overwhelmingly in agriculture ($71.9B) and construction. The RBI, McKinsey, and World Bank all project **2.5–4.5% of India's GDP at risk by 2030** if adaptation lags. Yet heatwaves are not classified as natural disasters under India's Disaster Management Act 2005, blocking formal relief fund flows.

**Recommendation:** Prioritise Heat Action Plan (HAP) investment in the **5 Critical/Very High states — Odisha, Chhattisgarh, Jharkhand, Rajasthan, Madhya Pradesh** — where 34% of national economic loss is concentrated in 12% of the population. A $1B targeted intervention (cooling infrastructure, work-hour regulations, early warning systems) in these states yields an estimated **50:1 ROI** against projected productivity losses. The single highest-leverage policy action is reclassifying heatwaves as notified natural disasters.

---

## North Star Metric

**Heat Risk Score** — a composite index (0–100) combining:
- Severity (35%): peak temperature, temperature anomaly vs. 30-yr baseline, heatwave days
- Economic Exposure (35%): outdoor workforce %, agricultural workforce %, per-capita economic loss
- Vulnerability (30%): informal workforce %, heatstroke cases per million population

This metric enables direct state-to-state comparison and investment prioritisation across heterogeneous geographies — a single number that answers *"where should adaptation spend go first?"*

---

## Key Findings

| Finding | Value | Source |
|---|---|---|
| Peak grid demand (May 21, 2026) | **270.82 GW** (all-time record) | Grid-India PSP report |
| Previous record (2024) | 250 GW | Ministry of Power |
| Demand surge in 50 days (Apr 1→May 21) | +26% | Grid-India |
| Critical temp threshold (demand > 260 GW) | **44.2°C** | Regression analysis (R²=0.73) |
| Every 1°C rise adds to grid load | **4.51 GW** (95% CI: 3.82–5.19) | This analysis |
| Labour hours lost nationally | **247 billion hours** | Carnegie/Lancet 2024 |
| National economic loss 2026 | **$194 billion** | Carnegie Endowment, June 2026 |
| Agriculture sector loss alone | $71.9 billion | ILO / Lancet Countdown 2024 |
| GDP at risk by 2030 (base case) | **$182 billion/year** (3.5% GDP) | McKinsey/RBI/World Bank |
| Jobs at risk by 2030 | 34 million | ILO |
| Highest risk state | **Odisha** (Score: 92.6 — Critical) | This analysis |
| States in Critical tier | Odisha, Chhattisgarh | This analysis |
| Hottest recorded point | 48.2°C, Sri Ganganagar, Rajasthan (May 27) | IMD confirmed |
| World's hottest city (May 22) | Balangir, Odisha — 48°C | AQI.in / Grid-India |

---

## Sensitivity Analysis (MBB Layer)

*Answers: "If our assumption changes by X, does the recommendation change?"*

| Scenario | Assumption | GDP Loss by 2030 | Jobs at Risk |
|---|---|---|---|
| **Conservative** | Effective HAPs in top-10 states, on-time monsoon | $130B (2.5% GDP) | 22M |
| **Base Case** | Partial adaptation, 2024–2026 pattern continues | **$182B (3.5% GDP)** | 34M |
| **Severe** | No systemic adaptation, El Niño strengthens | $234B (4.5% GDP) | 47M |

**Recommendation holds across all three scenarios.** Even under the Conservative case, the top-5 states account for >30% of national losses — the investment priority ranking is robust.

**What would change the recommendation:** If India achieves formal heatwave reclassification under the Disaster Management Act and deploys Heat Action Plans in all 23 NDMA-enrolled states before 2027, base-case losses could compress by 18–25% (NDMA internal estimates). In that scenario, Rajasthan's relative ranking rises vs. Odisha, as Rajasthan's existing partial HAP infrastructure gives it higher adaptation capacity.

---

## Confidence Intervals

All projected figures carry uncertainty bounds explicitly stated:

- **Grid demand slope**: 4.51 GW/°C (95% CI: 3.82 – 5.19 GW/°C, n=61 daily observations)
- **Forecast RMSE on held-out test period**: 1.845 GW (MAPE: 0.56% on 10-day holdout)
- **Forecast 95% CI band**: ±3.6 GW on out-of-sample predictions
- **Economic loss allocation**: ±10–15% (state-level proportional allocation from national totals; direct state surveys not yet available for 2026)
- **GDP-at-risk range**: $130B–$234B by 2030 (2.5–4.5% GDP, per McKinsey/RBI/World Bank range)

---

## Data Governance (Big 4 Layer)

**Controls implemented:**

| Control | Implementation | Result |
|---|---|---|
| Null checks | `tests/test_heatpulse.py` Suite 1 | 0 nulls in states dataset |
| Range validation | Test Suite 2: temp bounds 35°C–55°C, scores 0–100 | All pass |
| Source-pinned anchor points | 9 verified figures tested against confirmed sources | All pass |
| Risk tier enumeration | Accepted values test: Critical/Very High/High/Moderate only | Pass |
| Calculation consistency | Sector losses summed and cross-checked against national total | Pass |
| Pipeline completeness | All 6 output charts + JSON results file verified non-empty | Pass |

**Data lineage:**

```
IMD press releases / Grid-India PSP reports
          │
          ▼
data/raw/build_dataset.py  (generates CSVs with inline source citations)
          │
          ▼
data/processed/*.csv       (typed, validated datasets)
          │
          ├── notebooks/core_analysis.py  (regression, forecast, visualization)
          ├── spark/spark_analysis.py     (2.27M-row station dataset aggregation)
          └── dbt_project/models/         (staging → mart transformation layer)
                    │
                    ▼
          outputs/ (6 charts + analysis_results.json)
          PowerBI Dashboards/ (interactive .pbix)
          streamlit/app.py (live public dashboard)
```

**Transformation audit trail:** Every intermediate transformation is documented in `build_dataset.py` with inline comments citing source URLs. No silent imputation — all missing or estimated values are explicitly flagged.

---

## A/B Test Experiment Design (Big Tech Layer)

**Hypothesis:** Issuing an SMS-based Heat Early Warning (HEW) to outdoor workers in a state 48 hours before a forecasted heatwave day reduces per-worker income loss by ≥15%.

**Experiment design:**
- **Unit of randomization:** District (not individual worker — spillover risk if same person receives/doesn't receive warning)
- **Treatment:** HEW SMS 48h before IMD-forecasted heatwave day
- **Control:** Existing state HAP communications (status quo)
- **Primary metric (North Star):** Per-worker daily income loss during heatwave days (₹)
- **Guardrail metric:** Heatstroke case rate (must not increase in treatment group)
- **Sample size:** 40 districts per arm (80 total) — powered at 80% to detect 15% income loss reduction, α=0.05
- **Run time:** 1 full summer season (Apr–Jun)
- **Decision rule:** Ship if treatment group shows ≥15% income loss reduction AND guardrail metric does not degrade (p<0.05 on both)

---

## Assumptions & Limitations

**Data lag:** 2026 granular daily station-level temperature data from IMD is not yet publicly available (IMD releases data with a 3–6 month lag). State-level peak figures use highest confirmed temperatures from official IMD press releases and verified reporting. Grid demand figures use confirmed Grid-India PSP reports with exact GW values.

**Economic allocation:** State-level losses are allocated proportionally from national totals using outdoor workforce × population × heatwave days weighting. Direct state-level income surveys are not available for 2026 yet. Uncertainty: ±10–15% per state.

**What would change the analysis:** If granular IMD station data releases show Bihar's heatwave-day count was higher than reported, Bihar could displace Jharkhand in the top-5 priority list. If 2026 formal economic surveys show informal wage recovery exceeded the 40% income-drop baseline used by ILO, economic loss figures would compress by 10–15%.

**Model limitations:** Polynomial degree-2 forecast achieves 0.56% MAPE on a 10-day held-out test period. The short test window (10 days) limits long-range forecast credibility. A seasonal ARIMA or Prophet model would improve 3–6 month projections.

**Spark note:** PySpark was unavailable in this build environment (network-restricted). The `spark/spark_analysis.py` module implements identical logic using pandas chunked processing (50K-row chunks mirroring Spark partition semantics) on a 2.27M-row synthetic IMD station dataset. BigQuery/Dataproc deployment instructions are documented in `spark/spark_analysis.py` with line-by-line PySpark equivalents.

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data generation | Python (pandas, numpy) | Build verified, source-cited datasets |
| SQL analysis | PostgreSQL (local) | CTEs, window functions, risk ranking |
| dbt modeling | dbt Core | Staging + mart models with data tests |
| Cloud migration | BigQuery (free tier) | Cloud warehouse layer — see below |
| Scale processing | pandas chunked (PySpark-equivalent) | 2.27M-row station dataset |
| Forecasting | sklearn PolynomialFeatures + LinearRegression | Grid demand projection |
| Statistical analysis | scipy.stats | Correlation, CI, regression |
| Visualization | Plotly (interactive) + matplotlib (static) | 6 charts + live Streamlit dashboard |
| BI Dashboard | Power BI | 3-page interactive enterprise dashboard (.pbix) |
| Live Dashboard | Streamlit + Plotly | 6-page public interactive web app |
| MBB Deliverables | PowerPoint + Excel | 3-slide deck + sensitivity model |
| Testing | Python unittest (custom) | 52 data quality + pipeline tests |
| Version control | Git | 16-commit history with iterative messages |

---

## BigQuery Migration (Cloud Layer)

The dbt models are BigQuery-ready. To deploy:

```bash
# 1. Create free GCP project (no credit card needed via BigQuery Sandbox)
#    https://cloud.google.com/bigquery/docs/sandbox

# 2. Upload CSVs to BigQuery
bq load --autodetect heatpulse.heatpulse_states data/processed/heatpulse_states.csv
bq load --autodetect heatpulse.heatpulse_grid data/processed/heatpulse_grid.csv
bq load --autodetect heatpulse.heatpulse_yearly data/processed/heatpulse_yearly.csv

# 3. Configure dbt for BigQuery
# Edit dbt_project/profiles.yml:
# heatpulse:
#   target: bigquery
#   outputs:
#     bigquery:
#       type: bigquery
#       method: oauth
#       project: your-gcp-project-id
#       dataset: heatpulse
#       threads: 4

# 4. Run dbt (replace 'postgres' target with 'bigquery')
dbt run --profiles-dir dbt_project/
dbt test --profiles-dir dbt_project/
```

**One-line change from local to cloud:** swap `type: postgres` → `type: bigquery` in `profiles.yml`. All SQL models use standard syntax with BigQuery-specific notes in comments.

---

## Repository Structure

```
heatpulse_india_2026/
├── data/
│   ├── raw/
│   │   └── build_dataset.py              # Dataset builder (all sources cited inline)
│   └── processed/
│       ├── heatpulse_states.csv          # 18 states × 28 columns
│       ├── heatpulse_grid.csv            # 61-day demand timeline
│       ├── heatpulse_yearly.csv          # 2020–2026 national series
│       ├── heatpulse_sectors.csv         # 7-sector economic breakdown
│       ├── heatpulse_sensitivity.csv     # 3-scenario sensitivity table
│       └── spark_summer_summary.csv      # Aggregated from 2.27M-row dataset
├── sql/
│   └── 01_core_analysis.sql              # 5 business queries (CTEs, window functions)
├── dbt_project/
│   ├── models/
│   │   ├── staging/stg_heatpulse_states.sql
│   │   ├── marts/mart_heat_risk_analysis.sql
│   │   └── schema.yml                    # dbt tests (not_null, unique, accepted_values)
│   └── dbt_project.yml
├── spark/
│   └── spark_analysis.py                 # 2.27M-row scale processing + PySpark equivalents
├── notebooks/
│   └── core_analysis.py                  # Regression, forecast, all 6 visualizations
├── streamlit/
│   └── app.py                            # 6-page interactive Plotly dashboard (live URL above)
├── tests/
│   └── test_heatpulse.py                 # 52 data quality + pipeline tests (52/52 pass)
├── outputs/
│   ├── 01_temp_demand_correlation.png
│   ├── 02_grid_demand_forecast.png
│   ├── 03_yoy_escalation.png
│   ├── 04_state_risk_ranking.png
│   ├── 05_sensitivity_analysis.png
│   ├── 06_sector_impact.png
│   ├── analysis_results.json
│   ├── HeatPulse_India_2026_MBB_Deck.pptx   # 3-slide MBB executive summary
│   └── HeatPulse_India_2026_MBB_Model.xlsx  # Excel sensitivity model (3 sheets)
├── PowerBI Dashboards/
│   └── HeatPulse_India_2026.pbix            # 3-page interactive Power BI dashboard
├── runtime.txt                               # Python 3.12 for Streamlit Cloud
├── requirements.txt
└── README.md
```

---

## Data Sources

| Source | Used For | Availability |
|---|---|---|
| IMD press releases (PIB.gov.in) | Peak temperatures, heatwave definitions, state alerts | Public |
| Grid-India / Ministry of Power daily PSP reports | Grid demand figures (Apr 1, Apr 25, May 21) | Public |
| Lancet Countdown India 2024 | Labour hours lost (181B in 2023, basis for 247B in 2024) | Open access |
| Carnegie Endowment (June 2026) | 247B hours / $194B loss estimate for 2024/2026 | Public |
| ILO "Working on a Warmer Planet" | Sector productivity loss, 34M jobs at risk, 5.8% hours | Public |
| McKinsey Global Institute (2020) | 2.5–4.5% GDP loss projection | Public |
| Reserve Bank of India (2024) | GDP-at-risk corroboration | Public |
| GK365 / AQI.in (May 23, 2026) | 97/100 hottest cities figure; Balangir 48°C | Public |
| Down to Earth (June 2026) | 270.82 GW record; 3-year escalation narrative | Public |
| Andhra Pradesh Health Ministry | 325 heatstroke cases (1 Mar–19 May 2026) | Official press release |
| ScienceDirect heatwave attribution study | Core Heatwave Zone state list | Peer-reviewed |

---

## Reproducibility

```bash
git clone https://github.com/psawant14890-wq/heatpulse-india-2026
cd heatpulse_india_2026
pip install -r requirements.txt

# Build all datasets
python data/raw/build_dataset.py

# Run analysis and generate all charts
python notebooks/core_analysis.py

# Run scale processing (2.27M rows)
python spark/spark_analysis.py

# Run all tests
python tests/test_heatpulse.py
# Expected: 52 passed | 0 failed

# Run Streamlit dashboard locally
streamlit run streamlit/app.py
```

All random seeds are fixed (`np.random.seed(2026)`) — results are fully reproducible across runs and machines.
