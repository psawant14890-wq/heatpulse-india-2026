"""
HeatPulse India 2026 — Streamlit Dashboard
===========================================
Deploy to Streamlit Community Cloud:
  1. Push repo to GitHub
  2. Go to share.streamlit.io → New app → select repo
  3. Main file: streamlit/app.py
  4. Live URL: https://heatpulse-india-2026.streamlit.app (example)

Run locally: streamlit run streamlit/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import os
import sys

# ── Path resolution (works both locally and on Streamlit Cloud) ─────────────
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, ".."))  # fixed for Streamlit Cloud
DATA = os.path.join(ROOT, 'data', 'processed')
OUT  = os.path.join(ROOT, 'outputs')

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HeatPulse India 2026",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS (heat-themed dark design) ─────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0F1117; color: #FAFAFA; }
    .stMetric { background: #1A1A2E; border-radius: 8px; padding: 12px; border-left: 3px solid #FF4B4B; }
    .stMetric label { color: #AAA !important; font-size: 12px !important; }
    .stMetric [data-testid="stMetricValue"] { color: #FF4B4B !important; font-size: 28px !important; font-weight: bold; }
    .stMetric [data-testid="stMetricDelta"] { font-size: 12px !important; }
    h1 { color: #FF4B4B !important; font-size: 2.2rem !important; }
    h2 { color: #FF7F0E !important; font-size: 1.4rem !important; }
    h3 { color: #FAFAFA !important; }
    .insight-box { background: #1A1A2E; border-left: 4px solid #FF4B4B;
                   padding: 14px; border-radius: 6px; margin: 10px 0; }
    .recommendation-box { background: #0D2137; border-left: 4px solid #00D4AA;
                          padding: 14px; border-radius: 6px; margin: 10px 0; }
    .warning-box { background: #2D1500; border-left: 4px solid #FFD700;
                   padding: 14px; border-radius: 6px; margin: 10px 0; }
    .sidebar .sidebar-content { background: #1A1A2E; }
    [data-testid="stSidebar"] { background: #1A1A2E; }
</style>
""", unsafe_allow_html=True)

PALETTE = {
    "critical": "#D62728", "very_high": "#FF7F0E",
    "high": "#FFBB78",     "moderate": "#AEC7E8",
    "bg": "#0F1117",       "text": "#FAFAFA",
    "accent": "#FF4B4B",   "grid_line": "#2A2A3A",
    "teal": "#00D4AA",
}

plt.rcParams.update({
    "figure.facecolor": PALETTE["bg"], "axes.facecolor": PALETTE["bg"],
    "axes.edgecolor": PALETTE["grid_line"], "axes.labelcolor": PALETTE["text"],
    "xtick.color": PALETTE["text"], "ytick.color": PALETTE["text"],
    "text.color": PALETTE["text"], "grid.color": PALETTE["grid_line"], "grid.alpha": 0.4,
})

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    states  = pd.read_csv(f"{DATA}/heatpulse_states.csv")
    grid    = pd.read_csv(f"{DATA}/heatpulse_grid.csv", parse_dates=["date"])
    yearly  = pd.read_csv(f"{DATA}/heatpulse_yearly.csv")
    sectors = pd.read_csv(f"{DATA}/heatpulse_sectors.csv")
    sens    = pd.read_csv(f"{DATA}/heatpulse_sensitivity.csv")
    with open(f"{OUT}/analysis_results.json") as f:
        results = json.load(f)
    return states, grid, yearly, sectors, sens, results

states, grid, yearly, sectors, sens, results = load_all()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔥 HeatPulse India 2026")
    st.markdown("*Heat Stress Analytics Dashboard*")
    st.divider()

    page = st.radio("Navigate", [
        "📊 Executive Overview",
        "🗺️ State Risk Analysis",
        "⚡ Grid & Power Demand",
        "💰 Economic Impact",
        "📈 Year-on-Year Trend",
        "🔬 Sensitivity Analysis",
    ])

    st.divider()
    st.markdown("**North Star Metric**")
    st.markdown("""
    **Heat Risk Score** (0–100)
    - Severity 35%
    - Economic Exposure 35%
    - Vulnerability 30%
    """)
    st.divider()
    st.markdown("**Data Sources**")
    st.markdown("""
    - IMD press releases
    - Grid-India PSP reports
    - Lancet Countdown 2024
    - Carnegie Endowment 2026
    - ILO / McKinsey / World Bank
    """)
    st.caption("Build: June 2026 | 52/52 tests passing")

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Overview":
    st.title("🔥 HeatPulse India 2026")
    st.markdown("#### Heat Stress Analytics: Quantifying India's Record-Breaking Summer")

    st.markdown("""
    <div class="insight-box">
    <b>Situation:</b> India's Summer 2026 was the third consecutive record season. On May 22, India held 
    97 of the world's 100 hottest cities. Peak grid demand hit an all-time record of <b>270.82 GW</b> on May 21 — 
    surpassing 2024 by +20.82 GW (+8.3%) in just two years.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="recommendation-box">
    <b>Recommendation:</b> Prioritise Heat Action Plan investment in the 5 Critical/Very High states 
    (Odisha, Chhattisgarh, Jharkhand, Rajasthan, Madhya Pradesh) — where 34% of national economic loss 
    is concentrated in 12% of the population. Estimated 50:1 ROI on $1B targeted adaptation spend.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-box">
    <b>Policy Gap:</b> Heatwaves are NOT classified as natural disasters under India's Disaster Management 
    Act 2005 — blocking formal relief fund flows. Reclassification is the single highest-leverage 
    policy action available.
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    st.markdown("### Key Metrics")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Peak Grid Demand", "270.82 GW", "+20.82 vs 2024", delta_color="inverse")
    c2.metric("Economic Loss", "$194B", "+8.3% vs 2024", delta_color="inverse")
    c3.metric("Labour Hours Lost", "247B hrs", "3rd consecutive record", delta_color="inverse")
    c4.metric("Hottest Point", "48.2°C", "Sri Ganganagar, Rajasthan")
    c5.metric("Critical States", "2", "Odisha & Chhattisgarh", delta_color="inverse")
    c6.metric("Jobs at Risk '30", "34M", "ILO base case", delta_color="inverse")

    st.divider()

    # Two charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Grid Demand Timeline")
        img = plt.imread(f"{OUT}/02_grid_demand_forecast.png")
        st.image(img, use_container_width=True)

    with col2:
        st.markdown("##### State Heat Risk Ranking")
        img = plt.imread(f"{OUT}/04_state_risk_ranking.png")
        st.image(img, use_container_width=True)

    st.markdown("##### Year-on-Year Escalation")
    img = plt.imread(f"{OUT}/03_yoy_escalation.png")
    st.image(img, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: STATE RISK ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ State Risk Analysis":
    st.title("🗺️ State-Level Heat Risk Analysis")

    # Filter by risk tier
    tier_filter = st.multiselect(
        "Filter by Risk Tier",
        ["Critical", "Very High", "High", "Moderate"],
        default=["Critical", "Very High", "High", "Moderate"]
    )
    filtered = states[states["risk_tier"].isin(tier_filter)].copy()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(plt.imread(f"{OUT}/04_state_risk_ranking.png"), use_container_width=True)

    with col2:
        st.markdown("### Top 5 Priority States")
        top5 = states.nlargest(5, "heat_risk_score")
        for _, row in top5.iterrows():
            color = (PALETTE["critical"] if row["risk_tier"] == "Critical"
                     else PALETTE["very_high"] if row["risk_tier"] == "Very High"
                     else PALETTE["high"])
            st.markdown(f"""
            <div style="background:#1A1A2E;border-left:4px solid {color};
                        padding:10px;margin:6px 0;border-radius:4px;">
            <b>{row['state']}</b> &nbsp;
            <span style="color:{color};font-size:1.2em">{row['heat_risk_score']:.1f}</span>
            <br><small>Peak: {row['peak_temp_2026']}°C | 
            Loss: ${row['economic_loss_2026_usd_mn']/1000:.1f}B | 
            Cases: {int(row['heatstroke_cases_2026']):,}</small>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### State-Level Data Table")

    display_cols = ["state", "region", "risk_tier", "heat_risk_score",
                    "peak_temp_2026", "temp_anomaly_2026", "heatwave_days_2026",
                    "economic_loss_2026_usd_mn", "heatstroke_cases_2026",
                    "informal_workforce_pct", "outdoor_workforce_pct"]
    display_df = filtered[display_cols].copy()
    display_df["economic_loss_2026_usd_mn"] = display_df["economic_loss_2026_usd_mn"].round(0)
    display_df = display_df.sort_values("heat_risk_score", ascending=False)
    display_df.columns = ["State", "Region", "Risk Tier", "Risk Score",
                          "Peak Temp (°C)", "Anomaly (°C)", "HW Days 2026",
                          "Econ Loss ($M)", "Heatstroke Cases",
                          "Informal WF %", "Outdoor WF %"]

    def color_tier(val):
        colors = {"Critical": "background-color:#3D0000;color:#FF4B4B",
                  "Very High": "background-color:#3D1A00;color:#FF7F0E",
                  "High": "background-color:#3D3000;color:#FFBB78",
                  "Moderate": "background-color:#001A3D;color:#AEC7E8"}
        return colors.get(val, "")

    styled = display_df.style.map(color_tier, subset=["Risk Tier"])
    st.dataframe(styled, use_container_width=True, height=500)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: GRID & POWER DEMAND
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Grid & Power Demand":
    st.title("⚡ Grid & Power Demand Analysis")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("All-Time Record", "270.82 GW", "May 21, 2026", delta_color="inverse")
    c2.metric("Apr 25 Record", "256.11 GW", "Previous date record")
    c3.metric("Apr 1 Baseline", "214.9 GW", "+26% in 50 days", delta_color="inverse")
    c4.metric("Critical Temp", f"{results['correlation']['critical_threshold_temp_c']}°C",
              "Demand > 260 GW above this")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Demand Forecast vs Actual")
        st.image(plt.imread(f"{OUT}/02_grid_demand_forecast.png"), use_container_width=True)
        st.caption(f"Train RMSE: {results['forecasting']['rmse_train_gw']} GW | "
                   f"Test RMSE: {results['forecasting']['rmse_test_gw']} GW | "
                   f"Test MAPE: {results['forecasting']['mape_test_pct']}%")

    with col2:
        st.markdown("##### Temperature vs Demand Correlation")
        st.image(plt.imread(f"{OUT}/01_temp_demand_correlation.png"), use_container_width=True)
        st.caption(f"R²={results['correlation']['r_squared']} | "
                   f"Slope: {results['correlation']['slope_gw_per_degree']} GW/°C | "
                   f"p{results['correlation']['p_value']}")

    st.divider()
    st.markdown("### Daily Grid Demand Explorer")
    date_range = st.date_input(
        "Select date range",
        value=(grid["date"].min().date(), grid["date"].max().date()),
        min_value=grid["date"].min().date(),
        max_value=grid["date"].max().date(),
    )
    if len(date_range) == 2:
        mask = (grid["date"].dt.date >= date_range[0]) & (grid["date"].dt.date <= date_range[1])
        filtered_grid = grid[mask].copy()

        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(filtered_grid["date"], filtered_grid["peak_demand_gw"],
                color=PALETTE["accent"], lw=2, label="Peak Demand")
        ax.fill_between(filtered_grid["date"], 260, filtered_grid["peak_demand_gw"],
                        where=filtered_grid["peak_demand_gw"] > 260,
                        color=PALETTE["critical"], alpha=0.3, label="Critical Zone (>260 GW)")
        ax.axhline(260, color="#FFD700", lw=1.2, ls="--", alpha=0.7, label="Stress threshold")
        ax.set_xlabel("Date")
        ax.set_ylabel("Peak Demand (GW)")
        ax.legend(fontsize=9, framealpha=0.3)
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        plt.close()

        st.markdown(f"**Period stats:** Max {filtered_grid['peak_demand_gw'].max():.2f} GW | "
                    f"Avg {filtered_grid['peak_demand_gw'].mean():.2f} GW | "
                    f"Days in critical zone: {(filtered_grid['peak_demand_gw'] > 260).sum()}")

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: ECONOMIC IMPACT
# ════════════════════════════════════════════════════════════════════════════
elif page == "💰 Economic Impact":
    st.title("💰 Economic Impact Analysis")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Economic Loss", "$194B", "2026 estimate", delta_color="inverse")
    c2.metric("Agriculture Loss", "$71.9B", "37% of total", delta_color="inverse")
    c3.metric("Labour Hours Lost", "247 Billion", "Lancet / Carnegie 2026", delta_color="inverse")
    c4.metric("GDP at Risk 2030", "$182B/yr", "Base case (3.5% GDP)", delta_color="inverse")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Sector-Level Impact")
        st.image(plt.imread(f"{OUT}/06_sector_impact.png"), use_container_width=True)
    with col2:
        st.markdown("##### Sectors Detail")
        sec_display = sectors[["sector","workers_mn_india","income_loss_usd_bn_2026",
                                "productivity_loss_per_degree_pct"]].copy()
        sec_display.columns = ["Sector", "Workers (M)", "Loss ($B)", "Productivity Loss/°C (%)"]
        sec_display = sec_display.sort_values("Loss ($B)", ascending=False)
        st.dataframe(sec_display, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("**Intervention ROI estimate**")
        st.markdown("""
        A $1B targeted investment in the top-5 states covers:
        - 15,000 community cooling centres (~$50K each)
        - SMS early-warning system for 50M outdoor workers
        - Emergency healthcare surge capacity in Critical-tier districts
        
        Against $66B in projected losses in those 5 states alone → **66:1 ROI**.
        """)

    st.divider()
    st.markdown("### State Economic Loss vs Risk Score")
    fig, ax = plt.subplots(figsize=(12, 5))
    colors_scatter = [PALETTE["critical"] if t == "Critical"
                      else PALETTE["very_high"] if t == "Very High"
                      else PALETTE["high"] if t == "High"
                      else PALETTE["moderate"]
                      for t in states["risk_tier"]]
    scatter = ax.scatter(states["heat_risk_score"],
                         states["economic_loss_2026_usd_mn"] / 1000,
                         c=colors_scatter, s=states["population_mn"] * 2,
                         alpha=0.85, edgecolors="white", linewidths=0.5, zorder=3)
    for _, row in states.iterrows():
        ax.annotate(row["state"],
                    (row["heat_risk_score"], row["economic_loss_2026_usd_mn"]/1000),
                    textcoords="offset points", xytext=(6, 3), fontsize=7.5,
                    color=PALETTE["text"], alpha=0.9)
    ax.set_xlabel("Heat Risk Score (North Star Metric)", fontsize=11)
    ax.set_ylabel("Economic Loss 2026 ($B)", fontsize=11)
    ax.set_title("Economic Loss vs Heat Risk Score\n(Bubble size = population)", fontsize=12, fontweight="bold")
    legend_patches = [
        mpatches.Patch(color=PALETTE["critical"], label="Critical"),
        mpatches.Patch(color=PALETTE["very_high"], label="Very High"),
        mpatches.Patch(color=PALETTE["high"], label="High"),
        mpatches.Patch(color=PALETTE["moderate"], label="Moderate"),
    ]
    ax.legend(handles=legend_patches, framealpha=0.3, fontsize=9)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

# ════════════════════════════════════════════════════════════════════════════
# PAGE 5: YEAR-ON-YEAR TREND
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Year-on-Year Trend":
    st.title("📈 Year-on-Year Heatwave Escalation")

    st.markdown("""
    <div class="insight-box">
    India has seen three consecutive record-breaking summers (2024–2026). The 2025 summer 
    produced India's <b>first-ever February heatwave</b>. The onset window has shifted 
    from May → April → February over 3 years — signalling structural, not episodic, change.
    </div>
    """, unsafe_allow_html=True)

    st.image(plt.imread(f"{OUT}/03_yoy_escalation.png"), use_container_width=True)
    st.divider()
    st.markdown("### National Trend Data")
    yr_display = yearly.copy()
    yr_display.columns = ["Year", "Peak Temp (°C)", "Avg HW Days", "Peak Demand (GW)",
                          "Labour Hrs Lost (B)", "Econ Loss ($B)", "Hottest City", "Onset Month"]
    st.dataframe(yr_display, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 2030 Grid Demand Projection")
    proj_2030 = results["forecasting"]["demand_2030_projected_gw"]
    st.markdown(f"""
    At the current annual demand growth rate of ~4% (IEA India Energy Outlook):
    
    - **2026 record:** 270.82 GW  
    - **2027 projected:** {270.82 * 1.04:.1f} GW  
    - **2028 projected:** {270.82 * 1.04**2:.1f} GW  
    - **2030 projected:** **{proj_2030:.1f} GW**
    
    India's current installed capacity: ~950 GW (March 2026, Ministry of Power).  
    Peak demand breaching **316 GW by 2030** will require significant renewable + storage additions
    beyond the current trajectory.
    """)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 6: SENSITIVITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Sensitivity Analysis":
    st.title("🔬 Sensitivity Analysis")
    st.markdown("*MBB Layer: Does the recommendation hold if assumptions change?*")

    st.image(plt.imread(f"{OUT}/05_sensitivity_analysis.png"), use_container_width=True)
    st.divider()

    st.markdown("### Interactive Scenario Explorer")
    gdp_pct = st.slider(
        "Assumed GDP loss % by 2030 (McKinsey range: 2.5%–4.5%)",
        min_value=1.0, max_value=6.0, value=3.5, step=0.1
    )
    india_gdp_2030 = 5200.0
    gdp_loss = india_gdp_2030 * gdp_pct / 100

    col1, col2, col3 = st.columns(3)
    col1.metric("GDP Loss 2030", f"${gdp_loss:.0f}B", f"{gdp_pct}% of projected GDP")
    col2.metric("Monthly Loss", f"${gdp_loss/12:.1f}B/month", "If unmitigated")
    col3.metric("Per Capita Loss", f"${gdp_loss*1000/1450:.0f}", "Per person/year (pop 1.45B)")

    st.markdown("---")
    st.markdown("### Correlation Confidence Intervals")
    st.markdown(f"""
    **Temperature → Grid Demand regression:**
    - Slope: **{results['correlation']['slope_gw_per_degree']} GW per °C**
    - 95% Confidence Interval: **{results['correlation']['slope_95ci'][0]} – {results['correlation']['slope_95ci'][1]} GW/°C**
    - R² = {results['correlation']['r_squared']} | p {results['correlation']['p_value']}
    - Critical threshold (demand > 260 GW): **{results['correlation']['critical_threshold_temp_c']}°C**

    **Forecast performance (held-out test period, May 22–31):**
    - RMSE: **{results['forecasting']['rmse_test_gw']} GW** ({results['forecasting']['rmse_as_pct_of_mean']}% of mean demand)
    - MAPE: **{results['forecasting']['mape_test_pct']}%** on 10-day holdout
    """)

    st.divider()
    st.markdown("### Assumptions & Limitations")
    st.markdown("""
    **Data lag:** 2026 granular IMD station data not yet publicly released (3–6 month lag).
    State-level figures use confirmed IMD press releases and Grid-India PSP reports.
    
    **Economic allocation:** State losses allocated proportionally from national totals 
    (outdoor workforce × population × heatwave days). Uncertainty: ±10–15% per state.
    
    **What would change the recommendation:** If Bihar's heatwave-day count was understated 
    in available reports, it could displace Jharkhand in the top-5. The recommendation 
    to prioritise Odisha and Chhattisgarh is robust across all scenarios.
    
    **Model limitation:** 0.56% MAPE on a 10-day test window. Short test period limits 
    long-range forecast credibility. A seasonal ARIMA model would improve 3–6 month accuracy.
    """)
