"""
CarbonTrack - Regional & District Agricultural Explorer.
Enables researchers to analyze state-level and district-level rice cultivation,
yield trajectories, irrigation coverage, and season breakdowns.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.formatting import (
    GREEN, TERRACOTTA, MUTED_COLOR, apply_brand_theme, format_number
)

def render():
    st.title("🗺️ Regional & District Agricultural Explorer")
    st.markdown(
        "Explore historical trends, district hotspots, irrigation access, and seasonal breakdowns "
        "across India's top rice-producing states. Official data from DES India (2018–2023)."
    )
    st.divider()

    # Load datasets
    try:
        df_state = pd.read_csv("data/processed/regional_analysis.csv")
        df_district = pd.read_csv("data/processed/district_analysis.csv")
    except Exception as e:
        st.error(f"Error loading regional datasets: {e}")
        return

    # Sub-navigation tabs
    tab_state, tab_district, tab_deepdive = st.tabs([
        "📊 State-Level Landscape & Rankings",
        "🎯 District Hotspots & Feasibility",
        "📈 Multi-Year Trends & Season Dynamics"
    ])

    # ---------------- TAB 1: STATE LEVEL ----------------
    with tab_state:
        st.subheader("State-Level Rice Production & Irrigation Profile")
        latest_year = int(df_state["Year"].max())
        latest_df = df_state[df_state["Year"] == latest_year].sort_values(by="Production", ascending=False).reset_index(drop=True)

        # Filters
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            all_states = sorted(latest_df["State"].unique().tolist())
            selected_states = st.multiselect(
                "Filter States",
                options=all_states,
                default=all_states[:8],
                help="Select states to display in charts and comparison table."
            )
        with col_f2:
            min_irrig = st.slider("Minimum Irrigation Coverage (%)", min_value=0, max_value=100, value=0, step=5)

        filtered_df = latest_df[
            (latest_df["State"].isin(selected_states)) &
            (latest_df["Irrigation_Pct"] >= min_irrig)
        ].copy()

        # Summary KPIs
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Total Selected Production", f"{filtered_df['Production'].sum():.1f} Mt")
        with k2:
            st.metric("Total Selected Rice Area", f"{filtered_df['Area'].sum():.1f} M ha")
        with k3:
            avg_yield = filtered_df['Production'].sum() / filtered_df['Area'].sum() if filtered_df['Area'].sum() > 0 else 0
            st.metric("Weighted Average Yield", f"{avg_yield:.2f} t/ha")
        with k4:
            st.metric("Top Rice Producer", f"{latest_df.iloc[0]['State']} ({latest_df.iloc[0]['Production']:.1f} Mt)")

        st.markdown("<br>", unsafe_allow_html=True)

        # Visualizations
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fig_prod = px.bar(
                filtered_df,
                x="Production",
                y="State",
                orientation="h",
                color="Irrigation_Pct",
                title=f"Rice Production ({latest_year}) by State colored by Irrigation %",
                color_continuous_scale="Greens",
                labels={"Production": "Production (Million Tonnes)", "Irrigation_Pct": "Irrigation %"}
            )
            fig_prod.update_layout(height=420, yaxis={'categoryorder':'total ascending'})
            apply_brand_theme(fig_prod)
            st.plotly_chart(fig_prod, use_container_width=True)

        with col_c2:
            fig_scatter = px.scatter(
                filtered_df,
                x="Irrigation_Pct",
                y="Yield",
                size="Production",
                color="State",
                title="Yield vs. Irrigation Coverage (Bubble size = Production)",
                labels={"Irrigation_Pct": "Irrigated Rice Area (%)", "Yield": "Yield (t/ha)"},
                hover_data=["Dominant_Source"]
            )
            fig_scatter.update_layout(height=420)
            apply_brand_theme(fig_scatter)
            st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("#### Comprehensive State Comparison Table")
        display_cols = ["State", "Production", "Area", "Yield", "Irrigation_Pct", "Dominant_Source", "Kharif_Share_Pct", "Rabi_Share_Pct"]
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                "Production": "Production (Mt)",
                "Area": "Area (M ha)",
                "Yield": "Yield (t/ha)",
                "Irrigation_Pct": "Irrigated %",
                "Dominant_Source": "Predominant Irrigation Source",
                "Kharif_Share_Pct": "Kharif (Monsoon) %",
                "Rabi_Share_Pct": "Rabi (Winter/Boro) %"
            }),
            use_container_width=True,
            hide_index=True
        )

    # ---------------- TAB 2: DISTRICT HOTSPOTS ----------------
    with tab_district:
        st.subheader("District-Level Rice Hotspots & AWD Feasibility")
        st.markdown(
            "District-level granularity is critical for project origination: projects are aggregated "
            "at the canal command, block, or district cluster level rather than state boundaries."
        )

        col_d1, col_d2 = st.columns([1, 2])
        with col_d1:
            selected_district_state = st.selectbox(
                "Select State for District Drilldown",
                options=sorted(df_district["State"].unique()),
                index=0
            )
        with col_d2:
            tier_filter = st.multiselect(
                "Filter by AWD Feasibility Tier",
                options=sorted(df_district["AWD_Tier"].unique()),
                default=sorted(df_district["AWD_Tier"].unique())
            )

        state_districts = df_district[
            (df_district["State"] == selected_district_state) &
            (df_district["AWD_Tier"].isin(tier_filter))
        ].copy()

        if state_districts.empty:
            st.warning("No districts match the selected filters.")
        else:
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("Districts Evaluated", len(state_districts))
            with col_m2:
                st.metric("Total District Rice Area", f"{state_districts['Area_kHa'].sum():,.0f} kHa")
            with col_m3:
                st.metric(
                    "Annual Abatement Potential (20% adoption)",
                    f"{state_districts['Methane_Abatement_Potential_tCO2e'].sum():,.0f} tCO₂e/yr"
                )

            # Chart of districts
            fig_dist = px.bar(
                state_districts.sort_values(by="Prod_kTonnes", ascending=False),
                x="District",
                y="Prod_kTonnes",
                color="AWD_Tier",
                title=f"Rice Production by District in {selected_district_state} (Thousand Tonnes)",
                labels={"Prod_kTonnes": "Production (kTonnes)"},
                color_discrete_map={
                    "Tier 1: Prime Controlled": GREEN,
                    "Tier 2: Seasonally Feasible": TERRACOTTA,
                    "Tier 3: Drainage Risk": "#D03B3B"
                }
            )
            fig_dist.update_layout(height=380)
            apply_brand_theme(fig_dist)
            st.plotly_chart(fig_dist, use_container_width=True)

            st.markdown(f"#### District Profiles for {selected_district_state}")
            dist_cols = [
                "District", "Area_kHa", "Prod_kTonnes", "Yield", "Irrigated_Pct",
                "Source", "Soil_Type", "Drainage", "AWD_Tier", "Methane_Abatement_Potential_tCO2e"
            ]
            st.dataframe(
                state_districts[dist_cols].rename(columns={
                    "Area_kHa": "Area (kHa)",
                    "Prod_kTonnes": "Production (kTonnes)",
                    "Yield": "Yield (t/ha)",
                    "Irrigated_Pct": "Irrigated %",
                    "Source": "Irrigation Source",
                    "Soil_Type": "Soil Type",
                    "Drainage": "Natural Drainage",
                    "AWD_Tier": "AWD Suitability Tier",
                    "Methane_Abatement_Potential_tCO2e": "Abatement Potential (tCO₂e/yr)"
                }),
                use_container_width=True,
                hide_index=True
            )

    # ---------------- TAB 3: MULTI-YEAR TRENDS & SEASONS ----------------
    with tab_deepdive:
        st.subheader("Historical Trajectories & Seasonal Water Control (2018–2023)")

        col_trend_state, col_metric_type = st.columns([2, 1])
        with col_trend_state:
            trend_states = st.multiselect(
                "Select States for Multi-Year Comparison",
                options=sorted(df_state["State"].unique()),
                default=["Punjab", "West Bengal", "Telangana", "Uttar Pradesh", "Andhra Pradesh"]
            )
        with col_metric_type:
            metric_choice = st.selectbox(
                "Select Metric to Track",
                options=["Production", "Yield", "Area"]
            )

        trend_df = df_state[df_state["State"].isin(trend_states)]

        fig_trend = px.line(
            trend_df,
            x="Year",
            y=metric_choice,
            color="State",
            markers=True,
            title=f"Multi-Year {metric_choice} Trajectory (2018–2023)",
            labels={
                "Production": "Production (Million Tonnes)",
                "Yield": "Yield (t/ha)",
                "Area": "Area (Million Hectares)"
            }
        )
        fig_trend.update_layout(height=420)
        apply_brand_theme(fig_trend)
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🌾 Seasonal Breakdown: Kharif vs. Rabi (Boro / Summer) Rice")
        st.markdown("""
        **Strategic Implication for AWD Projects:**
        - **Kharif (Monsoon) Rice:** Accounts for ~80-85% of total Indian rice acreage, but during heavy monsoon downpours, field drainage can be difficult in flat lowlands.
        - **Rabi / Boro (Winter/Summer) Rice:** In states like **West Bengal (26% Boro)**, **Telangana (42% Rabi/Yasangi)**, **Tamil Nadu (65% Samba/Navarai)**, and **Andhra Pradesh (35% Rabi)**, rice is grown under **almost 100% controlled irrigation** with virtually zero erratic monsoon rainfall.
        - **Prime Carbon Window:** Boro and Rabi seasons provide **the ideal operational window for AWD carbon projects**, as farmers have total control over water inlet sluices and tubewell switches.
        """)

        # Stacked bar chart of seasonal share
        fig_season = go.Figure()
        sorted_season_df = latest_df.sort_values(by="Rabi_Share_Pct", ascending=False)
        fig_season.add_trace(go.Bar(
            name="Kharif (Monsoon) %",
            x=sorted_season_df["State"],
            y=sorted_season_df["Kharif_Share_Pct"],
            marker_color=GREEN
        ))
        fig_season.add_trace(go.Bar(
            name="Rabi / Boro (Summer) %",
            x=sorted_season_df["State"],
            y=sorted_season_df["Rabi_Share_Pct"],
            marker_color=TERRACOTTA
        ))
        fig_season.update_layout(
            barmode="stack",
            title="Rice Production Season Breakdown (%) by State",
            yaxis=dict(title="Percentage Share (%)", range=[0, 100]),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0)
        )
        apply_brand_theme(fig_season)
        st.plotly_chart(fig_season, use_container_width=True)
