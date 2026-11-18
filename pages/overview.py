"""
CarbonTrack - Executive Overview Dashboard.
Provides high-level national agricultural trends, emission profiles, and AWD context.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.formatting import (
    GREEN, TERRACOTTA, MUTED_COLOR, SURFACE_COLOR, BORDER_COLOR,
    apply_brand_theme, format_number
)

def render():
    st.title("🌾 Indian Rice Cultivation & Carbon Project Landscape")
    st.markdown(
        "A national intelligence dashboard for researchers, project developers, and climate investors "
        "evaluating **Alternate Wetting and Drying (AWD)** agricultural carbon offset opportunities in India."
    )
    st.divider()

    # Load national dataset
    try:
        df_faostat = pd.read_csv("data/processed/faostat_rice_cleaned.csv")
    except Exception as e:
        st.error(f"Error loading national dataset: {e}")
        return

    # Key Metrics Bar
    latest_rec = df_faostat.iloc[-1]
    prev_rec = df_faostat.iloc[-2]
    first_rec = df_faostat.iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            label="Annual Milled Rice Prod.",
            value=f"{latest_rec['Rice_Production']:.1f} Mt",
            delta=f"+{latest_rec['Rice_Production'] - prev_rec['Rice_Production']:.1f} Mt YoY"
        )
    with col2:
        st.metric(
            label="Total Rice Area Harvested",
            value=f"{latest_rec['Area_Harvested']:.1f} M ha",
            delta=f"+{latest_rec['Area_Harvested'] - prev_rec['Area_Harvested']:.1f} M ha YoY"
        )
    with col3:
        st.metric(
            label="National Average Yield",
            value=f"{latest_rec['Yield']:.2f} t/ha",
            delta=f"+{((latest_rec['Yield'] - first_rec['Yield']) / first_rec['Yield'] * 100):.1f}% since 2010"
        )
    with col4:
        irrig_share = latest_rec.get("Irrigation_Share_Pct", 67.0)
        st.metric(
            label="Rice Area Under Irrigation",
            value=f"{irrig_share:.1f}%",
            delta=f"+{(irrig_share - first_rec.get('Irrigation_Share_Pct', 58.0)):.1f}% pts"
        )
    with col5:
        # National methane estimate: ~3.4 Mt CH4 = ~95 Mt CO2e
        st.metric(
            label="Est. Annual CH₄ Emissions",
            value="~95 Mt CO₂e",
            delta="High Abatement Opportunity",
            delta_color="off"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Tabs for detailed perspectives
    tab1, tab2, tab3 = st.tabs([
        "📈 National Agricultural Trajectory (2010-2023)",
        "💧 Irrigation Dynamics & Yield Decoupling",
        "🎯 The Carbon Opportunity: Why Rice & AWD?"
    ])

    with tab1:
        st.markdown("### Production, Area, and Yield Evolution")
        st.caption("Official data sourced from FAOSTAT and Ministry of Agriculture & Farmers Welfare (DES India).")

        fig1 = go.Figure()
        # Production bar
        fig1.add_trace(go.Bar(
            x=df_faostat["Year"],
            y=df_faostat["Rice_Production"],
            name="Milled Production (Million Tonnes)",
            marker_color=GREEN,
            opacity=0.85,
            yaxis="y"
        ))
        # Area line
        fig1.add_trace(go.Scatter(
            x=df_faostat["Year"],
            y=df_faostat["Area_Harvested"],
            name="Area Harvested (Million Hectares)",
            mode="lines+markers",
            line=dict(color=TERRACOTTA, width=3),
            marker=dict(size=7),
            yaxis="y2"
        ))
        # Yield line
        fig1.add_trace(go.Scatter(
            x=df_faostat["Year"],
            y=df_faostat["Yield"],
            name="Yield (t/ha)",
            mode="lines+markers",
            line=dict(color="#2A78D6", width=2, dash="dot"),
            marker=dict(size=6),
            yaxis="y3"
        ))

        fig1.update_layout(
            height=460,
            yaxis=dict(title="Production (Million Tonnes)", side="left", showgrid=True),
            yaxis2=dict(title="Area (Million Hectares)", overlaying="y", side="right", showgrid=False, range=[35, 55]),
            yaxis3=dict(title="Yield (t/ha)", overlaying="y", side="right", position=0.95, showgrid=False, range=[1.8, 3.5]),
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0),
            margin=dict(l=50, r=80, t=50, b=40)
        )
        apply_brand_theme(fig1)
        st.plotly_chart(fig1, use_container_width=True)

        st.info(
            "💡 **Key Insight:** India's rice production expanded from 95.98 Mt (2010) to 137.83 Mt (2023), representing "
            "a **43.6% growth**, while land area increased only **10.6%**. This productivity expansion has been heavily "
            "driven by intensified irrigation and higher-yielding varieties, creating substantial, highly concentrated "
            "methane emission baselines in irrigated paddy ecologies."
        )

    with tab2:
        st.markdown("### Irrigation Penetration & Agricultural Intensification")
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            fig2 = px.area(
                df_faostat,
                x="Year",
                y="Irrigation_Share_Pct",
                title="Rice Area Under Controlled Irrigation (%)",
                color_discrete_sequence=[GREEN],
            )
            fig2.update_layout(height=360, yaxis_range=[50, 75], yaxis_title="% Irrigated")
            apply_brand_theme(fig2)
            st.plotly_chart(fig2, use_container_width=True)

        with col_chart2:
            # Yield vs Area Scatter to show decoupling
            fig3 = px.scatter(
                df_faostat,
                x="Area_Harvested",
                y="Yield",
                size="Rice_Production",
                color="Year",
                title="Yield vs. Area Harvested (Circle size = Production)",
                color_continuous_scale="Viridis",
            )
            fig3.update_layout(height=360, xaxis_title="Area (M ha)", yaxis_title="Yield (t/ha)")
            apply_brand_theme(fig3)
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("""
        **Why Irrigation Matters for Carbon Projects:**
        - **AWD Feasibility Requirement:** Alternate Wetting and Drying **cannot be practiced in purely rainfed lowlands** or uncontrolled deep floodplains because drying cycles cannot be enforced when water cannot be drained or re-supplied.
        - **Controlled Water Access:** The 67.0% of India's rice land with access to canal networks, shallow tubewells, and borewells constitutes the **prime addressable universe (~31.8 Million Hectares)** for carbon project development.
        """)

    with tab3:
        st.markdown("### Why Alternate Wetting and Drying (AWD)?")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("""
            #### 1. The Climate Challenge
            - **Global Methane Contribution:** Flooded rice cultivation accounts for ~8-12% of global agricultural GHG emissions and 1.5% of total anthropogenic GHGs.
            - **Anaerobic Soil Biology:** Continuously flooded paddies block atmospheric oxygen, creating anoxic soil conditions where methanogenic archaea decompose organic matter into methane ($CH_4$).
            - **Methane Potency:** Methane is 28x more potent than $CO_2$ over a 100-year timescale (GWP 28).
            """)
        with c2:
            st.markdown("""
            #### 2. The AWD Mechanism
            - **Intermittent Aeration:** Fields are alternately flooded and allowed to dry for 2 to 7 days until the water table drops to 15 cm below soil surface (safe AWD threshold).
            - **Aerobic Micro-intervals:** Introducing oxygen into the topsoil inhibits methanogens and promotes methanotrophic bacteria that oxidize methane into benign carbon dioxide.
            - **Zero Yield Penalty:** Documented by IRRI across thousands of multi-country field trials without yield reduction when maintained above the 15 cm limit.
            """)
        with c3:
            st.markdown("""
            #### 3. Co-benefits & Economics
            - **30% - 50% Methane Reduction:** Validated under Verra VM0042 and CDM ACM0022 methodologies.
            - **20% - 30% Irrigation Water Conserved:** Critical for depleting aquifers in Punjab, Haryana, and Telangana.
            - **Energy Cost Savings:** Reduces diesel consumption and pumping electricity by 25-35%.
            - **Direct Farmer Carbon Revenue:** Provides recurring cash payouts to smallholders through aggregated carbon credits.
            """)

    st.divider()

    # Strategic Decision Framework
    st.markdown("### 🗺️ CarbonTrack Early-Stage Project Screening Funnel")
    st.markdown(
        "How publicly available agricultural data guides carbon project developers from macro screening to field execution:"
    )

    stage_cols = st.columns(4)
    with stage_cols[0]:
        st.markdown("""
        <div style="background: white; border: 1px solid #E4E2DA; border-radius: 8px; padding: 16px; min-height: 220px;">
            <div style="color: #356B4A; font-weight: 600; font-size: 0.9rem;">STAGE 1</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin: 4px 0 8px 0;">Macro Screening</div>
            <p style="font-size: 0.85rem; color: #777B72; margin: 0;">
                Analyze state-level rice production (>5 Mt) and irrigation penetration (>60%) using DES and FAOSTAT data to identify high-density baseline emission clusters.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with stage_cols[1]:
        st.markdown("""
        <div style="background: white; border: 1px solid #E4E2DA; border-radius: 8px; padding: 16px; min-height: 220px;">
            <div style="color: #356B4A; font-weight: 600; font-size: 0.9rem;">STAGE 2</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin: 4px 0 8px 0;">District Hotspots</div>
            <p style="font-size: 0.85rem; color: #777B72; margin: 0;">
                Evaluate district acreage, irrigation command infrastructure (canals vs tubewells), soil drainage, and seasonal water control (Rabi/Boro vs Kharif).
            </p>
        </div>
        """, unsafe_allow_html=True)
    with stage_cols[2]:
        st.markdown("""
        <div style="background: white; border: 1px solid #E4E2DA; border-radius: 8px; padding: 16px; min-height: 220px;">
            <div style="color: #356B4A; font-weight: 600; font-size: 0.9rem;">STAGE 3</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin: 4px 0 8px 0;">Pre-Feasibility</div>
            <p style="font-size: 0.85rem; color: #777B72; margin: 0;">
                Deploy field surveys for plot boundaries, tenure verification, baseline water management practices, farmer willingness (FPIC), and FPO partnerships.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with stage_cols[3]:
        st.markdown("""
        <div style="background: white; border: 1px solid #E4E2DA; border-radius: 8px; padding: 16px; min-height: 220px;">
            <div style="color: #356B4A; font-weight: 600; font-size: 0.9rem;">STAGE 4</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin: 4px 0 8px 0;">MRV & Crediting</div>
            <p style="font-size: 0.85rem; color: #777B72; margin: 0;">
                Implement perforated pani pipes, Sentinel-1 SAR satellite monitoring, mobile farmer check-ins, and third-party VVB validation under Verra VM0042.
            </p>
        </div>
        """, unsafe_allow_html=True)
