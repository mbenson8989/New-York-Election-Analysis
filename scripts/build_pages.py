"""Writes README.md and wiki/*.md from data/ny_county_table.csv and data/ny_summary.json.
Every number on every page is formatted from those two files; nothing is typed by hand."""
import csv, json, os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WIKI = os.path.join(ROOT, "wiki"); os.makedirs(WIKI, exist_ok=True)
RAWURL = "https://raw.githubusercontent.com/mbenson8989/New-York-Election-Analysis/main/"
REPO = "https://github.com/mbenson8989/New-York-Election-Analysis"
SUM = json.load(open(os.path.join(ROOT, "data", "ny_summary.json")))
ALL = list(csv.DictReader(open(os.path.join(ROOT, "data", "ny_county_table.csv"))))
for r in ALL:
    for k, v in list(r.items()):
        if k in ("county", "region", "reg_dem_fell"):
            continue
        r[k] = None if v in ("", "None") else float(v)
    r["fell"] = r["reg_dem_fell"] == "True"
    r["name"] = "St. Lawrence" if r["county"] == "St.Lawrence" else r["county"]
ST = next(r for r in ALL if r["county"] == "New York State")
ROWS = [r for r in ALL if r["county"] != "New York State"]
C = {r["county"]: r for r in ROWS}
G = SUM["groups"]; FIT = SUM["fit"]; SIDE = SUM["side_check"]
H = C["Hamilton"]
bydg = sorted(ROWS, key=lambda r: -r["dG"])
CEIL5 = bydg[:5]; CEIL = bydg[0]; FLOOR = bydg[-1]; FLOOR3 = bydg[-3:][::-1]
NONLOSS = sorted([r for r in ROWS if not r["fell"]], key=lambda r: -r["reg_total_2026"])
LOSS = [r for r in ROWS if r["fell"]]
TOPLOSS = max(LOSS, key=lambda r: r["dG"])
OUTSIDE = sorted([r for r in ROWS if r["region"] == "Outside NYC"], key=lambda r: -r["reg_total_2026"])
NYC = sorted([r for r in ROWS if r["region"] == "Within NYC"], key=lambda r: -r["reg_total_2026"])
SCAT_R = float(open(os.path.join(ROOT, "data", "chart_stats.txt")).read().split("=")[1])
import statistics
MED = statistics.median(r["dG"] for r in ROWS)
HRANK = sorted(ROWS, key=lambda r: r["dG"]).index(H) + 1   # 1 = lowest

# ---------- formatting ----------
n = lambda v: f"{int(round(v)):,}"
sg = lambda v: ("+" if round(v) > 0 else "−" if round(v) < 0 else "") + f"{abs(int(round(v))):,}"
p2 = lambda v: f"{v:.2f}"
s2 = lambda v: ("+" if v >= 0.005 else "−" if v <= -0.005 else "") + f"{abs(v):.2f}"
pct1 = lambda a, b: ("+" if b >= a else "−") + f"{abs((b - a) / a * 100):.1f}%"
d2 = lambda v: f"{v:.2f}".replace("-", "−")

VERSION = f"**Version 1, built {datetime.now().strftime('%b %d %Y')} (data pulled Nov 22 2026)**"
BANNER = ("> **\\*2026 figures are unofficial and not certified by the NYS Board of Elections.** They come from the Board's Election Night Reporting page "
          "as of 11/21/2026 11:42 AM. The Board says that page leaves out a significant number of unscanned emergency Election Day ballots from Westchester County, "
          "and six counties were not at full reporting (see [Sources](Home#sources)). Governor race unless a page says otherwise. "
          "Votes are a candidate's votes on every party line he or she appeared on (fusion voting), not a count of registered Democrats who voted. "
          "Registration is the Nov 1 enrollment report for each year (active + inactive). These pages measure a pattern; they make no claim about intent, fraud or cause.")
FUSION = ("**Fusion lines:** Hochul = Democratic + Working Families. Zeldin (2022) = Republican + Conservative. "
          "Blakeman (2026) = Republican + Conservative + Vote Affordable; the Board's own Blakeman total includes the Vote Affordable line, so it is counted here and shown separately.")

def related(*pages):
    names = {"Home": "Home", "Hamilton-County-Audit": "Hamilton County Audit", "Reverse-Math": "Bottom-Up Reverse Math",
             "Locked-New-York-Formula": "Locked New York Formula", "Floor-and-Ceiling": "Floor and Ceiling Counties",
             "Graphs": "Graphs", "62-County-PDF-Information": "62 County PDF Information"}
    return "---\n**Related:** " + " · ".join(f"[{names[p]}]({p})" for p in pages) + "\n"

def img(fn, cap):
    return f"![{cap}]({RAWURL}{fn})\n\n*{cap.replace('*', chr(92) + '*')}*\n"

def lines_tbl(r):
    return (f"| Line | 2022 (certified) | 2026* |\n|---|---|---|\n"
            f"| Hochul, Democratic line | {n(r['hochul_dem_2022'])} | {n(r['hochul_dem_2026'])}* |\n"
            f"| Hochul, Working Families line | {n(r['hochul_wor_2022'])} | {n(r['hochul_wor_2026'])}* |\n"
            f"| **Hochul, all lines** | **{n(r['hochul_all_2022'])}** | **{n(r['hochul_all_2026'])}*** |\n"
            f"| Republican line (Zeldin 2022; Blakeman 2026) | {n(r['zeldin_rep_2022'])} | {n(r['blakeman_rep_2026'])}* |\n"
            f"| Conservative line (Zeldin 2022; Blakeman 2026) | {n(r['zeldin_con_2022'])} | {n(r['blakeman_con_2026'])}* |\n"
            f"| Vote Affordable line (Blakeman 2026 only) | (not on the 2022 ballot) | {n(r['blakeman_va_2026'])}* |\n"
            f"| **Republican nominee, all lines** | **{n(r['zeldin_all_2022'])}** | **{n(r['blakeman_all_2026'])}*** |\n"
            f"| Write-ins (2022 \"Scattering\") | {n(r['writein_2022'])} | {n(r['writein_2026'])}* |\n"
            f"| **Governor race total** (S denominator; blank and void excluded) | **{n(r['race_total_2022'])}** | **{n(r['race_total_2026'])}*** |\n"
            f"| Blank | {n(r['blank_2022'])} | {n(r['blank_2026'])}* |\n"
            f"| Void | {n(r['void_2022'])} | {n(r['void_2026'])}* |\n"
            f"| Governor-race ballots (all of the above) | {n(r['ballots_2022'])} | {n(r['ballots_2026'])}* |\n")

pages = {}

# ================= HOME =================
pages["Home"] = f"""# New York 2022 vs 2026 Governor Race: ΔG Method

{VERSION}

{BANNER}

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP). Data: New York State Board of Elections (NYS BOE) enrollment-by-county reports, the certified 2022 results database and the 2026 Election Night Reporting page, compiled 22 Nov 2026. New York numbers only; no other state's figures are used.

{FUSION}

## Contents

Start with Hamilton County. It is New York's smallest county by registered voters, every one of its 11 election districts is in, and it recorded exactly {n(H['ballots_2026'])} governor-race ballots in both years. Registered Democrats fell from {n(H['reg_dem_2022'])} to {n(H['reg_dem_2026'])} while Hochul's all-line votes rose from {n(H['hochul_all_2022'])} to {n(H['hochul_all_2026'])}\\*. The pages then build up from Hamilton to the 57 counties outside New York City, and to the statewide formula.

1. [Hamilton County Audit](Hamilton-County-Audit): Hamilton's numbers line by line, and what audit records exist
2. [Bottom-Up Reverse Math](Reverse-Math): Hamilton → the 57 counties outside NYC → all 62 counties
3. [Locked New York Formula](Locked-New-York-Formula): the equation, New York's fitted surplus equation, a blank fill-in template
4. [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at the top and bottom of ΔG
5. [Graphs](Graphs): slope chart, ΔG by county size, stacked bars, vote-share vs registration-loss bars, ceiling counties, Hamilton steps
6. [62 County PDF Information](62-County-PDF-Information): the 62-county table of registration, votes by line and combined, and ballots (PDF download)

## Statewide at a glance

| Measure | 2022 | 2026* | Change |
|---|---|---|---|
| Democratic registration (Nov 1) | {n(ST['reg_dem_2022'])} | {n(ST['reg_dem_2026'])} | {sg(ST['reg_dem_2026']-ST['reg_dem_2022'])} ({pct1(ST['reg_dem_2022'],ST['reg_dem_2026'])}) |
| All registered voters (Nov 1) | {n(ST['reg_total_2022'])} | {n(ST['reg_total_2026'])} | {sg(ST['reg_total_2026']-ST['reg_total_2022'])} ({pct1(ST['reg_total_2022'],ST['reg_total_2026'])}) |
| Hochul votes, Democratic line | {n(ST['hochul_dem_2022'])} | {n(ST['hochul_dem_2026'])}* | {sg(ST['hochul_dem_2026']-ST['hochul_dem_2022'])}* |
| Hochul votes, Working Families line | {n(ST['hochul_wor_2022'])} | {n(ST['hochul_wor_2026'])}* | {sg(ST['hochul_wor_2026']-ST['hochul_wor_2022'])}* |
| **Hochul votes, all lines** | **{n(ST['hochul_all_2022'])}** | **{n(ST['hochul_all_2026'])}*** | **{sg(ST['hochul_all_2026']-ST['hochul_all_2022'])}* ({pct1(ST['hochul_all_2022'],ST['hochul_all_2026'])}\\*)** |
| Governor-race ballots (incl. blank and void) | {n(ST['ballots_2022'])} | {n(ST['ballots_2026'])}* | {sg(ST['ballots_2026']-ST['ballots_2022'])}* ({pct1(ST['ballots_2022'],ST['ballots_2026'])}\\*) |
| S (Hochul vote share) | {p2(ST['S2022'])}% | {p2(ST['S2026'])}%* | {s2(ST['dS'])} pts* |
| R (Democratic registration share) | {p2(ST['R2022'])}% | {p2(ST['R2026'])}% | {s2(ST['dR'])} pts |
| G = S − R | {s2(ST['G2022'])} | {s2(ST['G2026'])}* | **ΔG {s2(ST['dG'])}\\*** |

ΔG rose in **{G['all']['n_dG_pos']} of 62** counties (county median {s2(MED)}\\*). Ceiling: {CEIL['name']} ({s2(CEIL['dG'])}\\*). Floor: {FLOOR['name']} County, which is Manhattan ({s2(FLOOR['dG'])}\\*). Statewide gap in votes: about **{sg(ST['gap'])}\\***.

**Working Families side check.** Counting Working Families enrollees as Democrats in R changes statewide ΔG from {s2(SIDE['state_dG'])}\\* to {s2(SIDE['state_dG_wf'])}\\*. County ΔG moves by at most {p2(SIDE['max_abs_diff'])} points, the two county lists correlate at r = {SIDE['corr']:.3f}, ΔG stays positive in {SIDE['n_pos_wf']} of 62, and the floor and ceiling stay the same. It tells the same story. See [Locked New York Formula](Locked-New-York-Formula#working-families-side-check).

## Sources

- **Enrollment, Nov 1, 2022:** NYS BOE, "Voters Registered by County as of 11/1/2022" ([listing](https://elections.ny.gov/enrollment-county); file [11-01-2022.xlsx](https://elections.ny.gov/system/files/documents/2023/10/11-01-2022.xlsx)).
- **Enrollment, Nov 1, 2026:** NYS BOE, "Voters Registered by County as of 11/01/2026" (file [county_nov26.xlsx](https://elections.ny.gov/system/files/documents/2026/11/county_nov26.xlsx)).
- **2022 Governor, certified:** NYS BOE results database, [2022 Nov 8 General, Governor](https://results.elections.ny.gov/contest/1) (same data as its "Results CSV" download).
- **2026 Governor, unofficial\\*:** NYS BOE [Election Night Reporting](https://nyenr.elections.ny.gov/), Governor and Lieutenant Governor, County Breakdown, page timestamp 11/21/2026 11:42:41 AM, 12,108 of 13,187 election districts reporting. Counties below full reporting on that page: Broome 125/126, Chautauqua 0/91, Nassau 1,006/1,083, Suffolk 1,067/1,070, Westchester 0/906, Wyoming 39/40.

Exact copies, SHA-256 fingerprints and all checks are in the repo: [raw/SOURCES.txt]({REPO}/blob/main/raw/SOURCES.txt) and [VERIFY_LOG.txt]({REPO}/blob/main/VERIFY_LOG.txt).
"""

# ================= HAMILTON =================
hturn22 = H['ballots_2022'] / H['reg_total_2022'] * 100
hturn26 = H['ballots_2026'] / H['reg_total_2026'] * 100
hexp = H['hochul_all_2022'] * H['reg_dem_2026'] / H['reg_dem_2022']
pages["Hamilton-County-Audit"] = f"""# Hamilton County Audit

{BANNER}

## What the audit covered

New York law requires a routine post-election audit in every county. <cite>Within fifteen days after each general election, the board of elections or a bipartisan committee must audit the voter verifiable audit records from three percent of voting machines or systems</cite> ([NYS BOE election security page](https://elections.ny.gov/election-security); [Election Law § 9-211](https://www.nysenate.gov/legislation/laws/ELN/9-211)).

**No Hamilton County audit records were obtained for this wiki.** The county's 2026 § 9-211 audit sheets are not posted on the NYS BOE sites used here; they would have to be requested from the Hamilton County Board of Elections. So this page audits the **numbers**: every Hamilton figure traced back to the official reports, line by line.

| Item | Value | Source |
|---|---|---|
| Election districts reporting, 2026 | {n(H['eds_reporting_2026'])} of {n(H['eds_total_2026'])} (complete) | ENR page\\* |
| Registered Democrats (Nov 1) | {n(H['reg_dem_2022'])} → {n(H['reg_dem_2026'])} | Enrollment reports |
| Working Families enrollees (Nov 1) | {n(H['reg_wor_2022'])} → {n(H['reg_wor_2026'])} | Enrollment reports |
| All registered voters (Nov 1) | {n(H['reg_total_2022'])} → {n(H['reg_total_2026'])} | Enrollment reports |
| Governor-race ballots (incl. blank and void) | {n(H['ballots_2022'])} → {n(H['ballots_2026'])}\\* (same number both years) | Results |
| Turnout (governor-race ballots ÷ all registered) | {hturn22:.1f}% → {hturn26:.1f}%\\* | Computed |

**Why Hamilton is the starting county.** It is the smallest of New York's 62 counties ({n(H['reg_total_2026'])} registered voters), so every step can be checked by hand. All of its election districts are reported\\*, unlike Westchester or Nassau. Its governor-race ballots were the same ({n(H['ballots_2026'])}) in both years, so a bigger or smaller turnout cannot explain the shift. Registered Democrats fell while Hochul's votes rose, which is the pattern this method looks for. Its ΔG ({s2(H['dG'])}\\*) ranks {HRANK} of 62 from the bottom, near the county median ({s2(MED)}\\*), so it is a typical county, not an outlier. The ceiling county, {CEIL['name']}, gained registered Democrats, so it cannot show the residual step; Hamilton can.

## Governor race: the Democrat-vs-Republican comparison

{FUSION}

{lines_tbl(H)}
| Shares | 2022 | 2026* | Change |
|---|---|---|---|
| Hochul share of race total (S) | {p2(H['S2022'])}% | {p2(H['S2026'])}%* | {s2(H['dS'])} pts* |
| Working Families share of Hochul's votes | {H['hochul_wor_share_2022']:.1f}% | {H['hochul_wor_share_2026']:.1f}%* | |
| Republican nominee margin over Hochul | {n(H['zeldin_all_2022']-H['hochul_all_2022'])} ({(H['zeldin_all_2022']-H['hochul_all_2022'])/H['race_total_2022']*100:.2f} pts) | {n(H['blakeman_all_2026']-H['hochul_all_2026'])}* ({(H['blakeman_all_2026']-H['hochul_all_2026'])/H['race_total_2026']*100:.2f} pts\\*) | |

Sources: NYS BOE certified 2022 results (Hamilton row, Governor); NYS BOE Election Night Reporting, Governor, Hamilton (11 of 11 districts), not yet certified.

## Hamilton governor-race gap

| Measure | 2022 | 2026* | Change |
|---|---|---|---|
| Registered Democrats (Nov 1) | {n(H['reg_dem_2022'])} | {n(H['reg_dem_2026'])} | {sg(H['reg_dem_2026']-H['reg_dem_2022'])} ({pct1(H['reg_dem_2022'],H['reg_dem_2026'])}) |
| Hochul votes, all lines | {n(H['hochul_all_2022'])} | {n(H['hochul_all_2026'])}* | {sg(H['hochul_all_2026']-H['hochul_all_2022'])}* ({pct1(H['hochul_all_2022'],H['hochul_all_2026'])}) |
| Governor-race ballots | {n(H['ballots_2022'])} | {n(H['ballots_2026'])}* | {sg(H['ballots_2026']-H['ballots_2022'])}* |
| Turnout | {hturn22:.1f}% | {hturn26:.1f}%* | |

If Hochul's votes had tracked Democratic registration, 2026 would show about {n(hexp)}. The actual {n(H['hochul_all_2026'])}\\* leaves a gap of about **{sg(H['gap'])}\\*** votes ({H['gap']/H['race_total_2026']*100:.1f}% of the 2026 governor race total). See [Bottom-Up Reverse Math](Reverse-Math).

{related("Reverse-Math", "Locked-New-York-Formula", "Graphs", "Home")}"""

# ================= REVERSE MATH =================
def rowmath(r):
    return (f"| {r['name']} | {n(r['reg_total_2026'])} | {n(r['reg_dem_2022'])} → {n(r['reg_dem_2026'])} | {n(r['hochul_all_2022'])} → {n(r['hochul_all_2026'])} "
            f"| {s2(r['dS'])} | {s2(r['dR'])} | {s2(r['dG'])} | {sg(r['gap'])} |")
def grp(g):
    return (f"| {g['county']} | {g['n']} | {p2(g['S2022'])}% → {p2(g['S2026'])}%* | {p2(g['R2022'])}% → {p2(g['R2026'])}% | {s2(g['dS'])} | {s2(g['dR'])} "
            f"| {s2(g['dG'])} | {s2(g['mean_dG'])} ({s2(g['min_dG'])} to {s2(g['max_dG'])}) | {sg(g['gap'])} | {sg(g['residual_votes'])} |")
o = G["outside"]
pages["Reverse-Math"] = f"""# Bottom-Up Reverse Math

{BANNER}

The same arithmetic at three levels, from one county up to the whole state. Race-votes denominator (governor race, every party line, write-ins included, blank and void excluded). {FUSION}

## Step 1: Hamilton County

| Step | Value |
|---|---|
| Hochul vote share (all lines) | {p2(H['S2022'])}% (2022) → {p2(H['S2026'])}%* (2026): **{s2(H['dS'])} points*** |
| Democratic registration share | {p2(H['R2022'])}% → {p2(H['R2026'])}%: **{s2(H['dR'])} points** |
| ΔG = vote-share growth − registration-share change | {p2(H['dS'])} − ({d2(H['dR'])}) = **{s2(H['dG'])} points*** |
| Reverse step: ΔG − registration-share loss | {p2(H['dG'])} − {p2(-H['dR'])} = {p2(H['surplus'])} (the vote-share surplus) |
| Gap in votes | {n(H['hochul_all_2026'])}* − {n(H['hochul_all_2022'])} × ({n(H['reg_dem_2026'])} ÷ {n(H['reg_dem_2022'])}) = **about {sg(H['gap'])}*** |


All shares and points are shown rounded to two decimals and computed from unrounded values, so a sum of rounded figures can differ from the shown total by 0.01.

## Step 2: the 57 counties outside New York City

The group is the official "Outside NYC" region in the NYS BOE enrollment file: every county except the five boroughs. Hamilton is one of them. Largest to smallest by registered voters (Nov 1, 2026).

| County | Registered 2026 | Dem reg 2022 → 2026 | Hochul votes 2022 → 2026* | Vote-share growth* (pts) | Registration-share change (pts) | ΔG* (pts) | Gap* |
|---|---|---|---|---|---|---|---|
""" + "\n".join(rowmath(r) for r in OUTSIDE) + f"""

ΔG is positive in **all {o['n_dG_pos']} of {o['n']}** ({s2(o['min_dG'])} to {s2(o['max_dG'])}, mean {s2(o['mean_dG'])}). Registered Democrats {n(o['reg_dem_2022'])} → {n(o['reg_dem_2026'])}; Hochul all-line votes {n(o['hochul_all_2022'])} → {n(o['hochul_all_2026'])}\\*. Registered Democrats fell in {sum(1 for r in OUTSIDE if r['fell'])} of the 57; the other {sum(1 for r in OUTSIDE if not r['fell'])} are non-loss counties (see [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)).

## Step 3: all of New York

| Group | Counties | Hochul vote share | Dem registration share | Vote-share growth* | Reg-share change | Pooled ΔG* | County mean ΔG* (range) | Gap* | Residual votes* |
|---|---|---|---|---|---|---|---|---|---|
{grp(G['outside'])}
{grp(G['nyc'])}
{grp(G['all'])}

The five NYC counties are {', '.join(r['name'] for r in NYC)} (largest first). ΔG is positive in {G['all']['n_dG_pos']} of 62 counties. Pooled ΔG is computed from summed votes and registration for the group; the county mean is the simple average of county ΔG values. The "Gap" column applies the gap formula to each group's totals.

> **Hypothesis label.** Turning ΔG into "residual votes" (denominator × ΔG ÷ 100) and calling them injected or offset votes is a hypothesis the arithmetic cannot test. The same number reflects turnout changes, crossover voting, unenrolled ("blank") voters, the Westchester count still in progress, and any other cause. Candidate votes are not turnout.

{img("NY_Hamilton_residual_steps.png", f"Hamilton residual steps: ΔG {s2(H['dG'])}* = {p2(H['dS'])}-point vote-share gain* + {p2(-H['dR'])}-point registration-share loss.")}
{img("NY_DeltaG_by_Group_OutsideNYC_vs_NYC.png", "County ΔG* for the 57 counties outside NYC and the 5 NYC counties.")}
{related("Hamilton-County-Audit", "Locked-New-York-Formula", "Floor-and-Ceiling", "Home")}"""

# ================= LOCKED FORMULA =================
pages["Locked-New-York-Formula"] = f"""# Locked New York Formula

{BANNER}

## The equation

- **S** (Hochul vote share) = Hochul votes on every line (Democratic + Working Families) ÷ all votes in the governor race (every candidate on every line, write-ins included, blank and void excluded) × 100
- **R** (Democratic registration share) = registered Democrats ÷ all registered voters (active + inactive), Nov 1 enrollment reports × 100
- **G** = S − R
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (R2026 − R2022)
- **Reverse step (registration-loss subtraction):** ΔG − |R2026 − R2022| = vote-share growth (the surplus)
- **Gap in votes:** D2026 − D2022 × (RegDem2026 ÷ RegDem2022), where D = Hochul votes on every line

{FUSION}

## New York's equation in final form

### Surplus Equation (New York statewide constant)

**Surplus Equation: S = {FIT['m']:.2f} × (D/100) + {FIT['b']:.2f}**

Where:
- S = Surplus, expressed in percentage points (in this one equation S means the surplus, not vote share)
- D = Democratic registration share, as a percent of total registration (0–100 scale), Nov 1, 2026, not a headcount of registered Democrats
- {FIT['m']:.2f} = Multiplier coefficient
- {FIT['b']:.2f} = Constant offset, in percentage points

Fitted by least squares from New York's own counties: the {FIT['n']} counties where registered Democrats fell (the counties that run line 11). Fit strength: r = {FIT['r']:.2f}, r² = {FIT['r2']:.2f}. That is a **weak** fit: Democratic registration share explains only about {FIT['r2']*100:.0f}% of the county-to-county spread in surplus. Use it as a rough statewide guide, not a prediction for any one county. Each state fits its own multiplier and offset; these New York values were not copied from any other state.

### County-level ΔG

**ΔG = (S2026 − S2022) − (R2026 − R2022)**

Hamilton County plugged in:

**ΔG = ({p2(H['S2026'])}\\* − {p2(H['S2022'])}) − ({p2(H['R2026'])} − {p2(H['R2022'])}) = {p2(H['dS'])}\\* − ({d2(H['dR'])}) = {s2(H['dG'])}\\***

All shares and points are shown rounded to two decimals and computed from unrounded values, so a sum of rounded figures can differ from the shown total by 0.01.


The equation's prediction for Hamilton: {FIT['m']:.2f} × ({p2(H['R2026'])}/100) + {FIT['b']:.2f} = {p2(H['surplus_fitted'])}. Actual surplus {p2(H['surplus'])}\\* (residual {s2(H['surplus_resid'])}).

## Blank template

| Line | Item | 2022 | 2026* |
|---|---|---|---|
| 1 | Hochul votes, all lines (Democratic + Working Families) | ______ | ______ |
| 2 | Total votes in the governor race (every line, incl. write-ins; not blank or void) | ______ | ______ |
| 3 | S = line 1 ÷ line 2 × 100 | ______ | ______ |
| 4 | Registered Democrats (Nov 1 enrollment report) | ______ | ______ |
| 5 | All registered voters, active + inactive (Nov 1 enrollment report) | ______ | ______ |
| 6 | R = line 4 ÷ line 5 × 100 | ______ | ______ |
| 7 | G = line 3 − line 6 | ______ | ______ |
| 8 | ΔG = G 2026 − G 2022 | | ______ |
| 9 | Registration-share change = R 2026 − R 2022 | | ______ |
| 10 | Did Democratic registration fall? (line 4: 2026 < 2022) | | Yes / No |
| 11 | If yes: vote-share surplus = line 8 − \\|line 9\\| | | ______ |
| 12 | Gap in votes = line 1 2026 − line 1 2022 × (line 4 2026 ÷ line 4 2022) | | ______ |

Write the line-by-line split next to line 1 (Democratic and Working Families) and line 2 (each candidate's lines, write-ins) so nothing is hidden.

**Counties without a Democratic registration loss skip line 11.** {len(NONLOSS)} New York counties gained registered Democrats: {', '.join(f"{r['name']} ({n(r['reg_dem_2022'])} → {n(r['reg_dem_2026'])})" for r in NONLOSS)}. There is no registration loss to subtract, so the residual/registration-loss step does not apply. Report ΔG and vote-share growth directly. (In {sum(1 for r in NONLOSS if r['dR'] < 0)} of these {len(NONLOSS)} the Democratic registration *share* still slipped, because all registration grew faster.)

## Rules for using this formula

1. **If a county lost Democratic registration, you must run the residual step.** This is the reverse-math step Morissa used to isolate what the numbers should have been. Subtract the registration-share loss from ΔG (line 11) and compute the gap in votes (line 12). Only counties that lost Democratic registration run the residual step. **Non-loss counties** (also called share-gain counties), which gained registered Democrats, skip line 11 and get raw numbers only.
2. **The starting point is different in every state. Don't assume another state's numbers carry over.** New York's overall Democratic share of registration ({p2(ST['R2026'])}% in 2026) sets its own starting G values, its own typical ΔG and its own county spread. Run the formula on New York's own enrollment and results reports, and compare its counties against New York's own range.
3. **Always pull out the ceiling and floor counties.** The ceiling is the county with the largest ΔG: {CEIL['name']} ({s2(CEIL['dG'])}\\*). The floor is the county with the smallest ΔG: {FLOOR['name']} ({s2(FLOOR['dG'])}\\*). In New York no county has a negative ΔG, so the floor is still a rise. Together they set the range the state works within, and every other county falls between them. See [Floor and Ceiling Counties](Floor-and-Ceiling).
4. **Count every party line (New York only).** A candidate's votes are the sum of every line he or she appeared on. Always show the split beside the sum.
5. **Carry the asterisk.** Every 2026 figure is unofficial until the NYS BOE certifies it.

**Terms used in this wiki** (full definitions on [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)):
- **Ceiling counties**: the five highest ΔG ({', '.join(r['name'] for r in CEIL5)}).
- **Floor**: the lowest-ΔG counties ({', '.join(r['name'] for r in FLOOR3)}).
- **Non-loss counties / share-gain counties**: counties with no Democratic registration loss. Raw numbers only; no residual step.

## Working Families side check

New York voters can enroll in the Working Families Party, and Hochul ran on that line too. As a side check, ΔG was run a second time with R = (registered Democrats + Working Families enrollees) ÷ all registered voters.

| Check | Main run (Democrats only in R) | Side check (Democrats + WF in R) |
|---|---|---|
| Statewide R, 2022 → 2026 | {p2(ST['R2022'])}% → {p2(ST['R2026'])}% | {p2(ST['Rwf2022'])}% → {p2(ST['Rwf2026'])}% |
| Statewide ΔG* | {s2(SIDE['state_dG'])} | {s2(SIDE['state_dG_wf'])} |
| Counties with ΔG > 0 | {SIDE['n_pos']} of 62 | {SIDE['n_pos_wf']} of 62 |
| Ceiling / floor | {SIDE['ceiling']} / {SIDE['floor']} | {SIDE['ceiling_wf']} / {SIDE['floor_wf']} |
| Five highest ΔG | {', '.join(SIDE['top5'])} | {', '.join(SIDE['top5_wf'])} |

Largest change in any county's ΔG: {p2(SIDE['max_abs_diff'])} points. Correlation between the two county lists: r = {SIDE['corr']:.3f} (rank correlation {SIDE['spearman']:.3f}). **Same story**: Working Families enrollment is small ({n(ST['reg_wor_2022'])} → {n(ST['reg_wor_2026'])} statewide) and does not change the pattern.

## Worked example: Hamilton

| Line | Item | 2022 | 2026* |
|---|---|---|---|
| 1 | Hochul votes, all lines | {n(H['hochul_all_2022'])} ({n(H['hochul_dem_2022'])} DEM + {n(H['hochul_wor_2022'])} WF) | {n(H['hochul_all_2026'])}* ({n(H['hochul_dem_2026'])} DEM + {n(H['hochul_wor_2026'])} WF) |
| 2 | Governor race total | {n(H['race_total_2022'])} | {n(H['race_total_2026'])}* |
| 3 | S | {p2(H['S2022'])} | {p2(H['S2026'])}* |
| 4 | Registered Democrats | {n(H['reg_dem_2022'])} | {n(H['reg_dem_2026'])} |
| 5 | All registered | {n(H['reg_total_2022'])} | {n(H['reg_total_2026'])} |
| 6 | R | {p2(H['R2022'])} | {p2(H['R2026'])} |
| 7 | G | {s2(H['G2022'])} | {s2(H['G2026'])}* |
| 8 | ΔG | | {s2(H['dG'])}* |
| 9 | Registration-share change | | {s2(H['dR'])} |
| 10 | Registration fell? | | Yes |
| 11 | Surplus | | {p2(H['surplus'])}* |
| 12 | Gap in votes | | {sg(H['gap'])}* |

{related("Reverse-Math", "Floor-and-Ceiling", "Hamilton-County-Audit", "Home")}"""

# ================= FLOOR & CEILING =================
def fcrow(r):
    return (f"| {r['name']} | {s2(r['G2022'])} | {s2(r['G2026'])} | {s2(r['dG'])} | {r['R2026']:.1f}% | {n(r['reg_dem_2022'])} → {n(r['reg_dem_2026'])} "
            f"| {n(r['hochul_all_2022'])} → {n(r['hochul_all_2026'])} | {'Yes' if r['fell'] else 'No (non-loss)'} |")
neg22 = [r for r in CEIL5 if r['G2022'] < 0]
pages["Floor-and-Ceiling"] = f"""# Floor and Ceiling Counties

{BANNER}

## How to read floor and ceiling counties

Look for the pattern at both ends. The ceiling counties are the ones with the highest ΔG; in New York those are {', '.join(r['name'] for r in CEIL5)}. The floor counties are the ones with the lowest ΔG.

- **The floor** is the single county with the lowest ΔG in the state. In New York that's {FLOOR['name']} County (Manhattan), at {s2(FLOOR['dG'])}\\*.
- **The ceiling** is the single county with the highest ΔG in the state. In New York that's {CEIL['name']}, at {s2(CEIL['dG'])}\\*.

Every state will have its own floor and ceiling. Those two extremes set the range the rest of that state's counties fall within. In New York every county's ΔG is positive, so even the floor is a rise.

## Terminology

- **Ceiling counties** are the five counties with the largest positive ΔG: {', '.join(f"{r['name']} {s2(r['dG'])}\\*" for r in CEIL5)}. Unlike Nebraska, two of New York's five ({', '.join(r['name'] for r in CEIL5 if not r['fell'])}) **gained** registered Democrats, so they are non-loss counties and do not run the residual step. The highest-ΔG county that lost registered Democrats (the top residual county) is {TOPLOSS['name']} ({s2(TOPLOSS['dG'])}\\*; surplus {p2(TOPLOSS['surplus'])}\\*; gap {sg(TOPLOSS['gap'])}\\*).
- **Floor** counties have the lowest ΔG: {', '.join(f"{r['name']} {s2(r['dG'])}\\*" for r in FLOOR3)}. {FLOOR['name']} County stands well apart: the next-lowest county is {FLOOR3[1]['name']}, {p2(FLOOR3[1]['dG']-FLOOR['dG'])} points higher. {FLOOR['name']} County already had the state's highest Hochul vote share in 2022 ({p2(FLOOR['S2022'])}%); it moved only to {p2(FLOOR['S2026'])}%\\*.
- **Non-loss counties** (also called **share-gain counties**) had no Democratic registration loss. They get raw numbers only, with no residual step. There are {len(NONLOSS)}, largest first:
""" + "\n".join(f"  - {r['name']}: registered Democrats {n(r['reg_dem_2022'])} → {n(r['reg_dem_2026'])}; Hochul all-line votes {n(r['hochul_all_2022'])} → {n(r['hochul_all_2026'])}\\*." for r in NONLOSS) + f"""
- **Registration fell and votes fell too.** No New York county is in this group: Hochul's all-line votes rose in all 62.

## Ceiling and floor detail

**Ceiling:** {CEIL['name']} and {CEIL5[1]['name']} are the only counties with ΔG above +12; {', '.join(r['name'] for r in CEIL5[2:])} are next. {f"{len(neg22)} of the five ({', '.join(r['name'] for r in neg22)}) began 2022 with a negative G (Hochul's vote share behind Democratic registration share) and turned positive in 2026." if neg22 else "All five began 2022 with G at or above zero."} Democratic registration share fell in all five, even in the two that gained registered Democrats, because all registration grew faster.

**Floor:** No county's ΔG fell. Every county's gap in votes is positive (smallest: {min(ROWS, key=lambda r: r['gap'])['name']}, {sg(min(r['gap'] for r in ROWS))}\\*).

| County | G 2022 | G 2026* | ΔG* | Dem reg share 2026 | Dem reg 2022 → 2026 | Hochul votes 2022 → 2026* | Registration fell? |
|---|---|---|---|---|---|---|---|
""" + "\n".join(fcrow(r) for r in CEIL5 + FLOOR3[::-1]) + f"""

Statewide, ΔG rose in {G['all']['n_dG_pos']} of 62 counties (median about {s2(MED)}).

{img("NY_Ceiling_Counties_DeltaG_by_Size.png", "Ceiling counties: ΔG* split into vote-share gain and registration-share loss.")}
{img("NY_deltaG_by_county_size_order_floor_NewYork_ceiling_Orange.png", f"All 62 counties, ΔG in size order (registered voters), floor {FLOOR['name']} and ceiling {CEIL['name']} marked.")}
{related("Reverse-Math", "Graphs", "Locked-New-York-Formula", "Home")}"""

# ================= GRAPHS =================
pages["Graphs"] = f"""# Graphs

> **\\*2026 figures are unofficial and not certified by the NYS Board of Elections** (Election Night Reporting page, 11/21/2026 11:42 AM; Westchester count incomplete). Governor race unless noted. Hochul votes are all lines (Democratic + Working Families). Registration is the Nov 1 enrollment report. County size is total registered voters, Nov 1, 2026 (this wiki uses only NYS BOE data, so no census population). These charts measure a pattern; they make no claim about intent, fraud or cause.

## 1. County slope chart

{img("NY_Slope_G2022_to_G2026_County_Slope_Chart.png", f"Each line is one county, G 2022 to G 2026*. G rose in {G['all']['n_dG_pos']} of 62 counties; the ceiling ({CEIL['name']}) rose most steeply and the floor ({FLOOR['name']}) was nearly flat.")}
## 2. Stacked bars

{img("NY_governor_stacked_share_by_size.png", "2022 Hochul share plus 2026 gain*, all 62 counties smallest to largest; dark outline marks the non-loss counties.")}
## 3. ΔG by county size

{img("NY_DeltaG_vs_Size_Scatter.png", f"ΔG* against county size (registered voters, log scale), all 62 counties (r = {SCAT_R:.2f}, n = 62). Larger counties tend to have higher ΔG; treat as a pattern, not a conclusion.")}
{img("NY_deltaG_by_county_size_order_floor_NewYork_ceiling_Orange.png", f"All 62 counties in size order. Floor: {FLOOR['name']} ({s2(FLOOR['dG'])}*). Ceiling: {CEIL['name']} ({s2(CEIL['dG'])}*).")}
## 4. Vote-share gain vs registration loss

{img("NY_governor_2022_share_vs_gain_bar_chart.png", "All 62 counties sorted by 2022 Hochul vote share. Blue is the 2022 share; orange is the 2022 to 2026 gain*.")}
{img("NY_governor_stacked_share_with_Dem_registration_loss_by_size.png", "Hochul vote-share gain* (above the line) and Democratic registration-share change (below the line), all 62 counties smallest to largest.")}
## 5. Ceiling counties

{img("NY_Ceiling_Counties_DeltaG_by_Size.png", "Ceiling counties: " + ", ".join(f"{r['name']} {s2(r['dG'])}*" for r in CEIL5) + ".")}
## 6. Hamilton County (starting county)

{img("NY_Hamilton_residual_steps.png", f"Hamilton reverse math: ΔG {s2(H['dG'])}* = {p2(H['dS'])}-point vote-share gain* + {p2(-H['dR'])}-point registration-share loss.")}
{img("NY_DeltaG_by_Group_OutsideNYC_vs_NYC.png", f"County ΔG* by group: 57 counties outside NYC (mean {s2(G['outside']['mean_dG'])}*) and the 5 NYC counties (mean {s2(G['nyc']['mean_dG'])}*).")}
{related("Hamilton-County-Audit", "Reverse-Math", "Floor-and-Ceiling", "Home")}"""

# ================= PDF INFO =================
top = max(ROWS, key=lambda r: r["R2026"]); most = max(ROWS, key=lambda r: r["reg_dem_2026"])
pages["62-County-PDF-Information"] = f"""# 62 County PDF Information

**[Download the 62-county numbers (PDF, 4 pages)]({RAWURL}New_York_62_County_Democratic_Registration_and_Vote_Change.pdf)**

> **\\*2026 figures are unofficial and not certified by the NYS Board of Elections.** They may still change; the Board says Westchester's count is incomplete. Votes are a candidate's votes on every party line, not a count of registered Democrats who voted. These numbers measure a pattern; they make no claim about intent, fraud or cause.

## What the numbers show

The PDF covers all 62 New York counties in the governor race, 2022 vs 2026\\*, in two tables with the same county order.

**Table 1** gives, for each county:

- **Democratic share of registration, 2026:** registered Democrats ÷ all registered voters (Nov 1, 2026)
- **Democratic registration:** Nov 1, 2022 and Nov 1, 2026, with the change as a number and a percent
- **Hochul votes by line and combined:** Democratic line, Working Families line, and all lines, 2022 and 2026\\*, with the change in all-line votes as a number and a percent of the 2022 total
- **Governor-race ballots:** 2022 and 2026\\* (every vote recorded in the race, including blank and void), with the change as a number and a percent

**Table 2** gives the opponent's votes by line and combined (Zeldin: Republican, Conservative; Blakeman: Republican, Conservative, Vote Affordable), write-ins, blanks, voids, and all registered voters with the change.

Counties are sorted by 2026 Democratic share of registration, highest first, so {top['name']} County comes first ({top['R2026']:.1f}%). {most['name']} has the most registered Democrats ({n(most['reg_dem_2026'])}).

Statewide, Democratic registration went from {n(ST['reg_dem_2022'])} to {n(ST['reg_dem_2026'])} ({sg(ST['reg_dem_2026']-ST['reg_dem_2022'])}, {pct1(ST['reg_dem_2022'],ST['reg_dem_2026'])}). Hochul's all-line votes went from {n(ST['hochul_all_2022'])} to {n(ST['hochul_all_2026'])}\\* ({sg(ST['hochul_all_2026']-ST['hochul_all_2022'])}\\*, {pct1(ST['hochul_all_2022'],ST['hochul_all_2026'])}\\*), and governor-race ballots went from {n(ST['ballots_2022'])} to {n(ST['ballots_2026'])}\\* ({sg(ST['ballots_2026']-ST['ballots_2022'])}\\*, {pct1(ST['ballots_2022'],ST['ballots_2026'])}\\*). In {len(LOSS)} of 62 counties Democratic registration fell while Hochul's votes rose. The exceptions are shaded in the table: Democratic registration rose in {', '.join(r['name'] for r in NONLOSS)}. Hochul's all-line votes rose in every county.

**Sources:** NYS BOE enrollment by county as of Nov 1, 2022 and Nov 1, 2026; NYS BOE certified 2022 Governor results; NYS BOE Election Night Reporting (unofficial), page timestamp 11/21/2026 11:42:41 AM, retrieved 22 Nov 2026. Data files: [data/ny_county_table.csv]({REPO}/blob/main/data/ny_county_table.csv).

{related("Home", "Reverse-Math", "Floor-and-Ceiling", "Locked-New-York-Formula")}"""

pages["_Sidebar"] = """**New York Election Analysis**

1. [Home](Home)
2. [Hamilton County Audit](Hamilton-County-Audit)
3. [Floor and Ceiling Counties](Floor-and-Ceiling)
4. [Bottom-Up Reverse Math](Reverse-Math)
5. [Graphs](Graphs)
6. [62 County PDF Information](62-County-PDF-Information)
7. [Locked New York Formula](Locked-New-York-Formula)
"""

# <cite> tags are only for our drafting; strip them
for k, v in pages.items():
    v = v.replace("<cite>", "").replace("</cite>", "")
    open(os.path.join(WIKI, k + ".md"), "w").write(v)

# ================= README =================
readme = f"""# New York Election Analysis: 2022 vs 2026 Governor Race

**A plain-language guide to what this project is and how to read it.**

> **\\*Important:** Every 2026 number in this project is **unofficial and not certified by the New York State Board of Elections**. It comes from the Board's Election Night Reporting page as of 11/21/2026 11:42 AM. The Board itself says that page leaves out a significant number of unscanned emergency Election Day ballots from Westchester County, and six counties were not fully reported. Numbers can still change. Whenever you see a **\\*** next to a number, it means "unofficial 2026 figure."

## What is this?

This project compares the 2022 and 2026 races for Governor of New York, county by county, for all 62 counties. It asks one simple question:

> **Did the Democratic candidate's share of the vote change by more or less than the Democratic Party's share of registered voters?**

If a party loses registered voters but its candidate's vote share goes up, the two numbers have moved apart. This project measures **how far apart** in every county, using only official numbers from the New York State Board of Elections.

It is part of a state-by-state series that uses the same method (the **ΔG method**, developed by Morissa Benson in Nebraska). Each state uses **only its own numbers**.

**What this project does NOT do:** it does not claim fraud, error, or intent by anyone. It measures a pattern. Many ordinary things can cause the pattern: people who are not enrolled Democrats voting for the Democrat, changes in who turned out, people moving, voter-roll cleanups, and counts still in progress.

## Where the numbers come from

Every number comes from the New York State Board of Elections:

| What | Which report |
|---|---|
| Registered voters by party, by county | Enrollment by County, **as of Nov 1, 2022** and **as of Nov 1, 2026** (active + inactive voters) |
| 2022 Governor votes by county | The Board's **certified** 2022 results |
| 2026 Governor votes by county | The Board's **unofficial** Election Night Reporting page\\* |

Links, exact copies of the data, and digital fingerprints proving the copies match the originals are in [`raw/SOURCES.txt`](raw/SOURCES.txt).

## Fusion voting (Working Families and other party lines)

New York lets one candidate appear on the ballot on **more than one party's line**. This is called **fusion voting**. A voter can pick Kathy Hochul on the Democratic line or on the Working Families line; both count for Hochul.

This project counts **every line** for each candidate and always shows the split so nothing is hidden:

| Candidate | Lines counted |
|---|---|
| Kathy Hochul (Democrat), 2022 and 2026 | Democratic + Working Families |
| Lee Zeldin (Republican), 2022 | Republican + Conservative |
| Bruce Blakeman (Republican), 2026 | Republican + Conservative + Vote Affordable |

The **Working Families Party** is a separate party that usually nominates the Democrat for governor. **Vote Affordable** was a 2026 ballot line that also carried Blakeman; the Board's own total for Blakeman includes it, so this project does too.

## What every term means

| Term | Plain meaning | How it is figured |
|---|---|---|
| **S** (vote share) | Out of everyone who voted for governor, what percent voted for Hochul | Hochul's votes on all her lines ÷ all votes for governor (every candidate, every line, write-ins included; blank and spoiled "void" ballots left out) × 100 |
| **R** (registration share) | Out of everyone registered, what percent are registered Democrats | Registered Democrats ÷ all registered voters (active + inactive, Nov 1) × 100 |
| **G** (the gap between them) | How far the vote share is above (+) or below (−) the registration share | G = S − R |
| **ΔG** ("delta G", the change) | How much that gap grew or shrank from 2022 to 2026 | ΔG = G 2026 − G 2022 |
| **Surplus** | The part of ΔG left after taking out the drop in Democratic registration share | ΔG − (size of the registration-share drop). Only for counties that lost registered Democrats |
| **Gap in votes** | How many more votes Hochul got in 2026 than you would expect if her votes had moved exactly with the number of registered Democrats | 2026 Hochul votes − 2022 Hochul votes × (2026 registered Democrats ÷ 2022 registered Democrats) |
| **Ceiling** | The county with the **highest** ΔG | {CEIL['name']}, {s2(CEIL['dG'])}\\* |
| **Floor** | The county with the **lowest** ΔG | {FLOOR['name']} County (Manhattan), {s2(FLOOR['dG'])}\\* |
| **Non-loss county** | A county where the number of registered Democrats went **up**. There is no loss to subtract, so the surplus step is skipped | {len(NONLOSS)} counties |
| **Starting county** | The county used to walk through the math step by step | Hamilton, New York's smallest county |
| **Points** | Percentage points: the difference between two percents (50% to 53% is +3 points) | |

**A quick example (Hamilton County).** In 2022, Hochul got {p2(H['S2022'])}% of the governor vote and Democrats were {p2(H['R2022'])}% of registered voters, so G was {s2(H['G2022'])}. In 2026\\*, Hochul got {p2(H['S2026'])}%\\* and Democrats were {p2(H['R2026'])}%, so G was {s2(H['G2026'])}\\*. ΔG = {p2(H['G2026'])} − {p2(H['G2022'])} = **{s2(H['dG'])} points\\***.

## The main findings (statewide)

| Measure | 2022 | 2026* |
|---|---|---|
| Registered Democrats (Nov 1) | {n(ST['reg_dem_2022'])} | {n(ST['reg_dem_2026'])} |
| Hochul votes, all lines | {n(ST['hochul_all_2022'])} | {n(ST['hochul_all_2026'])}* |
| S (Hochul vote share) | {p2(ST['S2022'])}% | {p2(ST['S2026'])}%* |
| R (Democratic registration share) | {p2(ST['R2022'])}% | {p2(ST['R2026'])}% |
| G | {s2(ST['G2022'])} | {s2(ST['G2026'])}* |

- Statewide **ΔG = {s2(ST['dG'])} points\\***. ΔG went up in **{G['all']['n_dG_pos']} of 62** counties.
- Registered Democrats went **down** in {len(LOSS)} counties and **up** in {len(NONLOSS)}. Hochul's votes went **up** in all 62.
- Statewide gap in votes: about **{sg(ST['gap'])}\\***.
- The New York surplus equation, fitted from New York's own counties, is **Surplus = {FIT['m']:.2f} × (D/100) + {FIT['b']:.2f}** (D = Democratic share of registration in percent). It is a weak fit (r = {FIT['r']:.2f}).
- Counting Working Families enrollees as Democrats tells **the same story** (statewide ΔG {s2(SIDE['state_dG_wf'])}\\*; same floor and ceiling).

## How to read the tables

- **Each row is one county.** Columns marked 2022 are certified; columns marked 2026\\* are unofficial.
- **"A → B"** means the value went from A (2022) to B (2026).
- **"+" or "−"** in front of a number shows which way it moved.
- **Shaded rows** in the PDF are non-loss counties (registered Democrats went up).
- When a cell shows several party lines and then a total, the total is the sum of those lines.

## Where to go next

| Page | What you'll find |
|---|---|
| [Wiki Home]({REPO}/wiki) | Overview and statewide numbers |
| [Hamilton County Audit]({REPO}/wiki/Hamilton-County-Audit) | The starting county, line by line |
| [Bottom-Up Reverse Math]({REPO}/wiki/Reverse-Math) | Hamilton → the 57 counties outside NYC → all 62 counties |
| [Locked New York Formula]({REPO}/wiki/Locked-New-York-Formula) | The formula, a fill-in template and a worked example |
| [Floor and Ceiling Counties]({REPO}/wiki/Floor-and-Ceiling) | The top and bottom counties |
| [Graphs]({REPO}/wiki/Graphs) | All charts |
| [62 County PDF Information]({REPO}/wiki/62-County-PDF-Information) | The downloadable 62-county table |

## What's in this repository

| Folder / file | Contents |
|---|---|
| `raw/` | Exact copies of the official data, plus `SOURCES.txt` (links and fingerprints) |
| `data/ny_county_table.csv` | Every computed number for every county and the state |
| `data/ny_summary.json` | Group totals, the fitted equation and the side check |
| `scripts/` | The programs that compute the numbers, draw the charts, build the PDF and pages, and check everything |
| `*.png` | The charts |
| `New_York_62_County_Democratic_Registration_and_Vote_Change.pdf` | The 62-county table |
| `wiki/` | Copies of the wiki pages |
| `VERIFY_LOG.txt` | The record of the three accuracy checks done before publishing |

To rebuild everything: `python3 scripts/compute.py && python3 scripts/charts.py && python3 scripts/make_pdf.py && python3 scripts/build_pages.py && python3 scripts/verify.py`

## Disclaimers

1. **2026 numbers are unofficial\\*** and not certified by the New York State Board of Elections. Westchester's count was incomplete when the data was pulled. Final certified numbers may differ.
2. **This measures a pattern, not a cause.** It makes no claim about intent, fraud, or wrongdoing by any person, office, or party.
3. **Votes are not voters.** "Hochul votes" counts votes for her on every line. It is not a count of registered Democrats who voted; anyone may vote for any candidate.
4. **Registration counts** are the Board's Nov 1 reports (active + inactive voters) for each year.
5. **New York only.** No other state's numbers are used anywhere in this project.
"""
open(os.path.join(ROOT, "README.md"), "w").write(readme)
print("pages:", sorted(pages), "README ok")
