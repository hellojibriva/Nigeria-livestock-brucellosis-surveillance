"""Render the Nigeria brucellosis (WAHIS) chart set to PNG + SVG + a combined PDF."""
import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages

from bruc_data import (RECORDS, YEAR_START, YEAR_END, TOTAL_STATES, TOTAL_OUTBREAKS,
                       RECORD_COUNT, YEARS_SPAN, YEARS_REPORTING, STATES_REPORTING,
                       PERIODS_REPORTED, PERIODS_POSSIBLE, COUNTRY,
                       FIELD_COMPLETENESS, SURFACE, INK, INK_2, INK_MUTED, GRID,
                       S1, S2, S3, SEQ, EMPTY_CELL, SOURCE_NOTE,
                       by_year, by_state, by_zone, by_subtype, by_semester, ZONE_STATES)

N_FULL = sum(1 for _f, p in FIELD_COMPLETENESS if p == 100)
N_EMPTY = sum(1 for _f, p in FIELD_COMPLETENESS if p == 0)
GAP_YEARS = YEARS_SPAN - YEARS_REPORTING

# Repository root: one level above scripts/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Generated chart outputs
OUT = os.path.join(PROJECT_ROOT, "charts")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "text.color": INK,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK_2,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "font.size": 10,
})

FIGS = []


def frame(ax):
    """Recessive chrome: no box, no ticks."""
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=0)


def titles(fig, title, subtitle, note=None):
    fig.text(0.035, 0.955, title, ha="left", va="top", fontsize=15, fontweight="bold", color=INK)
    fig.text(0.035, 0.898, subtitle, ha="left", va="top", fontsize=9.5, color=INK_2)
    w = int(fig.get_figwidth() * 15)
    parts = ([] if note is None else textwrap.wrap(note, w)) + textwrap.wrap(SOURCE_NOTE, w)
    fig.text(0.035, 0.022, "\n".join(parts), ha="left", va="bottom", fontsize=7.5,
             color=INK_MUTED, linespacing=1.45)


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=200)
    FIGS.append(fig)


# --- 1. annual trend ---------------------------------------------------------
def chart_annual():
    d, n = by_year()
    years = list(range(YEAR_START, YEAR_END + 1))
    vals = [d[y] for y in years]
    fig, ax = plt.subplots(figsize=(10, 5.6))
    fig.subplots_adjust(left=0.075, right=0.975, top=0.80, bottom=0.215)
    ax.bar(years, vals, width=0.6, color=S1, zorder=3)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], fontsize=9)
    ax.set_ylabel("Reported new outbreaks", fontsize=9.5)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    frame(ax)
    for y, v in zip(years, vals):
        if v:
            ax.text(y, v + 0.18, str(v), ha="center", va="bottom", fontsize=9.5,
                    fontweight="bold", color=INK)
        else:
            ax.text(y, 0.18, "no\nrecord", ha="center", va="bottom", fontsize=6.8,
                    color=INK_MUTED, linespacing=1.15)
    titles(fig, f"Reported brucellosis outbreaks in {COUNTRY} by year, {YEAR_START}–{YEAR_END}",
           f"Sum of the WAHIS “New outbreaks” field. {TOTAL_OUTBREAKS} outbreaks across "
           f"{RECORD_COUNT} records in {YEARS_REPORTING} of {YEARS_SPAN} years.",
           note=f"{GAP_YEARS} years carry no WAHIS record. That is an absence of a reported event, "
                "not verified absence of disease.")
    save(fig, "01-annual-outbreak-trend")


# --- 2. by state -------------------------------------------------------------
def chart_states():
    d, n = by_state()
    states = list(d)[::-1]
    vals = [d[s] for s in states]
    fig, ax = plt.subplots(figsize=(10, 6.4))
    fig.subplots_adjust(left=0.16, right=0.965, top=0.82, bottom=0.175)
    ax.barh(states, vals, height=0.62, color=S1, zorder=3)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel("Reported new outbreaks", fontsize=9.5)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", labelsize=9.5)
    frame(ax)
    for s, v in zip(states, vals):
        ax.text(v + max(vals) * 0.012, s, str(v), va="center", ha="left",
                fontsize=9.5, fontweight="bold", color=INK)
    titles(fig, f"Reported brucellosis outbreaks by state, {YEAR_START}–{YEAR_END}",
           f"{STATES_REPORTING} of {COUNTRY}’s {TOTAL_STATES} states (36 + FCT) appear in the extract; "
           f"the other {TOTAL_STATES - STATES_REPORTING} have no record.",
           note="Reported outbreak distribution, not confirmed epidemiological hotspots — WAHIS "
                "supplies no denominators or surveillance-intensity data.")
    save(fig, "02-outbreaks-by-state")


# --- 3. by zone --------------------------------------------------------------
def chart_zones():
    d, rep = by_zone()
    zones = list(d)[::-1]
    vals = [d[z] for z in zones]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    fig.subplots_adjust(left=0.155, right=0.965, top=0.80, bottom=0.255)
    ax.barh(zones, vals, height=0.55, color=S1, zorder=3)
    ax.set_xlim(0, max(vals) * 1.62)
    ax.set_xticks(range(0, max(vals) + 1, 2))
    ax.set_xlabel("Reported new outbreaks", fontsize=9.5)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", labelsize=10)
    frame(ax)
    for z, v in zip(zones, vals):
        label = f"{v}   ({len(rep[z])}/{len(ZONE_STATES[z])} states reporting)"
        ax.text(max(v, 0) + max(vals) * 0.015, z, label, va="center", ha="left",
                fontsize=9, color=INK)
    titles(fig, "Reported outbreaks by geopolitical zone (derived)",
           "Zone totals roll up the state figures using Nigeria’s standard 6-zone grouping.",
           note="DERIVED, not WAHIS-native: WAHIS reports Administrative Division (state) only. "
                "South South has no reporting state in this extract.")
    save(fig, "03-outbreaks-by-zone-derived")


# --- 4. species / category ---------------------------------------------------
def chart_subtypes():
    d, n = by_subtype()
    subs = list(d)[::-1]
    vals = [d[s] for s in subs]
    cols = {"Brucella abortus": S1, "Brucella melitensis": S2, "Brucella suis": S3}
    fig, ax = plt.subplots(figsize=(10, 4.4))
    fig.subplots_adjust(left=0.215, right=0.965, top=0.78, bottom=0.275)
    ax.barh(subs, vals, height=0.5, color=[cols[s] for s in subs], zorder=3)
    ax.set_xlim(0, max(vals) * 1.55)
    ax.set_xlabel("Reported new outbreaks", fontsize=9.5)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_yticks(range(len(subs)))
    ax.set_yticklabels(subs, fontsize=10, fontstyle="italic")
    frame(ax)
    for s, v in zip(subs, vals):
        pct = v / TOTAL_OUTBREAKS * 100
        ax.text(v + max(vals) * 0.02, s, f"{v}   ({pct:.1f}% of {TOTAL_OUTBREAKS} outbreaks · {n[s]} records)",
                va="center", ha="left", fontsize=9, color=INK)
    titles(fig, "Brucella species / category, by reported outbreaks",
           "Derived from the WAHIS “Disease” field, which varies per record.",
           note=f"The dedicated Serotype/Subtype/Genotype WAHIS field is empty in all "
                f"{RECORD_COUNT} records and is NOT the source of this breakdown.")
    save(fig, "04-brucella-species-breakdown")


# --- 5. semester split -------------------------------------------------------
def chart_semester():
    d, n = by_semester()
    labels = ["Jan–Jun (H1)", "Jul–Dec (H2)"]
    vals = [d["H1"], d["H2"]]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    fig.subplots_adjust(left=0.11, right=0.965, top=0.78, bottom=0.275)
    ax.bar(labels, vals, width=0.22, color=S1, zorder=3)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.set_ylabel("Reported new outbreaks", fontsize=9.5)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", labelsize=10)
    frame(ax)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.35, f"{v}  ({v / TOTAL_OUTBREAKS * 100:.1f}%)", ha="center",
                va="bottom", fontsize=10, fontweight="bold", color=INK)
    titles(fig, "Distribution by WAHIS reporting semester",
           f"How the {TOTAL_OUTBREAKS} reported outbreaks fall across the two half-year "
           "reporting periods.",
           note="A distribution by reporting semester — NOT a seasonality finding. No seasonal "
                "analysis is established by this extract.")
    save(fig, "05-reporting-semester-split")


# --- 6. reporting continuity heatmap ----------------------------------------
def chart_continuity():
    d_state, _ = by_state()
    states = list(d_state)
    years = list(range(YEAR_START, YEAR_END + 1))
    grid = {(s, y): None for s in states for y in years}
    for y, _sem, st, _sub, o in RECORDS:
        grid[(st, y)] = (grid[(st, y)] or 0) + o
    vmax = max(v for v in grid.values() if v)
    cmap = LinearSegmentedColormap.from_list("seq_blue", SEQ)

    fig, ax = plt.subplots(figsize=(11, 6.6))
    fig.subplots_adjust(left=0.145, right=0.90, top=0.80, bottom=0.215)
    for xi, y in enumerate(years):
        for yi, s in enumerate(states):
            v = grid[(s, y)]
            if v is None:
                fc, tx = EMPTY_CELL, None
            else:
                fc = cmap(0.30 + 0.70 * (v / vmax))
                tx = str(v)
            ax.add_patch(plt.Rectangle((xi + 0.03, yi + 0.03), 0.94, 0.94,
                                       facecolor=fc, edgecolor=SURFACE, linewidth=1.2))
            if tx:
                lum = 0.30 + 0.70 * (v / vmax)
                ax.text(xi + 0.5, yi + 0.5, tx, ha="center", va="center", fontsize=9,
                        fontweight="bold", color="#ffffff" if lum > 0.62 else INK)
    ax.set_xlim(0, len(years))
    ax.set_ylim(len(states), 0)
    ax.set_xticks([i + 0.5 for i in range(len(years))])
    ax.set_xticklabels([str(y) for y in years], fontsize=8.5)
    ax.set_yticks([i + 0.5 for i in range(len(states))])
    ax.set_yticklabels(states, fontsize=9)
    ax.xaxis.set_ticks_position("top")
    frame(ax)

    lx = 0.915
    fig.text(lx, 0.63, "Outbreaks\nreported", fontsize=8.5, color=INK_2, va="top", linespacing=1.4)
    for i, v in enumerate([1, 2, 3, 4]):
        fig.add_artist(plt.Rectangle((lx, 0.555 - i * 0.045), 0.022, 0.032,
                                     facecolor=cmap(0.30 + 0.70 * (v / vmax)),
                                     edgecolor=SURFACE, transform=fig.transFigure))
        fig.text(lx + 0.030, 0.571 - i * 0.045, str(v), fontsize=8.5, color=INK_2, va="center")
    fig.add_artist(plt.Rectangle((lx, 0.555 - 4 * 0.045 - 0.015), 0.022, 0.032,
                                 facecolor=EMPTY_CELL, edgecolor=SURFACE, transform=fig.transFigure))
    fig.text(lx + 0.030, 0.571 - 4 * 0.045 - 0.015, "no\nrecord", fontsize=7.5, color=INK_2,
             va="center", linespacing=1.2)

    titles(fig, "Reporting continuity: state × year",
           f"Where a WAHIS record exists, and what it reported. {PERIODS_REPORTED} of "
           f"{PERIODS_POSSIBLE} half-year periods are represented.",
           note="Blank cells mean no WAHIS record was identified for that state-year — a reporting "
                "gap, not a verified absence of disease.")
    save(fig, "06-reporting-continuity-matrix")


# --- 7. field completeness ---------------------------------------------------
def chart_completeness():
    fields = FIELD_COMPLETENESS[::-1]
    names = [f for f, _ in fields]
    vals = [v for _, v in fields]
    cols = [S1 if v == 100 else EMPTY_CELL for v in vals]
    fig, ax = plt.subplots(figsize=(10, 6.8))
    fig.subplots_adjust(left=0.30, right=0.955, top=0.83, bottom=0.175)
    ax.barh(names, [v if v else 100 for v in vals], height=0.5, color=cols, zorder=3)
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=9)
    ax.set_xlabel(f"Share of the {RECORD_COUNT} records in which the field is populated", fontsize=9.5)
    ax.xaxis.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", labelsize=9)
    frame(ax)
    for n_, v in zip(names, vals):
        ax.text(102, n_, f"{v}%", va="center", ha="left", fontsize=9,
                fontweight="bold" if v == 100 else "normal",
                color=INK if v == 100 else INK_MUTED)
    titles(fig, f"WAHIS field completeness across the {RECORD_COUNT} {COUNTRY} records",
           f"{N_FULL} fields are fully populated; {N_EMPTY} are empty in every record "
           "(shown as hollow bars).",
           note="A data-quality measure, not an epidemiological one. Because Cases, Susceptible, "
                "Deaths and Vaccinated are empty, no incidence, prevalence, case-fatality or "
                "vaccination-coverage figure can be computed from this extract.")
    save(fig, "07-wahis-field-completeness")


for fn in (chart_annual, chart_states, chart_zones, chart_subtypes,
           chart_semester, chart_continuity, chart_completeness):
    fn()

with PdfPages(os.path.join(OUT, "brucellosis-charts-all.pdf")) as pdf:
    for f in FIGS:
        pdf.savefig(f)

print("charts written to", OUT)
for f in sorted(os.listdir(OUT)):
    print(" ", f)
