# 🐦 Bird Species Observation Analysis

Forest vs. Grassland biodiversity analysis across 11 U.S. National Park Service administrative units — from raw multi-sheet survey data to a cleaned dataset, exploratory analysis, and an interactive Streamlit dashboard.

🔗 **Live Dashboard:** [Add your Streamlit Cloud link here once deployed]

---

## 📌 Overview

This project analyzes bird observation survey data collected across forest and grassland habitats to understand species distribution, seasonal activity patterns, and the influence of environmental conditions on bird populations — with insights relevant to habitat conservation and biodiversity management.

- **Domain:** Environmental Studies · Biodiversity Conservation · Ecology
- **Data source:** NPS Bird Monitoring Surveys — 11 administrative units, Forest & Grassland habitats
- **Records analyzed:** 15,368 cleaned observations
- **Unique species identified:** 127

---

## ✅ Project Deliverables

### 1. Cleaned Dataset
- **Final preprocessed dataset:** `data/bird_observations_clean.csv` (15,368 records, 34 columns)
- **Cleaning steps documented:** `data/cleaning_summary.txt` and Section 3 of the report below

### 2. Source Code
- `scripts/01_clean_data.py` — data cleaning & preprocessing (well-commented, raw XLSX → clean CSV)
- `scripts/02_eda.py` — exploratory analysis & chart generation (clean CSV → 10 charts + insights)
- `dashboard/app.py` — interactive Streamlit dashboard source

### 3. Interactive Dashboard
- **Streamlit application** (`dashboard/app.py`) with filters for habitat, administrative unit, year, species, and conservation watchlist status
- KPI cards, 5 analysis tabs (Overview, Species Analysis, Temporal Trends, Environmental Factors, Conservation), and interactive Plotly charts throughout

### 4. Documentation
- **Formal report:** `outputs/Bird_Species_Observation_Analysis_Report.docx` — approach, key findings, and actionable insights
- Every visualization in the report includes an explanation of what it shows and why it matters

---

## 🗂️ Project Structure

```
bird_project/
├── data/
│   ├── bird_observations_clean.csv     # Cleaned, combined dataset
│   └── cleaning_summary.txt            # Cleaning stats
├── scripts/
│   ├── 01_clean_data.py                # Raw XLSX → cleaned CSV
│   └── 02_eda.py                       # Cleaned CSV → charts + insights
├── dashboard/
│   └── app.py                          # Streamlit dashboard
├── outputs/
│   ├── *.png                           # EDA charts
│   ├── eda_insights.txt                # Key findings
│   └── Bird_Species_Observation_Analysis_Report.docx
├── requirements.txt                    # Python dependencies (for Streamlit Cloud)
├── runtime.txt                         # Pins Python 3.11 (for Streamlit Cloud)
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Data Processing | Python, pandas, numpy, openpyxl |
| Visualization (EDA) | matplotlib, seaborn |
| Dashboard | Streamlit, Plotly |
| Documentation | python-docx |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+

### Installation

```bash
git clone https://github.com/MAVERICKK97/bird-species-observation-analysis.git
cd bird-species-observation-analysis
pip install -r requirements.txt
```

### Run the dashboard locally

```bash
cd dashboard
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Re-run the data pipeline (optional)

```bash
python scripts/01_clean_data.py   # rebuilds data/bird_observations_clean.csv
python scripts/02_eda.py          # regenerates charts in outputs/
```

---

## ☁️ Deploying on Streamlit Community Cloud

1. Push this repo to GitHub (must include `requirements.txt` and `runtime.txt` at the repo root)
2. Go to [share.streamlit.io](https://share.streamlit.io) → sign in with GitHub → **New app**
3. Select this repository, branch `main`, main file path `dashboard/app.py`
4. Click **Deploy**

`runtime.txt` pins the app to Python 3.11, which has pre-built installers for pandas/plotly and avoids dependency build failures on newer Python versions.

---

## 📊 Key Insights

- **Species richness** is nearly identical between habitats — Forest: 108 species, Grassland: 107 species — though species composition differs meaningfully between the two.
- **ANTI (Antietam National Battlefield)** recorded the highest observation volume of any administrative unit.
- **June** is the peak observation month across both habitats, aligning with peak breeding-season activity.
- The **Northern Cardinal** was the most frequently observed species overall.
- **~2.5%** of all observations are of PIF Watchlist species — flagged for elevated conservation concern.
- **Singing** is the dominant detection method, confirming auditory survey techniques as the primary identification approach in the field.

---

## 👤 Author

**Ethan** — [GitHub: MAVERICKK97](https://github.com/MAVERICKK97)

---
**Live Dashboard:** https://bird-species-analysis.streamlit.app/
<img width="1919" height="913" alt="image" src="https://github.com/user-attachments/assets/f1605ecc-1bfe-41e4-a12f-2376e18b0498" />


## 📃 License

This project is for educational and portfolio purposes.
