"""Graphs for the New York wiki. Reads data/ny_county_table.csv only. Writes PNGs to the repo root.
County size = total registered voters, Nov 1, 2026 (NYS Board of Elections); no census data is used."""
import csv, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT
BLUE, ORANGE, AQUA, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c"
INK, INK2, SURF, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#e7e6e2"
STAR = "* 2026 figures are unofficial and not certified by the NYS Board of Elections (ENR page of 11/21/2026 11:42 AM; Westchester incomplete)."

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.axisbelow": True})

rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "data", "ny_county_table.csv"))) if r["county"] != "New York State"]
for r in rows:
    for k, v in list(r.items()):
        try:
            r[k] = float(v)
        except (ValueError, TypeError):
            pass
    r["name"] = "St. Lawrence" if r["county"] == "St.Lawrence" else r["county"]
    r["fell"] = r["reg_dem_fell"] == "True"
by_size = sorted(rows, key=lambda r: r["reg_total_2026"])
ceil = max(rows, key=lambda r: r["dG"]); floor = min(rows, key=lambda r: r["dG"])
top5 = sorted(rows, key=lambda r: -r["dG"])[:5]
START = next(r for r in rows if r["county"] == "Hamilton")


def foot(fig, extra=""):
    fig.text(0.01, 0.005, (extra + "\n" if extra else "") + STAR + "\nSource: NYS Board of Elections.", fontsize=7.5, color=INK2, ha="left", va="bottom")


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150)
    plt.close(fig)
    print("wrote", name)


# 1. Slope chart G2022 -> G2026
fig, ax = plt.subplots(figsize=(8, 9))
for r in rows:
    hi = r is ceil or r is floor or r is START
    ax.plot([0, 1], [r["G2022"], r["G2026"]], color=(BLUE if r is ceil else ORANGE if r is floor else AQUA if r is START else GRAY),
            lw=2.2 if hi else 1, alpha=1 if hi else 0.55, zorder=3 if hi else 2)
    if hi:
        tag = "ceiling" if r is ceil else "floor" if r is floor else "starting county"
        ax.text(1.03, r["G2026"], f'{r["name"]} ({tag}) {r["G2022"]:+.2f} → {r["G2026"]:+.2f}*', va="center", fontsize=9, color=INK)
ax.set_xticks([0, 1]); ax.set_xticklabels(["G 2022", "G 2026*"]); ax.set_xlim(-0.1, 1.9)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_ylabel("G = Hochul vote share − Democratic registration share (points)")
ax.set_title("New York: G 2022 to G 2026*, all 62 counties\nG rose in 62 of 62 counties", loc="left", fontsize=12)
foot(fig); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "NY_Slope_G2022_to_G2026_County_Slope_Chart.png")

# 2. dG by county in size order, floor/ceiling marked
fig, ax = plt.subplots(figsize=(14, 6))
x = np.arange(len(by_size))
cols = [BLUE if r is ceil else ORANGE if r is floor else AQUA if r is START else "#86b6ef" for r in by_size]
ax.bar(x, [r["dG"] for r in by_size], color=cols, width=0.8, edgecolor=SURF, linewidth=1)
ax.set_xticks(x); ax.set_xticklabels([r["name"] for r in by_size], rotation=90, fontsize=7.5)
ax.set_ylabel("ΔG* (points)")
for r, lab in ((ceil, "Ceiling"), (floor, "Floor"), (START, "Start")):
    i = by_size.index(r); ax.annotate(f'{lab}: {r["name"]} {r["dG"]:+.2f}*', (i, r["dG"]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8.5, color=INK)
ax.set_title("New York ΔG* by county, smallest to largest by registered voters (Nov 1, 2026)", loc="left", fontsize=12)
foot(fig); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "NY_deltaG_by_county_size_order_floor_NewYork_ceiling_Orange.png")

# 3. dG vs size scatter (log x)
fig, ax = plt.subplots(figsize=(9, 6))
xs = np.array([r["reg_total_2026"] for r in rows]); ys = np.array([r["dG"] for r in rows])
rr = np.corrcoef(np.log10(xs), ys)[0, 1]
ax.scatter([r["reg_total_2026"] for r in rows if r["fell"]], [r["dG"] for r in rows if r["fell"]], s=40, color=BLUE, edgecolor=SURF, lw=1.5, label="Registered Democrats fell", zorder=3)
ax.scatter([r["reg_total_2026"] for r in rows if not r["fell"]], [r["dG"] for r in rows if not r["fell"]], s=40, color=ORANGE, edgecolor=SURF, lw=1.5, marker="s", label="Registered Democrats rose (non-loss)", zorder=3)
for r in rows:
    if r in top5 or r is floor or r is START:
        off = {"Rockland": (-52, 4), "Orange": (6, 6)}.get(r["county"], (5, 3))
        ax.annotate(r["name"], (r["reg_total_2026"], r["dG"]), xytext=off, textcoords="offset points", fontsize=8, color=INK)
ax.set_xscale("log"); ax.set_xlabel("Total registered voters, Nov 1, 2026 (log scale)"); ax.set_ylabel("ΔG* (points)")
ax.legend(frameon=False, loc="upper left")
ax.set_title(f"ΔG* against county size, all 62 counties (r = {rr:.2f} with log size, n = 62)", loc="left", fontsize=12)
foot(fig, "A pattern, not a conclusion."); fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "NY_DeltaG_vs_Size_Scatter.png")
open(os.path.join(ROOT, "data", "chart_stats.txt"), "w").write(f"scatter_r_log_size_vs_dG={rr:.4f}\n")

# 4a. Stacked bars: 2022 Hochul share + 2026 gain, by size, non-loss outlined
fig, ax = plt.subplots(figsize=(14, 6))
s22 = [r["S2022"] for r in by_size]; gain = [r["dS"] for r in by_size]
ax.bar(x, s22, color=BLUE, width=0.8, label="Hochul vote share 2022 (all lines)", edgecolor=SURF, lw=1)
ax.bar(x, gain, bottom=s22, color=ORANGE, width=0.8, label="Gain to 2026*", edgecolor=[INK if not r["fell"] else SURF for r in by_size], lw=[1.4 if not r["fell"] else 1 for r in by_size])
ax.set_xticks(x); ax.set_xticklabels([r["name"] for r in by_size], rotation=90, fontsize=7.5)
ax.set_ylabel("Hochul share of governor-race votes (%)"); ax.legend(frameon=False, loc="upper left")
ax.set_title("Hochul vote share 2022 plus 2026* gain, smallest to largest county (dark outline = registered Democrats rose)", loc="left", fontsize=11.5)
foot(fig); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "NY_governor_stacked_share_by_size.png")

# 4b. 2022 share vs gain sorted by 2022 share
srt = sorted(rows, key=lambda r: r["S2022"])
fig, ax = plt.subplots(figsize=(14, 6))
ax.bar(x, [r["S2022"] for r in srt], color=BLUE, width=0.8, label="Hochul vote share 2022", edgecolor=SURF, lw=1)
ax.bar(x, [r["dS"] for r in srt], bottom=[r["S2022"] for r in srt], color=ORANGE, width=0.8, label="Gain to 2026*", edgecolor=SURF, lw=1)
ax.set_xticks(x); ax.set_xticklabels([r["name"] for r in srt], rotation=90, fontsize=7.5)
ax.set_ylabel("Hochul share (%)"); ax.legend(frameon=False, loc="upper left")
ax.set_title("All 62 counties sorted by 2022 Hochul vote share: 2022 share and 2022→2026* gain", loc="left", fontsize=12)
foot(fig); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "NY_governor_2022_share_vs_gain_bar_chart.png")

# 5. Vote-share gain above, registration-share change below
fig, ax = plt.subplots(figsize=(14, 6))
ax.bar(x, [r["dS"] for r in by_size], color=BLUE, width=0.8, label="Hochul vote-share gain* (points)", edgecolor=SURF, lw=1)
ax.bar(x, [r["dR"] for r in by_size], color=ORANGE, width=0.8, label="Democratic registration-share change (points)", edgecolor=SURF, lw=1)
ax.axhline(0, color=INK2, lw=0.8)
ax.set_xticks(x); ax.set_xticklabels([r["name"] for r in by_size], rotation=90, fontsize=7.5)
ax.set_ylabel("Points"); ax.legend(frameon=False, loc="upper left")
ax.set_title("Vote-share gain* (above the line) and Democratic registration-share change (below), smallest to largest county", loc="left", fontsize=11.5)
foot(fig, "ΔG = the blue bar minus the orange bar."); fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "NY_governor_stacked_share_with_Dem_registration_loss_by_size.png")

# 6. Ceiling counties
fig, ax = plt.subplots(figsize=(9, 5))
cs = sorted(top5, key=lambda r: r["reg_total_2026"])
y = np.arange(len(cs))
ax.barh(y - 0.2, [r["dS"] for r in cs], height=0.38, color=BLUE, label="Vote-share gain*")
ax.barh(y + 0.2, [-r["dR"] for r in cs], height=0.38, color=ORANGE, label="Registration-share loss (sign flipped)")
for i, r in enumerate(cs):
    ax.text(max(r["dS"], -r["dR"]) + 0.2, i, f'ΔG {r["dG"]:+.2f}*', va="center", fontsize=9, color=INK)
ax.set_yticks(y); ax.set_yticklabels([f'{r["name"]} ({int(r["reg_total_2026"]):,} reg.)' for r in cs])
ax.set_xlabel("Points"); ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2); ax.grid(axis="y", visible=False)
ax.set_xlim(-0.5, 14)
ax.set_title("Ceiling counties (five highest ΔG*), smallest to largest", loc="left", fontsize=12)
foot(fig); fig.tight_layout(rect=(0, 0.08, 1, 1)); save(fig, "NY_Ceiling_Counties_DeltaG_by_Size.png")

# 7. Starting county residual steps (Hamilton)
h = START
fig, ax = plt.subplots(figsize=(9, 5))
steps = [("Vote-share gain\n(S 2026* − S 2022)", h["dS"], BLUE, 0), ("+ registration-share loss\n|R 2026 − R 2022|", -h["dR"], ORANGE, h["dS"]),
         ("= ΔG*", h["dG"], AQUA, 0), ("ΔG − |ΔR|\n= surplus*", h["surplus"], BLUE, 0)]
for i, (lab, val, col, base) in enumerate(steps):
    ax.bar(i, val, bottom=base, color=col, width=0.6, edgecolor=SURF, lw=2)
    ax.text(i, base + val + 0.12, f"{val:.2f}", ha="center", fontsize=10, color=INK)
ax.set_xticks(range(4)); ax.set_xticklabels([s[0] for s in steps]); ax.set_ylabel("Points")
ax.set_ylim(0, h["dG"] + 1.2); ax.grid(axis="x", visible=False)
ax.set_title(f"Hamilton County reverse math: ΔG {h['dG']:+.2f}* = {h['dS']:.2f}-point vote-share gain* + {-h['dR']:.2f}-point registration-share loss", loc="left", fontsize=11)
foot(fig); fig.tight_layout(rect=(0, 0.06, 1, 1)); save(fig, "NY_Hamilton_residual_steps.png")

# 8. Group split: outside NYC vs NYC, county dG dot strip
fig, ax = plt.subplots(figsize=(9, 4.2))
out_ = [r for r in rows if r["region"] == "Outside NYC"]
ax.scatter([r["dG"] for r in out_], np.linspace(-0.25, 0.25, len(out_)), s=36, color=BLUE, edgecolor=SURF, lw=1.5, zorder=3)
for r in (START, ceil):
    i = out_.index(r); ax.annotate(f'{r["name"]} {r["dG"]:+.2f}', (r["dG"], np.linspace(-0.25, 0.25, len(out_))[i]), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8, color=INK)
nyc_ = sorted([r for r in rows if r["region"] == "Within NYC"], key=lambda r: r["dG"])
ys_ = np.linspace(0.75, 1.35, len(nyc_))
ax.scatter([r["dG"] for r in nyc_], ys_, s=36, color=ORANGE, edgecolor=SURF, lw=1.5, zorder=3, marker="s")
for r, yy in zip(nyc_, ys_):
    ax.annotate(f'{r["name"]} {r["dG"]:+.2f}', (r["dG"], yy), xytext=(-8, 0), textcoords="offset points", ha="right", va="center", fontsize=8, color=INK)
ax.set_yticks([0, 1.05]); ax.set_yticklabels(["57 counties outside NYC", "5 NYC counties"]); ax.set_xlabel("ΔG* (points)")
ax.set_ylim(-0.5, 1.6); ax.set_xlim(-1, 13.5); ax.grid(axis="y", visible=False)
ax.set_title("County ΔG* by group (the official REGION field in the enrollment file)", loc="left", fontsize=11.5)
foot(fig); fig.tight_layout(rect=(0, 0.12, 1, 1)); save(fig, "NY_DeltaG_by_Group_OutsideNYC_vs_NYC.png")
