const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow,
  TableCell, WidthType, ShadingType, ImageRun, AlignmentType, BorderStyle,
  PageBreak
} = require("docx");

const OUT = "/home/claude/bird_project/outputs";
const img = (name) => fs.readFileSync(`${OUT}/${name}`);

const H1 = (t) => new Paragraph({ text: t, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } });
const H2 = (t) => new Paragraph({ text: t, heading: HeadingLevel.HEADING_2, spacing: { before: 200, after: 100 } });
const P = (t, opts = {}) => new Paragraph({ children: [new TextRun({ text: t, ...opts })], spacing: { after: 120 } });
const Bullet = (t) => new Paragraph({ text: t, bullet: { level: 0 }, spacing: { after: 60 } });

function chart(name, caption, width = 550, height = 330) {
  return [
    new Paragraph({
      children: [new ImageRun({ data: img(name), transformation: { width, height }, type: "png" })],
      alignment: AlignmentType.CENTER,
      spacing: { before: 100, after: 60 },
    }),
    new Paragraph({
      children: [new TextRun({ text: caption, italics: true, size: 18 })],
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 },
    }),
  ];
}

function kvTable(rows) {
  return new Table({
    width: { size: 9000, type: WidthType.DXA },
    columnWidths: [3000, 6000],
    rows: rows.map(([k, v], i) =>
      new TableRow({
        children: [
          new TableCell({
            width: { size: 3000, type: WidthType.DXA },
            shading: { type: ShadingType.CLEAR, fill: "E8F0E5" },
            children: [new Paragraph({ children: [new TextRun({ text: k, bold: true })] })],
          }),
          new TableCell({
            width: { size: 6000, type: WidthType.DXA },
            children: [new Paragraph({ text: String(v) })],
          }),
        ],
      })
    ),
  });
}

const doc = new Document({
  sections: [
    {
      properties: { page: { size: { width: 12240, height: 15840 } } },
      children: [
        new Paragraph({
          children: [new TextRun({ text: "Bird Species Observation Analysis", bold: true, size: 44, color: "2E7D32" })],
          alignment: AlignmentType.CENTER,
          spacing: { before: 400, after: 100 },
        }),
        new Paragraph({
          children: [new TextRun({ text: "Forest vs. Grassland Biodiversity — Data Analysis Report", size: 26, italics: true, color: "555555" })],
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
        }),
        kvTable([
          ["Domain", "Environmental Studies, Biodiversity Conservation, Ecology"],
          ["Data Source", "NPS Bird Monitoring Surveys — 11 Administrative Units"],
          ["Habitats Compared", "Forest and Grassland"],
          ["Total Cleaned Records", "15,368 observations"],
          ["Unique Species Identified", "127"],
          ["Survey Year", "2018"],
        ]),
        new Paragraph({ children: [new PageBreak()] }),

        H1("1. Problem Statement"),
        P("This project analyzes the distribution and diversity of bird species across two distinct ecosystems — forests and grasslands — spanning 11 U.S. National Park Service administrative units. By examining bird observation data collected in the field, the study identifies habitat preferences, seasonal activity patterns, and the influence of environmental conditions on bird populations, providing insights relevant to habitat conservation and biodiversity management."),

        H1("2. Data Overview"),
        P("Two source workbooks were provided, each containing 11 sheets (one per administrative unit): Bird_Monitoring_Data_FOREST.XLSX and Bird_Monitoring_Data_GRASSLAND.XLSX. Each row represents a single bird observation, recording location, date/time, observer, detection method, distance, sex, species identity, environmental conditions, and conservation status flags."),
        kvTable([
          ["Forest raw records", "8,546"],
          ["Grassland raw records", "8,531"],
          ["Combined raw records", "17,077"],
          ["Duplicate rows removed", "1,709"],
          ["Final cleaned records", "15,368"],
          ["Administrative units", "ANTI, CATO, CHOH, GWMP, HAFE, MANA, MONO, NACE, PRWI, ROCR, WOTR"],
        ]),

        H1("3. Data Cleaning & Preprocessing"),
        P("The following steps were applied to consolidate and clean the raw data:"),
        Bullet("Combined all 11 sheets from each workbook into a single dataset, tagging each record with its source sheet and habitat type."),
        Bullet("Harmonized schema differences between the two files (e.g., Forest-only 'Site_Name' column, Grassland-only 'Previously_Obs' column; merged 'NPSTaxonCode' and 'TaxonCode' into one field)."),
        Bullet("Parsed Date, Start_Time, and End_Time into proper datetime fields; derived Month, Month_Name, and observation duration in minutes."),
        Bullet("Converted Flyover_Observed, PIF_Watchlist_Status, Regional_Stewardship_Status, and Previously_Obs into proper boolean fields."),
        Bullet("Converted Temperature and Humidity to numeric types."),
        Bullet("Trimmed whitespace and standardized text fields (species names, observer names, categorical fields)."),
        Bullet("Standardized missing/undetermined Sex values to a consistent 'Undetermined' category."),
        Bullet("Removed 1,709 exact duplicate rows and any records lacking a species identification."),
        P("The result is a single analysis-ready CSV (bird_observations_clean.csv) with 15,368 records and 34 columns, suitable for direct loading into SQL, Python, or Power BI/Streamlit."),

        H1("4. Exploratory Data Analysis — Key Findings"),

        H2("4.1 Species Richness by Habitat"),
        P("Forest plots recorded 108 unique species while Grassland plots recorded 107 — nearly identical overall richness, though the specific species composition differs meaningfully between habitats (see Section 4.2)."),
        ...chart("01_species_richness_by_habitat.png", "Figure 1: Unique species count by habitat type"),

        H2("4.2 Observations by Administrative Unit"),
        P("Antietam National Battlefield (ANTI) recorded the highest observation volume of any unit (3,463 observations), suggesting either higher survey effort or richer bird activity at that site relative to others."),
        ...chart("02_observations_by_admin_unit.png", "Figure 2: Observation counts by administrative unit, split by habitat"),

        H2("4.3 Seasonal / Monthly Trends"),
        P("Observation activity peaks in June across both habitats, consistent with peak breeding-season vocalization (singing/calling) activity in temperate bird species."),
        ...chart("03_monthly_trends.png", "Figure 3: Monthly observation trends by habitat"),

        H2("4.4 Most Frequently Observed Species"),
        P("The Northern Cardinal was the most frequently recorded species overall (1,125 observations), reflecting its status as a common, vocally conspicuous year-round resident across both forest and grassland edge habitats."),
        ...chart("04_top15_species.png", "Figure 4: Top 15 most frequently observed species"),

        H2("4.5 Environmental Conditions"),
        P("Observation counts cluster within moderate temperature bands, consistent with standard early-morning survey protocols conducted in mild spring/summer conditions."),
        ...chart("05_temperature_distribution.png", "Figure 5: Observation count by temperature range"),

        H2("4.6 Sex Distribution"),
        P("A substantial share of observations could not be sexed in the field (recorded as Undetermined), which is expected given that most detections rely on auditory cues (singing/calling) rather than visual sexing."),
        ...chart("06_sex_distribution.png", "Figure 6: Observation sex distribution"),

        H2("4.7 Disturbance Levels"),
        P("The large majority of observations occurred under conditions of 'No effect' or only 'Slight effect' from disturbance, indicating survey protocols were generally successful in minimizing observer/environmental interference."),
        ...chart("07_disturbance_levels.png", "Figure 7: Observation count by disturbance level"),

        H2("4.8 Conservation Watchlist Status"),
        P("Approximately 2.5% of all observations belong to PIF Watchlist species — species of elevated conservation concern. While a small share of total volume, these observations are disproportionately important for conservation planning and warrant targeted monitoring."),
        ...chart("08_watchlist_status.png", "Figure 8: Share of observations that are PIF Watchlist species"),

        H2("4.9 Detection Method"),
        P("'Singing' is the dominant detection method by a wide margin, confirming that auditory survey techniques are the primary means of species identification in both habitats."),
        ...chart("09_id_method.png", "Figure 9: Detection/identification method frequency"),

        H2("4.10 Observation Distance"),
        P("Most birds were detected within moderate distance bands of the observer, reflecting standard point-count survey radii used in the field protocol."),
        ...chart("10_distance_bands.png", "Figure 10: Observation distance band frequency"),

        H1("5. Actionable Insights & Recommendations"),
        Bullet("Prioritize conservation monitoring resources at ANTI and other high-volume units, while investigating whether lower counts elsewhere reflect lower survey effort or genuinely lower bird activity."),
        Bullet("Time future survey and outreach efforts around the May–June peak breeding season, when both detectability and species activity are highest."),
        Bullet("Flag and separately track the ~2.5% of observations tied to PIF Watchlist species for dedicated conservation follow-up, since these carry outsized ecological importance."),
        Bullet("Because Forest and Grassland habitats show similar overall species counts but different species composition and peak conditions, conservation and land-management strategies should be habitat-specific rather than uniform."),
        Bullet("Continue relying on auditory (singing/calling) detection protocols, but consider supplementary visual survey methods to improve sex-ratio data completeness."),

        H1("6. Deliverables"),
        Bullet("Cleaned dataset: bird_observations_clean.csv (15,368 records, 34 columns)."),
        Bullet("Data cleaning script: 01_clean_data.py."),
        Bullet("EDA script generating all charts in this report: 02_eda.py."),
        Bullet("Interactive Streamlit dashboard: dashboard/app.py — filterable by habitat, admin unit, year, species, and watchlist status, with KPI cards and five analysis tabs."),
        Bullet("This documentation report."),

        H1("7. Tools & Technologies Used"),
        P("Python (pandas, numpy) for data cleaning and preprocessing · matplotlib/seaborn for static EDA visualizations · Streamlit and Plotly for the interactive dashboard · openpyxl for reading multi-sheet Excel workbooks."),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(`${OUT}/Bird_Species_Observation_Analysis_Report.docx`, buf);
  console.log("Report written.");
});
