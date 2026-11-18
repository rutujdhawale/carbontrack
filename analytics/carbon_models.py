"""
IPCC & IRRI Methane and Carbon Abatement Analytics Engine.
Calculates baseline methane emissions, AWD reduction factors, net carbon credits,
and irrigation water savings based on IPCC Guidelines for National GHG Inventories
and IRRI AWD protocols.
"""
from typing import Dict, Any

# IPCC 2006 / 2019 Refinement Parameters for Rice Cultivation
# Baseline emission factor for continuously flooded fields without organic amendments (kg CH4 / ha / day)
IPCC_BASE_EF_CH4 = 1.30

# IPCC Water Regime Scaling Factors (SF_w)
WATER_REGIME_FACTORS = {
    "Continuously Flooded (Baseline)": 1.00,
    "Single Aeration / Drainage": 0.71,       # 29% reduction
    "Multiple Aeration (Standard AWD)": 0.52,  # 48% reduction
    "Safe AWD with pani pipe (-15 cm)": 0.45, # 55% reduction
}

# IPCC Pre-season Water Regime Scaling Factors (SF_p)
PRE_SEASON_FACTORS = {
    "Non-flooded pre-season (>180 days)": 1.00,
    "Flooded pre-season (>30 days)": 1.90,
}

# IPCC Organic Amendment Scaling Factors (SF_o)
ORGANIC_AMENDMENT_FACTORS = {
    "No organic amendment": 1.00,
    "Farmyard Manure (FYM 5 t/ha)": 1.15,
    "Green Manure / Straw incorporated": 1.45,
}

# Global Warming Potential (GWP-100) of CH4 (IPCC AR5 without climate-carbon feedback = 28)
GWP_CH4 = 28.0

# Verra VM0042 / CDM ACM0022 Recommended Risk Buffer
CONSERVATISM_BUFFER = 0.20  # 20% buffer deduction for leakage/reversal/measurement uncertainty


def calculate_awd_abatement(
    area_ha: float,
    cultivation_days: int = 105,
    water_regime: str = "Multiple Aeration (Standard AWD)",
    organic_regime: str = "No organic amendment",
    carbon_price_usd: float = 18.0,
    water_savings_rate_pct: float = 28.0,
) -> Dict[str, Any]:
    """
    Computes comprehensive carbon abatement, carbon credits, water savings,
    and revenue projections for a given rice project area under AWD.
    """
    sf_w = WATER_REGIME_FACTORS.get(water_regime, 0.52)
    sf_o = ORGANIC_AMENDMENT_FACTORS.get(organic_regime, 1.00)
    sf_p = 1.00

    # Daily emission rate in kg CH4/ha/day
    daily_baseline_ch4_ha = IPCC_BASE_EF_CH4 * 1.00 * sf_o * sf_p
    daily_project_ch4_ha = IPCC_BASE_EF_CH4 * sf_w * sf_o * sf_p

    # Season total CH4 (kg/ha)
    season_baseline_ch4_ha = daily_baseline_ch4_ha * cultivation_days
    season_project_ch4_ha = daily_project_ch4_ha * cultivation_days
    ch4_reduction_ha = season_baseline_ch4_ha - season_project_ch4_ha

    # Convert to tCO2e per hectare
    baseline_tco2e_ha = (season_baseline_ch4_ha * GWP_CH4) / 1000.0
    project_tco2e_ha = (season_project_ch4_ha * GWP_CH4) / 1000.0
    gross_abatement_tco2e_ha = (ch4_reduction_ha * GWP_CH4) / 1000.0

    # Apply Conservatism & Risk Buffer (e.g., 20% deduction for Verra VCS buffer pool)
    net_creditable_tco2e_ha = gross_abatement_tco2e_ha * (1.0 - CONSERVATISM_BUFFER)

    # Scale to total project area
    total_baseline_tco2e = baseline_tco2e_ha * area_ha
    total_gross_abatement_tco2e = gross_abatement_tco2e_ha * area_ha
    total_net_credits_tco2e = net_creditable_tco2e_ha * area_ha

    # Irrigation water savings:
    # Typical rice water requirement = 10,000 to 12,500 m3/ha (10-12.5 ML/ha)
    base_water_m3_ha = 11000.0
    water_saved_m3_ha = base_water_m3_ha * (water_savings_rate_pct / 100.0)
    total_water_saved_m3 = water_saved_m3_ha * area_ha

    # Revenue
    gross_revenue_usd = total_net_credits_tco2e * carbon_price_usd
    farmer_share_pct = 65.0  # Common equitable carbon revenue split to smallholders
    farmer_pool_revenue_usd = gross_revenue_usd * (farmer_share_pct / 100.0)

    # Energy / Pumping diesel savings (liters diesel saved per hectare ~ 60-90 L/ha)
    diesel_saved_liters_ha = 75.0 * (water_savings_rate_pct / 28.0)
    total_diesel_saved_liters = diesel_saved_liters_ha * area_ha

    return {
        "area_ha": area_ha,
        "cultivation_days": cultivation_days,
        "water_regime": water_regime,
        "reduction_percentage": round((1.0 - sf_w) * 100.0, 1),
        "baseline_tco2e_ha": round(baseline_tco2e_ha, 2),
        "gross_abatement_tco2e_ha": round(gross_abatement_tco2e_ha, 2),
        "net_creditable_tco2e_ha": round(net_creditable_tco2e_ha, 2),
        "total_baseline_tco2e": round(total_baseline_tco2e, 1),
        "total_gross_abatement_tco2e": round(total_gross_abatement_tco2e, 1),
        "total_net_credits_tco2e": round(total_net_credits_tco2e, 1),
        "total_water_saved_million_liters": round(total_water_saved_m3 / 1000.0, 1),
        "total_diesel_saved_liters": round(total_diesel_saved_liters, 0),
        "gross_revenue_usd": round(gross_revenue_usd, 2),
        "farmer_pool_revenue_usd": round(farmer_pool_revenue_usd, 2),
        "buffer_tco2e": round(total_gross_abatement_tco2e * CONSERVATISM_BUFFER, 1),
    }
