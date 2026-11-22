# New York 2022 vs 2026 Governor Race: ΔG Method

**Version 1, built Nov 22 2026 (data pulled Nov 22 2026)**

> **\*2026 figures are unofficial and not certified by the NYS Board of Elections.** They come from the Board's Election Night Reporting page as of 11/21/2026 11:42 AM. The Board says that page leaves out a significant number of unscanned emergency Election Day ballots from Westchester County, and six counties were not at full reporting (see [Sources](Home#sources)). Governor race unless a page says otherwise. Votes are a candidate's votes on every party line he or she appeared on (fusion voting), not a count of registered Democrats who voted. Registration is the Nov 1 enrollment report for each year (active + inactive). These pages measure a pattern; they make no claim about intent, fraud or cause.

Method developed by Morissa Benson (CD3 Vice Chair, Nebraska GOP). Data: New York State Board of Elections (NYS BOE) enrollment-by-county reports, the certified 2022 results database and the 2026 Election Night Reporting page, compiled 22 Nov 2026. New York numbers only; no other state's figures are used.

**Fusion lines:** Hochul = Democratic + Working Families. Zeldin (2022) = Republican + Conservative. Blakeman (2026) = Republican + Conservative + Vote Affordable; the Board's own Blakeman total includes the Vote Affordable line, so it is counted here and shown separately.

## Contents

Start with Hamilton County. It is New York's smallest county by registered voters, every one of its 11 election districts is in, and it recorded exactly 2,935 governor-race ballots in both years. Registered Democrats fell from 953 to 871 while Hochul's all-line votes rose from 831 to 961\*. The pages then build up from Hamilton to the 57 counties outside New York City, and to the statewide formula.

1. [Hamilton County Audit](Hamilton-County-Audit): Hamilton's numbers line by line, and what audit records exist
2. [Bottom-Up Reverse Math](Reverse-Math): Hamilton → the 57 counties outside NYC → all 62 counties
3. [Locked New York Formula](Locked-New-York-Formula): the equation, New York's fitted surplus equation, a blank fill-in template
4. [Floor and Ceiling Counties](Floor-and-Ceiling): the counties at the top and bottom of ΔG
5. [Graphs](Graphs): slope chart, ΔG by county size, stacked bars, vote-share vs registration-loss bars, ceiling counties, Hamilton steps
6. [62 County PDF Information](62-County-PDF-Information): the 62-county table of registration, votes by line and combined, and ballots (PDF download)

## Statewide at a glance

| Measure | 2022 | 2026* | Change |
|---|---|---|---|
| Democratic registration (Nov 1) | 6,511,132 | 6,500,386 | −10,746 (−0.2%) |
| All registered voters (Nov 1) | 13,129,900 | 13,572,803 | +442,903 (+3.4%) |
| Hochul votes, Democratic line | 2,879,092 | 3,263,690* | +384,598* |
| Hochul votes, Working Families line | 261,323 | 374,337* | +113,014* |
| **Hochul votes, all lines** | **3,140,415** | **3,638,027*** | **+497,612* (+15.8%\*)** |
| Governor-race ballots (incl. blank and void) | 5,962,278 | 6,140,811* | +178,533* (+3.0%\*) |
| S (Hochul vote share) | 53.12% | 59.86%* | +6.74 pts* |
| R (Democratic registration share) | 49.59% | 47.89% | −1.70 pts |
| G = S − R | +3.53 | +11.97* | **ΔG +8.44\*** |

ΔG rose in **62 of 62** counties (county median +6.68\*). Ceiling: Orange (+12.38\*). Floor: New York County, which is Manhattan (+0.58\*). Statewide gap in votes: about **+502,795\***.

**Working Families side check.** Counting Working Families enrollees as Democrats in R changes statewide ΔG from +8.44\* to +8.31\*. County ΔG moves by at most 0.35 points, the two county lists correlate at r = 0.999, ΔG stays positive in 62 of 62, and the floor and ceiling stay the same. It tells the same story. See [Locked New York Formula](Locked-New-York-Formula#working-families-side-check).

## Sources

- **Enrollment, Nov 1, 2022:** NYS BOE, "Voters Registered by County as of 11/1/2022" ([listing](https://elections.ny.gov/enrollment-county); file [11-01-2022.xlsx](https://elections.ny.gov/system/files/documents/2023/10/11-01-2022.xlsx)).
- **Enrollment, Nov 1, 2026:** NYS BOE, "Voters Registered by County as of 11/01/2026" (file [county_nov26.xlsx](https://elections.ny.gov/system/files/documents/2026/11/county_nov26.xlsx)).
- **2022 Governor, certified:** NYS BOE results database, [2022 Nov 8 General, Governor](https://results.elections.ny.gov/contest/1) (same data as its "Results CSV" download).
- **2026 Governor, unofficial\*:** NYS BOE [Election Night Reporting](https://nyenr.elections.ny.gov/), Governor and Lieutenant Governor, County Breakdown, page timestamp 11/21/2026 11:42:41 AM, 12,108 of 13,187 election districts reporting. Counties below full reporting on that page: Broome 125/126, Chautauqua 0/91, Nassau 1,006/1,083, Suffolk 1,067/1,070, Westchester 0/906, Wyoming 39/40.

Exact copies, SHA-256 fingerprints and all checks are in the repo: [source_data/SOURCES.txt](https://github.com/mbenson8989/New-York-Election-Analysis/blob/main/source_data/SOURCES.txt) and [VERIFY_LOG.txt](https://github.com/mbenson8989/New-York-Election-Analysis/blob/main/VERIFY_LOG.txt).
