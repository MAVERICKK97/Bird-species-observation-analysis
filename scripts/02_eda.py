"""
Bird Species Observation Analysis - Exploratory Data Analysis
Generates key charts + a text insights summary from the cleaned dataset.
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")
DATA = Path("/home/claude/bird_project/data/bird_observations_clean.csv")
OUT = Path("/home/claude/bird_project/outputs")
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Date"])

insights = []

# 1. Species richness by habitat
richness = df.groupby("Location_Type")["Scientific_Name"].nunique()
insights.append(f"Species richness — Forest: {richness.get('Forest',0)} species, "
                 f"Grassland: {richness.get('Grassland',0)} species.")

fig, ax = plt.subplots(figsize=(6, 4))
richness.plot(kind="bar", ax=ax, color=["#2E7D32", "#C0A030"])
ax.set_title("Unique Species Count by Habitat")
ax.set_ylabel("Number of unique species")
ax.set_xlabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "01_species_richness_by_habitat.png", dpi=150)
plt.close()

# 2. Observations by admin unit
unit_counts = df.groupby(["Admin_Unit_Code", "Location_Type"]).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(9, 5))
unit_counts.plot(kind="bar", stacked=True, ax=ax, color=["#2E7D32", "#C0A030"])
ax.set_title("Bird Observations by Administrative Unit and Habitat")
ax.set_ylabel("Number of observations")
ax.set_xlabel("Admin Unit Code")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "02_observations_by_admin_unit.png", dpi=150)
plt.close()

top_unit = df["Admin_Unit_Code"].value_counts().idxmax()
insights.append(f"Most-observed administrative unit: {top_unit} "
                 f"({df['Admin_Unit_Code'].value_counts().max():,} observations).")

# 3. Seasonal / monthly trend
monthly = df.groupby(["Month_Name", "Location_Type"]).size().unstack(fill_value=0)
month_order = ["January","February","March","April","May","June","July",
                "August","September","October","November","December"]
monthly = monthly.reindex([m for m in month_order if m in monthly.index])
fig, ax = plt.subplots(figsize=(9, 5))
monthly.plot(ax=ax, marker="o", color=["#2E7D32", "#C0A030"])
ax.set_title("Monthly Observation Trends by Habitat")
ax.set_ylabel("Number of observations")
ax.set_xlabel("Month")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "03_monthly_trends.png", dpi=150)
plt.close()

peak_month = df["Month_Name"].value_counts().idxmax()
insights.append(f"Peak observation month overall: {peak_month}.")

# 4. Top 15 most observed species
top_species = df["Common_Name"].value_counts().head(15)
fig, ax = plt.subplots(figsize=(8, 6))
top_species.sort_values().plot(kind="barh", ax=ax, color="#3E7CB1")
ax.set_title("Top 15 Most Frequently Observed Species")
ax.set_xlabel("Number of observations")
plt.tight_layout()
plt.savefig(OUT / "04_top15_species.png", dpi=150)
plt.close()

insights.append(f"Most frequently observed species overall: {top_species.index[0]} "
                 f"({top_species.iloc[0]:,} observations).")

# 5. Temperature vs observation count (environmental correlation)
temp_bins = pd.cut(df["Temperature"], bins=10)
temp_group = df.groupby(temp_bins, observed=True).size()
fig, ax = plt.subplots(figsize=(8, 5))
temp_group.plot(kind="bar", ax=ax, color="#D9822B")
ax.set_title("Observation Count by Temperature Range")
ax.set_ylabel("Number of observations")
ax.set_xlabel("Temperature range (°C)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "05_temperature_distribution.png", dpi=150)
plt.close()

# 6. Sex ratio
sex_counts = df["Sex"].value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(sex_counts, labels=sex_counts.index, autopct="%1.1f%%",
       colors=sns.color_palette("Set2"))
ax.set_title("Observation Sex Distribution")
plt.tight_layout()
plt.savefig(OUT / "06_sex_distribution.png", dpi=150)
plt.close()

# 7. Disturbance effect
if "Disturbance" in df.columns:
    dist_counts = df["Disturbance"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    dist_counts.plot(kind="bar", ax=ax, color="#8E44AD")
    ax.set_title("Observation Count by Disturbance Level")
    ax.set_ylabel("Number of observations")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "07_disturbance_levels.png", dpi=150)
    plt.close()

# 8. Watchlist / conservation status
watchlist_pct = df["PIF_Watchlist_Status"].mean() * 100
insights.append(f"{watchlist_pct:.1f}% of observations are of PIF Watchlist species "
                 "(species of conservation concern).")

fig, ax = plt.subplots(figsize=(6, 4))
df["PIF_Watchlist_Status"].value_counts().rename({True: "Watchlist", False: "Not Watchlist"}) \
    .plot(kind="bar", ax=ax, color=["#B0BEC5", "#E53935"])
ax.set_title("PIF Watchlist Species Share")
ax.set_ylabel("Number of observations")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUT / "08_watchlist_status.png", dpi=150)
plt.close()

# 9. ID Method breakdown
fig, ax = plt.subplots(figsize=(7, 5))
df["ID_Method"].value_counts().plot(kind="bar", ax=ax, color="#00897B")
ax.set_title("Detection Method Frequency")
ax.set_ylabel("Number of observations")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT / "09_id_method.png", dpi=150)
plt.close()

top_method = df["ID_Method"].value_counts().idxmax()
insights.append(f"Most common detection method: {top_method}.")

# 10. Distance distribution
fig, ax = plt.subplots(figsize=(7, 5))
df["Distance"].value_counts().plot(kind="bar", ax=ax, color="#5C6BC0")
ax.set_title("Observation Distance Bands")
ax.set_ylabel("Number of observations")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT / "10_distance_bands.png", dpi=150)
plt.close()

# Save insights
with open(OUT / "eda_insights.txt", "w") as f:
    f.write("BIRD SPECIES OBSERVATION ANALYSIS — KEY EDA INSIGHTS\n")
    f.write("=" * 55 + "\n\n")
    for i, line in enumerate(insights, 1):
        f.write(f"{i}. {line}\n")

print("EDA complete. Charts + insights saved to", OUT)
for line in insights:
    print(" -", line)
