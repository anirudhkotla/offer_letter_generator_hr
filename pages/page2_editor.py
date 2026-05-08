"""
Page 2 — Offer Letter Editor & Live Preview
Left panel  : editable form fields + AI refine
Right panel : HTML preview styled to match the Tericsoft letterhead
"""
import re
import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.mistral_helper import refine_section
from utils.pdf_generator import generate_internship_pdf, generate_fulltime_pdf

LETTERHEAD = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "assets", "letterhead.pdf"
)


# ─────────────────────────────────────────────────────────────────────────
#  Markdown → HTML helpers
# ─────────────────────────────────────────────────────────────────────────
def _md_html(text: str) -> str:
    """Convert **bold** / *italic* to HTML. Escape raw HTML entities first."""
    if not text:
        return ""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text, flags=re.DOTALL)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         text, flags=re.DOTALL)
    return text


def _resp_html(raw: str) -> str:
    """
    Render responsibilities text as HTML:
    - Lines ending with ':' (after stripping markdown) → bold sub-heading
    - Lines starting with bullet chars → <li>
    - Everything else → <p>
    """
    html = ""
    for line in raw.split("\n"):
        stripped = line.strip()
        if not stripped:
            html += "<div style='height:6px'></div>"
            continue

        # Strip surrounding ** to detect headings
        clean = re.sub(r'^\*{1,2}(.*?)\*{1,2}$', r'\1', stripped)

        if stripped.startswith(("•", "-")) or (
                stripped.startswith("*") and not stripped.startswith("**")):
            inner = re.sub(r'^[•\-\*]\s*', '', stripped)
            html += (
                f"<li style='margin:2px 0 4px 24px;line-height:1.6;'>"
                f"{_md_html(inner)}</li>"
            )
        elif clean.endswith(":"):
            html += (
                f"<p style='margin:8px 0 3px 10px;font-weight:bold;"
                f"font-family:Arial,sans-serif;font-size:10.5px;'>"
                f"{_md_html(clean)}</p>"
            )
        else:
            html += (
                f"<p style='margin:4px 0;text-align:justify;'>"
                f"{_md_html(stripped)}</p>"
            )
    return html


# ─────────────────────────────────────────────────────────────────────────
#  Letterhead chrome (mirrors the actual PDF exactly)
# ─────────────────────────────────────────────────────────────────────────
LH_HEADER = """
<div style="display:flex;justify-content:space-between;align-items:flex-start;
            padding:12px 24px 10px 18px;border-bottom:2px solid #1A3C6B;
            background:#ffffff;">
  <img src="https://tericsoft.com/wp-content/uploads/2022/05/cropped-Tericsoft_Logo-removebg.png"
       style="height:36px;" onerror="this.style.display='none'">
  <!-- Fallback text logo if image fails -->
  <div style="display:flex;align-items:center;gap:6px;">
    <span style="font-size:20px;font-weight:700;color:#1A3C6B;
                 font-family:Arial,sans-serif;letter-spacing:-0.5px;">
      &#8658;&nbsp;Tericsoft
    </span>
  </div>
  <div style="font-size:7.5px;color:#444;text-align:right;line-height:1.65;
              font-family:Arial,sans-serif;max-width:260px;">
    Tericsoft Technology Solutions Pvt. Ltd.<br>
    3rd Floor, 16 – 2 – 664/1, Yunas Plaza, Press road<br>
    New Malakpet, Hyderabad, Telangana, India – 500036<br>
    CIN: U72900TG2018PTC125275 &nbsp;|&nbsp; info@tericsoft.com
  </div>
</div>"""

LH_FOOTER = """
<div style="border-top:1px solid #1A3C6B;
            display:flex;justify-content:space-between;
            padding:6px 24px;font-size:8px;color:#555;
            font-family:Arial,sans-serif;background:#fff;margin-top:20px;">
  <span>www.tericsoft.com</span>
  <span>+91-9398093938</span>
  <span>info@tericsoft.com</span>
</div>"""

BODY_CSS = (
    "padding:20px 32px 8px 26px;"
    "font-family:Georgia,'Times New Roman',serif;"
    "font-size:10.5px;color:#1a1a1a;line-height:1.75;background:#fff;"
)


# ─────────────────────────────────────────────────────────────────────────
#  Main render
# ─────────────────────────────────────────────────────────────────────────
def render():
    st.title("✏️ Editor & Preview")

    if "offer_data" not in st.session_state:
        st.warning("⚠️ No data found. Complete **Page 1 — Offer Letter Form** first.")
        return

    data       = st.session_state["offer_data"].copy()
    offer_type = data.get("type", "internship")

    st.markdown(
        "Edit fields on the **left** → click **Save & Refresh Preview** → "
        "see live result on the **right**."
    )
    st.markdown("---")

    left, right = st.columns([1, 1], gap="large")

    # ── LEFT ──────────────────────────────────────────────────────────────
    with left:
        st.subheader("📝 Edit Content")
        if offer_type == "internship":
            data = _edit_internship(data)
        else:
            data = _edit_fulltime(data)

        st.markdown("---")
        st.markdown("#### 🤖 AI Refine a Section")
        paste  = st.text_area("Paste paragraph to refine", height=90, key="ai_paste",
                              placeholder="Paste any section here…")
        instr  = st.text_input("Instruction",
                               placeholder="e.g. Make more formal / shorten / focus on leadership",
                               key="ai_instr")
        if st.button("✨ Refine with AI", key="ai_btn"):
            if paste and instr:
                with st.spinner("Calling Mistral…"):
                    try:
                        result = refine_section(paste, instr)
                        st.success("Refined — copy this back into the editor above:")
                        st.text_area("", value=result, height=110, key="ai_result")
                    except Exception as e:
                        st.error(f"AI error: {e}")
            else:
                st.warning("Provide both text and an instruction.")

        st.markdown("")
        if st.button("💾  Save & Refresh Preview", type="primary", key="save_btn"):
            st.session_state["offer_data"] = data
            st.rerun()

    # ── RIGHT ─────────────────────────────────────────────────────────────
    with right:
        st.subheader("👁️ Live Preview")
        _show_preview(data, offer_type)


# ─────────────────────────────────────────────────────────────────────────
#  Editor panels
# ─────────────────────────────────────────────────────────────────────────
def _edit_internship(d):
    d["name"]          = st.text_input("First Name",      value=d.get("name",""),           key="i_name")
    d["full_name"]     = st.text_input("Full Name",       value=d.get("full_name",""),       key="i_full")
    d["role"]          = st.text_input("Role",            value=d.get("role",""),            key="i_role")
    d["joining_date"]  = st.text_input("Date of Joining", value=d.get("joining_date",""),    key="i_join")
    d["duration"]      = st.text_input("Duration",        value=d.get("duration","3 months"),key="i_dur")
    d["timings"]       = st.text_input("Timings",         value=d.get("timings","10:30am – 7pm"), key="i_time")
    d["letter_date"]   = st.text_input("Letter Date",     value=d.get("letter_date",""),     key="i_ldate")
    d["responsibilities"] = st.text_area(
        "Responsibilities Paragraph",
        value=d.get("responsibilities",""), height=160, key="i_resp")
    return d


def _edit_fulltime(d):
    c1, c2 = st.columns(2)
    with c1:
        d["name"]          = st.text_input("First Name",          value=d.get("name",""),          key="f_name")
        d["email"]         = st.text_input("Email",               value=d.get("email",""),         key="f_email")
        d["role"]          = st.text_input("Role",                value=d.get("role",""),          key="f_role")
        d["joining_date"]  = st.text_input("Date of Joining",     value=d.get("joining_date",""),  key="f_join")
        d["letter_date"]   = st.text_input("Letter Date",         value=d.get("letter_date",""),   key="f_ldate")
    with c2:
        d["full_name"]        = st.text_input("Full Name",            value=d.get("full_name",""),      key="f_full")
        d["reporting_to"]     = st.text_input("Reporting To",         value=d.get("reporting_to",""),   key="f_rep")
        d["probation_period"] = st.text_input("Probation (months)",   value=d.get("probation_period","3"), key="f_prob")
        d["monthly_salary"]   = st.text_input("Monthly Salary (INR)", value=d.get("monthly_salary",""),key="f_sal")
        d["ctc"]              = st.text_input("Annual CTC (INR)",     value=d.get("ctc",""),           key="f_ctc")
    d["responsibilities"] = st.text_area(
        "Responsibilities (editable)",
        value=d.get("responsibilities",""), height=260, key="f_resp")
    return d


# ─────────────────────────────────────────────────────────────────────────
#  Preview renderer
# ─────────────────────────────────────────────────────────────────────────
def _show_preview(data, offer_type):
    body = _body_internship(data) if offer_type == "internship" else _body_fulltime(data)

    html = f"""
    <div style="background:#fff;border:1px solid #ccc;border-radius:8px;
                overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.13);">
      {LH_HEADER}
      <div style="{BODY_CSS}">{body}</div>
      {LH_FOOTER}
    </div>"""

    # Scrollable container
    st.markdown(
        f'<div style="max-height:700px;overflow-y:auto;'
        f'border-radius:8px;border:1px solid #e0e0e0;">{html}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("⬇️ Quick PDF Download", key="qpdf"):
        lh = LETTERHEAD if os.path.isfile(LETTERHEAD) else None
        try:
            if offer_type == "internship":
                pdf = generate_internship_pdf(data, lh)
            else:
                pdf = generate_fulltime_pdf(data, lh, data.get("comp_table_data"))
            st.session_state["final_pdf"]  = pdf
            st.session_state["offer_data"] = data
            fname = f"offer_letter_{data.get('full_name','candidate').replace(' ','_')}.pdf"
            st.download_button("📥 Download PDF", data=pdf,
                               file_name=fname, mime="application/pdf", key="dl_q")
        except Exception as e:
            st.error(f"PDF error: {e}")
            import traceback
            st.code(traceback.format_exc())


# ─────────────────────────────────────────────────────────────────────────
#  HTML body builders
# ─────────────────────────────────────────────────────────────────────────
def _body_internship(d):
    resp = _md_html(d.get("responsibilities", "")).replace("\n", "<br>")
    name = _md_html(d.get("name","Candidate"))
    role = _md_html(d.get("role","Intern"))
    return f"""
<p><strong>{_md_html(d.get('letter_date',''))}</strong></p>
<p style="margin-top:12px;">
  <strong>Subject: <u>Internship at Tericsoft Technology</u></strong>
</p>
<p>Dear {name},</p>
<p>In reference to your application, we would like to congratulate you on your internship
for the position of <strong>{role}</strong> for {d.get('duration','3 months')}.
Your internship is scheduled to start effective from {d.get('joining_date','')}.
All of us at Tericsoft are excited that you will be joining our team.</p>
<p>{resp}</p>
<p>The in-depth details of the internship will be shared by your mentor.</p>
<p>
  <strong>Date of Joining:</strong> {d.get('joining_date','')}<br>
  <strong>Timings:</strong> {d.get('timings','10:30am – 7pm')}<br>
  <strong>Weekdays:</strong> Monday to Friday
</p>
<p>Again, congratulations and we look forward to working with you.</p>
<p style="margin-top:16px;">Yours sincerely,</p>
<p style="margin-top:40px;">
  <strong>Abdul Rahman</strong><br>Director<br>Tericsoft Technology
</p>
<hr style="margin-top:22px;border:none;border-top:1px solid #aaa;">
<p>I accept the terms of this offer with Tericsoft.</p>
<p>_____________________________________ &nbsp;&nbsp; Date – _____________________________________</p>
<p>{_md_html(d.get('full_name',''))}</p>"""


def _body_fulltime(d):
    resp   = _resp_html(d.get("responsibilities",""))
    name   = _md_html(d.get("name","Candidate"))
    role   = _md_html(d.get("role","Executive"))
    rep_to = _md_html(d.get("reporting_to","the Director"))
    prob   = d.get("probation_period","3")
    salary = _md_html(d.get("monthly_salary",""))
    ctc    = _md_html(d.get("ctc",""))
    return f"""
<p><strong>{_md_html(d.get('letter_date',''))}</strong></p>
<p style="margin:4px 0;">
  {_md_html(d.get('full_name',''))}<br>
  {_md_html(d.get('email',''))}
</p>
<p>Dear {name},</p>
<p>It gives us great pleasure to extend you an offer to join the Tericsoft Technology team!
We would like you to join in the role of <strong>{role}</strong> reporting to {rep_to}.
We were impressed with your strong ability combined with your enthusiasm to support the
development of Tericsoft's vision &amp; mission. Together, we feel that these attributes
will make you an outstanding fit as part of Tericsoft's technology team.</p>
<p>This letter contains the relevant information regarding your offer.</p>

<p><strong>1. &nbsp; Term:</strong><br>
As <strong>{role}</strong>, you will start on a {prob}-month probation period with the
intention of extending into the permanent role. Your services will be confirmed in writing
after the successful completion of your probation period. The probation period may be
extended if your performance does not meet expectations.</p>

<p><strong>2. &nbsp; Responsibilities:</strong><br>
<em>This role covers several key areas:</em></p>
{resp}

<p style="margin-top:12px;"><strong>Compensation:</strong>
We are pleased to offer you compensation including:</p>
<p><em>Salary:</em> You will receive a fixed salary of INR {salary}/- per month
(Inclusive of all taxes &amp; benefits). Your fixed CTC (Cost to Company) will be
INR {ctc}/- per annum.</p>

<p>Offer stands cancelled in case of any deviations in information/if not reported before
the date of acceptance.</p>
<p><strong>Notice Period</strong> – During probation period, the notice period stands for
30 days. Post probation, the notice period stands for 60 days. You will be on probation
for {prob} months from the date of your joining.</p>
<p><strong>Date of Joining: {d.get('joining_date','')}.</strong></p>
<p>I am confident you will have a rewarding experience with a phenomenal team.
We look forward to welcoming you to Tericsoft Technology.</p>

<p style="margin-top:16px;">Sincerely,</p>
<p style="margin-top:40px;">
  <strong>Abdul Rahman</strong><br>Director<br>Tericsoft Technology
</p>
<hr style="margin-top:22px;border:none;border-top:1px solid #aaa;">
<p>I accept this action as outlined above and confirm with the above mentioned start date.</p>
<p>_____________________________________ &nbsp;&nbsp; Date – _____________________________________</p>
<p>{_md_html(d.get('full_name',''))}</p>"""