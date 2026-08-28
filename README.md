# Nigeria Livestock Brucellosis Surveillance

**WAHIS-based analysis of reported brucellosis outbreaks in Nigeria, 2008–2023**

A reproducible analysis of reported livestock brucellosis outbreaks in Nigeria using a quantitative export from the **World Organisation for Animal Health (WOAH) World Animal Health Information System (WAHIS)**.

The analysis focuses on **reported outbreaks and reporting patterns**. It does not estimate disease prevalence, incidence, mortality, or population-level burden.

---

## Project Overview

This project examines Nigeria's reported brucellosis surveillance records in the WOAH WAHIS quantitative dataset covering **2008–2023**.

The analysis was designed to answer questions such as:

* How many brucellosis outbreak records were reported?
* How many new outbreaks were reported?
* Which Nigerian states appear in the reporting data?
* How are reported outbreaks distributed across years and reporting semesters?
* Which *Brucella* categories are represented in the WAHIS `Disease` field?
* How complete are selected epidemiological fields in the extracted data?
* Where are the major gaps in the available reporting record?

All analytical counts and percentages are calculated programmatically from the source dataset.

---

## Key Findings

The extracted WAHIS dataset contains:

| Metric                                    |       Result |
| ----------------------------------------- | -----------: |
| Reporting records                         |       **24** |
| Reported new outbreaks                    |       **39** |
| Nigerian states/FCT represented           | **15 of 37** |
| Years represented                         | **10 of 16** |
| Reporting periods represented             | **16 of 32** |
| Duplicate state × year × semester records |        **0** |

### Reported *Brucella* categories

Based on the WAHIS `Disease` field:

* *Brucella abortus*: **33 reported outbreaks**
* *Brucella melitensis*: **4 reported outbreaks**
* *Brucella suis*: **2 reported outbreaks**

These are **reported outbreak totals**, not numbers of infected animals or human cases.

---

## Important Interpretation

This repository deliberately distinguishes **surveillance reporting** from **disease burden**.

### What the dataset can support

The analysis can describe:

* reported outbreak counts;
* reporting records;
* geographic distribution of reported outbreaks;
* reporting over time;
* reporting-semester distribution;
* reported *Brucella* categories;
* reporting continuity;
* completeness of selected WAHIS fields.

### What the dataset cannot support

The extracted data do **not** provide sufficient information to calculate:

* prevalence;
* incidence;
* attack rate;
* mortality rate;
* case-fatality rate;
* vaccination coverage;
* population-level disease burden;
* animal-level positivity.

In particular, the `Cases`, `Susceptible`, `Deaths`, and `Vaccinated` fields are empty in the extracted records.

Therefore:

> **39 reported outbreaks should not be interpreted as 39 infected animals, 39 cases, or 39 disease events at the individual-animal level.**

Likewise, the fact that only 15 of 37 Nigerian states appear in the dataset represents **observed reporting coverage**, not evidence that brucellosis was absent from the other states.

---

## Visualizations

The repository contains seven analytical visualizations.

### 1. Annual reported outbreak trend

Shows reported new outbreaks by year from 2008–2023.

Years without a reporting record are distinguished from years with a recorded value of zero.

### 2. Reported outbreaks by state

Ranks the 15 Nigerian states/FCT represented in the extracted WAHIS records according to reported new outbreaks.

### 3. Reported outbreaks by geopolitical zone

Aggregates state-level reporting into Nigeria's six geopolitical zones.

**Important:** geopolitical zones are derived analytically from the WAHIS administrative-division field. WAHIS reports the administrative division, not the geopolitical zone.

### 4. *Brucella* category breakdown

Shows reported outbreak totals by the *Brucella* category recorded in the WAHIS `Disease` field.

### 5. Reporting-semester distribution

Compares reported outbreaks during:

* January–June
* July–December

This is a **reporting-period distribution**, not evidence of seasonality.

### 6. Reporting continuity matrix

Shows which state-year combinations contain reporting records.

Blank cells should not be interpreted as evidence of disease absence.

### 7. WAHIS field completeness

Assesses completeness of selected fields in the 24 extracted records.

The six core descriptive fields below were populated in all records:

* Year
* Semester
* Administrative Division
* Disease
* Animal Category
* New outbreaks

Several additional epidemiological fields were unpopulated in the extracted dataset.

---

## Repository Structure

```text
Nigeria-livestock-brucellosis-surveillance/
│
├── README.md
├── brucellosis-tables.xlsx
│
├── charts/
│   ├── 01-annual-outbreak-trend.png
│   ├── 01-annual-outbreak-trend.svg
│   ├── 02-outbreaks-by-state.png
│   ├── 02-outbreaks-by-state.svg
│   ├── 03-outbreaks-by-zone-derived.png
│   ├── 03-outbreaks-by-zone-derived.svg
│   ├── 04-brucella-species-breakdown.png
│   ├── 04-brucella-species-breakdown.svg
│   ├── 05-reporting-semester-split.png
│   ├── 05-reporting-semester-split.svg
│   ├── 06-reporting-continuity-matrix.png
│   ├── 06-reporting-continuity-matrix.svg
│   ├── 07-wahis-field-completeness.png
│   ├── 07-wahis-field-completeness.svg
│   └── brucellosis-charts-all.pdf
│
├── tables/
│   ├── 01-summary-metrics.csv
│   ├── 02-annual-outbreaks.csv
│   ├── 03-state-outbreaks.csv
│   ├── 04-zone-outbreaks-derived.csv
│   ├── 05-brucella-species.csv
│   ├── 06-semester-split.csv
│   ├── 07-field-completeness.csv
│   ├── 08-wahis-records.csv
│   ├── 09-state-by-year-matrix.csv
│   └── brucellosis-tables.md
│
└── scripts/
    ├── bruc_data.py
    ├── bruc_charts.py
    └── bruc_tables.py
```

---

## Reproducibility

The analytical workflow is script-based.

`bruc_data.py` handles:

* loading the WAHIS export;
* parsing the records;
* calculating summary metrics;
* checking duplicate state × year × semester combinations;
* calculating field completeness;
* deriving geopolitical zones.

`bruc_charts.py` generates the seven visualizations.

`bruc_tables.py` generates the analytical tables and Excel workbook.

The scripts are designed so that a refreshed WAHIS export can be supplied without manually rewriting the analytical results.

### Local source-data configuration

The raw WAHIS export is intentionally **excluded from this public repository**.

The scripts expect the source file at:

```text
source-data/WAHIS BRUSCELLAQuantitative data 2026-08-18.csv
```

or at a path supplied through the `WAHIS_CSV` environment variable.

For example:

```powershell
$env:WAHIS_CSV="C:\path\to\new-export.csv"
python scripts\bruc_charts.py
python scripts\bruc_tables.py
```

The raw dataset is excluded through `.gitignore` to prevent accidental publication of the source extract.

---

## Data Governance

The source dataset is not included in this public repository.

This is intentional.

The repository contains derived analytical outputs, scripts, tables, and visualizations while excluding the raw WAHIS export.

The analysis should therefore be interpreted alongside the provenance and limitations of the original WAHIS data.

---

## Analytical Cautions

### Reporting is not disease absence

A state or year without a WAHIS record should not automatically be interpreted as absence of brucellosis.

The absence of a record may reflect differences in:

* surveillance;
* diagnosis;
* reporting;
* data submission;
* data completeness.

The available extract cannot distinguish among these explanations.

### Geographic concentration is not necessarily a hotspot

Higher reported outbreak counts in a state or geopolitical zone indicate greater **reported outbreak activity in this dataset**.

They do not establish that the area is an epidemiological hotspot.

### Reporting semester is not seasonality

The January–June versus July–December comparison describes the distribution of reported outbreaks across WAHIS reporting periods.

It does not establish seasonal transmission patterns.

### Derived geopolitical zones

WOAH WAHIS provides administrative divisions in the extracted records.

Geopolitical zones were assigned using a predefined Nigeria state-to-zone mapping and are therefore **derived variables**.

---

## Source

**World Organisation for Animal Health (WOAH)**
World Animal Health Information System (WAHIS)

Quantitative WAHIS export used for this analysis:

`WAHIS BRUSCELLAQuantitative data 2026-08-18.csv`

Analysis period: **2008–2023**

Country: **Nigeria**

Disease: **Brucellosis**

---

## Disclaimer

This repository represents an independent analytical exercise and does not constitute an official publication, position, endorsement, or statement by WOAH or the Government of Nigeria.
All interpretations are limited to the extracted WAHIS data and the analytical methods documented in this repository.

want to inspect the change first, because there are a couple of things we should verify before we push the polished versio
