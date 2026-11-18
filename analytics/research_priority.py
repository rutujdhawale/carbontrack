"""
AWD Research Priority Scoring Engine.
Computes explainable, multi-criteria research priority indices for Indian states
to guide early-stage agricultural carbon project feasibility studies.
"""
import os
import pandas as pd
import numpy as np

def calculate_research_priority(
    input_path: str = "data/processed/regional_analysis.csv",
    output_path: str = "data/processed/research_priority_scores.csv"
) -> pd.DataFrame:
    """
    Calculates explainable research priority score for AWD carbon projects.
    Multi-criteria weighting:
      1. Rice Cultivation Footprint (35%): Scale of rice area and production.
      2. Water Info & Irrigation Control (25%): Controlled irrigation coverage vs flood/rainfed risk.
      3. Data Availability (20%): Completeness and transparency of public agricultural records.
      4. Project Evidence & Feasibility (20%): Prior AWD field trial history and extension readiness.
    """
    if not os.path.exists(input_path):
        from analytics.regional_analysis import analyze_regional_trends
        analyze_regional_trends()

    df = pd.read_csv(input_path)
    latest_year = df["Year"].max()
    latest_df = df[df["Year"] == latest_year].copy()

    # Prior AWD institutional research presence & extension readiness by state
    evidence_ratings = {
        "Punjab": 90.0,         # PAU (Punjab Agricultural Univ) extensive AWD/DSR trials
        "Haryana": 88.0,        # HAU extensive water-saving rice cultivation data
        "Telangana": 86.0,      # PJTSAU & IRRI direct seeded / alternate wetting pilots
        "Andhra Pradesh": 88.0, # ANGRAU & Godavari delta AWD research
        "Tamil Nadu": 89.0,     # TNAU & IRRI long-term Cauvery AWD validation
        "West Bengal": 78.0,    # BCKV Boro rice water management studies
        "Uttar Pradesh": 76.0,  # ANDUAT & Western UP groundwater research
        "Bihar": 72.0,          # BAU Sabour & CSISA water management trials
        "Odisha": 68.0,         # NRRI Cuttack (National Rice Research Institute) headquarters
        "Chhattisgarh": 66.0,   # IGKV Raipur canal water management
        "Karnataka": 74.0,      # UAS Bangalore/Dharwad Cauvery & Tungabhadra trials
        "Madhya Pradesh": 65.0, # State trials in central rice zones
        "Maharashtra": 64.0,    # Regional trial data in Vidarbha
        "Gujarat": 68.0,        # AAU Anand rice water regime research
        "Assam": 58.0,          # AAU Jorhat (limited AWD due to flood plain hydrology)
        "Kerala": 62.0,         # KAU Kuttanad special polder water regimes
    }

    # Public data availability & cadastral digitization index (0-100)
    data_avail_ratings = {
        "Punjab": 92.0, "Haryana": 90.0, "Telangana": 91.0, "Andhra Pradesh": 90.0,
        "Tamil Nadu": 91.0, "West Bengal": 82.0, "Uttar Pradesh": 84.0, "Bihar": 78.0,
        "Odisha": 80.0, "Chhattisgarh": 79.0, "Karnataka": 86.0, "Madhya Pradesh": 81.0,
        "Maharashtra": 84.0, "Gujarat": 85.0, "Assam": 74.0, "Kerala": 83.0
    }

    max_prod = latest_df["Production"].max()
    scores = []

    for _, row in latest_df.iterrows():
        state = row["State"]
        prod = row["Production"]
        irrig_pct = row.get("Irrigation_Pct", 50.0)

        # 1. Footprint score (scale: min 30, max 100 based on production volume)
        footprint = min(100.0, max(30.0, 30.0 + (prod / max_prod) * 70.0))

        # 2. Water info & controlled irrigation score (AWD requires controllable sluices/tubewells)
        # Scaled largely from verified irrigation percentage
        water_info = min(100.0, max(25.0, irrig_pct * 0.95 + 4.0))

        # 3. Data availability score
        data_avail = data_avail_ratings.get(state, 80.0)

        # 4. Project evidence score
        evidence = evidence_ratings.get(state, 70.0)

        # Composite Weighted Priority Score
        total_score = (
            (footprint * 0.35) +
            (water_info * 0.25) +
            (data_avail * 0.20) +
            (evidence * 0.20)
        )
        total_score = round(total_score, 1)

        # Status: High Priority vs Moderate Priority
        status = "High Priority" if total_score >= 78.0 else "Moderate Priority"

        # Rationale notes for researchers
        if total_score >= 85.0:
            tier = "Tier 1: Prime Feasibility (High acreage + >85% controlled irrigation)"
        elif total_score >= 78.0:
            tier = "Tier 1: High Priority (Large footprint, target irrigated seasons/pockets)"
        else:
            tier = "Tier 2: Moderate Priority (Requires drainage assessment / rainfed risk)"

        scores.append({
            "State": state,
            "Production_Mt": round(prod, 2),
            "Irrigation_Pct": round(irrig_pct, 1),
            "Footprint_Score": round(footprint, 1),
            "Water_Info_Score": round(water_info, 1),
            "Data_Availability_Score": round(data_avail, 1),
            "Project_Evidence_Score": round(evidence, 1),
            "Research_Priority_Score": total_score,
            "Status": status,
            "Strategic_Recommendation": tier,
        })

    score_df = pd.DataFrame(scores).sort_values(by="Research_Priority_Score", ascending=False).reset_index(drop=True)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    score_df.to_csv(output_path, index=False)
    print(f"Explainable research priority scores saved to {output_path} ({len(score_df)} states)")
    return score_df

if __name__ == "__main__":
    calculate_research_priority()
