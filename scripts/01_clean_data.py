"""
Bird Species Observation Analysis - Data Cleaning & Preprocessing
Consolidates FOREST and GRASSLAND multi-sheet Excel workbooks (11 admin
units each) into a single clean, analysis-ready dataset.
"""
import pandas as pd
import numpy as np
from pathlib import Path

RAW_DIR = Path("/mnt/user-data/uploads")
OUT_DIR = Path("/home/claude/bird_project/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FOREST_FILE = RAW_DIR / "Bird_Monitoring_Data_FOREST.XLSX"
GRASSLAND_FILE = RAW_DIR / "Bird_Monitoring_Data_GRASSLAND.XLSX"


def load_all_sheets(path, habitat_label):
    """Read every admin-unit sheet in a workbook and stack into one frame."""
    xl = pd.ExcelFile(path)
    frames = []
    for sheet in xl.sheet_names:
        df = xl.parse(sheet)
        df["Source_Sheet"] = sheet
        frames.append(df)
    out = pd.concat(frames, ignore_index=True, sort=False)
    out["Habitat_Source_File"] = habitat_label
    return out


def clean(df):
    df = df.copy()

    # --- Standardize column names (strip whitespace) ---
    df.columns = [c.strip() for c in df.columns]

    # --- Location_Type is the authoritative habitat label; fill any gaps ---
    if "Location_Type" in df.columns:
        df["Location_Type"] = df["Location_Type"].fillna(df["Habitat_Source_File"])

    # --- Harmonize the forest-only "NPSTaxonCode" vs grassland "TaxonCode" ---
    if "NPSTaxonCode" in df.columns and "TaxonCode" in df.columns:
        df["TaxonCode"] = df["TaxonCode"].fillna(df["NPSTaxonCode"])
        df = df.drop(columns=["NPSTaxonCode"])
    elif "NPSTaxonCode" in df.columns:
        df = df.rename(columns={"NPSTaxonCode": "TaxonCode"})

    # --- Site_Name only exists in FOREST sheets; keep column, fill with Plot_Name root ---
    if "Site_Name" not in df.columns:
        df["Site_Name"] = np.nan

    # --- Previously_Obs only exists in GRASSLAND sheets ---
    if "Previously_Obs" not in df.columns:
        df["Previously_Obs"] = np.nan

    # --- Dates / times ---
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%B")
    df["Day"] = df["Date"].dt.day

    def to_minutes(t):
        try:
            return t.hour * 60 + t.minute
        except AttributeError:
            return np.nan

    df["Start_Time_Min"] = df["Start_Time"].apply(to_minutes)
    df["End_Time_Min"] = df["End_Time"].apply(to_minutes)
    df["Observation_Duration_Min"] = df["End_Time_Min"] - df["Start_Time_Min"]

    # --- Boolean-like columns: coerce to real booleans ---
    bool_cols = ["Flyover_Observed", "PIF_Watchlist_Status",
                 "Regional_Stewardship_Status", "Previously_Obs",
                 "Initial_Three_Min_Cnt"]
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].map({True: True, False: False, "TRUE": True, "FALSE": False,
                                "Yes": True, "No": False, 1: True, 0: False})

    # --- Numeric environmental columns ---
    for c in ["Temperature", "Humidity"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- Text field cleanup: strip whitespace, standardize case ---
    text_cols = ["Admin_Unit_Code", "Sub_Unit_Code", "Site_Name", "Plot_Name",
                 "Location_Type", "Observer", "ID_Method", "Distance", "Sex",
                 "Common_Name", "Scientific_Name", "AOU_Code", "Sky", "Wind",
                 "Disturbance", "Interval_Length"]
    for c in text_cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan})

    # --- Sex: standardize categories ---
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].replace({"Undetermined": "Undetermined",
                                        "U": "Undetermined"})
        df["Sex"] = df["Sex"].fillna("Undetermined")

    # --- Drop exact duplicate rows ---
    before = len(df)
    df = df.drop_duplicates()
    dupes_removed = before - len(df)

    # --- Drop rows with no species identified (unusable for species analysis) ---
    before2 = len(df)
    df = df.dropna(subset=["Scientific_Name"])
    no_species_removed = before2 - len(df)

    # --- Reset index ---
    df = df.reset_index(drop=True)

    return df, {"duplicates_removed": dupes_removed,
                "no_species_removed": no_species_removed}


def main():
    print("Loading FOREST workbook (11 sheets)...")
    forest = load_all_sheets(FOREST_FILE, "Forest")
    print(f"  -> {len(forest):,} rows")

    print("Loading GRASSLAND workbook (11 sheets)...")
    grassland = load_all_sheets(GRASSLAND_FILE, "Grassland")
    print(f"  -> {len(grassland):,} rows")

    combined = pd.concat([forest, grassland], ignore_index=True, sort=False)
    print(f"Combined raw rows: {len(combined):,}")

    cleaned, stats = clean(combined)
    print(f"Duplicates removed: {stats['duplicates_removed']:,}")
    print(f"Rows without species ID removed: {stats['no_species_removed']:,}")
    print(f"Final cleaned rows: {len(cleaned):,}")
    print(f"Missing values per key column:\n{cleaned[['Temperature','Humidity','Sex','Distance']].isna().sum()}")

    out_csv = OUT_DIR / "bird_observations_clean.csv"
    cleaned.to_csv(out_csv, index=False)
    print(f"Saved cleaned dataset -> {out_csv}")

    # Quick summary stats file
    summary_path = OUT_DIR / "cleaning_summary.txt"
    with open(summary_path, "w") as f:
        f.write("BIRD OBSERVATION DATA - CLEANING SUMMARY\n")
        f.write("=" * 50 + "\n")
        f.write(f"Forest raw rows: {len(forest):,}\n")
        f.write(f"Grassland raw rows: {len(grassland):,}\n")
        f.write(f"Combined raw rows: {len(combined):,}\n")
        f.write(f"Duplicates removed: {stats['duplicates_removed']:,}\n")
        f.write(f"Rows without species ID removed: {stats['no_species_removed']:,}\n")
        f.write(f"Final cleaned rows: {len(cleaned):,}\n")
        f.write(f"Unique species (Scientific_Name): {cleaned['Scientific_Name'].nunique():,}\n")
        f.write(f"Admin units covered: {sorted(cleaned['Admin_Unit_Code'].dropna().unique().tolist())}\n")
        f.write(f"Years covered: {sorted(cleaned['Year'].dropna().unique().tolist())}\n")
    print(f"Saved summary -> {summary_path}")


if __name__ == "__main__":
    main()
