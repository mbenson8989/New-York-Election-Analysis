# New York Election Analysis: 2022 vs 2026 Governor Race

**A plain-language guide to what this project is and how to read it.**

> **\*Important:** Every 2026 number in this project is **unofficial and not certified by the New York State Board of Elections**. It comes from the Board's Election Night Reporting page as of 11/21/2026 11:42 AM. The Board itself says that page leaves out a significant number of unscanned emergency Election Day ballots from Westchester County, and six counties were not fully reported. Numbers can still change. Whenever you see a **\*** next to a number, it means "unofficial 2026 figure."

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
| 2026 Governor votes by county | The Board's **unofficial** Election Night Reporting page\* |

Links, exact copies of the data, and digital fingerprints proving the copies match the originals are in [`source_data/SOURCES.txt`](source_data/SOURCES.txt).

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
| **Ceiling** | The county with the **highest** ΔG | Orange, +12.38\* |
| **Floor** | The county with the **lowest** ΔG | New York County (Manhattan), +0.58\* |
| **Non-loss county** | A county where the number of registered Democrats went **up**. There is no loss to subtract, so the surplus step is skipped | 13 counties |
| **Starting county** | The county used to walk through the math step by step | Hamilton, New York's smallest county |
| **Points** | Percentage points: the difference between two percents (50% to 53% is +3 points) | |

**A quick example (Hamilton County).** In 2022, Hochul got 28.83% of the governor vote and Democrats were 20.59% of registered voters, so G was +8.25. In 2026\*, Hochul got 33.40%\* and Democrats were 19.54%, so G was +13.86\*. ΔG = 13.86 − 8.25 = **+5.61 points\***.

## The main findings (statewide)

| Measure | 2022 | 2026* |
|---|---|---|
| Registered Democrats (Nov 1) | 6,511,132 | 6,500,386 |
| Hochul votes, all lines | 3,140,415 | 3,638,027* |
| S (Hochul vote share) | 53.12% | 59.86%* |
| R (Democratic registration share) | 49.59% | 47.89% |
| G | +3.53 | +11.97* |

- Statewide **ΔG = +8.44 points\***. ΔG went up in **62 of 62** counties.
- Registered Democrats went **down** in 49 counties and **up** in 13. Hochul's votes went **up** in all 62.
- Statewide gap in votes: about **+502,795\***.
- The New York surplus equation, fitted from New York's own counties, is **Surplus = 7.98 × (D/100) + 2.54** (D = Democratic share of registration in percent). It is a weak fit (r = 0.40).
- Counting Working Families enrollees as Democrats tells **the same story** (statewide ΔG +8.31\*; same floor and ceiling).

## How to read the tables

- **Each row is one county.** Columns marked 2022 are certified; columns marked 2026\* are unofficial.
- **"A → B"** means the value went from A (2022) to B (2026).
- **"+" or "−"** in front of a number shows which way it moved.
- **Shaded rows** in the PDF are non-loss counties (registered Democrats went up).
- When a cell shows several party lines and then a total, the total is the sum of those lines.

## Where to go next

| Page | What you'll find |
|---|---|
| [Wiki Home](https://github.com/mbenson8989/New-York-Election-Analysis/wiki) | Overview and statewide numbers |
| [Hamilton County Audit](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/Hamilton-County-Audit) | The starting county, line by line |
| [Bottom-Up Reverse Math](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/Reverse-Math) | Hamilton → the 57 counties outside NYC → all 62 counties |
| [Locked New York Formula](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/Locked-New-York-Formula) | The formula, a fill-in template and a worked example |
| [Floor and Ceiling Counties](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/Floor-and-Ceiling) | The top and bottom counties |
| [Graphs](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/Graphs) | All charts |
| [62 County PDF Information](https://github.com/mbenson8989/New-York-Election-Analysis/wiki/62-County-PDF-Information) | The downloadable 62-county table |

## What's in this repository

| Folder / file | Contents |
|---|---|
| `source_data/` | Exact copies of the official data, plus `SOURCES.txt` (links and fingerprints) |
| `data/ny_county_table.csv` | Every computed number for every county and the state |
| `data/ny_summary.json` | Group totals, the fitted equation and the side check |
| `scripts/` | The programs that compute the numbers, draw the charts, build the PDF and pages, and check everything |
| `*.png` | The charts |
| `New_York_62_County_Democratic_Registration_and_Vote_Change.pdf` | The 62-county table |
| `wiki/` | Copies of the wiki pages |
| `VERIFY_LOG.txt` | The record of the three accuracy checks done before publishing |

To rebuild everything: `python3 scripts/compute.py && python3 scripts/charts.py && python3 scripts/make_pdf.py && python3 scripts/build_pages.py && python3 scripts/verify.py`

## Disclaimers

1. **2026 numbers are unofficial\*** and not certified by the New York State Board of Elections. Westchester's count was incomplete when the data was pulled. Final certified numbers may differ.
2. **This measures a pattern, not a cause.** It makes no claim about intent, fraud, or wrongdoing by any person, office, or party.
3. **Votes are not voters.** "Hochul votes" counts votes for her on every line. It is not a count of registered Democrats who voted; anyone may vote for any candidate.
4. **Registration counts** are the Board's Nov 1 reports (active + inactive voters) for each year.
5. **New York only.** No other state's numbers are used anywhere in this project.
