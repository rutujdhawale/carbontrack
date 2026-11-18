# 🌱 CarbonTrack: Agricultural Carbon Intelligence Platform
---

## Overview

Rice cultivation is the **3rd largest anthropogenic source of methane ($CH_4$) globally**, contributing ~8–12% of agricultural greenhouse gas emissions. India, as the world's 2nd largest rice producer (~137.8 Million Tonnes of milled rice across 47.4 Million Hectares), possesses one of the world's largest agricultural decarbonization opportunities.

**Alternate Wetting and Drying (AWD)** is a scientifically validated water management practice that reduces rice methane emissions by **30%–50%** and conserves **20%–30%** of irrigation water without yield penalty. **CarbonTrack** provides the quantitative foundation to screen regions, quantify carbon offsets, structure MRV protocols, and originate high-integrity carbon projects under **Verra VM0042** and **CDM ACM0022** methodologies.

---

## Core Questions Answered

### 1. Which Indian states and districts have substantial rice-growing activity?
- **Top Producing States:** West Bengal (16.65 Mt), Uttar Pradesh (15.66 Mt), Punjab (13.15 Mt), Telangana (12.30 Mt), Odisha (9.29 Mt), Chhattisgarh (8.24 Mt), Andhra Pradesh (8.15 Mt), and Bihar (7.42 Mt).
- **Key District Hotspots:**
  - *Punjab:* Sangrur (290 kHa), Ludhiana (258 kHa), Patiala (235 kHa)
  - *West Bengal:* Purba Bardhaman (440 kHa), Paschim Medinipur (380 kHa), Murshidabad (350 kHa)
  - *Telangana:* Nalgonda (295 kHa), Suryapet (220 kHa), Nizamabad (195 kHa)
  - *Andhra Pradesh:* Krishna (245 kHa), West Godavari (230 kHa), East Godavari (215 kHa)
  - *Uttar Pradesh:* Shahjahanpur (210 kHa), Gorakhpur (195 kHa), Barabanki (185 kHa)
  - *Haryana:* Karnal (172 kHa), Kaithal (168 kHa), Kurukshetra (122 kHa)

### 2. How have cultivation, production, yield and irrigation patterns changed over time?
- **Yield Decoupling (2010–2023):** National rice production expanded by **+43.6%** (95.98 Mt to 137.83 Mt) while harvested area increased only **+10.6%** (42.86 M ha to 47.40 M ha), driven by yield gains from 2.24 t/ha to 2.91 t/ha.
- **Irrigation Penetration:** Rice area under irrigation expanded from **58.0% (2010) to 67.0% (2023)**. States with >90% irrigation (Punjab, Haryana, Andhra Pradesh, Tamil Nadu, Telangana) achieve yields exceeding 3.5–4.5 t/ha.
- **Seasonal Water Control:** Kharif (Monsoon) represents ~80–85% of national output, but **Rabi / Boro (Winter/Summer) rice** in West Bengal (26% Boro), Telangana (42% Rabi), and Tamil Nadu (65% Samba) is cultivated under 100% controlled irrigation with zero monsoon flooding—representing the prime operational window for AWD.

### 3. Which regions may be worth investigating for agricultural carbon projects?
CarbonTrack implements an explainable **Research Priority Index (0–100)**:
- **Tier 1 (Prime Feasibility - High Score & Controlled Water):**
  - **Punjab (90.9):** 99.6% irrigation, severe groundwater depletion, huge water-saving incentive.
  - **Uttar Pradesh (86.5):** 15.66 Mt production, 84.2% irrigation, Western UP tubewell belt.
  - **Telangana (86.2):** 89.4% irrigation, massive Rabi (Yasangi) acreage, extensive borewell networks.
  - **Andhra Pradesh (81.9):** 96.2% irrigation, canal commands in Godavari & Krishna deltas.
  - **Tamil Nadu (80.3):** 93.8% irrigation, Cauvery delta command, active institutional AWD trials.
  - **West Bengal (80.2):** #1 national producer (16.65 Mt); prime focus on the 3.5 Mt Boro season.
  - **Haryana (78.7):** 99.8% irrigation, high yields, Basmati and non-Basmati clusters.
- **Tier 2 (Moderate Priority / Localized Command):** Bihar (68.2), Karnataka (66.8), Odisha (63.9), Chhattisgarh (61.1).
- **Tier 3 (High Drainage Risk / Low Irrigation):** Assam (50.9) due to flood-prone river basin hydrology.

### 4. What information is available from public datasets?
- **Available:** National and state historical production, area, and yield (FAOSTAT / DES India 2010–2023), district acreage and production totals, irrigation source breakdown (canals, tubewells, tanks), and broad agro-ecological zones.

### 5. What additional field-level information must be collected before assessing a project?
1. **Sub-meter GPS Field Polygons (<0.5 ha)** with cadastral survey numbers.
2. **Farmer KYC, Tenancy Proof & Signed FPIC** (Free, Prior and Informed Consent).
3. **Historical Baseline Hydrology** (proof of ≥30 days continuous flooding).
4. **Soil Drainage & Micro-Topography** (percolation rates, bund height >15 cm, water stagnation risk).
5. **Irrigation Infrastructure Audits** (pumping horsepower, flow rate, electricity schedule, canal turn frequency).
6. **Residue Management Practice** (straw incorporation vs. burning vs. removal).

### 6. What is required to monitor and verify an AWD-based carbon project?
- **In-Situ Field Sensors:** Perforated 30 cm PVC *pani pipes* installed 15 cm into topsoil to monitor water table drawdown.
- **Satellite Radar (SAR):** Sentinel-1 C-band Synthetic Aperture Radar microwave backscatter ($\sigma^0$) to remotely detect field drainage and flooding cycles through heavy monsoon cloud cover.
- **Traceable Mobile Farmer Logs:** Timestamped, geo-tagged mobile photographs looking down pani pipes during drying intervals.
- **GHG Chamber Sampling:** Static closed-chamber gas chromatography on sample plots to calibrate emission models and check $N_2O$ trade-offs.
- **Third-Party Registry Audit:** Designated Operational Entity (DOE / VVB) verification under Verra VM0042 / CDM ACM0022.

---

## Architecture & Dashboards

```
carbontrack/
│
├── app.py                         # Master Streamlit application & custom brand UI
├── pytest.ini                     # Test configuration
├── requirements.txt               # Dependencies
├── README.md                      # Platform documentation
│
├── .streamlit/
│   └── config.toml                # Custom theme & sidebar configuration
│
├── pages/
│   ├── overview.py                # Executive Overview: National trends, metrics, and funnel
│   ├── regional_explorer.py       # State rankings, district hotspots, and multi-year trajectories
│   ├── awd_intelligence.py        # Priority scoring, carbon offset calculator, field gap, and MRV
│   ├── report_generator.py        # Automated Evidence-Backed Research Report Generator (.md / .txt)
│   └── data_quality.py            # Data governance, pedigree, and CSV downloads
│
├── analytics/
│   ├── carbon_models.py           # IPCC 2019 Refinement & Verra carbon calculations
│   ├── regional_analysis.py       # State & district trend analytics
│   └── research_priority.py       # Multi-criteria research priority scoring engine
│
├── ingestion/
│   ├── faostat.py                 # UN FAOSTAT national rice time-series ingestion
│   └── des_india.py               # Ministry of Agriculture DES state & district data
│
├── processing/
│   └── cleaning.py                # Schema validation & data cleaning pipeline
│
├── utils/
│   └── formatting.py              # Brand colors, Plotly layouts, and numerical formatters
│
├── docs/
│   └── DATA_SOURCES.md            # Detailed data dictionary & methodology citations
│
└── tests/
    ├── test_analytics.py          # Unit tests for scoring, carbon models, and data integrity
    └── test_cleaning.py           # Data cleaning unit tests
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.11)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Pipeline (Self-Initializing)
Data ingestion and processing pipelines run automatically on startup, or can be triggered manually:
```bash
python -m ingestion.faostat
python -m processing.cleaning
python -m ingestion.des_india
python -m analytics.regional_analysis
python -m analytics.research_priority
```

### 4. Run Automated Test Suite
```bash
pytest -v
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---


