"""New York 2022 vs 2026 Governor, ΔG method. Reads only the four raw New York files.

S  = Hochul all-line votes / all governor-race votes (every line + write-ins; blank and void excluded) x 100
R  = registered Democrats / all registered voters (active + inactive, Nov 1 reports) x 100
G  = S - R ;  dG = G2026 - G2022
surplus = dG - |R2026 - R2022|   (only where registered Democrats fell; Nebraska rule)
gap = D2026 - D2022 x (RegDem2026 / RegDem2022)
Side check: R_wf uses DEM + WOR enrollees.
"""
import csv, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "source_data")
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)


def norm(name):
    return name.replace("St. Lawrence", "St.Lawrence").strip()


def ints(row, keys):
    return {k: int(row[k]) for k in keys}


def load_enroll(path):
    out, region = {}, {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if r["REGION"] in ("Outside NYC", "Within NYC") and r["COUNTY"]:
                c = norm(r["COUNTY"])
                out[c] = ints(r, ["DEM", "REP", "CON", "WOR", "OTH", "BLANK", "TOTAL"])
                region[c] = r["REGION"]
            elif r["REGION"] == "Statewide Total":
                out["__STATE__"] = ints(r, ["DEM", "REP", "CON", "WOR", "OTH", "BLANK", "TOTAL"])
    return out, region


def load_2022(path):
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            c = norm(r["County"])
            v = ints(r, ["Hochul_DEM", "Hochul_WOR", "Zeldin_REP", "Zeldin_CON", "Scattering", "Blank", "Void", "Total_Votes"])
            out["__STATE__" if c == "Totals" else c] = v
    return out


def load_2026(path):
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            c = norm(r["County"])
            v = ints(r, ["Active_Registered_ENR", "EDs_Reporting", "EDs_Total", "Hochul_DEM", "Hochul_WOR", "Hochul_Total",
                         "Blakeman_REP", "Blakeman_CON", "Blakeman_VoteAffordable", "Blakeman_Total", "Write_in", "Blank", "Void", "Total_Votes"])
            out["__STATE__" if c == "All Counties" else c] = v
    return out


e22, region = load_enroll(os.path.join(RAW, "2022_enrollment_by_county_nov1_totals.csv"))
e26, region26 = load_enroll(os.path.join(RAW, "2026_enrollment_by_county_nov1_totals.csv"))
v22 = load_2022(os.path.join(RAW, "2022_governor_by_county_certified.csv"))
v26 = load_2026(os.path.join(RAW, "2026_governor_by_county_unofficial_ENR.csv"))

counties = sorted(k for k in e22 if k != "__STATE__")
assert len(counties) == 62, len(counties)
for d in (e26, v22, v26):
    assert sorted(k for k in d if k != "__STATE__") == counties
assert region == region26

# --- integrity checks against the official totals rows ---
checks = []
for name, d, keys in (("enroll2022", e22, ["DEM", "WOR", "TOTAL"]), ("enroll2026", e26, ["DEM", "WOR", "TOTAL"]),
                      ("votes2022", v22, ["Hochul_DEM", "Hochul_WOR", "Zeldin_REP", "Zeldin_CON", "Scattering", "Blank", "Void", "Total_Votes"]),
                      ("votes2026", v26, ["Hochul_DEM", "Hochul_WOR", "Blakeman_REP", "Blakeman_CON", "Blakeman_VoteAffordable", "Write_in", "Blank", "Void", "Total_Votes"])):
    for k in keys:
        s = sum(d[c][k] for c in counties)
        checks.append((name, k, s, d["__STATE__"][k], s == d["__STATE__"][k]))
for c in counties:
    a = v22[c]
    assert a["Hochul_DEM"] + a["Hochul_WOR"] + a["Zeldin_REP"] + a["Zeldin_CON"] + a["Scattering"] + a["Blank"] + a["Void"] == a["Total_Votes"], c
    b = v26[c]
    assert b["Hochul_DEM"] + b["Hochul_WOR"] == b["Hochul_Total"], c
    assert b["Blakeman_REP"] + b["Blakeman_CON"] + b["Blakeman_VoteAffordable"] == b["Blakeman_Total"], c
    assert b["Hochul_Total"] + b["Blakeman_Total"] + b["Write_in"] + b["Blank"] + b["Void"] == b["Total_Votes"], c


def compute(c, A22, A26, V22, V26):
    D22 = V22["Hochul_DEM"] + V22["Hochul_WOR"]
    D26 = V26["Hochul_DEM"] + V26["Hochul_WOR"]
    O22 = V22["Zeldin_REP"] + V22["Zeldin_CON"]
    O26 = V26["Blakeman_REP"] + V26["Blakeman_CON"] + V26["Blakeman_VoteAffordable"]
    T22 = D22 + O22 + V22["Scattering"]
    T26 = D26 + O26 + V26["Write_in"]
    S22, S26 = D22 / T22 * 100, D26 / T26 * 100
    R22, R26 = A22["DEM"] / A22["TOTAL"] * 100, A26["DEM"] / A26["TOTAL"] * 100
    Rw22 = (A22["DEM"] + A22["WOR"]) / A22["TOTAL"] * 100
    Rw26 = (A26["DEM"] + A26["WOR"]) / A26["TOTAL"] * 100
    G22, G26 = S22 - R22, S26 - R26
    dG = G26 - G22
    reg_fell = A26["DEM"] < A22["DEM"]
    surplus = dG - abs(R26 - R22) if reg_fell else None
    gap = D26 - D22 * (A26["DEM"] / A22["DEM"])
    dG_wf = (S26 - Rw26) - (S22 - Rw22)
    return dict(
        county=c,
        region=region.get(c, "Statewide"),
        reg_total_2022=A22["TOTAL"], reg_total_2026=A26["TOTAL"],
        reg_dem_2022=A22["DEM"], reg_dem_2026=A26["DEM"],
        reg_wor_2022=A22["WOR"], reg_wor_2026=A26["WOR"],
        hochul_dem_2022=V22["Hochul_DEM"], hochul_wor_2022=V22["Hochul_WOR"], hochul_all_2022=D22,
        zeldin_rep_2022=V22["Zeldin_REP"], zeldin_con_2022=V22["Zeldin_CON"], zeldin_all_2022=O22,
        writein_2022=V22["Scattering"], blank_2022=V22["Blank"], void_2022=V22["Void"],
        race_total_2022=T22, ballots_2022=V22["Total_Votes"],
        hochul_dem_2026=V26["Hochul_DEM"], hochul_wor_2026=V26["Hochul_WOR"], hochul_all_2026=D26,
        blakeman_rep_2026=V26["Blakeman_REP"], blakeman_con_2026=V26["Blakeman_CON"], blakeman_va_2026=V26["Blakeman_VoteAffordable"],
        blakeman_all_2026=O26, writein_2026=V26["Write_in"], blank_2026=V26["Blank"], void_2026=V26["Void"],
        race_total_2026=T26, ballots_2026=V26["Total_Votes"],
        eds_reporting_2026=V26["EDs_Reporting"], eds_total_2026=V26["EDs_Total"],
        S2022=S22, S2026=S26, dS=S26 - S22,
        R2022=R22, R2026=R26, dR=R26 - R22,
        G2022=G22, G2026=G26, dG=dG,
        reg_dem_fell=reg_fell, surplus=surplus, gap=gap,
        Rwf2022=Rw22, Rwf2026=Rw26, dG_wf=dG_wf,
        hochul_wor_share_2022=V22["Hochul_WOR"] / D22 * 100, hochul_wor_share_2026=V26["Hochul_WOR"] / D26 * 100,
    )


rows = [compute(c, e22[c], e26[c], v22[c], v26[c]) for c in counties]
state = compute("New York State", e22["__STATE__"], e26["__STATE__"], v22["__STATE__"], v26["__STATE__"])
state["region"] = "Statewide"


def pooled(name, cs):
    sub = [r for r in rows if r["county"] in cs]
    agg = lambda k: sum(r[k] for r in sub)
    A22 = dict(DEM=agg("reg_dem_2022"), WOR=agg("reg_wor_2022"), TOTAL=agg("reg_total_2022"))
    A26 = dict(DEM=agg("reg_dem_2026"), WOR=agg("reg_wor_2026"), TOTAL=agg("reg_total_2026"))
    V22 = dict(Hochul_DEM=agg("hochul_dem_2022"), Hochul_WOR=agg("hochul_wor_2022"), Zeldin_REP=agg("zeldin_rep_2022"),
               Zeldin_CON=agg("zeldin_con_2022"), Scattering=agg("writein_2022"), Blank=agg("blank_2022"), Void=agg("void_2022"), Total_Votes=agg("ballots_2022"))
    V26 = dict(Hochul_DEM=agg("hochul_dem_2026"), Hochul_WOR=agg("hochul_wor_2026"), Blakeman_REP=agg("blakeman_rep_2026"),
               Blakeman_CON=agg("blakeman_con_2026"), Blakeman_VoteAffordable=agg("blakeman_va_2026"), Write_in=agg("writein_2026"),
               Blank=agg("blank_2026"), Void=agg("void_2026"), Total_Votes=agg("ballots_2026"), EDs_Reporting=agg("eds_reporting_2026"), EDs_Total=agg("eds_total_2026"))
    p = compute(name, A22, A26, V22, V26)
    dgs = [r["dG"] for r in sub]
    p.update(n=len(sub), mean_dG=float(np.mean(dgs)), min_dG=min(dgs), max_dG=max(dgs),
             n_dG_pos=sum(d > 0 for d in dgs), sum_gap=sum(r["gap"] for r in sub),
             residual_votes=p["race_total_2026"] * p["dG"] / 100)
    return p


outside = [r["county"] for r in rows if r["region"] == "Outside NYC"]
nyc = [r["county"] for r in rows if r["region"] == "Within NYC"]
groups = {"outside": pooled("57 counties outside NYC", outside),
          "nyc": pooled("5 NYC counties", nyc),
          "all": pooled("All 62 counties", counties)}

# --- fitted New York surplus equation: surplus = m * (D/100) + b, D = 2026 Dem registration share (%) ---
fit_rows = [r for r in rows if r["reg_dem_fell"]]
x = np.array([r["R2026"] / 100 for r in fit_rows])
y = np.array([r["surplus"] for r in fit_rows])
m, b = np.polyfit(x, y, 1)
pred = m * x + b
r_corr = float(np.corrcoef(x, y)[0, 1])
fit = dict(n=len(fit_rows), m=float(m), b=float(b), r=r_corr, r2=r_corr ** 2,
           note="least squares over counties where registered Democrats fell; D = 2026 Democratic share of registration in percent")
for r in rows:
    r["surplus_fitted"] = m * r["R2026"] / 100 + b if r["reg_dem_fell"] else None
    r["surplus_resid"] = r["surplus"] - r["surplus_fitted"] if r["reg_dem_fell"] else None

# WF side check
dg = np.array([r["dG"] for r in rows]); dgw = np.array([r["dG_wf"] for r in rows])
rank = lambda a: np.argsort(np.argsort(-a))
side = dict(corr=float(np.corrcoef(dg, dgw)[0, 1]),
            spearman=float(np.corrcoef(rank(dg), rank(dgw))[0, 1]),
            n_pos=int((dg > 0).sum()), n_pos_wf=int((dgw > 0).sum()),
            max_abs_diff=float(np.max(np.abs(dg - dgw))),
            state_dG=state["dG"], state_dG_wf=state["dG_wf"],
            top5=[r["county"] for r in sorted(rows, key=lambda r: -r["dG"])[:5]],
            top5_wf=[r["county"] for r in sorted(rows, key=lambda r: -r["dG_wf"])[:5]],
            floor=min(rows, key=lambda r: r["dG"])["county"], floor_wf=min(rows, key=lambda r: r["dG_wf"])["county"],
            ceiling=max(rows, key=lambda r: r["dG"])["county"], ceiling_wf=max(rows, key=lambda r: r["dG_wf"])["county"])

# --- write outputs ---
cols = list(rows[0].keys())
with open(os.path.join(DATA, "ny_county_table.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in rows + [dict(state, surplus_fitted=None, surplus_resid=None)]:
        w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})
with open(os.path.join(DATA, "ny_summary.json"), "w") as f:
    json.dump(dict(state=state, groups=groups, fit=fit, side_check=side,
                   integrity=[dict(file=a, column=b_, county_sum=c_, official_total=d_, match=e_) for a, b_, c_, d_, e_ in checks]),
              f, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))

if __name__ == "__main__":
    print("integrity:", all(c[-1] for c in checks), [c for c in checks if not c[-1]])
    print("fit:", fit)
    print("side:", side)
    print("state: S %.2f->%.2f R %.2f->%.2f dG %.2f gap %.0f" % (state["S2022"], state["S2026"], state["R2022"], state["R2026"], state["dG"], state["gap"]))
    for k, g in groups.items():
        print(k, "dG %.2f mean %.2f range %.2f..%.2f pos %d/%d gap %.0f" % (g["dG"], g["mean_dG"], g["min_dG"], g["max_dG"], g["n_dG_pos"], g["n"], g["gap"]))
    print("\n%-13s %8s %7s %7s %7s %7s %7s %8s %s" % ("county", "reg26", "S22", "S26", "R22", "R26", "dG", "gap", "fell"))
    for r in sorted(rows, key=lambda r: -r["dG"]):
        print("%-13s %8d %7.2f %7.2f %7.2f %7.2f %+7.2f %+8.0f %s %s" % (r["county"], r["reg_total_2026"], r["S2022"], r["S2026"], r["R2022"], r["R2026"], r["dG"], r["gap"], r["reg_dem_fell"], "" if r["surplus"] is None else "%.2f" % r["surplus"]))
