"""
CarbonTrack - AWD Project Intelligence & Carbon Feasibility.
Provides research priority rankings, carbon abatement modeling,
field data requirement checklists, and MRV verification protocols.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.formatting import (
    GREEN, TERRACOTTA, MUTED_COLOR, apply_brand_theme, format_number
)
from analytics.carbon_models import (
    calculate_awd_abatement, WATER_REGIME_FACTORS, ORGANIC_AMENDMENT_FACTORS
)

def render():
    st.title("🌱 AWD Carbon Project Intelligence & MRV Architecture")
    st.markdown(
        "Scientific prioritization, carbon offset estimation, and audit-grade MRV guidelines "
        "for **Alternate Wetting and Drying (AWD)** project development in India."
    )
    st.divider()

    # Load Research Priority Scores
    try:
        priority_df = pd.read_csv("data/processed/research_priority_scores.csv")
    except Exception as e:
        st.error(f"Error loading research priority scores: {e}")
        return

    # Sub-sections using tabs
    tab_priority, tab_calculator, tab_field_gap, tab_mrv = st.tabs([
        "🏆 Regional Research Priority Scores",
        "🧮 Interactive Carbon Abatement Calculator",
        "📋 Public vs. Field-Level Information Gap",
        "🛰️ MRV Architecture & Verification Protocol"
    ])

    # ---------------- TAB 1: RESEARCH PRIORITY ----------------
    with tab_priority:
        st.subheader("Regional Research Priority Index (0–100)")
        st.markdown("""
        An explainable, multi-factor decision matrix that ranks Indian states for in-depth pre-feasibility research.
        
        **Weighting Methodology:**
        - **Rice Cultivation Footprint (35%):** Total baseline production and acreage.
        - **Water Info & Irrigation Control (25%):** % of rice land under controlled irrigation (essential for AWD drainage).
        - **Data Availability & Cadastre (20%):** Completeness of public statistics and land record transparency.
        - **Project Evidence & Institutional Readiness (20%):** Prior AWD trial validation (IRRI / State Agri Universities).
        """)

        # Priority Table
        st.dataframe(
            priority_df[[
                "State", "Production_Mt", "Irrigation_Pct", "Footprint_Score",
                "Water_Info_Score", "Data_Availability_Score", "Project_Evidence_Score",
                "Research_Priority_Score", "Status", "Strategic_Recommendation"
            ]].rename(columns={
                "Production_Mt": "Production (Mt)",
                "Irrigation_Pct": "Irrigated %",
                "Footprint_Score": "Footprint (35%)",
                "Water_Info_Score": "Water Control (25%)",
                "Data_Availability_Score": "Data Quality (20%)",
                "Project_Evidence_Score": "AWD Trials (20%)",
                "Research_Priority_Score": "Priority Score",
                "Strategic_Recommendation": "Screening Recommendation"
            }),
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            # Bar chart of priority scores
            fig_bar = px.bar(
                priority_df.sort_values(by="Research_Priority_Score", ascending=True),
                x="Research_Priority_Score",
                y="State",
                color="Status",
                orientation="h",
                title="Overall Research Priority Index by State",
                labels={"Research_Priority_Score": "Priority Index (0–100)"},
                color_discrete_map={"High Priority": GREEN, "Moderate Priority": TERRACOTTA}
            )
            fig_bar.update_layout(
                height=480,
                margin=dict(l=60, r=30, t=50, b=50),
                legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5)
            )
            apply_brand_theme(fig_bar)
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_p2:
            # Weighted component breakdown for top priority states - Stacked Horizontal Bar (zero overlap)
            top_states = priority_df.head(7).sort_values(by="Research_Priority_Score", ascending=True)
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                name="Footprint (35%)",
                y=top_states["State"],
                x=(top_states["Footprint_Score"] * 0.35).round(1),
                orientation="h",
                marker_color=GREEN,
                hovertemplate="%{y} - Footprint: %{x:.1f} pts<extra></extra>"
            ))
            fig_comp.add_trace(go.Bar(
                name="Water Control (25%)",
                y=top_states["State"],
                x=(top_states["Water_Info_Score"] * 0.25).round(1),
                orientation="h",
                marker_color=TERRACOTTA,
                hovertemplate="%{y} - Water Control: %{x:.1f} pts<extra></extra>"
            ))
            fig_comp.add_trace(go.Bar(
                name="Data Quality (20%)",
                y=top_states["State"],
                x=(top_states["Data_Availability_Score"] * 0.20).round(1),
                orientation="h",
                marker_color="#2A78D6",
                hovertemplate="%{y} - Data Quality: %{x:.1f} pts<extra></extra>"
            ))
            fig_comp.add_trace(go.Bar(
                name="AWD Field Trials (20%)",
                y=top_states["State"],
                x=(top_states["Project_Evidence_Score"] * 0.20).round(1),
                orientation="h",
                marker_color="#E6A817",
                hovertemplate="%{y} - Field Trials: %{x:.1f} pts<extra></extra>"
            ))

            fig_comp.update_layout(
                barmode="stack",
                title="Weighted Dimension Contribution to Total Score",
                xaxis_title="Weighted Points (Sum = Total Score out of 100)",
                height=480,
                margin=dict(l=60, r=30, t=50, b=80),
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.18,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=10)
                )
            )
            apply_brand_theme(fig_comp)
            st.plotly_chart(fig_comp, use_container_width=True)

        st.caption(
            "📌 **Methodological Note:** The Research Priority Index is an analytical decision-support model structured according "
            "to IPCC 2019 Refinement parameters and Verra VM0042 criteria to assist project origination teams in prioritizing field audit resources."
        )

    # ---------------- TAB 2: CALCULATOR ----------------
    with tab_calculator:
        st.subheader("AWD Carbon Abatement & Project Economics Calculator")
        st.markdown(
            "Model gross and net carbon offsets ($tCO_2e$), irrigation water conserved, and smallholder revenue "
            "under IPCC 2019 Refinement and Verra VM0042 methodology guidelines."
        )

        col_input1, col_input2, col_input3 = st.columns(3)
        with col_input1:
            project_ha = st.number_input("Project Area (Hectares)", min_value=100.0, max_value=500000.0, value=5000.0, step=500.0)
            cult_days = st.slider("Rice Cultivation Duration (Days)", min_value=80, max_value=140, value=105, step=5)
        with col_input2:
            regime = st.selectbox(
                "AWD Water Management Protocol",
                options=list(WATER_REGIME_FACTORS.keys()),
                index=2  # Standard AWD
            )
            organic = st.selectbox(
                "Organic Soil Amendment Baseline",
                options=list(ORGANIC_AMENDMENT_FACTORS.keys()),
                index=0
            )
        with col_input3:
            carbon_price = st.number_input("Expected Carbon Price ($/tCO₂e)", min_value=5.0, max_value=80.0, value=18.0, step=1.0)
            water_savings_pct = st.slider("Expected Water Savings (%)", min_value=15.0, max_value=40.0, value=28.0, step=1.0)

        # Run carbon model
        res = calculate_awd_abatement(
            area_ha=project_ha,
            cultivation_days=cult_days,
            water_regime=regime,
            organic_regime=organic,
            carbon_price_usd=carbon_price,
            water_savings_rate_pct=water_savings_pct
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Projected Project Impacts (Single Season)")

        c_out1, c_out2, c_out3, c_out4 = st.columns(4)
        with c_out1:
            st.metric(
                label="Baseline Gross Emissions",
                value=f"{res['total_baseline_tco2e']:,.0f} tCO₂e",
                delta=f"{res['baseline_tco2e_ha']} t/ha"
            )
        with c_out2:
            st.metric(
                label="Net Creditable Offsets",
                value=f"{res['total_net_credits_tco2e']:,.0f} tCO₂e",
                delta=f"-{res['reduction_percentage']}% CH₄ (20% buffer deducted)"
            )
        with c_out3:
            st.metric(
                label="Total Water Conserved",
                value=f"{res['total_water_saved_million_liters']:,.0f} ML",
                delta=f"{water_savings_pct:.0f}% irrigation cut"
            )
        with c_out4:
            st.metric(
                label="Total Carbon Revenue",
                value=f"${res['gross_revenue_usd']:,.0f}",
                delta=f"${res['farmer_pool_revenue_usd']:,.0f} to farmers (65%)"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Detailed Abatement & Co-benefit Ledger")

        col_led1, col_led2 = st.columns(2)
        with col_led1:
            st.markdown(f"""
            - **Gross Methane Abatement:** `{res['total_gross_abatement_tco2e']:,.1f} tCO₂e` ({res['gross_abatement_tco2e_ha']} tCO₂e/ha)
            - **Verra/Registry Risk Buffer Deduction (20%):** `-{res['buffer_tco2e']:,.1f} tCO₂e`
            - **Net Issued Carbon Credits:** `{res['total_net_credits_tco2e']:,.1f} VCUs / Credits`
            - **Estimated Diesel Pumping Saved:** `{res['total_diesel_saved_liters']:,.0f} Liters`
            """)
        with col_led2:
            st.markdown(f"""
            - **Net Carbon Price:** `${carbon_price:.2f} USD per ton`
            - **Total Gross Credit Value:** `${res['gross_revenue_usd']:,.2f} USD`
            - **Farmer Community Pool Share (65%):** `${res['farmer_pool_revenue_usd']:,.2f} USD`
            - **Per Hectare Net Incentive:** `${(res['farmer_pool_revenue_usd'] / project_ha):,.2f} USD/ha` (~₹{(res['farmer_pool_revenue_usd'] / project_ha * 83):,.0f} INR/ha)
            """)

    # ---------------- TAB 3: FIELD GAP ANALYSIS ----------------
    with tab_field_gap:
        st.subheader("What Public Datasets Provide vs. What MUST Be Collected on the Ground")
        st.markdown(
            "Public datasets (DES India, FAOSTAT, Central Ground Water Board) provide invaluable macro-level "
            "filtering, but **cannot substantiate carbon project registration alone**. The table below highlights the "
            "information gaps that must be resolved through primary field surveys."
        )

        gap_data = [
            {
                "Parameter": "Field Boundaries & Polygons",
                "Public Data": "District & State aggregate acreages (ha). No cadastral GIS.",
                "Field Level Required": "Precise GPS polygon per plot (<0.5 ha) with cadastral survey numbers.",
                "Why Required by Verra/CDM": "Prevents double-counting and enables remote sensing polygon overlay."
            },
            {
                "Parameter": "Farmer Consent & Land Tenure",
                "Public Data": "Agricultural census tenant proportions.",
                "Field Level Required": "Signed Free, Prior and Informed Consent (FPIC) + proof of cultivation (patta/lease).",
                "Why Required by Verra/CDM": "Ensures carbon rights ownership and equitable revenue distribution."
            },
            {
                "Parameter": "Baseline Water Practices",
                "Public Data": "Broad classification ('irrigated' vs 'unirrigated').",
                "Field Level Required": "Historical flooding duration, customary drying intervals, and pump operating hours.",
                "Why Required by Verra/CDM": "Mandatory for proving additionality and establishing baseline emission factor."
            },
            {
                "Parameter": "Elevation & Soil Drainage",
                "Public Data": "Coarse regional soil classifications (e.g. 'Alluvial').",
                "Field Level Required": "Micro-topography, bund height (>15 cm), percolation rate, and water stagnation risk.",
                "Why Required by Verra/CDM": "Fields that remain naturally submerged cannot execute AWD drying cycles."
            },
            {
                "Parameter": "Pumping & Energy Source",
                "Public Data": "State minor irrigation census totals.",
                "Field Level Required": "Pump type (electric, solar, diesel), horsepower, flow rate, and power schedule.",
                "Why Required by Verra/CDM": "Calculates secondary fossil fuel emission reductions and pump access reliability."
            },
            {
                "Parameter": "Residue & Straw Management",
                "Public Data": "State burning estimates from satellite VIIRS/MODIS.",
                "Field Level Required": "Exact straw management (burned, incorporated, removed for fodder, or composted).",
                "Why Required by Verra/CDM": "Organic matter incorporation dramatically alters the baseline IPCC $SF_o$ factor."
            }
        ]

        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("#### Pre-Feasibility Due Diligence Checklist")
        st.checkbox("1. Confirm site is within controllable command area (canal outlet or independent tubewell)", value=True)
        st.checkbox("2. Verify that field plot does not suffer from natural waterlogging during target season", value=True)
        st.checkbox("3. Execute FPIC agreement with legal titleholders or registered tenant farmers", value=True)
        st.checkbox("4. Collect geo-referenced polygon coordinates using handheld GPS / GIS survey tool", value=True)
        st.checkbox("5. Establish baseline water table depth using continuous data logger or control plot", value=True)
        st.checkbox("6. Partner with local FPO (Farmer Producer Organization) or Krishi Vigyan Kendra (KVK)", value=True)

    # ---------------- TAB 4: MRV PROTOCOL ----------------
    with tab_mrv:
        st.subheader("Auditable MRV Protocol for AWD Rice Carbon Projects")
        st.markdown("""
        To satisfy carbon registries (Verra VM0042, CDM ACM0022, Gold Standard), projects must deploy an auditable,
        multi-tiered Measurement, Reporting, and Verification (MRV) architecture combining physical sensors,
        satellite radar, and digital farmer records.
        """)

        mrv_cols = st.columns(3)
        with mrv_cols[0]:
            st.markdown("""
            #### 1. In-Situ Field Sensors
            **The 'Pani Pipe' Protocol:**
            - **Specification:** 30 cm long, 10–15 cm diameter perforated PVC pipe.
            - **Installation:** Inserted 15 cm into the soil; bottom 15 cm perforated with 5 mm holes spaced 2 cm apart.
            - **Monitoring Rule:** Field is re-irrigated only when water level drops to 15 cm below soil surface.
            - **Density:** 1 sensor pipe per 1-2 hectares or 1 smart telemetry logger per 10-hectare cluster.
            """)
        with mrv_cols[1]:
            st.markdown("""
            #### 2. Synthetic Aperture Radar (SAR)
            **Cloud-Penetrating Remote Sensing:**
            - **Satellite:** Sentinel-1 C-band SAR (12-day repeat or 6-day dual constellation).
            - **Detection:** Measures microwave backscatter ($\sigma^0$).
            - **Physics:** Standing water acts as a specular reflector (very low backscatter); dry aerated soil produces rough surface scattering (high backscatter).
            - **Advantage:** Unaffected by heavy monsoon cloud cover, validating drying cycles remotely across all registered polygons.
            """)
        with mrv_cols[2]:
            st.markdown("""
            #### 3. Traceable Digital Logs
            **Farmer Mobile Verification:**
            - **Mobile App:** Farmers or field animators record water level readings.
            - **Geo-Tagging & Timestamps:** EXIF-verified photographs looking down the perforated pani pipe.
            - **Audit Trail:** Immutable cloud ledger linked to individual farmer ID and plot polygon.
            - **Third-Party Verification:** Designated Operational Entity (DOE / VVB) conducts statistical field sampling.
            """)

        st.markdown("---")
        st.markdown("#### GHG Sampling & Calibration (Tier 2 / Tier 3)")
        st.markdown("""
        - **Closed-Chamber Flux Sampling:** Deploy static closed chambers on representative control (flooded) and project (AWD) plots.
        - **Gas Chromatography (GC):** Sample headspace air at 0, 10, 20, and 30 minutes to quantify $CH_4$ and $N_2O$ fluxes.
        - **Nitrous Oxide ($N_2O$) Check:** Crucial to verify that drying intervals do not trigger excessive $N_2O$ emissions that offset methane savings.
        """)
