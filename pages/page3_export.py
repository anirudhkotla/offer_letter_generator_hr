"""
Page 3 — Download & Export
"""
import streamlit as st
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.pdf_generator import generate_internship_pdf, generate_fulltime_pdf
from utils.docx_generator import generate_internship_docx, generate_fulltime_docx

LETTERHEAD = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "letterhead.pdf")


def render():
    st.title("📥 Download & Export")

    if "offer_data" not in st.session_state:
        st.warning("⚠️ No offer letter data found. Please complete **Page 1** and **Page 2** first.")
        return

    data = st.session_state["offer_data"]
    offer_type = data.get("type", "internship")
    candidate_name = data.get("full_name", "Candidate").replace(" ", "_")

    st.markdown("Your offer letter is ready to export. Choose your preferred format below.")
    st.markdown("---")

    # ── Summary card ──────────────────────────────────────────────────────────
    st.markdown("#### 📋 Offer Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Candidate", data.get("full_name", "—"))
        st.metric("Type", "Internship" if offer_type == "internship" else "Full-Time")
    with col2:
        st.metric("Role", data.get("role", "—"))
        st.metric("Date of Joining", data.get("joining_date", "—"))
    with col3:
        if offer_type == "fulltime":
            st.metric("Monthly Salary", f"INR {data.get('monthly_salary', '—')}")
            st.metric("Annual CTC", f"INR {data.get('ctc', '—')}")
        else:
            st.metric("Duration", data.get("duration", "—"))
            st.metric("Timings", data.get("timings", "—"))

    st.markdown("---")

    # ── Export options ─────────────────────────────────────────────────────────
    st.markdown("#### 🖨️ Export Options")

    lh_path = LETTERHEAD if os.path.exists(LETTERHEAD) else None
    lh_status = "✅ Letterhead PDF found" if lh_path else "⚠️ Letterhead not found — PDF will be generated without letterhead"
    st.info(lh_status)

    col_pdf, col_docx = st.columns(2)

    # PDF export
    with col_pdf:
        st.markdown("##### 📄 PDF Export")
        st.markdown("Generates a print-ready PDF with the official Tericsoft letterhead.")

        if st.button("🔄 Generate PDF", type="primary", key="gen_pdf"):
            with st.spinner("Generating PDF…"):
                try:
                    if offer_type == "internship":
                        pdf_bytes = generate_internship_pdf(data, lh_path)
                    else:
                        pdf_bytes = generate_fulltime_pdf(
                            data, lh_path, data.get("comp_table_data")
                        )
                    st.session_state["final_pdf"] = pdf_bytes
                    st.success("✅ PDF generated successfully!")
                except Exception as e:
                    st.error(f"PDF generation failed: {e}")
                    import traceback
                    st.code(traceback.format_exc())

        if "final_pdf" in st.session_state:
            st.download_button(
                label="⬇️ Download PDF",
                data=st.session_state["final_pdf"],
                file_name=f"offer_letter_{candidate_name}.pdf",
                mime="application/pdf",
                key="dld_pdf",
            )
            # Show page count info
            try:
                from pypdf import PdfReader
                import io
                reader = PdfReader(io.BytesIO(st.session_state["final_pdf"]))
                st.caption(f"📑 {len(reader.pages)} page(s) | Print-ready A4 format")
            except Exception:
                pass

    # DOCX export
    with col_docx:
        st.markdown("##### 📝 DOCX Export")
        st.markdown("Generates an editable Word document of the offer letter.")

        if st.button("🔄 Generate DOCX", key="gen_docx"):
            with st.spinner("Generating DOCX…"):
                try:
                    if offer_type == "internship":
                        docx_bytes = generate_internship_docx(data)
                    else:
                        docx_bytes = generate_fulltime_docx(data, data.get("comp_table_data"))
                    st.session_state["final_docx"] = docx_bytes
                    st.success("✅ DOCX generated successfully!")
                except Exception as e:
                    st.error(f"DOCX generation failed: {e}")

        if "final_docx" in st.session_state:
            st.download_button(
                label="⬇️ Download DOCX",
                data=st.session_state["final_docx"],
                file_name=f"offer_letter_{candidate_name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                key="dld_docx",
            )
            st.caption("📝 Editable in Microsoft Word or Google Docs")

    st.markdown("---")

    # ── New offer letter button ──────────────────────────────────────────────
    st.markdown("#### 🔁 Create Another Offer Letter")
    if st.button("➕ Start New Offer Letter", key="new_offer"):
        for key in ["offer_data", "final_pdf", "final_docx"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state["nav"] = "1️⃣  Offer Letter Form"
        st.success("Session cleared. Navigate to Page 1 to start fresh.")
        st.rerun()
