"""
CarbonTrack - Evidence-Backed Research Report Generator.
Generates comprehensive, audit-ready pre-feasibility research reports
for agricultural carbon project developers and research teams.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from analytics.carbon_models import calculate_awd_abatement, GWP_CH4, IPCC_BASE_EF_CH4

def render():
    st.title("📄 Evidence-Backed Research Report Generator")
    st.markdown(
        "Generate a structured, evidence-backed pre-feasibility research report "
        "tailored to any Indian state or rice-growing region for project development and investment review."
    )
    st.divider()

    # Load data
    try:
        df_state = pd.read_csv("data/processed/regional_analysis.csv")
        df_priority = pd.read_csv("data/processed/research_priority_scores.csv")
        df_district = pd.read_csv("data/processed/district_analysis.csv")
    except Exception as e:
        st.error(f"Error loading analytical data: {e}")
        return

    # User Configuration
    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    with col_cfg1:
        state_list = sorted(df_state["State"].unique())
        selected_state = st.selectbox("Select Target State", options=state_list, index=0)
        target_ha = st.number_input("Target Project Scope (Hectares)", min_value=500.0, max_value=200000.0, value=10000.0, step=1000.0)

    with col_cfg2:
        regime_opt = st.selectbox(
            "Selected AWD Practice",
            options=["Multiple Aeration (Standard AWD)", "Safe AWD with pani pipe (-15 cm)", "Single Aeration / Drainage"]
        )
        carbon_price = st.number_input("Carbon Credit Price Assumption ($/tCO₂e)", min_value=5.0, max_value=60.0, value=18.0, step=1.0)

    with col_cfg3:
        author = st.text_input("Lead Author / Organization", value="CarbonTrack Agricultural Research Team")
        report_date = datetime.now().strftime("%B %d, %Y")
        include_mrv = st.checkbox("Include Complete MRV Architecture", value=True)

    # Fetch State metrics
    state_hist = df_state[df_state["State"] == selected_state].sort_values("Year")
    latest_rec = state_hist.iloc[-1]
    priority_rec = df_priority[df_priority["State"] == selected_state].iloc[0] if not df_priority[df_priority["State"] == selected_state].empty else None
    state_districts = df_district[df_district["State"] == selected_state]

    # Calculate model projections
    res = calculate_awd_abatement(
        area_ha=target_ha,
        cultivation_days=105,
        water_regime=regime_opt,
        carbon_price_usd=carbon_price
    )

    # Build Report Content in Markdown
    dist_table_md = "| District | Area (kHa) | Prod (kTonnes) | Yield (t/ha) | Irrigated % | Source | AWD Feasibility Tier |\n|---|---|---|---|---|---|---|\n"
    if not state_districts.empty:
        for _, d in state_districts.iterrows():
            dist_table_md += f"| {d['District']} | {d['Area_kHa']:,.0f} | {d['Prod_kTonnes']:,.0f} | {d['Yield']:.2f} | {d['Irrigated_Pct']:.1f}% | {d['Source']} | {d['AWD_Tier']} |\n"
    else:
        dist_table_md += f"| Multiple Blocks ({selected_state}) | {latest_rec['Area']*100:,.0f} | {latest_rec['Production']*100:,.0f} | {latest_rec['Yield']:.2f} | {latest_rec['Irrigation_Pct']:.1f}% | {latest_rec['Dominant_Source']} | Regional Cluster |\n"

    report_markdown = f"""# AGRICULTURAL CARBON PROJECT PRE-FEASIBILITY REPORT
**Target Region:** {selected_state}, India  
**Date of Assessment:** {report_date}  
**Lead Evaluator:** {author}  
**Methodological Standard:** IPCC 2019 Refinement / Verra VM0042 (v2.0) / CDM ACM0022  

---

## 1. EXECUTIVE SUMMARY & RESEARCH PRIORITY RATING
- **Target State:** {selected_state}
- **CarbonTrack Research Priority Score:** **{priority_rec['Research_Priority_Score'] if priority_rec is not None else 'N/A'}/100** ({priority_rec['Status'] if priority_rec is not None else 'N/A'})
- **Strategic Recommendation:** {priority_rec['Strategic_Recommendation'] if priority_rec is not None else 'Under Review'}
- **Evaluated Project Acreage:** {target_ha:,.0f} Hectares
- **Gross Methane Abatement:** **{res['total_gross_abatement_tco2e']:,.0f} tCO₂e/season** ({res['gross_abatement_tco2e_ha']} tCO₂e/ha)
- **Net Issued Carbon Credits (VCUs):** **{res['total_net_credits_tco2e']:,.0f} tCO₂e/season** (after 20% registry buffer pool deduction)
- **Gross Offset Revenue:** **${res['gross_revenue_usd']:,.2f} USD** (at ${carbon_price:.2f}/tCO₂e)
- **Smallholder Revenue Pool (65% share):** **${res['farmer_pool_revenue_usd']:,.2f} USD** (~${(res['farmer_pool_revenue_usd']/target_ha):.2f}/ha)
- **Conserved Irrigation Water:** **{res['total_water_saved_million_liters']:,.0f} Million Liters**

---

## 2. REGIONAL AGRICULTURAL & IRRIGATION BASELINE
According to official statistics from the Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers Welfare:
- **Total Annual Rice Production:** {latest_rec['Production']:.2f} Million Metric Tonnes
- **Total Rice Cultivated Area:** {latest_rec['Area']:.2f} Million Hectares
- **State Average Rice Yield:** {latest_rec['Yield']:.2f} t/ha (compared to national average ~2.91 t/ha)
- **Rice Area Under Irrigation:** **{latest_rec['Irrigation_Pct']:.1f}%**
- **Predominant Irrigation Infrastructure:** {latest_rec['Dominant_Source']}
- **Seasonal Distribution:** Kharif (Monsoon): {latest_rec['Kharif_Share_Pct']:.1f}% | Rabi / Boro (Summer): {latest_rec['Rabi_Share_Pct']:.1f}%

### Priority District Hotspots in {selected_state}:
{dist_table_md}

---

## 3. CARBON ABATEMENT METHODOLOGY & QUANTIFICATION
Calculations follow **IPCC 2019 Refinement to the 2006 Guidelines (Volume 4, Chapter 5)** and **Verra VM0042 Methodology for Improved Agricultural Land Management**:

$$\\text{{Baseline Emissions}} = EF_{{baseline}} \\times SF_w \\times SF_p \\times SF_o \\times t_{{days}} \\times GWP_{{CH_4}}$$

- **Baseline Emission Factor ($EF_{{baseline}}$):** {IPCC_BASE_EF_CH4} kg $CH_4$/ha/day
- **AWD Water Regime Scaling Factor ($SF_w$):** {regime_opt} ($SF_w = 0.52$)
- **Global Warming Potential ($GWP_{{CH_4}}$):** {GWP_CH4} (IPCC AR5 100-year timescale)
- **Cultivation Duration:** 105 days
- **Methane Emission Reduction Rate:** **{res['reduction_percentage']}%** relative to continuous flooding
- **Conservatism / Buffer Deduction:** 20% reserved for non-permanence buffer pool

---

## 4. PRE-FEASIBILITY FIELD DATA GAPS & COLLECTION PROTOCOL
While public datasets validate regional eligibility, the project team must collect the following primary field data before investment approval:
1. **Cadastral Boundary Mapping:** Sub-meter GPS polygon coordinates for each farm parcel (<0.5 ha).
2. **Farmer Tenure & FPIC:** Documented Free, Prior and Informed Consent and verifiable land title (patta or leasehold agreements).
3. **Historical Baseline Hydrology:** Proof that fields were continuously flooded for ≥30 consecutive days under pre-project practice.
4. **Percolation & Bund Survey:** Minimum bund height of 15 cm and loam/clay soil profile with acceptable percolation rates (<5 mm/day).
5. **Irrigation Control Audit:** Verification of independent or clustered tubewell / sluice gate operation allowing controlled drying.

---

## 5. MRV (MEASUREMENT, REPORTING & VERIFICATION) PROTOCOL
To achieve carbon registry issuance under Verra / Gold Standard / CDM:
- **Field Pani Pipe Monitoring:** Perforated 30 cm PVC pipe installed per 1-2 ha; drying cycle verified when water drops 15 cm below ground.
- **Sentinel-1 SAR Remote Sensing:** 6-12 day revisit C-band microwave backscatter ($\sigma^0$) to confirm field drainage without cloud interference.
- **Farmer Digital App:** Timestamped, geo-tagged mobile photos looking down pani pipes during drying intervals.
- **Independent VVB Audit:** Designated Operational Entity (DOE) statistical ground sampling and audit trail verification.

---

## 6. RISK MITIGATION & FINANCIAL SUMMARY
- **Water Stress Risk:** Irrigation must be available on demand when pani pipe threshold (-15 cm) is reached.
- **Nitrous Oxide ($N_2O$) Trade-off:** Drying periods must not exceed 7 days to prevent aerobic nitrification/denitrification $N_2O$ spikes.
- **Smallholder Benefit Sharing:** 65% of net revenues (${res['farmer_pool_revenue_usd']:,.0f} USD) directed to participating farmers to guarantee high long-term adoption.

*Report compiled via CarbonTrack Agricultural Intelligence Platform.*
"""

    st.markdown("### 🔍 Live Report Preview")
    with st.expander("Expand to Preview Full Report", expanded=True):
        st.markdown(report_markdown)

    st.markdown("<br>", unsafe_allow_html=True)

    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        st.download_button(
            label=f"📥 Download Full Research Report for {selected_state} (.md)",
            data=report_markdown,
            file_name=f"CarbonTrack_Research_Report_{selected_state.replace(' ', '_')}.md",
            mime="text/markdown",
            key="dl_rep_md"
        )
    with col_b2:
        st.download_button(
            label=f"📄 Download Plain Text Summary (.txt)",
            data=report_markdown,
            file_name=f"CarbonTrack_Research_Report_{selected_state.replace(' ', '_')}.txt",
            mime="text/plain",
            key="dl_rep_txt"
        )
