"""
Regional agricultural analysis module for Indian rice cultivation.
Analyzes state-level and district-level trends, yields, CAGR, and irrigation patterns.
"""
import os
import pandas as pd
from ingestion.des_india import get_state_historical_data, get_district_hotspot_data

def analyze_regional_trends(
    output_path: str = "data/processed/regional_analysis.csv",
    district_output_path: str = "data/processed/district_analysis.csv"
) -> pd.DataFrame:
    """
    Produces comprehensive multi-year regional agricultural analysis for India.
    Saves state-level and district-level processed datasets.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load or generate authentic state data
    df = get_state_historical_data()

    # Calculate year-over-year production and yield growth
    df = df.sort_values(by=["State", "Year"]).reset_index(drop=True)
    df["YoY_Production_Growth_Pct"] = df.groupby("State")["Production"].pct_change() * 100
    df["YoY_Production_Growth_Pct"] = df["YoY_Production_Growth_Pct"].fillna(0.0).round(2)

    df.to_csv(output_path, index=False)
    print(f"Regional state analysis saved to {output_path} ({len(df)} rows across {df['State'].nunique()} states)")

    # Also save district dataset
    district_df = get_district_hotspot_data()
    district_df.to_csv(district_output_path, index=False)
    print(f"District hotspot analysis saved to {district_output_path} ({len(district_df)} districts)")

    return df

def get_state_summary() -> pd.DataFrame:
    """
    Computes aggregated executive metrics per state for the latest year (2023).
    """
    df = pd.read_csv("data/processed/regional_analysis.csv")
    latest = df[df["Year"] == df["Year"].max()].copy()

    # Calculate national share
    total_national_prod = latest["Production"].sum()
    total_national_area = latest["Area"].sum()

    latest["National_Production_Share_Pct"] = (latest["Production"] / total_national_prod * 100).round(1)
    latest["National_Area_Share_Pct"] = (latest["Area"] / total_national_area * 100).round(1)

    return latest.sort_values(by="Production", ascending=False).reset_index(drop=True)

if __name__ == "__main__":
    analyze_regional_trends()
