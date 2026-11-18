import pytest
import pandas as pd
import numpy as np
from analytics.carbon_models import calculate_awd_abatement, WATER_REGIME_FACTORS
from utils.formatting import format_number, format_area, format_production, format_yield

def test_priority_scores_calculation():
    """Verify AWD research priority scores schema, ranges, and classification."""
    df = pd.read_csv('data/processed/research_priority_scores.csv')

    assert 'Research_Priority_Score' in df.columns
    assert 'Status' in df.columns
    assert 'Footprint_Score' in df.columns
    assert 'Water_Info_Score' in df.columns
    assert 'Data_Availability_Score' in df.columns
    assert 'Project_Evidence_Score' in df.columns

    # Test that scores are bounded in [0, 100]
    assert df['Research_Priority_Score'].between(0, 100).all()
    assert df['Footprint_Score'].between(0, 100).all()
    assert df['Water_Info_Score'].between(0, 100).all()

    # Test that status is assigned correctly
    assert set(df['Status'].unique()).issubset({'High Priority', 'Moderate Priority'})

    # Differentiated scoring check (not all rows identical)
    assert df['Research_Priority_Score'].nunique() > 1

def test_data_integrity():
    """Verify FAOSTAT cleaned rice time-series data."""
    df = pd.read_csv('data/processed/faostat_rice_cleaned.csv')

    # Test that data has expected columns
    expected_cols = ['Year', 'Country', 'Rice_Production', 'Area_Harvested', 'Yield']
    assert all(col in df.columns for col in expected_cols)

    # Test that data has no nulls in critical columns
    assert df['Rice_Production'].notna().all()
    assert df['Area_Harvested'].notna().all()
    assert df['Yield'].notna().all()

    # Test data ranges: Production > 80 Mt, Area > 40 M ha, Yield > 2.0 t/ha
    assert (df['Rice_Production'] > 80.0).all()
    assert (df['Area_Harvested'] > 40.0).all()
    assert (df['Yield'] > 2.0).all()

def test_regional_data_integrity():
    """Verify regional state dataset integrity."""
    df = pd.read_csv('data/processed/regional_analysis.csv')

    # Should have multiple states
    assert df['State'].nunique() >= 10

    # Test that years are in 2018-2023 range
    assert df['Year'].between(2018, 2023).all()

    # Test that production and area are positive
    assert (df['Production'] > 0).all()
    assert (df['Area'] > 0).all()
    assert (df['Yield'] > 0).all()

def test_district_analysis_integrity():
    """Verify district-level analysis dataset."""
    df = pd.read_csv('data/processed/district_analysis.csv')

    expected_cols = ['State', 'District', 'Area_kHa', 'Prod_kTonnes', 'Yield', 'Irrigated_Pct', 'AWD_Tier', 'Methane_Abatement_Potential_tCO2e']
    assert all(col in df.columns for col in expected_cols)

    assert len(df) >= 20
    assert (df['Area_kHa'] > 0).all()
    assert (df['Prod_kTonnes'] > 0).all()
    assert (df['Irrigated_Pct'].between(0, 100)).all()
    assert (df['Methane_Abatement_Potential_tCO2e'] > 0).all()

def test_carbon_abatement_model():
    """Verify IPCC & Verra carbon abatement model logic."""
    res = calculate_awd_abatement(
        area_ha=1000.0,
        cultivation_days=105,
        water_regime="Multiple Aeration (Standard AWD)",
        carbon_price_usd=20.0
    )

    # Gross abatement must be positive and less than baseline
    assert res['total_baseline_tco2e'] > res['total_gross_abatement_tco2e'] > 0
    # Net credits should be gross * (1 - 0.20)
    assert np.isclose(res['total_net_credits_tco2e'], res['total_gross_abatement_tco2e'] * 0.8, rtol=1e-2)
    # Revenue should equal net credits * price
    assert np.isclose(res['gross_revenue_usd'], res['total_net_credits_tco2e'] * 20.0, rtol=1e-2)
    # Water saved must be positive
    assert res['total_water_saved_million_liters'] > 0

def test_formatting_utilities():
    """Verify UI formatting helpers."""
    assert format_number(1234.56, 1) == "1,234.6"
    assert format_area(5000) == "5,000 ha"
    assert format_production(150000) == "150,000 t"
    assert format_yield(3.456) == "3.46 t/ha"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
