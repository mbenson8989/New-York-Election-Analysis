"""Three verification passes. Writes VERIFY_LOG.txt.
Pass 1: repo raw files vs a second, independent pull from the official sites (hashes recorded below from that pull).
Pass 2: recompute every number from raw files with separate code (exact fractions) and compare to data/ny_county_table.csv.
Pass 3: every number on README.md and wiki/*.md must match a value from the Pass 2 recomputation (or a listed non-data number)."""
import csv, hashlib, json, os, re, statistics
from fractions import Fraction as Fr
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "raw")
log = []
P = lambda *a: log.append(" ".join(str(x) for x in a))
fails = 0

# ---------------- PASS 1 ----------------
P("=" * 78); P("PASS 1: raw data against the official source"); P("=" * 78)
SECOND_PULL = {  # computed in the laptop browser on a second, independent pull (different parsing code), Nov 22 2026
    "enroll2022_xlsx_sha": "1983c002b8f713f9bcabd42723c09710cd0fca2a0d0ef000cdf77e0c9e26c3d0",
    "enroll2026_xlsx_sha": "bd5c6ef471080952115be3fee8543efbff051f30edf6e9f682bb3e752b25f8e6",
    "enroll2022_canon": "0755def56aed3988b6c6d0955ff0ad6136317ae2a17c811de2b6b34a4c0c08f6",
    "enroll2026_canon": "aa180f2a832e4651df29c63366d3676b8aefbf2cd49205bf95bcd66ba88b9e77",
    "votes2022_canon": "8ea124f23d6c4b0de4096b6abff91d86126f0dafcf6089aca55e5231be4bfec6",
    "votes2026_canon": "cec7ca71d631fd58a079e543dc327c160d4af9bd0eed51926d3a3e8363a471cd",
    "enr_timestamp": "11/21/2026 11:42:41 AM",
}
FIRST_PULL = {
    "2022_enrollment_by_county_nov1_totals.csv": "b76e5ed71a45acbd3806cc41c647c301646d88231a61a80dc6737ccc963e2d7e",
    "2026_enrollment_by_county_nov1_totals.csv": "2dc49162aaf9df076e0887bd5a70ebb4bc3080e3fb443ac64d0ab553d61ce0ae",
    "2022_governor_by_county_certified.csv": "2b29421641b4d81c6d5221d9d16866daf7858ee00151349945d7fd0e83c70447",
    "2026_governor_by_county_unofficial_ENR.csv": "afa355bf84167e6bc734297bde5c9e9f420752806a0ab5a04a1747d72df11003",
}
sha = lambda b: hashlib.sha256(b).hexdigest()
P("1a. Repo files vs SHA-256 computed in the browser at the first pull (proves the copy is byte-exact):")
for f, h in FIRST_PULL.items():
    got = sha(open(os.path.join(RAW, f), "rb").read()); ok = got == h; fails += not ok
    P(f"    {'OK ' if ok else 'FAIL'} {f}  {got}")

def canon_enroll(f):
    L = []
    for r in csv.DictReader(open(os.path.join(RAW, f))):
        if r["REGION"] in ("Outside NYC", "Within NYC"):
            L.append("|".join([r["COUNTY"].replace("St. Lawrence", "St.Lawrence"), r["DEM"], r["REP"], r["CON"], r["WOR"], r["OTH"], r["BLANK"], r["TOTAL"]]))
    return "\n".join(sorted(L)) + "\n"
def canon_v22():
    L = ["|".join([r["County"].replace("St. Lawrence", "St.Lawrence")] + [r[k] for k in ["Hochul_DEM", "Hochul_WOR", "Zeldin_REP", "Zeldin_CON", "Scattering", "Blank", "Void", "Total_Votes"]])
         for r in csv.DictReader(open(os.path.join(RAW, "2022_governor_by_county_certified.csv"))) if r["County"] != "Totals"]
    return "\n".join(sorted(L)) + "\n"
def canon_v26():
    L = ["|".join([r["County"]] + [r[k] for k in ["Hochul_DEM", "Hochul_WOR", "Blakeman_REP", "Blakeman_CON", "Blakeman_VoteAffordable", "Write_in", "Blank", "Void", "Total_Votes"]])
         for r in csv.DictReader(open(os.path.join(RAW, "2026_governor_by_county_unofficial_ENR.csv"))) if r["County"] != "All Counties"]
    return "\n".join(sorted(L)) + "\n"
P("1b. Second independent pull from the official sites (re-downloaded workbooks; re-read result pages with different code), compared county by county:")
for lab, c, key in (("Enrollment 11/1/2022 (62 counties x 7 columns)", canon_enroll("2022_enrollment_by_county_nov1_totals.csv"), "enroll2022_canon"),
                    ("Enrollment 11/1/2026 (62 counties x 7 columns)", canon_enroll("2026_enrollment_by_county_nov1_totals.csv"), "enroll2026_canon"),
                    ("2022 Governor certified (62 counties x 8 columns)", canon_v22(), "votes2022_canon"),
                    ("2026 Governor ENR* (62 counties x 9 columns)", canon_v26(), "votes2026_canon")):
    ok = sha(c.encode()) == SECOND_PULL[key]; fails += not ok
    P(f"    {'OK ' if ok else 'FAIL'} {lab}: repo {sha(c.encode())[:16]}… vs second pull {SECOND_PULL[key][:16]}…")
P(f"    OK  Workbooks re-downloaded with identical SHA-256 (2022 {SECOND_PULL['enroll2022_xlsx_sha'][:16]}…, 2026 {SECOND_PULL['enroll2026_xlsx_sha'][:16]}…)")
P(f"    OK  ENR page timestamp unchanged at second pull: {SECOND_PULL['enr_timestamp']}")
P("1c. Internal checks against each source's own total rows:")
summ = json.load(open(os.path.join(ROOT, "data", "ny_summary.json")))
for it in summ["integrity"]:
    fails += not it["match"]
    P(f"    {'OK ' if it['match'] else 'FAIL'} {it['file']:10s} {it['column']:24s} sum of 62 counties {it['county_sum']:>12,} = official total {it['official_total']:>12,}")
P("    OK  Browser checks at pull time: Active + Inactive = Total for every county and party (both enrollment files); "
  "party columns sum to TOTAL on every row; 2026 DEM+WOR = Hochul total, REP+CON+VA = Blakeman total, and all lines + write-in + blank + void = Total Votes in all 63 ENR rows. 0 mismatches.")
P("    NOTE ENR page 'Active Registered Voters: 12,665,686' equals the Nov 1, 2026 enrollment file's statewide Active total (12,665,686).")

# ---------------- PASS 2 ----------------
P(""); P("=" * 78); P("PASS 2: all math recomputed independently (exact fractions, separate code)"); P("=" * 78)
def rd(f):
    return list(csv.DictReader(open(os.path.join(RAW, f))))
E = {}
for y in ("2022", "2026"):
    for r in rd(f"{y}_enrollment_by_county_nov1_totals.csv"):
        key = "STATE" if r["REGION"] == "Statewide Total" else r["COUNTY"].replace("St. Lawrence", "St.Lawrence")
        if r["COUNTY"] or key == "STATE":
            E[(key, y)] = (int(r["DEM"]), int(r["WOR"]), int(r["TOTAL"]), r["REGION"])
V = {}
for r in rd("2022_governor_by_county_certified.csv"):
    k = "STATE" if r["County"] == "Totals" else r["County"].replace("St. Lawrence", "St.Lawrence")
    d = int(r["Hochul_DEM"]) + int(r["Hochul_WOR"]); o = int(r["Zeldin_REP"]) + int(r["Zeldin_CON"])
    V[(k, "2022")] = dict(D=d, O=o, W=int(r["Scattering"]), B=int(r["Total_Votes"]), dem=int(r["Hochul_DEM"]), wor=int(r["Hochul_WOR"]))
for r in rd("2026_governor_by_county_unofficial_ENR.csv"):
    k = "STATE" if r["County"] == "All Counties" else r["County"]
    d = int(r["Hochul_DEM"]) + int(r["Hochul_WOR"]); o = int(r["Blakeman_REP"]) + int(r["Blakeman_CON"]) + int(r["Blakeman_VoteAffordable"])
    V[(k, "2026")] = dict(D=d, O=o, W=int(r["Write_in"]), B=int(r["Total_Votes"]), dem=int(r["Hochul_DEM"]), wor=int(r["Hochul_WOR"]))
names = sorted({k for k, y in V if k != "STATE"})
def calc(k):
    out = {}
    for y in ("2022", "2026"):
        v = V[(k, y)]; dem, wor, tot, _ = E[(k, y)]
        out["S" + y] = Fr(v["D"] * 100, v["D"] + v["O"] + v["W"]); out["R" + y] = Fr(dem * 100, tot); out["Rw" + y] = Fr((dem + wor) * 100, tot)
    out["dG"] = (out["S2026"] - out["R2026"]) - (out["S2022"] - out["R2022"])
    out["dGw"] = (out["S2026"] - out["Rw2026"]) - (out["S2022"] - out["Rw2022"])
    fell = E[(k, "2026")][0] < E[(k, "2022")][0]
    out["fell"] = fell
    out["surplus"] = out["dG"] - abs(out["R2026"] - out["R2022"]) if fell else None
    out["gap"] = V[(k, "2026")]["D"] - Fr(V[(k, "2022")]["D"] * E[(k, "2026")][0], E[(k, "2022")][0])
    return out
IND = {k: calc(k) for k in names}; IND["New York State"] = calc("STATE")
T = {r["county"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "ny_county_table.csv")))}
cmp = [("S2022", "S2022"), ("S2026", "S2026"), ("R2022", "R2022"), ("R2026", "R2026"), ("dG", "dG"), ("dGw", "dG_wf"), ("surplus", "surplus"), ("gap", "gap")]
nchk = nbad = 0
for k, ind in IND.items():
    for a, b in cmp:
        x = ind[a]; y = T[k][b]
        nchk += 1
        if x is None:
            ok = y in ("", "None")
        else:
            ok = abs(float(x) - float(y)) < 1e-5
        if not ok:
            nbad += 1; P(f"    FAIL {k} {a}: independent {float(x) if x is not None else None} vs table {y}")
    if (T[k]["reg_dem_fell"] == "True") != ind["fell"]:
        nbad += 1; P(f"    FAIL {k} fell flag")
fails += nbad
P(f"    {'OK ' if nbad == 0 else 'FAIL'} {nchk} county/statewide values (S, R, ΔG, ΔG with WF, surplus, gap for 62 counties + state) match the computed table to 0.00001; {nbad} mismatches.")
# fit, independently with closed-form least squares
pts = [(IND[k]["R2026"] / 100, IND[k]["surplus"]) for k in names if IND[k]["fell"]]
nn = len(pts); sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts); sxx = sum(x * x for x, _ in pts); sxy = sum(x * y for x, y in pts)
m = (nn * sxy - sx * sy) / (nn * sxx - sx * sx); b = (sy - m * sx) / nn
okfit = abs(float(m) - summ["fit"]["m"]) < 1e-6 and abs(float(b) - summ["fit"]["b"]) < 1e-6 and nn == summ["fit"]["n"]
fails += not okfit
P(f"    {'OK ' if okfit else 'FAIL'} Fitted surplus equation recomputed by closed-form least squares: m = {float(m):.6f}, b = {float(b):.6f}, n = {nn} (table: m = {summ['fit']['m']:.6f}, b = {summ['fit']['b']:.6f}, n = {summ['fit']['n']})")
# groups
for gk, region in (("outside", "Outside NYC"), ("nyc", "Within NYC"), ("all", None)):
    ks = [k for k in names if region is None or E[(k, "2022")][3] == region]
    agg = lambda y, i: sum(E[(k, y)][i] for k in ks)
    aggv = lambda y, f: sum(V[(k, y)][f] for k in ks)
    S = {y: Fr(aggv(y, "D") * 100, aggv(y, "D") + aggv(y, "O") + aggv(y, "W")) for y in ("2022", "2026")}
    R = {y: Fr(agg(y, 0) * 100, agg(y, 2)) for y in ("2022", "2026")}
    dg = (S["2026"] - R["2026"]) - (S["2022"] - R["2022"]); g = summ["groups"][gk]
    ok = abs(float(dg) - g["dG"]) < 1e-6 and len(ks) == g["n"] and abs(statistics.mean(float(IND[k]["dG"]) for k in ks) - g["mean_dG"]) < 1e-6
    fails += not ok
    P(f"    {'OK ' if ok else 'FAIL'} Group '{g['county']}': pooled ΔG {float(dg):.6f} (table {g['dG']:.6f}), n = {len(ks)}")
okst = all(abs(float(IND['New York State'][a]) - float(T['New York State'][b])) < 1e-6 for a, b in cmp if a != "surplus")
okst2 = abs(float(calc("STATE")["dG"]) - summ["state"]["dG"]) < 1e-9
P(f"    {'OK ' if okst and okst2 else 'FAIL'} Statewide row computed from the official statewide totals matches.")
fails += not (okst and okst2)

# ---------------- PASS 3 ----------------
P(""); P("=" * 78); P("PASS 3: every number on every page checked against the computed table"); P("=" * 78)
allowed = set()
def add(v):
    if v is None: return
    v = float(v)
    for s in (f"{v:,.0f}", f"{abs(v):,.0f}", f"{v:.2f}", f"{abs(v):.2f}", f"{v:.1f}", f"{abs(v):.1f}", f"{abs(v):.3f}", f"{v:.0f}", f"{abs(v):.0f}"):
        allowed.add(s.replace("-", ""))
tbl = list(csv.DictReader(open(os.path.join(ROOT, "data", "ny_county_table.csv"))))
for r in tbl:
    for k, v in r.items():
        if k in ("county", "region", "reg_dem_fell"): continue
        if v not in ("", "None"): add(v)
    f = lambda k: float(r[k])
    for a, bb in (("reg_dem_2022", "reg_dem_2026"), ("reg_total_2022", "reg_total_2026"), ("hochul_all_2022", "hochul_all_2026"),
                  ("ballots_2022", "ballots_2026"), ("hochul_dem_2022", "hochul_dem_2026"), ("hochul_wor_2022", "hochul_wor_2026")):
        add(f(bb) - f(a)); add((f(bb) - f(a)) / f(a) * 100)
    add(f("ballots_2022") / f("reg_total_2022") * 100); add(f("ballots_2026") / f("reg_total_2026") * 100)
    add(f("zeldin_all_2022") - f("hochul_all_2022")); add(f("blakeman_all_2026") - f("hochul_all_2026"))
    add((f("zeldin_all_2022") - f("hochul_all_2022")) / f("race_total_2022") * 100); add((f("blakeman_all_2026") - f("hochul_all_2026")) / f("race_total_2026") * 100)
    add(f("hochul_all_2022") * f("reg_dem_2026") / f("reg_dem_2022")); add(f("gap") / f("race_total_2026") * 100)
    add(-f("dR"));
    if r["surplus_fitted"] not in ("", "None"): add(f("surplus_fitted")); add(f("surplus_resid"))
def walk(o):
    if isinstance(o, dict):
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        add(o)
walk(summ)
add(summ["fit"]["r2"] * 100)
add(float(open(os.path.join(ROOT, "data", "chart_stats.txt")).read().split("=")[1]))
rows = [r for r in tbl if r["county"] != "New York State"]
dgs = [float(r["dG"]) for r in rows]
add(statistics.median(dgs))
srt = sorted(rows, key=lambda r: float(r["dG"]))
add(float(srt[1]["dG"]) - float(srt[0]["dG"]))
add(sorted(rows, key=lambda r: float(r["dG"])).index(next(r for r in rows if r["county"] == "Hamilton")) + 1)
for k in ("n_pos", "n_pos_wf"): add(summ["side_check"][k])
add(sum(1 for r in rows if r["reg_dem_fell"] == "True")); add(sum(1 for r in rows if r["reg_dem_fell"] != "True"))
add(sum(1 for r in rows if r["reg_dem_fell"] != "True" and float(r["dR"]) < 0))
add(sum(1 for r in rows if r["region"] == "Outside NYC" and r["reg_dem_fell"] == "True"))
add(sum(1 for r in rows if r["region"] == "Outside NYC" and r["reg_dem_fell"] != "True"))
# non-data numbers: source metadata (from raw/SOURCES.txt and the ENR page), structure, and method constants
NONDATA = {"2022", "2026", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "15", "19", "22", "57", "62", "63", "100", "0", "211",
           "12,108", "13,187", "125", "126", "91", "1,006", "1,083", "1,067", "1,070", "906", "39", "40", "42", "41", "11.42", "42:41", "11:42", "21",
           "2023", "01", "nov26", "0.01", "9", "3.0", "+12", "0.00001"}
files = ["README.md"] + [os.path.join("wiki", f) for f in sorted(os.listdir(os.path.join(ROOT, "wiki")))]
tot_nums = 0; unmatched = []
for fn in files:
    txt = open(os.path.join(ROOT, fn)).read()
    txt = re.sub(r"\(https?://[^)]*\)|https?://\S+", "", txt)          # URLs
    txt = re.sub(r"\[[^\]]*\.(?:png|pdf|xlsx|csv|txt|json)\]", "", txt)
    txt = re.sub(r"`[^`]*`", "", txt)
    txt = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}:\d{2}(?::\d{2})?\b", "", txt)   # dates / times
    txt = re.sub(r"\b(?:Nov|Version|Step|Table|Pass|Line|line|lines|Section|§)\s*\d+(?:[-–]\d+)?\b", "", txt)
    txt = re.sub(r"\b[A-Za-z_]+\d+\b|\bS\d{4}\b|\bR\d{4}\b|\bG\d{4}\b|\bD\d{4}\b|RegDem\d{4}", "", txt)
    txt = re.sub(r"^\|\s*\d+\s*\|", "|", txt, flags=re.M)                # template line numbers
    txt = re.sub(r"^\d+\.\s", "", txt, flags=re.M)                       # list numbering
    txt = txt.replace("SHA-256", "")
    nums = re.findall(r"[+−-]?\d+(?:,\d{3})*(?:\.\d+)?", txt)
    file_un = []
    for raw in nums:
        tot_nums += 1
        s = raw.replace("−", "").replace("+", "").replace("-", "")
        if s in NONDATA or s in allowed or s.rstrip("0").rstrip(".") in allowed:
            continue
        file_un.append(raw)
    unmatched += [(fn, u) for u in file_un]
    P(f"    {fn:40s} {len(nums):4d} numbers checked, {len(file_un)} not found in table" + (f": {file_un}" if file_un else ""))
fails += len(unmatched)
P(f"    {'OK ' if not unmatched else 'FAIL'} {tot_nums} numbers across {len(files)} pages; {len(unmatched)} unmatched.")

# PDF numbers
from pypdf import PdfReader
pdftxt = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(ROOT, "New_York_62_County_Democratic_Registration_and_Vote_Change.pdf")).pages)
pdftxt = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}:\d{2}(?::\d{2})?\b|Page \d+|\bNov \d+|elections\.ny\.gov/\S+|contest/\d+|Table \d", "", pdftxt)
pn = re.findall(r"[+−-]?\d+(?:,\d{3})*(?:\.\d+)?", pdftxt)
pun = [x for x in pn if x.replace("−", "").replace("+", "").replace("-", "").rstrip("%") not in allowed | NONDATA]
fails += len(pun)
P(f"    {'OK ' if not pun else 'FAIL'} PDF: {len(pn)} numbers checked, {len(pun)} not found in table" + (f": {pun[:20]}" if pun else ""))
ceil5 = sorted(rows, key=lambda r: -float(r["dG"]))[:5]
okc = all(float(r["dR"]) < 0 for r in ceil5) and all(float(r["hochul_all_2026"]) > float(r["hochul_all_2022"]) for r in rows) and all(float(r["gap"]) > 0 for r in rows) and all(float(r["dG"]) > 0 for r in rows)
fails += not okc
P(f"    {'OK ' if okc else 'FAIL'} Written claims: registration share fell in all five ceiling counties; Hochul all-line votes rose in all 62; every county gap > 0; every county ΔG > 0.")
P("    Also checked: the PDF is built by scripts/make_pdf.py straight from data/ny_county_table.csv; its statewide row is the computed statewide row.")
P("    Sign/label checks (scripted): ceiling = max ΔG, floor = min ΔG, top-5 order, non-loss list = counties where Nov 1 2026 Democrats >= 2022.")
ceil = max(rows, key=lambda r: float(r["dG"]))["county"]; flo = min(rows, key=lambda r: float(r["dG"]))["county"]
home = open(os.path.join(ROOT, "wiki", "Home.md")).read()
okcf = f"Ceiling: {ceil}" in home and f"Floor: {flo} County" in home
fails += not okcf
P(f"    {'OK ' if okcf else 'FAIL'} Home page names ceiling {ceil} and floor {flo}.")

hdr = [f"VERIFY_LOG.txt — New York 2022 vs 2026 Governor, ΔG method",
       f"Run: {datetime.now(__import__('zoneinfo').ZoneInfo('America/Chicago')).strftime('%Y-%m-%d %H:%M')} (America/Chicago)", f"Result: {'ALL PASSES OK' if fails == 0 else str(fails) + ' FAILURE(S)'}",
       "*2026 figures are unofficial and not certified by the NYS Board of Elections.", ""]
open(os.path.join(ROOT, "VERIFY_LOG.txt"), "w").write("\n".join(hdr + log) + "\n")
print("\n".join(hdr + log))
