"""Shared data + palette for the Nigeria brucellosis (WAHIS) chart/table build.

Records are parsed directly from the raw WOAH WAHIS export
("WAHIS BRUSCELLAQuantitative data 2026-08-18.csv"). Nothing is transcribed by
hand and no value is invented or estimated. Point SOURCE_CSV at a refreshed
export and every chart and table follows.
"""
import csv
import os

from pathlib import Path

# Repository root: one level above the scripts/ directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Default source location for the local WAHIS extract.
# source-data/ is intentionally excluded from the public repository.
DEFAULT_SOURCE_CSV = (
    PROJECT_ROOT
    / "source-data"
    / "WAHIS BRUSCELLAQuantitative data 2026-08-18.csv"
)

SOURCE_CSV = os.environ.get(
    "WAHIS_CSV",
    str(DEFAULT_SOURCE_CSV),
)

# WAHIS schema fields this analysis reports completeness for, in display order.
TRACKED_FIELDS = [
    "Year", "Semester", "Administrative Division", "Disease", "Animal Category",
    "New outbreaks", "Serotype/Subtype/Genotype", "Species", "Event_id",
    "Outbreak_id", "Susceptible", "Measuring units", "Cases",
    "Killed and disposed of", "Slaughtered", "Deaths", "Vaccinated",
]
FIELD_LABELS = {
    "Administrative Division": "Administrative Division (state)",
    "Serotype/Subtype/Genotype": "Serotype/Subtype/Genotype",
    "Species": "Species (host)",
}
# WAHIS writes an unpopulated cell as "-" or as an empty string.
EMPTY_TOKENS = {"", "-", "n/a", "na", "null"}


def _empty(value):
    return value is None or str(value).strip().lower() in EMPTY_TOKENS


def load_rows(path=SOURCE_CSV):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return [r for r in csv.DictReader(fh) if not all(_empty(v) for v in r.values())]


RAW_ROWS = load_rows()

# (year, semester, state, subtype, new_outbreaks) — one tuple per CSV row.
RECORDS = []
for r in RAW_ROWS:
    label = r["Semester"].strip()                      # e.g. "Jul-Dec 2008"
    RECORDS.append((
        int(r["Year"]),
        "H1" if label.lower().startswith("jan") else "H2",
        r["Administrative Division"].strip(),
        r["Disease"].strip().replace(" (Inf. with)", ""),
        int(r["New outbreaks"]),
    ))
RECORDS.sort(key=lambda t: (t[0], t[1], t[2]))

COUNTRY = RAW_ROWS[0]["Country"].strip()
WORLD_REGION = RAW_ROWS[0]["World region"].strip()
ANIMAL_CATEGORY = RAW_ROWS[0]["Animal Category"].strip()
SOURCE_FILENAME = os.path.basename(SOURCE_CSV)
RECORD_COUNT = len(RECORDS)
TOTAL_OUTBREAKS = sum(r[4] for r in RECORDS)

# Completeness computed from the file, not asserted.
FIELD_COMPLETENESS = [
    (FIELD_LABELS.get(f, f),
     round(sum(0 if _empty(r.get(f)) else 1 for r in RAW_ROWS) / len(RAW_ROWS) * 100))
    for f in TRACKED_FIELDS
]

# Duplicate check on state x year x semester.
_keys = [(y, s, st) for y, s, st, _sub, _o in RECORDS]
DUPLICATE_RECORDS = len(_keys) - len(set(_keys))

ZONE_STATES = {
    "North Central": ["Benue", "Kogi", "Kwara", "Nasarawa", "Niger", "Plateau",
                      "Abuja Federal Capital Territory"],
    "North East":    ["Adamawa", "Bauchi", "Borno", "Gombe", "Taraba", "Yobe"],
    "North West":    ["Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Sokoto", "Zamfara"],
    "South East":    ["Abia", "Anambra", "Ebonyi", "Enugu", "Imo"],
    "South South":   ["Akwa Ibom", "Bayelsa", "Cross River", "Delta", "Edo", "Rivers"],
    "South West":    ["Ekiti", "Lagos", "Ogun", "Ondo", "Osun", "Oyo"],
}
STATE_TO_ZONE = {s: z for z, states in ZONE_STATES.items() for s in states}

_unmapped = sorted({st for _y, _s, st, _sub, _o in RECORDS if st not in STATE_TO_ZONE})
if _unmapped:
    raise SystemExit(f"State(s) in the CSV have no geopolitical zone mapping: {_unmapped}")

YEAR_START = min(r[0] for r in RECORDS)
YEAR_END = max(r[0] for r in RECORDS)
TOTAL_STATES = 37  # 36 states + FCT
YEARS_SPAN = YEAR_END - YEAR_START + 1
PERIODS_POSSIBLE = YEARS_SPAN * 2
PERIODS_REPORTED = len({(y, s) for y, s, _st, _sub, _o in RECORDS})
STATES_REPORTING = len({r[2] for r in RECORDS})
YEARS_REPORTING = len({r[0] for r in RECORDS})

# --- palette (dataviz reference instance, light mode; validated) -------------
SURFACE   = "#fcfcfb"
INK       = "#0b0b0b"
INK_2     = "#52514e"
INK_MUTED = "#8a8880"
GRID      = "#e6e5e1"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"   # categorical slots 1-3
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95"]
EMPTY_CELL = "#f0efec"

SOURCE_NOTE = (f"Source: WOAH WAHIS quantitative data, {COUNTRY}, Brucellosis "
               f"(extract “{SOURCE_FILENAME}”), {RECORD_COUNT} records, "
               f"{TOTAL_OUTBREAKS} reported new outbreaks, {YEAR_START}–{YEAR_END}.")


def by_year():
    d = {y: 0 for y in range(YEAR_START, YEAR_END + 1)}
    n = {y: 0 for y in range(YEAR_START, YEAR_END + 1)}
    for y, _s, _st, _sub, o in RECORDS:
        d[y] += o
        n[y] += 1
    return d, n


def by_state():
    d, n = {}, {}
    for _y, _s, st, _sub, o in RECORDS:
        d[st] = d.get(st, 0) + o
        n[st] = n.get(st, 0) + 1
    return dict(sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))), n


def by_zone():
    d = {z: 0 for z in ZONE_STATES}
    rep = {z: set() for z in ZONE_STATES}
    for _y, _s, st, _sub, o in RECORDS:
        z = STATE_TO_ZONE[st]
        d[z] += o
        rep[z].add(st)
    return dict(sorted(d.items(), key=lambda kv: -kv[1])), rep


def by_subtype():
    d, n = {}, {}
    for _y, _s, _st, sub, o in RECORDS:
        d[sub] = d.get(sub, 0) + o
        n[sub] = n.get(sub, 0) + 1
    return dict(sorted(d.items(), key=lambda kv: -kv[1])), n


def by_semester():
    d, n = {"H1": 0, "H2": 0}, {"H1": 0, "H2": 0}
    for _y, s, _st, _sub, o in RECORDS:
        d[s] += o
        n[s] += 1
    return d, n


if __name__ == "__main__":
    print(f"source            {SOURCE_CSV}")
    print(f"records           {RECORD_COUNT}")
    print(f"outbreaks         {TOTAL_OUTBREAKS}")
    print(f"states reporting  {STATES_REPORTING} of {TOTAL_STATES}")
    print(f"years with record {YEARS_REPORTING} of {YEARS_SPAN} ({YEAR_START}-{YEAR_END})")
    print(f"periods reported  {PERIODS_REPORTED} of {PERIODS_POSSIBLE}")
    print(f"duplicates        {DUPLICATE_RECORDS}")
    print(f"by semester       {by_semester()[0]}")
    print(f"by subtype        {by_subtype()[0]}")
    print("completeness      " + ", ".join(f"{f}={p}%" for f, p in FIELD_COMPLETENESS))
