"""62-county PDF. Reads data/ny_county_table.csv only."""
import csv, os
from reportlab.lib.pagesizes import landscape, legal
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "New_York_62_County_Democratic_Registration_and_Vote_Change.pdf")
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "data", "ny_county_table.csv")))]
state = next(r for r in rows if r["county"] == "New York State")
rows = [r for r in rows if r["county"] != "New York State"]
I = lambda r, k: int(float(r[k]))
F = lambda r, k: float(r[k])
rows.sort(key=lambda r: -F(r, "R2026"))
name = lambda r: "St. Lawrence" if r["county"] == "St.Lawrence" else r["county"]
n = lambda v: f"{v:,}"
sg = lambda v: f"{v:+,}"
pc = lambda a, b: f"{(b - a) / a * 100:+.1f}%"

ss = getSampleStyleSheet()
H = ParagraphStyle("h", parent=ss["Title"], fontSize=13, leading=16, alignment=0, spaceAfter=4)
P = ParagraphStyle("p", parent=ss["Normal"], fontSize=7.6, leading=9.6)
HDR = ParagraphStyle("hdr", parent=ss["Normal"], fontSize=6.6, leading=7.8, alignment=1, textColor=colors.white, fontName="Helvetica-Bold")
NAVY = colors.HexColor("#1c3f6e"); ROSE = colors.HexColor("#fbe3d6"); STRIPE = colors.HexColor("#f2f5f9")

regup = [r for r in rows if I(r, "reg_dem_2026") >= I(r, "reg_dem_2022")]
votesdown = [r for r in rows if I(r, "hochul_all_2026") < I(r, "hochul_all_2022")]

notes = [
    Paragraph("New York 62 Counties — Democratic Registration, Hochul Governor Votes (every line) and Governor-Race Ballots, 2022 vs 2026*", H),
    Paragraph("Sorted by 2026 Democratic share of registration (registered Democrats ÷ all registered voters, active + inactive, Nov 1, 2026), highest first. "
              f"{name(rows[0])} leads by share; Kings leads by raw Democratic registration.", P),
    Paragraph("<b>*2026 figures are unofficial and not certified by the NYS Board of Elections.</b> They come from the Board's Election Night Reporting page "
              "(timestamp 11/21/2026 11:42:41 AM, 12,108 of 13,187 election districts reporting). The Board's own notice says the results do not include a "
              "significant number of unscanned emergency Election Day ballots from Westchester County. Not every county was at full reporting on that page: "
              "Broome 125/126, Chautauqua 0/91, Nassau 1,006/1,083, Suffolk 1,067/1,070, Westchester 0/906, Wyoming 39/40.", P),
    Paragraph("Sources: NYS Board of Elections enrollment by county as of Nov 1, 2022 and Nov 1, 2026 (elections.ny.gov/enrollment-county); 2022 certified Governor results "
              "(results.elections.ny.gov/contest/1); 2026 unofficial results (nyenr.elections.ny.gov). Fusion voting: Hochul = Democratic + Working Families lines. "
              "Zeldin (2022) = Republican + Conservative. Blakeman (2026) = Republican + Conservative + Vote Affordable (the Board's own Blakeman total includes all three). "
              "Ballots = all votes recorded in the governor race, including blank and void. Votes are votes for the candidate, not a count of registered Democrats who voted. "
              "These numbers measure a pattern; they make no claim about intent, fraud or cause.", P),
    Paragraph(f"Shaded rows: registered Democrats did not fall ({', '.join(name(r) for r in regup)}). "
              + (f"Hochul votes fell: {', '.join(name(r) for r in votesdown)}." if votesdown else "Hochul all-line votes rose in all 62 counties."), P),
    Spacer(1, 5),
]

def table(header, body, widths, shade):
    t = Table([[Paragraph(h, HDR) for h in header]] + body, colWidths=widths, repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("FONT", (0, 1), (-1, -1), "Helvetica", 6.9), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c8ccd2")),
          ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6), ("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 6.9)]
    for i, r in enumerate(shade, start=1):
        if r == "total":
            st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#dfe6ef")))
        elif r:
            st.append(("BACKGROUND", (0, i), (-1, i), ROSE))
        elif i % 2 == 0:
            st.append(("BACKGROUND", (0, i), (-1, i), STRIPE))
    t.setStyle(TableStyle(st))
    return t

def body1(r):
    a, b = I(r, "reg_dem_2022"), I(r, "reg_dem_2026")
    v1, v2 = I(r, "hochul_all_2022"), I(r, "hochul_all_2026")
    t1, t2 = I(r, "ballots_2022"), I(r, "ballots_2026")
    return [name(r), f"{F(r, 'R2026'):.1f}%", n(a), n(b), sg(b - a), pc(a, b),
            n(I(r, "hochul_dem_2022")), n(I(r, "hochul_wor_2022")), n(v1),
            n(I(r, "hochul_dem_2026")), n(I(r, "hochul_wor_2026")), n(v2), sg(v2 - v1), pc(v1, v2),
            n(t1), n(t2), sg(t2 - t1), pc(t1, t2)]

h1 = ["County", "Dem Reg Share 2026", "Dem Reg 2022 (Nov 1)", "Dem Reg 2026 (Nov 1)", "Reg Change #", "Reg Change %",
      "Hochul DEM 2022", "Hochul WOR 2022", "Hochul All Lines 2022", "Hochul DEM 2026*", "Hochul WOR 2026*", "Hochul All Lines 2026*",
      "Vote Change #*", "Vote Change % (on 2022 base)*", "Ballots 2022", "Ballots 2026*", "Ballot Change #*", "Ballot Change %*"]
w1 = [0.95 * inch] + [0.66 * inch] * 17
b1 = [body1(r) for r in rows]; b1.append(["Statewide"] + body1(state)[1:])
s1 = [r in regup for r in rows] + ["total"]

def body2(r):
    z, bk = I(r, "zeldin_all_2022"), I(r, "blakeman_all_2026")
    return [name(r), n(I(r, "zeldin_rep_2022")), n(I(r, "zeldin_con_2022")), n(z), n(I(r, "writein_2022")), n(I(r, "blank_2022")), n(I(r, "void_2022")),
            n(I(r, "blakeman_rep_2026")), n(I(r, "blakeman_con_2026")), n(I(r, "blakeman_va_2026")), n(bk),
            n(I(r, "writein_2026")), n(I(r, "blank_2026")), n(I(r, "void_2026")),
            n(I(r, "reg_total_2022")), n(I(r, "reg_total_2026")), sg(I(r, "reg_total_2026") - I(r, "reg_total_2022"))]

h2 = ["County", "Zeldin REP 2022", "Zeldin CON 2022", "Zeldin All Lines 2022", "Write-in 2022", "Blank 2022", "Void 2022",
      "Blakeman REP 2026*", "Blakeman CON 2026*", "Blakeman Vote Afford. 2026*", "Blakeman All Lines 2026*", "Write-in 2026*", "Blank 2026*", "Void 2026*",
      "All Registered 2022 (Nov 1)", "All Registered 2026 (Nov 1)", "All Registered Change #"]
w2 = [0.95 * inch] + [0.70 * inch] * 16
b2 = [body2(r) for r in rows]; b2.append(["Statewide"] + body2(state)[1:])

def onpage(c, d):
    c.saveState(); c.setFont("Helvetica", 7); c.setFillColor(colors.HexColor("#52514e"))
    c.drawString(0.4 * inch, 0.3 * inch, "*2026 figures unofficial, not certified by the NYS Board of Elections")
    c.drawRightString(landscape(legal)[0] - 0.4 * inch, 0.3 * inch, f"Page {d.page}")
    c.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=landscape(legal), leftMargin=0.4 * inch, rightMargin=0.4 * inch, topMargin=0.4 * inch, bottomMargin=0.5 * inch,
                        title="New York 62 County Democratic Registration and Vote Change, 2022 vs 2026*", author="New York Election Analysis")
story = notes + [Paragraph("<b>Table 1.</b> Democratic registration, Hochul votes by line and combined, and governor-race ballots", P), Spacer(1, 3), table(h1, b1, w1, s1),
                 PageBreak(), Paragraph("<b>Table 2.</b> Opponent votes by line and combined, write-ins, blanks, voids and all registered voters (same county order)", P),
                 Spacer(1, 3), table(h2, b2, w2, s1)]
doc.build(story, onFirstPage=onpage, onLaterPages=onpage)
print("wrote", OUT, "regup", len(regup), "votesdown", len(votesdown))
