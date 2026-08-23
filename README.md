# Bird Species Observation Analysis

## Contents
- `data/bird_observations_clean.csv` — cleaned, combined dataset (15,368 records)
- `data/cleaning_summary.txt` — cleaning stats
- `scripts/01_clean_data.py` — cleaning/preprocessing script (reads the two raw XLSX files)
- `scripts/02_eda.py` — generates all EDA charts + insights into `outputs/`
- `outputs/` — all charts (PNG) + `eda_insights.txt` + the Word report
- `dashboard/app.py` — Streamlit interactive dashboard

## Run the dashboard
```bash
pip install streamlit plotly pandas
cd dashboard
streamlit run app.py
```

## Re-run the pipeline from raw data
```bash
pip install pandas numpy openpyxl matplotlib seaborn
python scripts/01_clean_data.py   # raw XLSX -> data/bird_observations_clean.csv
python scripts/02_eda.py          # cleaned CSV -> outputs/ (charts + insights)
```
