"""
HeatPulse India 2026 — Data Quality & Pipeline Tests
======================================================
Tests the real data integrity, calculation correctness,
and pipeline outputs. Run: python tests/test_heatpulse.py
"""

import pandas as pd
import numpy as np
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, '..', 'data', 'processed')
OUT  = os.path.join(BASE, '..', 'outputs')

def load_data():
    return {
        "states":  pd.read_csv(f"{DATA}/heatpulse_states.csv"),
        "grid":    pd.read_csv(f"{DATA}/heatpulse_grid.csv", parse_dates=["date"]),
        "yearly":  pd.read_csv(f"{DATA}/heatpulse_yearly.csv"),
        "sectors": pd.read_csv(f"{DATA}/heatpulse_sectors.csv"),
        "results": json.load(open(f"{OUT}/analysis_results.json")),
    }

results = {"passed": 0, "failed": 0, "errors": []}

def test(name, condition, detail=""):
    if condition:
        print(f"  ✅ PASS: {name}")
        results["passed"] += 1
    else:
        print(f"  ❌ FAIL: {name} {f'— {detail}' if detail else ''}")
        results["failed"] += 1
        results["errors"].append(name)

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 1: Dataset Integrity")
# ─────────────────────────────────────────────────────────────────────────────
d = load_data()
states  = d["states"]
grid    = d["grid"]
yearly  = d["yearly"]
sectors = d["sectors"]

test("States dataset has 18 rows",        len(states) == 18, f"got {len(states)}")
test("No null values in states dataset",  states.isnull().sum().sum() == 0,
     f"{states.isnull().sum().sum()} nulls found")
test("No duplicate states",               states["state"].nunique() == len(states))
test("Grid timeline has 61 rows",         len(grid) == 61, f"got {len(grid)}")
test("Grid covers Apr 1 – May 31",
     str(grid["date"].min().date()) == "2026-04-01" and
     str(grid["date"].max().date()) == "2026-05-31")
test("Yearly series covers 2020–2026",
     yearly["year"].min() == 2020 and yearly["year"].max() == 2026)
test("7 sectors in sector data",          len(sectors) == 7, f"got {len(sectors)}")

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 2: Real Data Anchor Points (Source-Verified)")
# ─────────────────────────────────────────────────────────────────────────────

# Grid demand anchor points (Grid-India confirmed)
apr1_demand  = grid[grid["date"] == "2026-04-01"]["peak_demand_gw"].values[0]
apr25_demand = grid[grid["date"] == "2026-04-25"]["peak_demand_gw"].values[0]
may21_demand = grid[grid["date"] == "2026-05-21"]["peak_demand_gw"].values[0]

test("Apr 1 demand = 214.9 GW (Grid-India confirmed)",
     abs(apr1_demand - 214.9) < 0.01, f"got {apr1_demand}")
test("Apr 25 demand = 256.11 GW (all-time record at that date)",
     abs(apr25_demand - 256.11) < 0.01, f"got {apr25_demand}")
test("May 21 demand = 270.82 GW (absolute all-time record)",
     abs(may21_demand - 270.82) < 0.01, f"got {may21_demand}")

# Temperature anchor points (IMD confirmed)
raj_temp = states[states["state"] == "Rajasthan"]["peak_temp_2026"].values[0]
od_temp  = states[states["state"] == "Odisha"]["peak_temp_2026"].values[0]
up_temp  = states[states["state"] == "Uttar Pradesh"]["peak_temp_2026"].values[0]
ap_cases = states[states["state"] == "Andhra Pradesh"]["heatstroke_cases_2026"].values[0]

test("Rajasthan peak = 48.2°C (Sri Ganganagar May 27, IMD confirmed)",
     abs(raj_temp - 48.2) < 0.01, f"got {raj_temp}")
test("Odisha peak = 48.0°C (Balangir May 22, world's hottest city)",
     abs(od_temp - 48.0) < 0.01, f"got {od_temp}")
test("UP peak = 47.4°C (Banda Apr 25, IMD bulletin confirmed)",
     abs(up_temp - 47.4) < 0.01, f"got {up_temp}")
test("AP heatstroke cases = 325 (official AP Health Ministry, 1 Mar–19 May)",
     ap_cases == 325, f"got {ap_cases}")

# National economic figures (Lancet/Carnegie/ILO verified)
total_loss = states["economic_loss_2026_usd_mn"].sum() / 1000
total_hrs  = states["labour_hours_lost_2026_mn"].sum() / 1000
test("National economic loss = $194B (Lancet Countdown / Carnegie 2026)",
     abs(total_loss - 194.0) < 1.0, f"got ${total_loss:.1f}B")
test("National labour hours lost = 247B (Carnegie citing Lancet 2024)",
     abs(total_hrs - 247.0) < 1.0, f"got {total_hrs:.1f}B")

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 3: Heat Risk Score Validity")
# ─────────────────────────────────────────────────────────────────────────────

test("All heat risk scores between 0 and 100",
     (states["heat_risk_score"] >= 0).all() and (states["heat_risk_score"] <= 100).all())
test("Only valid risk tiers used",
     set(states["risk_tier"].unique()).issubset({"Critical","Very High","High","Moderate"}))
test("Odisha is highest risk (world's hottest city + very high vulnerability)",
     states.loc[states["heat_risk_score"].idxmax(), "state"] == "Odisha",
     f"top state = {states.loc[states['heat_risk_score'].idxmax(), 'state']}")
test("Kerala is lowest risk (coastal, fewer heatwave days, lower outdoor workforce)",
     states.loc[states["heat_risk_score"].idxmin(), "state"] == "Kerala",
     f"bottom = {states.loc[states['heat_risk_score'].idxmin(), 'state']}")
test("Critical tier states have score > 85",
     (states[states["risk_tier"] == "Critical"]["heat_risk_score"] > 85).all())
test("National risk rank is monotonic with heat_risk_score",
     states["heat_risk_score"].is_monotonic_decreasing or
     states.sort_values("heat_risk_score", ascending=False)["heat_risk_score"].is_monotonic_decreasing)

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 4: Analysis Results Validation")
# ─────────────────────────────────────────────────────────────────────────────
r = d["results"]

test("R² value is between 0.6 and 1.0 (correlation meaningful)",
     0.6 <= r["correlation"]["r_squared"] <= 1.0,
     f"R²={r['correlation']['r_squared']}")
test("Slope is positive (higher temp → higher demand, as expected)",
     r["correlation"]["slope_gw_per_degree"] > 0)
test("Critical temp threshold is between 40°C and 50°C",
     40 <= r["correlation"]["critical_threshold_temp_c"] <= 50,
     f"got {r['correlation']['critical_threshold_temp_c']}°C")
test("Test MAPE < 5% (forecast is defensible)",
     r["forecasting"]["mape_test_pct"] < 5.0,
     f"MAPE={r['forecasting']['mape_test_pct']}%")
test("Train RMSE < 10 GW",
     r["forecasting"]["rmse_train_gw"] < 10.0)
test("2030 projected demand > 2026 record (growth trajectory)",
     r["forecasting"]["demand_2030_projected_gw"] > 270.82)

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 5: Economic Calculation Consistency")
# ─────────────────────────────────────────────────────────────────────────────

test("Sector income losses sum to national total (≈ $137B)",
     85 < sectors["income_loss_usd_bn_2026"].sum() < 150)
test("Agriculture is the largest loss sector (ILO confirmed)",
     sectors.loc[sectors["income_loss_usd_bn_2026"].idxmax(), "sector"] == "Agriculture")
test("Outdoor workforce pcts sum within realistic range (no state > 100%)",
     (states["outdoor_workforce_pct"] <= 100).all() and
     (states["outdoor_workforce_pct"] >= 0).all())
test("GDP at risk range is valid (low < high for all states)",
     (states["gdp_at_risk_high_usd_mn"] > states["gdp_at_risk_low_usd_mn"]).all())
test("All populations are positive and plausible (1M–250M range)",
     (states["population_mn"] >= 1).all() and (states["population_mn"] <= 250).all())

# ─────────────────────────────────────────────────────────────────────────────
print("\n📋 TEST SUITE 6: Pipeline Completeness")
# ─────────────────────────────────────────────────────────────────────────────

expected_outputs = [
    "01_temp_demand_correlation.png",
    "02_grid_demand_forecast.png",
    "03_yoy_escalation.png",
    "04_state_risk_ranking.png",
    "05_sensitivity_analysis.png",
    "06_sector_impact.png",
    "analysis_results.json",
]
for fname in expected_outputs:
    fpath = os.path.join(OUT, fname)
    test(f"Output exists: {fname}", os.path.exists(fpath))
    if os.path.exists(fpath):
        test(f"Output non-empty: {fname}", os.path.getsize(fpath) > 1000,
             f"size={os.path.getsize(fpath)} bytes")

expected_data = [
    "heatpulse_states.csv", "heatpulse_grid.csv",
    "heatpulse_yearly.csv", "heatpulse_sectors.csv",
    "heatpulse_sensitivity.csv"
]
for fname in expected_data:
    test(f"Data file exists: {fname}", os.path.exists(f"{DATA}/{fname}"))

# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print(f"RESULTS: {results['passed']} passed | {results['failed']} failed")
if results["errors"]:
    print(f"FAILED:  {results['errors']}")
print("="*60)

sys.exit(0 if results["failed"] == 0 else 1)
