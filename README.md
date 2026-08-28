# Nigeria brucellosis — charts & tables (WAHIS, 2008–2023)

Generated directly from the raw WOAH WAHIS export
`WAHIS BRUSCELLAQuantitative data 2026-08-18.csv` (a copy is in `source-data/`).
Nothing is transcribed by hand: the scripts parse the CSV, and every count, percentage
and completeness figure on every chart and in every table is computed from it.

**Scope:** Nigeria, Brucellosis, 2008–2023 — 24 records, 39 reported new outbreaks,
15 of 37 states, 10 of 16 years, 16 of 32 half-year reporting periods, 0 duplicate records.

## What's here

| File | What it is |
|---|---|
| `brucellosis-tables.xlsx` | All nine tables, one per sheet, plus a "Read me" sheet with provenance and cautions |
| `charts/*.png` | Print-ready 200 dpi rasters |
| `charts/*.svg` | Same charts as vectors — scale cleanly, editable in Illustrator/Figma |
| `charts/brucellosis-charts-all.pdf` | All seven charts, one per page |
| `tables/*.csv` | One CSV per table (UTF-8 with BOM, so Excel opens them correctly) |
| `tables/brucellosis-tables.md` | All tables as Markdown, for pasting into a manuscript or doc |
| `source-data/` | The raw WAHIS CSV this was built from |
| `bruc_data.py`, `bruc_charts.py`, `bruc_tables.py` | The generators |

## Charts

1. **Annual outbreak trend, 2008–2023** — years with no record are labelled as such, not drawn as zero.
2. **Outbreaks by state** — 15 reporting states, ranked.
3. **Outbreaks by geopolitical zone** — derived roll-up, labelled as derived.
4. **Brucella species / category** — from the `Disease` field.
5. **Distribution by reporting semester** — 17 Jan–Jun vs 22 Jul–Dec.
6. **Reporting continuity matrix** — state × year, showing where records exist and where they don't.
7. **WAHIS field completeness** — 6 fields at 100%, 11 empty in every record.

## Five things the numbers are not

1. **24 records ≠ 39 outbreaks.** One record can carry a `New outbreaks` value greater than 1.
2. **39 outbreaks ≠ 39 cases or animals.** WAHIS reports no case- or animal-level counts in this extract.
3. **Coverage ≠ burden.** 15/37 states and 10/16 years describe reporting coverage, not prevalence.
4. **Completeness ≠ epidemiology.** Field completeness is a data-quality measure.
5. **No true burden figure is computable.** Incidence, prevalence, attack rate, mortality,
   case-fatality and vaccination coverage all need denominators this extract does not contain —
   `Cases`, `Susceptible`, `Deaths` and `Vaccinated` are empty in all 24 records.

## Cautions carried on every chart

- Absence of a WAHIS record is **not** absence of disease — it may be a reporting, surveillance,
  diagnostic or submission gap, and this extract cannot tell them apart.
- Geographic concentration (Plateau, Kaduna, North Central, North West) describes **reported
  outbreak distribution**, not confirmed epidemiological hotspots.
- The 17 / 22 Jan–Jun vs Jul–Dec split is a distribution by reporting semester, **not seasonality**.
- Geopolitical-zone totals are **derived**; WAHIS reports Administrative Division (state) only.
- The dedicated Serotype/Subtype/Genotype field is empty in all 24 records. The species breakdown
  comes from the `Disease` field — a different field, which does vary per record.
- This analysis is independent and does not represent an official position of WOAH or the
  Nigerian government.

## Regenerating after a fresh WAHIS export

`bruc_data.py` points at the CSV via `SOURCE_CSV`; override it without editing the file:

```bash
WAHIS_CSV="C:\path\to\new-export.csv" python bruc_charts.py && python bruc_tables.py
```

Both write into `out/` beside the scripts. Titles, subtitles, footers, totals and the
completeness table all follow the new file — including the record count, the year range and
the source filename printed on each chart. The scripts stop with an error if a state in the
CSV has no geopolitical-zone mapping, so a new reporting state can't be silently dropped from
the zone roll-up. Requires `matplotlib` and `openpyxl`.
