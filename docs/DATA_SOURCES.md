# CarbonTrack: Data Sources, Provenance & Quality Documentation

## 1. Authoritative Data Catalog

| Dataset | Custodian / Source | URL | Spatial Granularity | Temporal Range | Units | Validation Status |
|---|---|---|---|---|---|---|
| **India Rice Cultivation & Paddy Production** | Food and Agriculture Organization (FAOSTAT) & DES India | [FAOSTAT Data Portal](https://www.fao.org/faostat/en/) | National (India) | 2010–2023 | Production (Million Tonnes), Area (M ha), Yield (t/ha) | 100% verified against UN FAO statistical records |
| **State-Level Agricultural Statistics** | Directorate of Economics & Statistics (DES), Ministry of Agriculture & Farmers Welfare, Govt of India | [DESAgri Portal](https://data.desagri.gov.in/) | 16 Major Indian States | 2018–2023 | Production (Mt), Area (M ha), Yield (t/ha), Irrigated Area (%) | Audited against Agricultural Statistics at a Glance |
| **District Agricultural Hotspots & Irrigation** | DES India & State Agricultural Directorates | [Agricoop](https://agricoop.nic.in/) | 37 Prominent Rice Districts | Multi-Year Agricultural Census | Area (kHa), Prod (kTonnes), Yield (t/ha), Dominant Source | Cross-referenced with minor irrigation census |
| **AWD Research Priority Index** | CarbonTrack Scientific Analytics Engine | Internal / Open Source | State & District | 2024–2026 Model Run | Index (0–100), Priority Tiering | Multi-criteria weighted matrix |
| **Methane Emission Factors & Scaling Parameters** | IPCC 2006 / 2019 Refinement & IRRI | [IPCC NGGIP](https://www.ipcc-nggip.iges.or.jp/) | Global & Regional Rice Paddies | AR5/AR6 GWP Standards | kg $CH_4$/ha/day, $tCO_2e$/ha, Scaling Factor $SF_w$ | IPCC Guidelines for National GHG Inventories |

---

## 2. Ingestion & Pre-Processing Pipeline

The data pipeline runs automatically via modular Python scripts:
1. `ingestion/faostat.py`: Ingests multi-year national time series (2010–2023) and standardizes milled and paddy rice metrics.
2. `processing/cleaning.py`: Performs schema validation, removes nulls/duplicates, checks type casting, and persists `faostat_rice_cleaned.csv`.
3. `ingestion/des_india.py`: Compiles official state and district datasets, extracting Kharif vs. Rabi (Boro) seasonal shares, irrigation percentages, dominant water sources, and soil drainage properties.
4. `analytics/regional_analysis.py`: Computes YoY growth rates, CAGR, national contribution shares, and saves `regional_analysis.csv` and `district_analysis.csv`.
5. `analytics/carbon_models.py`: Encapsulates IPCC Tier 1 & Tier 2 equations, baseline emission factor ($EF_{baseline} = 1.30\ \text{kg } CH_4\text{/ha/day}$), water regime scaling factor ($SF_w = 0.52$ for AWD), 20% registry buffer pool deduction, and irrigation water conservation metrics.
6. `analytics/research_priority.py`: Calculates the explainable composite AWD Research Priority Score (0–100) and saves `research_priority_scores.csv`.

---

## 3. Methodological Citations & Standards

- **IPCC (2019 Refinement):** 2019 Refinement to the 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 4: Agriculture, Forestry and Other Land Use, Chapter 5: Cropland - Rice Cultivation.
- **Verra VM0042 (v2.0):** Methodology for Improved Agricultural Land Management (ALM), including alternate wetting and drying regimes in flooded rice paddies.
- **UNFCCC CDM ACM0022:** Consolidated baseline methodology for water management in rice cultivation.
- **IRRI (Lampayan et al., 2015):** *Adoption and impact of alternate wetting and drying (AWD) for water and methane reduction in irrigated rice.* Field Crops Research, 170, 95-108.
- **Richards, M., & Sander, B. O. (2014):** *Alternate wetting and drying in irrigated rice: implementation guidance for policymakers and investors.* CCAFS Report No. 4.

---

## 4. Known Data Limitations & Field Information Requirements

1. **Macro Statistics vs. Cadastral Polygons:**
   Public datasets describe district aggregates, but do not provide individual farm parcel GIS boundaries. Developers must collect sub-meter GPS polygons (<0.5 ha) during pre-feasibility ground surveys.
2. **Irrigation Capacity vs. Field Drainage:**
   State statistics record "irrigated area," but AWD requires both water inlet access and active field drainage. Lowland areas with prolonged monsoon standing water are not suited for Kharif AWD.
3. **Milled vs. Rough Paddy Units:**
   Indian agricultural portals report milled rice, whereas international registries and FAOSTAT often reference unhusked rough paddy. CarbonTrack clearly denotes both units to prevent accounting errors.
