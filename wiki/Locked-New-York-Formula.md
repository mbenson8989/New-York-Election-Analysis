# Locked New York Formula

> **\*2026 figures are unofficial and not certified by the NYS Board of Elections.** They come from the Board's Election Night Reporting page as of 11/21/2026 11:42 AM. The Board says that page leaves out a significant number of unscanned emergency Election Day ballots from Westchester County, and six counties were not at full reporting (see [Sources](Home#sources)). Governor race unless a page says otherwise. Votes are a candidate's votes on every party line he or she appeared on (fusion voting), not a count of registered Democrats who voted. Registration is the Nov 1 enrollment report for each year (active + inactive). These pages measure a pattern; they make no claim about intent, fraud or cause.

## The equation

- **S** (Hochul vote share) = Hochul votes on every line (Democratic + Working Families) ÷ all votes in the governor race (every candidate on every line, write-ins included, blank and void excluded) × 100
- **R** (Democratic registration share) = registered Democrats ÷ all registered voters (active + inactive), Nov 1 enrollment reports × 100
- **G** = S − R
- **ΔG** = G(2026) − G(2022) = (S2026 − S2022) − (R2026 − R2022)
- **Reverse step (registration-loss subtraction):** ΔG − |R2026 − R2022| = vote-share growth (the surplus)
- **Gap in votes:** D2026 − D2022 × (RegDem2026 ÷ RegDem2022), where D = Hochul votes on every line

**Fusion lines:** Hochul = Democratic + Working Families. Zeldin (2022) = Republican + Conservative. Blakeman (2026) = Republican + Conservative + Vote Affordable; the Board's own Blakeman total includes the Vote Affordable line, so it is counted here and shown separately.

## New York's equation in final form

### Surplus Equation (New York statewide constant)

**Surplus Equation: S = 7.98 × (D/100) + 2.54**

Where:
- S = Surplus, expressed in percentage points (in this one equation S means the surplus, not vote share)
- D = Democratic registration share, as a percent of total registration (0–100 scale), Nov 1, 2026, not a headcount of registered Democrats
- 7.98 = Multiplier coefficient
- 2.54 = Constant offset, in percentage points

Fitted by least squares from New York's own counties: the 49 counties where registered Democrats fell (the counties that run line 11). Fit strength: r = 0.40, r² = 0.16. That is a **weak** fit: Democratic registration share explains only about 16% of the county-to-county spread in surplus. Use it as a rough statewide guide, not a prediction for any one county. Each state fits its own multiplier and offset; these New York values were not copied from any other state.

### County-level ΔG

**ΔG = (S2026 − S2022) − (R2026 − R2022)**

Hamilton County plugged in:

**ΔG = (33.40\* − 28.83) − (19.54 − 20.59) = 4.57\* − (−1.05) = +5.61\***

All shares and points are shown rounded to two decimals and computed from unrounded values, so a sum of rounded figures can differ from the shown total by 0.01.


The equation's prediction for Hamilton: 7.98 × (19.54/100) + 2.54 = 4.10. Actual surplus 4.57\* (residual +0.47).

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
| 11 | If yes: vote-share surplus = line 8 − \|line 9\| | | ______ |
| 12 | Gap in votes = line 1 2026 − line 1 2022 × (line 4 2026 ÷ line 4 2022) | | ______ |

Write the line-by-line split next to line 1 (Democratic and Working Families) and line 2 (each candidate's lines, write-ins) so nothing is hidden.

**Counties without a Democratic registration loss skip line 11.** 13 New York counties gained registered Democrats: Kings (1,147,500 → 1,184,803), Queens (830,745 → 835,420), New York (795,607 → 832,410), Westchester (334,221 → 342,767), Orange (98,857 → 99,652), Dutchess (80,773 → 82,243), Saratoga (54,073 → 56,439), Ulster (57,067 → 58,490), Rensselaer (35,144 → 36,508), Ontario (24,663 → 24,797), Tompkins (35,568 → 36,829), Warren (13,433 → 13,732), Columbia (19,852 → 19,885). There is no registration loss to subtract, so the residual/registration-loss step does not apply. Report ΔG and vote-share growth directly. (In 13 of these 13 the Democratic registration *share* still slipped, because all registration grew faster.)

## Rules for using this formula

1. **If a county lost Democratic registration, you must run the residual step.** This is the reverse-math step Morissa used to isolate what the numbers should have been. Subtract the registration-share loss from ΔG (line 11) and compute the gap in votes (line 12). Only counties that lost Democratic registration run the residual step. **Non-loss counties** (also called share-gain counties), which gained registered Democrats, skip line 11 and get raw numbers only.
2. **The starting point is different in every state. Don't assume another state's numbers carry over.** New York's overall Democratic share of registration (47.89% in 2026) sets its own starting G values, its own typical ΔG and its own county spread. Run the formula on New York's own enrollment and results reports, and compare its counties against New York's own range.
3. **Always pull out the ceiling and floor counties.** The ceiling is the county with the largest ΔG: Orange (+12.38\*). The floor is the county with the smallest ΔG: New York (+0.58\*). In New York no county has a negative ΔG, so the floor is still a rise. Together they set the range the state works within, and every other county falls between them. See [Floor and Ceiling Counties](Floor-and-Ceiling).
4. **Count every party line (New York only).** A candidate's votes are the sum of every line he or she appeared on. Always show the split beside the sum.
5. **Carry the asterisk.** Every 2026 figure is unofficial until the NYS BOE certifies it.

**Terms used in this wiki** (full definitions on [Floor and Ceiling Counties](Floor-and-Ceiling#terminology)):
- **Ceiling counties**: the five highest ΔG (Orange, Rockland, Queens, Richmond, Suffolk).
- **Floor**: the lowest-ΔG counties (New York, Schuyler, Wyoming).
- **Non-loss counties / share-gain counties**: counties with no Democratic registration loss. Raw numbers only; no residual step.

## Working Families side check

New York voters can enroll in the Working Families Party, and Hochul ran on that line too. As a side check, ΔG was run a second time with R = (registered Democrats + Working Families enrollees) ÷ all registered voters.

| Check | Main run (Democrats only in R) | Side check (Democrats + WF in R) |
|---|---|---|
| Statewide R, 2022 → 2026 | 49.59% → 47.89% | 49.98% → 48.41% |
| Statewide ΔG* | +8.44 | +8.31 |
| Counties with ΔG > 0 | 62 of 62 | 62 of 62 |
| Ceiling / floor | Orange / New York | Orange / New York |
| Five highest ΔG | Orange, Rockland, Queens, Richmond, Suffolk | Orange, Rockland, Queens, Suffolk, Richmond |

Largest change in any county's ΔG: 0.35 points. Correlation between the two county lists: r = 0.999 (rank correlation 0.998). **Same story**: Working Families enrollment is small (50,642 → 69,959 statewide) and does not change the pattern.

## Worked example: Hamilton

| Line | Item | 2022 | 2026* |
|---|---|---|---|
| 1 | Hochul votes, all lines | 831 (770 DEM + 61 WF) | 961* (895 DEM + 66 WF) |
| 2 | Governor race total | 2,882 | 2,877* |
| 3 | S | 28.83 | 33.40* |
| 4 | Registered Democrats | 953 | 871 |
| 5 | All registered | 4,629 | 4,457 |
| 6 | R | 20.59 | 19.54 |
| 7 | G | +8.25 | +13.86* |
| 8 | ΔG | | +5.61* |
| 9 | Registration-share change | | −1.05 |
| 10 | Registration fell? | | Yes |
| 11 | Surplus | | 4.57* |
| 12 | Gap in votes | | +202* |

---
**Related:** [Bottom-Up Reverse Math](Reverse-Math) · [Floor and Ceiling Counties](Floor-and-Ceiling) · [Hamilton County Audit](Hamilton-County-Audit) · [Home](Home)
