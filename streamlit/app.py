"""
HeatPulse India 2026 — Interactive Streamlit Dashboard (Plotly)
===============================================================
All charts are fully interactive: zoom, hover, filter, click.
Deploy: share.streamlit.io → repo: heatpulse-india-2026 → main file: streamlit/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json, os

# ── Path resolution ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, '..'))
DATA = os.path.join(ROOT, 'data', 'processed')
OUT  = os.path.join(ROOT, 'outputs')

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HeatPulse India 2026",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0F1117; }
    [data-testid="stSidebar"] { background-color: #1A1A2E; }
    h1 { color: #FF4B4B !important; }
    h2, h3 { color: #FF7F0E !important; }
    .metric-card {
        background: #1A1A2E; border-left: 3px solid #FF4B4B;
        border-radius: 8px; padding: 16px; margin: 4px 0;
    }
    .metric-val { font-size: 2rem; font-weight: bold; color: #FF4B4B; }
    .metric-lbl { font-size: 0.75rem; color: #AAA; text-transform: uppercase; letter-spacing: 1px; }
    .metric-sub { font-size: 0.8rem; color: #FF7F0E; }
    .insight { background:#1A1A2E; border-left:4px solid #FF4B4B; padding:12px; border-radius:6px; margin:8px 0; }
    .recommend { background:#0D2137; border-left:4px solid #00D4AA; padding:12px; border-radius:6px; margin:8px 0; }
    .warning { background:#2D1500; border-left:4px solid #FFD700; padding:12px; border-radius:6px; margin:8px 0; }
    p, li { color: #FAFAFA !important; }
</style>
""", unsafe_allow_html=True)

COLORS = {
    "critical":  "#D62728", "very_high": "#FF7F0E",
    "high":      "#FFBB78", "moderate":  "#AEC7E8",
    "teal":      "#00D4AA", "navy":      "#0D1B2A",
    "bg":        "#0F1117", "card_bg":   "#1A1A2E",
    "text":      "#FAFAFA", "muted":     "#94A3B8",
}

PLOTLY_THEME = dict(
    paper_bgcolor="#0F1117", plot_bgcolor="#1A1A2E",
    font=dict(color="#FAFAFA", family="Arial"),
    xaxis=dict(gridcolor="#2A2A3A", linecolor="#2A2A3A"),
    yaxis=dict(gridcolor="#2A2A3A", linecolor="#2A2A3A"),
)

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    states  = pd.read_csv(f"{DATA}/heatpulse_states.csv")
    grid    = pd.read_csv(f"{DATA}/heatpulse_grid.csv", parse_dates=["date"])
    yearly  = pd.read_csv(f"{DATA}/heatpulse_yearly.csv")
    sectors = pd.read_csv(f"{DATA}/heatpulse_sectors.csv")
    sens    = pd.read_csv(f"{DATA}/heatpulse_sensitivity.csv")
    with open(f"{OUT}/analysis_results.json") as f:
        results = json.load(f)
    return states, grid, yearly, sectors, sens, results

states, grid, yearly, sectors, sens, results = load()

# Add stress level column
grid["stress_level"] = pd.cut(
    grid["peak_demand_gw"],
    bins=[0, 240, 255, 265, 999],
    labels=["Normal (<240 GW)", "Elevated (240–255 GW)",
            "High Stress (255–265 GW)", "Critical (≥265 GW)"]
)

tier_color_map = {
    "Critical":  COLORS["critical"],
    "Very High": COLORS["very_high"],
    "High":      COLORS["high"],
    "Moderate":  COLORS["moderate"],
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔥 HeatPulse India 2026")
    st.markdown("*Interactive Heat Stress Analytics*")
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
    st.markdown("**Heat Risk Score** (0–100)\n- Severity 35%\n- Economic Exposure 35%\n- Vulnerability 30%")
    st.divider()
    st.markdown("**Data Sources**")
    st.markdown("- IMD press releases\n- Grid-India PSP reports\n- Lancet Countdown 2024\n- Carnegie Endowment 2026\n- ILO / McKinsey / World Bank")
    st.caption("52/52 tests passing | Python 3.12")

def metric_card(label, value, sub=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-lbl">{label}</div>
        <div class="metric-val">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: EXECUTIVE OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if page == "📊 Executive Overview":
    st.title("🔥 HeatPulse India 2026")
    st.markdown("#### Heat Stress Analytics — India's Record-Breaking Summer")

    st.markdown('<div class="insight"><b>Situation:</b> India\'s Summer 2026 was the third consecutive record season. On May 22, India held 97 of the world\'s 100 hottest cities. Peak grid demand hit an all-time record of <b>270.82 GW</b> on May 21 — surpassing 2024 by +20.82 GW (+8.3%).</div>', unsafe_allow_html=True)
    st.markdown('<div class="recommend"><b>Recommendation:</b> Prioritise Heat Action Plan investment in 5 Critical/Very High states (Odisha, Chhattisgarh, Jharkhand, Rajasthan, MP) — 34% of national loss in 12% of population. Estimated 50:1 ROI on $1B adaptation spend.</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning"><b>Policy Gap:</b> Heatwaves are NOT classified as natural disasters under India\'s Disaster Management Act 2005 — blocking formal relief fund flows.</div>', unsafe_allow_html=True)

    # KPI row
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: metric_card("Peak Grid Demand", "270.82 GW", "+20.82 vs 2024")
    with c2: metric_card("Economic Loss", "$194B", "+8.3% vs 2024")
    with c3: metric_card("Labour Hours Lost", "247B hrs", "3rd record year")
    with c4: metric_card("Hottest Point", "48.2°C", "Sri Ganganagar, RJ")
    with c5: metric_card("Critical States", "2", "Odisha & Chhattisgarh")
    with c6: metric_card("Jobs at Risk '30", "34M", "ILO base case")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Grid Demand Timeline — Apr–May 2026")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=grid["date"], y=grid["peak_demand_gw"],
            mode="lines", name="Peak Demand",
            line=dict(color=COLORS["critical"], width=2.5),
            hovertemplate="<b>%{x|%b %d}</b><br>Demand: %{y:.2f} GW<extra></extra>"
        ))
        fig.add_hline(y=260, line_dash="dash", line_color="#FFD700",
                      annotation_text="Stress Threshold (260 GW)",
                      annotation_font_color="#FFD700")
        fig.add_hline(y=270.82, line_dash="dot", line_color=COLORS["critical"],
                      annotation_text="All-time record 270.82 GW",
                      annotation_font_color=COLORS["critical"])
        fig.add_vline(x="2026-04-25", line_dash="dot", line_color=COLORS["very_high"],
                      annotation_text="Apr 25: 256.11 GW", annotation_font_size=9)
        fig.add_vline(x="2026-05-21", line_dash="dot", line_color=COLORS["critical"],
                      annotation_text="May 21: Record", annotation_font_size=9)
        fig.update_layout(**PLOTLY_THEME, height=350,
                          xaxis_title="Date", yaxis_title="Peak Demand (GW)",
                          showlegend=False, margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### State Heat Risk Score — All 18 States")
        df_sorted = states.sort_values("heat_risk_score", ascending=True)
        colors_bar = [tier_color_map.get(t, COLORS["moderate"]) for t in df_sorted["risk_tier"]]
        fig2 = go.Figure(go.Bar(
            x=df_sorted["heat_risk_score"],
            y=df_sorted["state"],
            orientation="h",
            marker_color=colors_bar,
            text=df_sorted["heat_risk_score"].round(1),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Risk Score: %{x:.1f}<extra></extra>",
        ))
        fig2.update_layout(**PLOTLY_THEME, height=500,
                           xaxis_title="Heat Risk Score (0–100)",
                           xaxis_range=[0, 110],
                           margin=dict(l=0,r=40,t=20,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("##### Economic Loss & Grid Demand — Year-on-Year 2020–2026")
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    bar_colors = [COLORS["moderate"]]*4 + [COLORS["very_high"], COLORS["very_high"], COLORS["critical"]]
    fig3.add_trace(go.Bar(
        x=yearly["year"], y=yearly["economic_loss_usd_bn"],
        name="Economic Loss ($B)", marker_color=bar_colors,
        text=yearly["economic_loss_usd_bn"].apply(lambda x: f"${x:.0f}B"),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Loss: $%{y:.0f}B<extra></extra>"
    ), secondary_y=False)
    fig3.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["national_peak_demand_gw"],
        name="Peak Demand (GW)", mode="lines+markers",
        line=dict(color=COLORS["critical"], width=2),
        marker=dict(size=8),
        hovertemplate="<b>%{x}</b><br>Demand: %{y:.0f} GW<extra></extra>"
    ), secondary_y=True)
    fig3.update_layout(**PLOTLY_THEME, height=320,
                       legend=dict(orientation="h", y=1.1),
                       margin=dict(l=0,r=0,t=30,b=0))
    fig3.update_yaxes(title_text="Economic Loss ($B)", secondary_y=False)
    fig3.update_yaxes(title_text="Peak Demand (GW)", secondary_y=True)
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: STATE RISK ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ State Risk Analysis":
    st.title("🗺️ State-Level Heat Risk Analysis")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tier_filter = st.multiselect("Filter by Risk Tier",
            ["Critical","Very High","High","Moderate"],
            default=["Critical","Very High","High","Moderate"])
    with col_f2:
        region_filter = st.multiselect("Filter by Region",
            sorted(states["region"].unique()),
            default=list(states["region"].unique()))

    filtered = states[
        states["risk_tier"].isin(tier_filter) &
        states["region"].isin(region_filter)
    ].copy()

    col1, col2 = st.columns([3, 2])
    with col1:
        df_s = filtered.sort_values("heat_risk_score", ascending=True)
        colors_s = [tier_color_map.get(t, COLORS["moderate"]) for t in df_s["risk_tier"]]
        fig = go.Figure(go.Bar(
            x=df_s["heat_risk_score"], y=df_s["state"],
            orientation="h", marker_color=colors_s,
            text=df_s["heat_risk_score"].round(1), textposition="outside",
            customdata=np.stack([
                df_s["risk_tier"], df_s["peak_temp_2026"],
                df_s["economic_loss_2026_usd_mn"].round(0),
                df_s["heatstroke_cases_2026"]
            ], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Risk Score: %{x:.1f}<br>"
                "Tier: %{customdata[0]}<br>"
                "Peak Temp: %{customdata[1]}°C<br>"
                "Economic Loss: $%{customdata[2]:,.0f}M<br>"
                "Heatstroke Cases: %{customdata[3]:,}<extra></extra>"
            )
        ))
        fig.update_layout(**PLOTLY_THEME, height=500,
                          xaxis_title="Heat Risk Score",
                          xaxis_range=[0, 110],
                          title="Heat Risk Score by State (hover for details)",
                          margin=dict(l=0,r=40,t=40,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Top 5 Priority States")
        top5 = states.nlargest(5, "heat_risk_score")
        for _, row in top5.iterrows():
            color = tier_color_map.get(row["risk_tier"], COLORS["moderate"])
            st.markdown(f"""
            <div style="background:#1A1A2E;border-left:4px solid {color};
                        padding:10px;margin:6px 0;border-radius:4px;">
            <b style="color:{color}">{row['state']}</b>
            <span style="float:right;color:{color};font-size:1.3em;font-weight:bold">{row['heat_risk_score']:.1f}</span>
            <br><small style="color:#AAA">Peak: {row['peak_temp_2026']}°C |
            Loss: ${row['economic_loss_2026_usd_mn']/1000:.1f}B |
            Cases: {int(row['heatstroke_cases_2026']):,}</small>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### State Data Table (click column headers to sort)")
    display = filtered[[
        "state","region","risk_tier","heat_risk_score",
        "peak_temp_2026","temp_anomaly_2026","heatwave_days_2026",
        "economic_loss_2026_usd_mn","heatstroke_cases_2026",
        "informal_workforce_pct","outdoor_workforce_pct"
    ]].sort_values("heat_risk_score", ascending=False).copy()
    display.columns = ["State","Region","Risk Tier","Risk Score","Peak Temp °C",
                       "Anomaly °C","HW Days","Econ Loss $M","Cases","Informal WF%","Outdoor WF%"]
    display["Econ Loss $M"] = display["Econ Loss $M"].round(0).astype(int)
    st.dataframe(display, use_container_width=True, hide_index=True, height=400)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: GRID & POWER DEMAND
# ════════════════════════════════════════════════════════════════════════════
elif page == "⚡ Grid & Power Demand":
    st.title("⚡ Grid & Power Demand Analysis")

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("All-Time Record", "270.82 GW", "May 21, 2026")
    with c2: metric_card("Apr 25 Record", "256.11 GW", "Previous date record")
    with c3: metric_card("Critical Days (≥265)", f"{(grid['peak_demand_gw']>=265).sum()}", "Days above threshold")
    with c4: metric_card("Peak Deficit", f"{grid['demand_deficit_gw'].max():.2f} GW", "May 22, 2026")

    st.divider()

    # Interactive date range selector
    date_range = st.date_input("Select date range",
        value=(grid["date"].min().date(), grid["date"].max().date()),
        min_value=grid["date"].min().date(),
        max_value=grid["date"].max().date())

    if len(date_range) == 2:
        mask = (grid["date"].dt.date >= date_range[0]) & (grid["date"].dt.date <= date_range[1])
        gf = grid[mask].copy()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Interactive Demand Timeline")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=gf["date"], y=gf["peak_demand_gw"],
                mode="lines+markers", name="Peak Demand",
                line=dict(color=COLORS["critical"], width=2),
                marker=dict(size=5),
                fill="tozeroy", fillcolor="rgba(214,39,40,0.1)",
                hovertemplate="<b>%{x|%b %d, %Y}</b><br>Demand: %{y:.2f} GW<extra></extra>"
            ))
            fig.add_trace(go.Scatter(
                x=gf["date"], y=gf["solar_supply_gw"],
                mode="lines", name="Solar Supply",
                line=dict(color="#FFD700", width=1.5, dash="dot"),
                hovertemplate="Solar: %{y:.2f} GW<extra></extra>"
            ))
            fig.add_hline(y=260, line_dash="dash", line_color="#FFD700",
                          annotation_text="Stress Threshold 260 GW")
            fig.update_layout(**PLOTLY_THEME, height=350,
                              xaxis_title="Date", yaxis_title="GW",
                              legend=dict(orientation="h", y=1.1),
                              margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Period: Max {gf['peak_demand_gw'].max():.2f} GW | Avg {gf['peak_demand_gw'].mean():.2f} GW | Critical days: {(gf['peak_demand_gw']>=265).sum()}")

        with col2:
            st.markdown("##### Temperature vs Demand Correlation")
            slope_val  = results["correlation"]["slope_gw_per_degree"]
            interc_val = results["correlation"]["intercept"]
            x_line = np.linspace(gf["avg_temp_c"].min(), gf["avg_temp_c"].max(), 100)
            y_line = slope_val * x_line + interc_val
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=gf["avg_temp_c"], y=gf["peak_demand_gw"],
                mode="markers",
                marker=dict(color=gf["peak_demand_gw"],
                            colorscale=["#AEC7E8","#FF7F0E","#D62728"],
                            size=8, showscale=False),
                customdata=gf["date"].dt.strftime("%b %d"),
                hovertemplate="<b>%{customdata}</b><br>Temp: %{x:.1f}°C<br>Demand: %{y:.2f} GW<extra></extra>",
                name="Daily observation"
            ))
            fig2.add_trace(go.Scatter(
                x=x_line, y=y_line, mode="lines",
                line=dict(color="#D62728", width=2, dash="dash"),
                name=f"Regression (R²={results['correlation']['r_squared']})",
                hovertemplate="Regression: %{y:.2f} GW<extra></extra>"
            ))
            fig2.add_hline(y=260, line_dash="dash", line_color="#FFD700",
                           annotation_text="Stress Threshold 260 GW")
            fig2.update_layout(**PLOTLY_THEME, height=350,
                               xaxis_title="Avg Temperature (°C)",
                               yaxis_title="Peak Demand (GW)",
                               title=f"R²={results['correlation']['r_squared']} | Slope: {slope_val} GW/°C",
                               legend=dict(orientation="h", y=1.15),
                               margin=dict(l=0,r=0,t=55,b=0))
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("##### Days by Stress Level")
        stress_counts = grid["stress_level"].value_counts().reset_index()
        stress_counts.columns = ["Stress Level", "Days"]
        stress_colors = [COLORS["moderate"], COLORS["high"],
                         COLORS["very_high"], COLORS["critical"]]
        fig3 = px.pie(stress_counts, values="Days", names="Stress Level",
                      hole=0.45, color_discrete_sequence=stress_colors)
        fig3.update_layout(**PLOTLY_THEME, height=300,
                           margin=dict(l=0,r=0,t=20,b=0))
        fig3.update_traces(textinfo="label+percent",
                           hovertemplate="<b>%{label}</b><br>Days: %{value}<br>%{percent}<extra></extra>")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("##### YoY Peak Demand Comparison")
        fig4 = go.Figure()
        yr_colors = [COLORS["moderate"]]*4 + [COLORS["very_high"], COLORS["very_high"], COLORS["critical"]]
        fig4.add_trace(go.Bar(
            x=yearly["year"], y=yearly["national_peak_demand_gw"],
            marker_color=yr_colors, name="Peak Demand",
            text=yearly["national_peak_demand_gw"].apply(lambda x: f"{x:.0f}"),
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>%{y:.1f} GW<extra></extra>"
        ))
        fig4.add_hline(y=270.82, line_dash="dot", line_color=COLORS["critical"],
                       annotation_text="2026 Record: 270.82 GW")
        fig4.update_layout(**PLOTLY_THEME, height=300,
                           yaxis_title="GW", showlegend=False,
                           margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig4, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: ECONOMIC IMPACT
# ════════════════════════════════════════════════════════════════════════════
elif page == "💰 Economic Impact":
    st.title("💰 Economic Impact Analysis")

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Total Economic Loss", "$194B", "2026 national estimate")
    with c2: metric_card("Agriculture Loss", "$71.9B", "37% of total")
    with c3: metric_card("Labour Hours Lost", "247B hrs", "Lancet / Carnegie")
    with c4: metric_card("GDP at Risk 2030", "$182B/yr", "Base case (3.5% GDP)")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Sector Economic Loss — 2026")
        sec_sorted = sectors.sort_values("income_loss_usd_bn_2026", ascending=True)
        fig = go.Figure(go.Bar(
            x=sec_sorted["income_loss_usd_bn_2026"],
            y=sec_sorted["sector"],
            orientation="h",
            marker=dict(
                color=sec_sorted["income_loss_usd_bn_2026"],
                colorscale=[[0,"#AEC7E8"],[0.5,"#FF7F0E"],[1,"#D62728"]],
            ),
            text=sec_sorted["income_loss_usd_bn_2026"].apply(lambda x: f"${x:.1f}B"),
            textposition="outside",
            customdata=np.stack([
                sec_sorted["workers_mn_india"],
                sec_sorted["productivity_loss_per_degree_pct"]
            ], axis=-1),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Loss: $%{x:.1f}B<br>"
                "Workers: %{customdata[0]:.0f}M<br>"
                "Productivity loss/°C: %{customdata[1]}%<extra></extra>"
            )
        ))
        fig.update_layout(**PLOTLY_THEME, height=380,
                          xaxis_title="Income Loss ($B)",
                          xaxis_range=[0, 85],
                          margin=dict(l=0,r=60,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("##### GDP at Risk — 3 Scenarios (2030)")
        scen_colors = [COLORS["moderate"], COLORS["very_high"], COLORS["critical"]]
        fig2 = go.Figure(go.Bar(
            x=sens["scenario"],
            y=sens["gdp_loss_usd_bn_2030"],
            marker_color=scen_colors,
            text=sens.apply(lambda r: f"${r['gdp_loss_usd_bn_2030']:.0f}B\n({r['gdp_loss_pct']*100:.1f}% GDP)", axis=1),
            textposition="outside",
            customdata=np.stack([
                sens["labour_hours_at_risk_bn"],
                sens["jobs_at_risk_mn"],
                sens["assumption"]
            ], axis=-1),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "GDP Loss: $%{y:.0f}B/yr<br>"
                "Labour Hours at Risk: %{customdata[0]:.0f}B<br>"
                "Jobs at Risk: %{customdata[1]:.0f}M<br>"
                "<i>%{customdata[2]}</i><extra></extra>"
            )
        ))
        fig2.update_layout(**PLOTLY_THEME, height=380,
                           yaxis_title="GDP Loss ($B/yr by 2030)",
                           yaxis_range=[0, 280],
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.markdown("##### Economic Loss vs Heat Risk Score (bubble size = population)")

    # Region filter
    region_sel = st.multiselect("Filter by Region",
        sorted(states["region"].unique()),
        default=list(states["region"].unique()),
        key="econ_region")
    econ_states = states[states["region"].isin(region_sel)]

    fig3 = px.scatter(
        econ_states,
        x="heat_risk_score",
        y="economic_loss_2026_usd_mn",
        size="population_mn",
        color="risk_tier",
        color_discrete_map=tier_color_map,
        hover_name="state",
        hover_data={
            "heat_risk_score": ":.1f",
            "economic_loss_2026_usd_mn": ":,.0f",
            "population_mn": ":.1f",
            "risk_tier": True,
            "peak_temp_2026": True,
        },
        labels={
            "heat_risk_score": "Heat Risk Score (North Star Metric)",
            "economic_loss_2026_usd_mn": "Economic Loss 2026 ($M)",
            "population_mn": "Population (M)",
        },
        size_max=60,
    )
    fig3.update_layout(**PLOTLY_THEME, height=420,
                       legend=dict(orientation="h", y=1.05),
                       margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig3, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 5: YEAR-ON-YEAR TREND
# ════════════════════════════════════════════════════════════════════════════
elif page == "📈 Year-on-Year Trend":
    st.title("📈 Year-on-Year Heatwave Escalation")
    st.markdown('<div class="insight">India has seen three consecutive record-breaking summers (2024–2026). The 2025 summer produced India\'s <b>first-ever February heatwave</b>. Onset has shifted from May → April → February over 3 years — structural, not episodic.</div>', unsafe_allow_html=True)

    metric_sel = st.selectbox("Select metric to explore",
        ["economic_loss_usd_bn", "national_peak_demand_gw",
         "labour_hours_lost_bn", "heatwave_days_avg", "peak_temp_india"])

    metric_labels = {
        "economic_loss_usd_bn": "Economic Loss ($B)",
        "national_peak_demand_gw": "Peak Grid Demand (GW)",
        "labour_hours_lost_bn": "Labour Hours Lost (Billion)",
        "heatwave_days_avg": "Avg Heatwave Days",
        "peak_temp_india": "Peak Temperature (°C)",
    }

    bar_colors = [COLORS["moderate"]]*4 + [COLORS["very_high"], COLORS["very_high"], COLORS["critical"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=yearly["year"], y=yearly[metric_sel],
        marker_color=bar_colors, name=metric_labels[metric_sel],
        text=yearly[metric_sel].round(1),
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>" + metric_labels[metric_sel] + ": %{y:.1f}<br>Hottest city: " +
                      yearly["hottest_city"].astype(str) + "<extra></extra>",
        customdata=yearly[["hottest_city","onset_month"]].values
    ))
    fig.update_layout(**PLOTLY_THEME, height=400,
                      yaxis_title=metric_labels[metric_sel],
                      xaxis_title="Year",
                      margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("### Full National Trend Data")
    yd = yearly.copy()
    yd.columns = ["Year","Peak Temp °C","Avg HW Days","Peak Demand GW",
                  "Labour Hrs Lost B","Econ Loss $B","Hottest City","Onset Month"]
    st.dataframe(yd, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### 2030 Grid Demand Projection")
    proj = results["forecasting"]["demand_2030_projected_gw"]
    years_proj = list(range(2026, 2031))
    demand_proj = [270.82 * (1.04**i) for i in range(5)]
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["national_peak_demand_gw"],
        mode="lines+markers", name="Historical",
        line=dict(color=COLORS["critical"], width=2),
        marker=dict(size=8)
    ))
    fig2.add_trace(go.Scatter(
        x=years_proj, y=demand_proj,
        mode="lines+markers", name="Projected (4%/yr)",
        line=dict(color=COLORS["very_high"], width=2, dash="dash"),
        marker=dict(size=8, symbol="diamond"),
        hovertemplate="<b>%{x}</b><br>Projected: %{y:.1f} GW<extra></extra>"
    ))
    fig2.add_hline(y=270.82, line_dash="dot", line_color=COLORS["critical"],
                   annotation_text="2026 Record")
    fig2.update_layout(**PLOTLY_THEME, height=350,
                       yaxis_title="Peak Demand (GW)",
                       legend=dict(orientation="h", y=1.1),
                       margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig2, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 6: SENSITIVITY ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Sensitivity Analysis":
    st.title("🔬 Sensitivity Analysis")
    st.markdown("*MBB Layer: Does the recommendation hold if assumptions change?*")

    st.markdown("### Interactive GDP-at-Risk Explorer")
    gdp_pct = st.slider("Assumed GDP loss % by 2030 (McKinsey range: 2.5%–4.5%)",
                        1.0, 6.0, 3.5, 0.1)
    india_gdp_2030 = 5200.0
    gdp_loss = india_gdp_2030 * gdp_pct / 100

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("GDP Loss 2030", f"${gdp_loss:.0f}B", f"{gdp_pct}% of projected GDP")
    with c2: metric_card("Monthly Loss", f"${gdp_loss/12:.1f}B/mo", "If unmitigated")
    with c3: metric_card("Per Capita", f"${gdp_loss*1000/1450:.0f}", "Per person/year")
    with c4: metric_card("Top-5 State Share", f"${gdp_loss*0.34:.0f}B", "34% concentration")

    st.divider()
    st.markdown("### Three-Scenario Comparison")
    scen_colors = [COLORS["teal"], COLORS["very_high"], COLORS["critical"]]
    fig = make_subplots(rows=1, cols=3,
                        subplot_titles=["GDP Loss ($B/yr)", "Labour Hours at Risk (B)", "Jobs at Risk (M)"])
    for i, (col_name, label) in enumerate([
        ("gdp_loss_usd_bn_2030", "GDP Loss $B"),
        ("labour_hours_at_risk_bn", "Labour Hours B"),
        ("jobs_at_risk_mn", "Jobs at Risk M")
    ]):
        fig.add_trace(go.Bar(
            x=sens["scenario"], y=sens[col_name],
            marker_color=scen_colors,
            text=sens[col_name].round(0).astype(int),
            textposition="outside",
            showlegend=False,
            hovertemplate="<b>%{x}</b><br>" + label + ": %{y:.0f}<extra></extra>"
        ), row=1, col=i+1)
    fig.update_layout(**PLOTLY_THEME, height=380,
                      margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Regression Confidence Intervals")
        st.markdown(f"""
        **Temperature → Grid Demand:**
        - Slope: **{results['correlation']['slope_gw_per_degree']} GW per °C**
        - 95% CI: **{results['correlation']['slope_95ci'][0]} – {results['correlation']['slope_95ci'][1]} GW/°C**
        - R² = {results['correlation']['r_squared']} | p {results['correlation']['p_value']}
        - Critical threshold: **{results['correlation']['critical_threshold_temp_c']}°C**

        **Forecast (10-day holdout):**
        - RMSE: **{results['forecasting']['rmse_test_gw']} GW**
        - MAPE: **{results['forecasting']['mape_test_pct']}%**
        """)
    with col2:
        st.markdown("### Assumptions & Limitations")
        st.markdown("""
        **Data lag:** 2026 granular IMD station data not yet publicly released.
        State figures use confirmed IMD press releases and Grid-India PSP reports.

        **Economic allocation:** State losses allocated proportionally from national
        totals. Uncertainty: ±10–15% per state.

        **What would change the recommendation:** If Bihar heatwave-day count
        was understated, it could displace Jharkhand in top-5. Odisha and
        Chhattisgarh are robust across all scenarios.
        """)
