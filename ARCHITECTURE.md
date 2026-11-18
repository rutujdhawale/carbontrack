# CarbonTrack System Architecture & Mathematical Specifications

> **Technical Architecture, Mathematical Formulations, and MRV Engineering Framework for Agricultural Carbon Project Origination and Pre-Feasibility Intelligence.**

---

## 1. System Overview & Core Philosophy

CarbonTrack is an enterprise-grade agricultural intelligence and carbon project analytics platform engineered specifically for **Alternate Wetting and Drying (AWD)** project origination in India.

The platform bridges the gap between macro-level public agricultural statistics (UN FAOSTAT, Ministry of Agriculture DES India) and the micro-level rigorous requirements of international carbon registries (**Verra VM0042**, **UNFCCC CDM ACM0022**, and **Gold Standard**).

```
                      +------------------------------------------------+
                      |               PUBLIC DATA ASSETS               |
                      |  - UN FAOSTAT (National Time-Series 2010-2023) |
                      |  - DES India (State Agricultural Statistics)  |
                      |  - Agricoop (District Hotspots & Irrigation)   |
                      +-----------------------+------------------------+
                                              |
                                              v
                      +------------------------------------------------+
                      |         INGESTION & CLEANING PIPELINE          |
                      |  - ingestion/faostat.py & des_india.py         |
                      |  - processing/cleaning.py                      |
                      |  - Schema Validation & Deduplication Engine    |
                      +-----------------------+------------------------+
                                              |
                                              v
                      +------------------------------------------------+
                      |           SCIENTIFIC ANALYTICS ENGINES         |
                      |  - analytics/carbon_models.py (IPCC Engine)    |
                      |  - analytics/regional_analysis.py (Trends)     |
                      |  - analytics/research_priority.py (RPI Matrix) |
                      +-----------------------+------------------------+
                                              |
                                              v
                      +------------------------------------------------+
                      |           PRESENTATION & DASHBOARD LAYER       |
                      |  - pages/overview.py (Executive Macro KPIs)    |
                      |  - pages/regional_explorer.py (State/District) |
                      |  - pages/awd_intelligence.py (AWD Modeling)    |
                      |  - pages/report_generator.py (Audit Reports)   |
                      |  - pages/data_quality.py (Data Provenance)     |
                      +------------------------------------------------+
```

---

## 2. Platform Architecture Layers

### Layer 1: Ingestion & Data Harmonization Layer
- **`ingestion/faostat.py`**: Ingests national time-series data (2010–2023). Handles metric conversions between unhusked rough paddy and milled rice (using official conversion factor $1\text{ unit paddy} \approx 0.667\text{ units milled rice}$).
- **`ingestion/des_india.py`**: Compiles official state-level (16 states) and district-level (37 districts) agricultural datasets from the Directorate of Economics and Statistics (DES). Tracks Kharif vs. Rabi (Boro) production splits, irrigation command types (canals, tubewells, tanks), and soil drainage properties.
- **`processing/cleaning.py`**: Enforces strict typing, range validity, zero-null policies, and schema constraints before persisting cleaned CSVs to `data/processed/`.

### Layer 2: Scientific Analytics & Modeling Engines
- **`analytics/carbon_models.py`**: Executes IPCC Tier 1 and Tier 2 greenhouse gas accounting, water regime scaling calculations, non-permanence buffer pool deductions, and water conservation estimates.
- **`analytics/regional_analysis.py`**: Computes year-over-year production growth rates, yield CAGR, national production and area shares, and district-level feasibility classifications.
- **`analytics/research_priority.py`**: Evaluates the multi-criteria decision matrix to produce the **Research Priority Index (RPI)** for state and district origination.

### Layer 3: Presentation & User Interface Layer
- **`app.py`**: Central coordinator with brand-aligned UI (`#356B4A`, `#F6F5F0`), reactive sidebar navigation, and self-bootstrapping data initialization.
- **Streamlit Modular Pages**:
  - `pages/overview.py`: National KPIs, dual-axis historical trends, and strategic project origination funnel.
  - `pages/regional_explorer.py`: Interactive state rankings, district drill-downs, and season breakdowns.
  - `pages/awd_intelligence.py`: RPI priority tables, stacked dimension contribution charts, carbon & revenue calculator, field gap analysis, and MRV architecture.
  - `pages/report_generator.py`: Dynamic pre-feasibility research report generator exporting structured `.md` and `.txt` files.
  - `pages/data_quality.py`: Transparent data inventory, provenance metadata, audit health status, and direct CSV exports.

---

## 3. Detailed Mathematical Formulations

### 3.1 IPCC Methane Baseline Quantification

Methane emissions from continuously flooded rice paddies are quantified using the **IPCC 2006 / 2019 Refinement Guidelines for National Greenhouse Gas Inventories (Volume 4, Chapter 5: Cropland - Rice Cultivation)**:

$$\text{Daily Emission Rate } (\text{kg } CH_4/\text{ha/day}) = EF_{\text{baseline}} \times SF_w \times SF_p \times SF_o$$

$$\text{Seasonal Methane Baseline } (\text{kg } CH_4/\text{ha}) = \text{Daily Rate} \times t_{\text{cultivation}}$$

Where:
- $EF_{\text{baseline}} = 1.30\ \text{kg } CH_4\text{/ha/day}$: IPCC default baseline emission factor for continuously flooded fields without organic amendments.
- $SF_w = 1.00$: Baseline water regime scaling factor for continuous flooding throughout the growing period.
- $SF_p = 1.00$: Pre-season water regime factor (non-flooded pre-season $>180$ days).
- $SF_o$: Organic amendment scaling factor:
  - $SF_o = 1.00$: No organic amendment.
  - $SF_o = 1.15$: Farmyard manure (FYM $5\text{ t/ha}$).
  - $SF_o = 1.45$: Crop residue / straw incorporated $<30$ days before cultivation.
- $t_{\text{cultivation}} = 105\ \text{days}$: Average active rice cultivation window (transplanting to harvest drainage).

---

### 3.2 Alternate Wetting and Drying (AWD) Project Emissions

Under AWD, introducing intermittent aerobic drying intervals suppresses methanogenic archaea, applying a reduced water regime scaling factor $SF_{w, \text{AWD}}$:

$$\text{Seasonal Project Emissions } (\text{kg } CH_4/\text{ha}) = EF_{\text{baseline}} \times SF_{w, \text{AWD}} \times SF_p \times SF_o \times t_{\text{cultivation}}$$

| AWD Water Management Practice | Scaling Factor ($SF_{w, \text{AWD}}$) | Methane Reduction (%) |
|---|:---:|:---:|
| **Continuously Flooded (Baseline)** | $1.00$ | $0.0\%$ |
| **Single Aeration / Drainage** | $0.71$ | $29.0\%$ |
| **Multiple Aeration (Standard AWD)** | $0.52$ | $48.0\%$ |
| **Safe AWD with Pani Pipe ($-15\text{ cm}$)** | $0.45$ | $55.0\%$ |

---

### 3.3 Conversion to Carbon Dioxide Equivalents ($tCO_2e$)

Methane reductions are converted into metric tonnes of carbon dioxide equivalent ($tCO_2e$) using the **Global Warming Potential ($GWP_{100}$)** defined in the IPCC Fifth Assessment Report (AR5):

$$\Delta CH_4\ (\text{kg } CH_4/\text{ha}) = \text{Seasonal Baseline} - \text{Seasonal Project}$$

$$\text{Gross Abatement } (tCO_2e/\text{ha}) = \frac{\Delta CH_4 \times GWP_{CH_4}}{1,000}$$

Where:
- $GWP_{CH_4} = 28.0$ (IPCC AR5 standard without climate-carbon feedbacks).

---

### 3.4 Non-Permanence Risk Buffer & Net Creditable Offsets

To comply with **Verra VM0042 (v2.0)** and international risk governance, a mandatory risk buffer deduction is applied to account for non-permanence, reversals, and measurement uncertainty:

$$\text{Net Creditable Offsets } (tCO_2e/\text{ha}) = \text{Gross Abatement } (tCO_2e/\text{ha}) \times (1 - \beta)$$

$$\text{Total Project Net Credits } (tCO_2e) = \text{Net Creditable Offsets} \times A_{\text{project}}$$

Where:
- $\beta = 0.20$ ($20.0\%$ deduction deposited into the Verra AFOLU pooled buffer reserve).
- $A_{\text{project}}$: Total registered project area in hectares.

---

### 3.5 Irrigation Water Conservation Modeling

AWD substantially reduces water withdrawal by eliminating continuous percolation and surface evaporation:

$$\text{Water Saved per Hectare } (\text{m}^3/\text{ha}) = W_{\text{baseline}} \times \left(\frac{\eta_{\text{water}}}{100}\right)$$

$$\text{Total Water Conserved } (\text{Million Liters / ML}) = \frac{\text{Water Saved per Hectare} \times A_{\text{project}}}{1,000}$$

Where:
- $W_{\text{baseline}} = 11,000\ \text{m}^3/\text{ha}$: Standard water input for continuously flooded rice in India.
- $\eta_{\text{water}} = 28.0\%$: Empirically verified water savings rate under safe AWD protocols.

---

### 3.6 Pumping Energy & Secondary Fossil Fuel Savings

In tubewell-irrigated regions (e.g., Punjab, Haryana, Western Uttar Pradesh, Bihar), reduced irrigation pumping hours translate directly into fuel conservation:

$$\text{Diesel Fuel Conserved } (\text{Liters}) = \left[75.0 \times \left(\frac{\eta_{\text{water}}}{28.0}\right)\right] \times A_{\text{project}}$$

Where $75.0\ \text{L/ha}$ is the average diesel consumption avoided through a $28\%$ pumping reduction.

---

### 3.7 Economic & Smallholder Revenue Distribution

$$\text{Total Gross Carbon Revenue } (\$) = \text{Total Project Net Credits } (tCO_2e) \times P_{\text{carbon}}$$

$$\text{Smallholder Community Pool } (\$) = \text{Total Gross Carbon Revenue} \times \phi_{\text{farmer}}$$

$$\text{Incentive per Hectare } (\$/\text{ha}) = \frac{\text{Smallholder Community Pool}}{A_{\text{project}}}$$

Where:
- $P_{\text{carbon}}$: Market price per verified credit ($18.00\ \$/tCO_2e$ default).
- $\phi_{\text{farmer}} = 0.65$ ($65.0\%$ equitable revenue share allocated directly to participating farmers).

---

## 4. Multi-Criteria Research Priority Index (RPI)

To identify the most viable states and districts for early-stage investment, CarbonTrack employs a weighted, explainable multi-factor scoring algorithm:

$$RPI = \sum_{k=1}^{4} (w_k \times S_k)$$

$$RPI = (0.35 \times S_{\text{footprint}}) + (0.25 \times S_{\text{water}}) + (0.20 \times S_{\text{data}}) + (0.20 \times S_{\text{evidence}})$$

### Dimension Definitions & Normalization

1. **Rice Cultivation Footprint Score ($S_{\text{footprint}}$ - Weight: $35\%$):**
   Scales baseline rice production ($P_i$) against maximum state production ($P_{\max}$):
   $$S_{\text{footprint}} = \min\left(100.0,\ \max\left(30.0,\ 30.0 + \frac{P_i}{P_{\max}} \times 70.0\right)\right)$$

2. **Water Control & Irrigation Feasibility Score ($S_{\text{water}}$ - Weight: $25\%$):**
   Measures controlled irrigation coverage ($I_i$) critical for executing drying cycles:
   $$S_{\text{water}} = \min\left(100.0,\ \max\left(25.0,\ I_i \times 0.95 + 4.0\right)\right)$$

3. **Public Data Quality & Cadastral Transparency ($S_{\text{data}}$ - Weight: $20\%$):**
   Evaluates digital land registry accessibility, district reporting cadence, and agricultural statistical depth (scored $70.0\text{--}92.0$).

4. **Institutional AWD Evidence & Extension Readiness ($S_{\text{evidence}}$ - Weight: $20\%$):**
   Reflects documented historical AWD field trials conducted by State Agricultural Universities (PAU, TNAU, PJTSAU, BCKV, ANGRAU) and IRRI (scored $58.0\text{--}90.0$).

### Feasibility Tier Classifications

- **Tier 1: Prime Feasibility ($RPI \ge 85.0$):** High production footprint coupled with $>85\%$ controlled irrigation. Prime candidates for immediate pre-feasibility ground studies (Punjab, Uttar Pradesh, Telangana).
- **Tier 1: High Priority ($78.0 \le RPI < 85.0$):** Large acreage with seasonal or regional water control. Prioritize specific canal commands or the winter/summer Rabi/Boro season (Andhra Pradesh, Tamil Nadu, West Bengal, Haryana).
- **Tier 2: Moderate Priority ($60.0 \le RPI < 78.0$):** Moderate irrigation penetration; requires targeted drainage due diligence (Bihar, Karnataka, Odisha, Chhattisgarh, Gujarat).
- **Tier 3: Constrained / High Risk ($RPI < 60.0$):** Poor irrigation infrastructure or severe natural floodplain waterlogging where controlled drainage cannot be enforced (Assam, Maharashtra Konkan).

---

## 5. MRV (Measurement, Reporting, and Verification) Technical Protocol

To satisfy **Verra VM0042** and **CDM ACM0022** requirements, CarbonTrack specifies a multi-tiered MRV framework:

```
+-------------------------------------------------------------------------+
|                         TIERED MRV ARCHITECTURE                         |
+-------------------------------------------------------------------------+
|  Tier 1: In-Situ Hydrology      | 30 cm perforated PVC 'pani pipe'      |
|                                 | Installed 15 cm into topsoil          |
|                                 | Re-irrigate only when water reaches   |
|                                 | -15 cm threshold                      |
+---------------------------------+---------------------------------------+
|  Tier 2: Satellite Remote       | Sentinel-1 C-band Synthetic Aperture  |
|          Sensing (SAR)          | Radar (SAR) microwave backscatter     |
|                                 | Penetrates monsoon cloud cover        |
|                                 | Detects water vs dry aerated soil     |
+---------------------------------+---------------------------------------+
|  Tier 3: Digital Farmer Logs    | EXIF-timestamped, geo-tagged mobile   |
|                                 | photos looking down pani pipes        |
|                                 | Immutable digital audit trail         |
+---------------------------------+---------------------------------------+
|  Tier 4: Gas Flux Calibration   | Closed-chamber gas chromatography     |
|                                 | Baseline vs project test plots        |
|                                 | Monitors CH4 and N2O balance          |
+---------------------------------+---------------------------------------+
|  Tier 5: Third-Party VVB Audit  | Designated Operational Entity (DOE)   |
|                                 | Statistical random field inspection   |
|                                 | Registry credit issuance (VCUs)       |
+-------------------------------------------------------------------------+
```

---

## 6. Automated Report Generation Engine

The report generator ([pages/report_generator.py](file:///c:/Users/Rutuj%20Dhawale/Desktop/carbontrack/pages/report_generator.py)) automates pre-feasibility documentation:
1. Dynamically compiles state-level and district-level baselines.
2. Ingests user-specified project acreage ($A_{\text{project}}$), AWD water protocol, and carbon price.
3. Computes live mathematical carbon offsets, buffer pool reserves, and smallholder revenue splits.
4. Generates an audit-ready, structured Markdown document with executive summary, baseline data, mathematical quantifications, pre-feasibility checklists, and MRV specifications.
5. Provides instant one-click downloads in `.md` and `.txt` formats.

---

## 7. Verification & Automated Test Suite

The system includes automated tests in [tests/test_analytics.py](file:///c:/Users/Rutuj%20Dhawale/Desktop/carbontrack/tests/test_analytics.py) and [tests/test_cleaning.py](file:///c:/Users/Rutuj%20Dhawale/Desktop/carbontrack/tests/test_cleaning.py):
- `test_priority_scores_calculation`: Verifies schema, ranges $[0, 100]$, and priority classification.
- `test_data_integrity`: Verifies national FAOSTAT records, positive production, and complete columns.
- `test_regional_data_integrity`: Verifies 16-state multi-year records and year bounds ($2018\text{--}2023$).
- `test_district_analysis_integrity`: Validates 37 district hotspots, irrigation bounds, and positive abatement potentials.
- `test_carbon_abatement_model`: Asserts IPCC equations, gross abatement positivity, $20\%$ buffer math, and revenue consistency.
- `test_formatting_utilities`: Validates numerical formatters and units.
