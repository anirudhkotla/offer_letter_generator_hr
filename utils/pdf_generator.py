"""
PDF Generator — Tericsoft HR Offer Letter System

Letterhead strategy:
  - assets/letterhead_bg.png is the pre-converted letterhead image (shipped with the app)
  - A ReportLab PageTemplate draws it as background on EVERY page via onPage callback
  - No pdf2image / poppler dependency needed at runtime
  - Content flows on top through the normal platypus story

Letterhead safe zones (measured at 150 dpi on A4):
  - Header  : top ~3.4 cm  → TOP_MARGIN    = 3.8 cm
  - Footer  : bot ~2.0 cm  → BOTTOM_MARGIN = 2.2 cm
"""

import io
import os
import re

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

# ── Brand colours ──────────────────────────────────────────────────────────
BLUE  = colors.HexColor("#1A3C6B")
LIGHT = colors.HexColor("#E8EEF7")
GREY  = colors.HexColor("#666666")

# ── Page measurements ──────────────────────────────────────────────────────
W, H     = A4
LEFT_M   = 2.2 * cm
RIGHT_M  = 2.2 * cm
TOP_M    = 3.8 * cm
BOTTOM_M = 2.2 * cm

# ── Locate the bundled letterhead PNG ─────────────────────────────────────
_HERE    = os.path.dirname(os.path.abspath(__file__))          # utils/
_ASSETS  = os.path.join(_HERE, "..", "assets")                  # assets/
_LH_PNG  = os.path.join(_ASSETS, "letterhead_bg.png")          # preferred
_LH_PDF  = os.path.join(_ASSETS, "letterhead.pdf")             # fallback source


def _ensure_lh_png() -> str | None:
    """
    Return the path to the letterhead background PNG.
    1. Use pre-bundled assets/letterhead_bg.png if it exists.
    2. Try to convert assets/letterhead.pdf via pdf2image (needs poppler).
    3. Return None if neither works (PDF generated without letterhead).
    """
    if os.path.isfile(_LH_PNG):
        return _LH_PNG

    if os.path.isfile(_LH_PDF):
        try:
            from pdf2image import convert_from_path
            import tempfile
            imgs = convert_from_path(_LH_PDF, dpi=150)
            tmp  = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            imgs[0].save(tmp.name, "PNG")
            return tmp.name
        except Exception:
            pass
    return None


def _bg_callback(lh_png: str):
    """Return a ReportLab onPage function that draws the letterhead on every page."""
    def draw(canvas, doc):
        canvas.saveState()
        canvas.drawImage(lh_png, 0, 0, width=W, height=H, preserveAspectRatio=False)
        canvas.restoreState()
    return draw


def _build_doc(buf: io.BytesIO, lh_png: str | None) -> BaseDocTemplate:
    """Create a BaseDocTemplate with optional letterhead background on every page."""
    doc   = BaseDocTemplate(
        buf, pagesize=A4,
        leftMargin=LEFT_M, rightMargin=RIGHT_M,
        topMargin=TOP_M,   bottomMargin=BOTTOM_M,
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin,
                  doc.width, doc.height, id="main")
    on_page = _bg_callback(lh_png) if lh_png else (lambda c, d: None)
    doc.addPageTemplates([PageTemplate(id="lh", frames=[frame], onPage=on_page)])
    return doc


# ── Text helpers ───────────────────────────────────────────────────────────
def _xml(text: str) -> str:
    """Escape & then convert **bold** / *italic* markdown to ReportLab XML."""
    if not text:
        return ""
    text = text.replace("&", "&amp;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    text = re.sub(r'\*(.+?)\*',     r'<i>\1</i>', text, flags=re.DOTALL)
    return text


# ── Paragraph styles ───────────────────────────────────────────────────────
def _styles() -> dict:
    b = getSampleStyleSheet()
    def S(name, **kw):
        return ParagraphStyle(name, parent=b["Normal"], **kw)
    return {
        "date"    : S("date",     fontName="Helvetica-Bold",    fontSize=10, spaceAfter=8),
        "recip"   : S("recip",    fontName="Helvetica",         fontSize=10, spaceAfter=3, leading=15),
        "subj"    : S("subj",     fontName="Helvetica-Bold",    fontSize=10, spaceAfter=10),
        "greet"   : S("greet",    fontName="Helvetica",         fontSize=10, spaceAfter=8),
        "body"    : S("body",     fontName="Helvetica",         fontSize=10, leading=16,
                                  spaceAfter=8, alignment=TA_JUSTIFY),
        "subhead" : S("subhead",  fontName="Helvetica-Bold",    fontSize=10,
                                  spaceAfter=4, spaceBefore=6, leftIndent=10),
        "bullet"  : S("bullet",   fontName="Helvetica",         fontSize=10, leading=15,
                                  spaceAfter=3, leftIndent=22),
        "clause"  : S("clause",   fontName="Helvetica-Bold",    fontSize=10,
                                  spaceAfter=4, spaceBefore=10),
        "italic"  : S("italic",   fontName="Helvetica-Oblique", fontSize=10,
                                  spaceAfter=6, leading=15),
        "closing" : S("closing",  fontName="Helvetica",         fontSize=10, spaceAfter=4),
        "signame" : S("signame",  fontName="Helvetica-Bold",    fontSize=10, spaceAfter=2),
        "sigtitle": S("sigtitle", fontName="Helvetica",         fontSize=10, spaceAfter=2),
        "accept"  : S("accept",   fontName="Helvetica",         fontSize=10,
                                  spaceAfter=6, leading=15),
        "ctitle"  : S("ctitle",   fontName="Helvetica-Bold",    fontSize=13,
                                  alignment=TA_CENTER, spaceAfter=14, textColor=BLUE),
    }


# ── Responsibilities renderer ──────────────────────────────────────────────
def _add_resp(story: list, raw: str, S: dict):
    """Parse AI responsibilities text → sub-headings + bullets."""
    for line in raw.split("\n"):
        stripped = line.strip()
        if not stripped:
            story.append(Spacer(1, 3))
            continue
        # Strip surrounding ** to detect heading
        clean = re.sub(r'^\*{1,2}(.*?)\*{1,2}$', r'\1', stripped).strip()

        if stripped.startswith(("•", "-")) or (
                stripped.startswith("*") and not stripped.startswith("**")):
            inner = re.sub(r'^[•\-\*]\s*', '', stripped)
            story.append(Paragraph(f"&#8226;&nbsp;&nbsp;{_xml(inner)}", S["bullet"]))
        elif clean.endswith(":"):
            story.append(Paragraph(f"<b>{_xml(clean)}</b>", S["subhead"]))
        else:
            story.append(Paragraph(_xml(stripped), S["body"]))


# ── Compensation table ─────────────────────────────────────────────────────
def _comp_table(story: list, data: list):
    headers = ["Component", "Percentage", "Per Month (INR)", "Per Annum (INR)"]
    rows = [headers] + [
        [str(c) if c not in (None, "") else "–" for c in row]
        for row in data
    ]
    tbl = Table(rows, colWidths=[5.5*cm, 3.5*cm, 4.0*cm, 4.0*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),  (-1,0),  BLUE),
        ("TEXTCOLOR",      (0,0),  (-1,0),  colors.white),
        ("FONTNAME",       (0,0),  (-1,0),  "Helvetica-Bold"),
        ("FONTNAME",       (0,1),  (-1,-1), "Helvetica"),
        ("FONTSIZE",       (0,0),  (-1,-1), 9),
        ("ALIGN",          (0,0),  (-1,-1), "CENTER"),
        ("ALIGN",          (0,1),  (0,-1),  "LEFT"),
        ("GRID",           (0,0),  (-1,-1), 0.5, GREY),
        ("ROWBACKGROUNDS", (0,1),  (-1,-1), [colors.white, LIGHT]),
        ("TOPPADDING",     (0,0),  (-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),  (-1,-1), 5),
    ]))
    story.append(tbl)


# ── Shared blocks ──────────────────────────────────────────────────────────
def _signature(story: list, S: dict, closing: str = "Sincerely"):
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"{closing},", S["closing"]))
    story.append(Spacer(1, 36))
    story.append(Paragraph("Abdul Rahman",         S["signame"]))
    story.append(Paragraph("Director",             S["sigtitle"]))
    story.append(Paragraph("Tericsoft Technology", S["sigtitle"]))


def _acceptance(story: list, S: dict, full_name: str, text: str):
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GREY))
    story.append(Spacer(1, 10))
    story.append(Paragraph(text, S["body"]))
    story.append(Spacer(1, 26))
    # Single-line signature + date using a two-column table (prevents wrapping)
    sig_table = Table(
        [["_" * 38, "Date – " + "_" * 28]],
        colWidths=[9.5*cm, 7.5*cm],
    )
    sig_table.setStyle(TableStyle([
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",    (0,0), (-1,-1), 10),
        ("TOPPADDING",  (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph(_xml(full_name), S["accept"]))


# ═══════════════════════════════════════════════════════════════════════════
#  INTERNSHIP PDF
# ═══════════════════════════════════════════════════════════════════════════
def generate_internship_pdf(data: dict, letterhead_path: str | None = None) -> bytes:
    lh_png = _ensure_lh_png()
    buf    = io.BytesIO()
    doc    = _build_doc(buf, lh_png)
    S      = _styles()
    story  = []

    story.append(Paragraph(f"<b>{_xml(data.get('letter_date',''))}</b>", S["date"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Subject: <u>Internship at Tericsoft Technology</u></b>", S["subj"]))
    story.append(Paragraph(
        f"Dear {_xml(data.get('name','Candidate'))},", S["greet"]))

    role    = _xml(data.get("role",         "Intern"))
    dur     = _xml(data.get("duration",     "3 months"))
    joining = _xml(data.get("joining_date", ""))
    timings = _xml(data.get("timings",      "10:30am – 7pm"))

    story.append(Paragraph(
        f"In reference to your application, we would like to congratulate you on your "
        f"internship for the position of <b>{role}</b> for {dur}. Your internship is "
        f"scheduled to start effective from {joining}. All of us at Tericsoft are "
        f"excited that you will be joining our team.", S["body"]))

    resp = data.get("responsibilities", "").strip()
    if resp:
        story.append(Paragraph(_xml(resp), S["body"]))

    story.append(Paragraph(
        "The in-depth details of the internship will be shared by your mentor.", S["body"]))
    story.append(Paragraph(f"<b>Date of Joining:</b> {joining}", S["body"]))
    story.append(Paragraph(f"<b>Timings:</b> {timings}", S["body"]))
    story.append(Paragraph("<b>Weekdays:</b> Monday to Friday", S["body"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Again, congratulations and we look forward to working with you.", S["body"]))

    _signature(story, S, "Yours sincerely")
    _acceptance(story, S,
        full_name=data.get("full_name", ""),
        text="I accept the terms of this offer with Tericsoft.")

    doc.build(story)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════
#  FULL-TIME PDF
# ═══════════════════════════════════════════════════════════════════════════
def generate_fulltime_pdf(data: dict,
                          letterhead_path: str | None = None,
                          comp_table_data: list | None = None) -> bytes:
    lh_png = _ensure_lh_png()
    buf    = io.BytesIO()
    doc    = _build_doc(buf, lh_png)
    S      = _styles()
    story  = []

    # Header
    story.append(Paragraph(f"<b>{_xml(data.get('letter_date',''))}</b>", S["date"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(_xml(data.get("full_name", "")), S["recip"]))
    story.append(Paragraph(_xml(data.get("email",      "")), S["recip"]))
    story.append(Spacer(1, 6))

    name    = _xml(data.get("name",             "Candidate"))
    role    = _xml(data.get("role",             "Executive"))
    rep     = _xml(data.get("reporting_to",     "the Director"))
    prob    = _xml(data.get("probation_period", "3"))
    joining = _xml(data.get("joining_date",     ""))
    sal     = _xml(data.get("monthly_salary",   ""))
    ctc     = _xml(data.get("ctc",              ""))

    story.append(Paragraph(f"Dear {name},", S["greet"]))
    story.append(Paragraph(
        f"It gives us great pleasure to extend you an offer to join the Tericsoft "
        f"Technology team! We would like you to join in the role of <b>{role}</b> "
        f"reporting to {rep}. We were impressed with your strong ability combined "
        f"with your enthusiasm to support the development of Tericsoft&apos;s vision "
        f"&amp; mission. Together, we feel that these attributes will make you an "
        f"outstanding fit as part of Tericsoft&apos;s technology team.", S["body"]))
    story.append(Paragraph(
        "This letter contains the relevant information regarding your offer.", S["body"]))

    # 1. Term
    story.append(Paragraph("<b>1. &nbsp;&nbsp; Term:</b>", S["clause"]))
    story.append(Paragraph(
        f"As <b>{role}</b>, you will start on a {prob}-month probation period with "
        f"the intention of extending into the permanent role. Your services will be "
        f"confirmed in writing after the successful completion of your probation period. "
        f"The probation period may be extended if your performance does not meet "
        f"expectations.", S["body"]))

    # 2. Responsibilities
    story.append(Paragraph("<b>2. &nbsp;&nbsp; Responsibilities:</b>", S["clause"]))
    story.append(Paragraph("<i>This role covers several key areas:</i>", S["italic"]))
    _add_resp(story, data.get("responsibilities", ""), S)

    # Compensation
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>Compensation:</b> We are pleased to offer you compensation including:",
        S["clause"]))
    story.append(Paragraph(
        f"<i>Salary:</i> You will receive a fixed salary of INR {sal}/- per month "
        f"(Inclusive of all taxes &amp; benefits). Your fixed CTC (Cost to Company) "
        f"will be INR {ctc}/- per annum.", S["body"]))

    # Closing
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "Offer stands cancelled in case of any deviations in information/if not "
        "reported before the date of acceptance.", S["body"]))
    story.append(Paragraph(
        "Please reply with your confirmation of acceptance of offer. You will have "
        "to submit certain documents as a part of the onboarding process on the "
        "joining date.", S["body"]))
    story.append(Paragraph(
        f"<b>Notice Period</b> – During probation period, the notice period stands "
        f"for 30 days. Post probation, the notice period stands for 60 days. You "
        f"will be on probation for {prob} months from the date of your joining.",
        S["body"]))
    story.append(Paragraph(f"<b>Date of Joining: {joining}.</b>", S["body"]))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "I am confident you will have a rewarding experience with a phenomenal team. "
        "We look forward to welcoming you to Tericsoft Technology.", S["body"]))

    _signature(story, S, "Sincerely")
    _acceptance(story, S,
        full_name=data.get("full_name", ""),
        text="I accept this action as outlined above and confirm with the above "
             "mentioned start date.")

    if comp_table_data:
        story.append(PageBreak())
        story.append(Paragraph("COMPENSATION LETTER", S["ctitle"]))
        _comp_table(story, comp_table_data)

    doc.build(story)
    return buf.getvalue()