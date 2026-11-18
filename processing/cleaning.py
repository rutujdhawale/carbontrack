"""
Data cleaning and validation module for CarbonTrack.
Processes raw FAOSTAT and national agricultural datasets into validated tabular records.
"""
import os
import pandas as pd

def clean_faostat_data(
    input_path: str = "data/raw/faostat_rice.csv",
    output_path: str = "data/processed/faostat_rice_cleaned.csv",
) -> pd.DataFrame:
    """
    Cleans and standardizes FAOSTAT / national rice data.
    Ensures required schema: Year, Country, Rice_Production, Area_Harvested, Yield.
    """
    if not os.path.exists(input_path):
        from ingestion.faostat import fetch_faostat_data
        fetch_faostat_data(input_path)

    df = pd.read_csv(input_path)

    # Validate mandatory columns
    required_cols = ["Year", "Country", "Rice_Production", "Area_Harvested", "Yield"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column in input data: {col}")

    # Remove duplicates and nulls
    df = df.drop_duplicates(subset=["Year", "Country"]).dropna(subset=required_cols)

    # Type casting and sorting
    df["Year"] = df["Year"].astype(int)
    df["Rice_Production"] = df["Rice_Production"].astype(float)
    df["Area_Harvested"] = df["Area_Harvested"].astype(float)
    df["Yield"] = df["Yield"].astype(float)
    df = df.sort_values("Year").reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned FAOSTAT data saved to {output_path} ({len(df)} records)")
    return df

if __name__ == "__main__":
    clean_faostat_data()
