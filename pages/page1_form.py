"""
Page 1 — Offer Letter Form
"""
import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from templates.role_definitions import ROLE_DEFINITIONS
from utils.mistral_helper import (
    generate_internship_responsibilities,
    generate_fulltime_responsibilities,
)


def render():
    st.title("📝 Offer Letter Form")
    st.markdown("Fill in the candidate details to generate an AI-assisted offer letter draft.")
    st.markdown("---")

    # Employment type selector
    emp_type = st.radio(
        "Employment Type",
        ["Internship", "Full-Time"],
        horizontal=True,
        key="emp_type",
    )

    st.markdown("---")

    if emp_type == "Internship":
        _internship_form()
    else:
        _fulltime_form()


# ─────────────────────────────────────────────────────────────────
def _internship_form():
    st.subheader("🎓 Internship Offer Letter Details")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("First Name *", placeholder="e.g. Anirudh", key="i_name")
        role_options = list(ROLE_DEFINITIONS.keys())
        role = st.selectbox("Role *", role_options, key="i_role")
        custom_role = st.text_input("Custom Role (overrides above)", placeholder="e.g. Data Science Intern", key="i_custom_role")
        joining_date = st.date_input("Date of Joining *", value=date.today(), key="i_joining")

    with col2:
        full_name = st.text_input("Full Name *", placeholder="e.g. Kotla Anirudh", key="i_full_name")
        duration = st.selectbox("Internship Duration *", ["1 month", "2 months", "3 months", "6 months"], index=2, key="i_duration")
        timings = st.text_input("Work Timings", value="10:30am – 7pm", key="i_timings")
        letter_date = st.date_input("Letter Date", value=date.today(), key="i_letter_date")

    short_desc = st.text_area(
        "Short Description of Internship Responsibilities *",
        placeholder="e.g. The intern will work on building AI models, data preprocessing, Python scripting, and assist with research tasks in our AI team.",
        height=120,
        key="i_short_desc",
    )

    st.markdown("---")
    col_btn1, col_btn2, _ = st.columns([1.2, 1.2, 4])

    with col_btn1:
        generate = st.button("🤖 Generate with AI", type="primary", key="i_generate")
    with col_btn2:
        use_placeholder = st.button("📄 Use Template", key="i_placeholder")

    if generate:
        if not name or not full_name or not short_desc:
            st.error("Please fill all required fields (*) before generating.")
            return
        final_role = custom_role.strip() if custom_role.strip() else role
        with st.spinner("Generating responsibilities with Mistral AI…"):
            try:
                responsibilities = generate_internship_responsibilities(
                    final_role, short_desc, duration
                )
                st.success("✅ AI content generated successfully!")
            except Exception as e:
                st.error(f"AI generation failed: {e}")
                responsibilities = f"Your internship will include training and focus primarily on learning and developing new skills related to {final_role}, working alongside your mentor, assisting in day-to-day tasks and creating positive impact in the team. Based on your performance after {duration}, your employment will be rediscussed."

        _save_internship_data(name, full_name, final_role, joining_date, duration, timings, letter_date, responsibilities, short_desc)
        st.info("➡️ Proceed to **Editor & Preview** in the sidebar.")

    if use_placeholder:
        if not name or not full_name:
            st.error("Please fill at least Name and Full Name.")
            return
        final_role = custom_role.strip() if custom_role.strip() else role
        responsibilities = (
            f"Your internship will include training and focus primarily on learning and developing "
            f"new skills and gaining a deeper understanding of {final_role}, working alongside your mentor, "
            f"assisting in day-to-day tasks and creating positive impact in the team. "
            f"Based on your performance after {duration}, your employment will be rediscussed."
        )
        _save_internship_data(name, full_name, final_role, joining_date, duration, timings, letter_date, responsibilities, short_desc)
        st.success("✅ Template draft created!")
        st.info("➡️ Proceed to **Editor & Preview** in the sidebar.")


def _save_internship_data(name, full_name, role, joining_date, duration, timings, letter_date, responsibilities, short_desc):
    joining_str = joining_date.strftime("%-d %B %Y") if hasattr(joining_date, 'strftime') else str(joining_date)
    # Format letter date with ordinal
    ld = letter_date if hasattr(letter_date, 'strftime') else datetime.strptime(str(letter_date), "%Y-%m-%d").date()
    day = ld.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    letter_date_str = ld.strftime(f"%-d{suffix} %B %Y")

    st.session_state["offer_data"] = {
        "type": "internship",
        "name": name,
        "full_name": full_name,
        "role": role,
        "joining_date": joining_str,
        "duration": duration,
        "timings": timings,
        "letter_date": letter_date_str,
        "responsibilities": responsibilities,
        "short_desc": short_desc,
    }


# ─────────────────────────────────────────────────────────────────
def _fulltime_form():
    st.subheader("💼 Full-Time Offer Letter Details")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("First Name *", placeholder="e.g. Kanan", key="f_name")
        email = st.text_input("Email *", placeholder="e.g. kanan@gmail.com", key="f_email")
        role_options = list(ROLE_DEFINITIONS.keys())
        role = st.selectbox("Role *", role_options, key="f_role")
        custom_role = st.text_input("Custom Role (overrides above)", placeholder="e.g. Senior DevOps Engineer", key="f_custom_role")
        joining_date = st.date_input("Date of Joining *", value=date.today(), key="f_joining")
        letter_date = st.date_input("Letter Date", value=date.today(), key="f_letter_date")

    with col2:
        full_name = st.text_input("Full Name *", placeholder="e.g. Kanan Goyal", key="f_full_name")
        reporting_to = st.text_input("Reporting To *", placeholder="e.g. Abdul", key="f_reporting")
        probation = st.selectbox("Probation Period (months) *", ["1", "2", "3", "6"], index=2, key="f_probation")
        monthly_salary = st.text_input("Monthly Salary (INR) *", placeholder="e.g. 30,000", key="f_monthly")
        ctc = st.text_input("Annual CTC (INR) *", placeholder="e.g. 3,60,000", key="f_ctc")

    short_desc = st.text_area(
        "Short Description of Responsibilities *",
        placeholder="e.g. The candidate will lead growth marketing initiatives including ABM campaigns, social media strategy, content creation, and performance analytics across B2B channels.",
        height=120,
        key="f_short_desc",
    )

    st.markdown("#### 📊 Compensation Table (Optional)")
    st.markdown("Upload a CSV with columns: `Component, Percentage, Per Month, Per Annum`")
    comp_file = st.file_uploader("Upload Compensation CSV", type=["csv"], key="f_comp_csv")

    comp_table_data = None
    if comp_file:
        try:
            df = pd.read_csv(comp_file)
            st.dataframe(df, use_container_width=True)
            comp_table_data = df.values.tolist()
        except Exception as e:
            st.warning(f"Could not parse compensation file: {e}")

    st.markdown("---")
    col_btn1, col_btn2, _ = st.columns([1.2, 1.2, 4])

    with col_btn1:
        generate = st.button("🤖 Generate with AI", type="primary", key="f_generate")
    with col_btn2:
        use_placeholder = st.button("📄 Use Template", key="f_placeholder")

    if generate:
        if not name or not full_name or not email or not short_desc or not monthly_salary or not ctc:
            st.error("Please fill all required (*) fields before generating.")
            return
        final_role = custom_role.strip() if custom_role.strip() else role
        with st.spinner("Generating responsibilities with Mistral AI…"):
            try:
                responsibilities = generate_fulltime_responsibilities(final_role, short_desc)
                st.success("✅ AI content generated successfully!")
            except Exception as e:
                st.error(f"AI generation failed: {e}")
                responsibilities = f"This role covers several key areas:\n\n{final_role} Responsibilities:\n• Lead and execute key initiatives aligned with business goals.\n• Collaborate with cross-functional teams to deliver results.\n• Monitor performance metrics and iterate based on data insights.\n• Contribute to the growth and development of Tericsoft's mission.\n\nBeyond the specific mentioned core areas, the role also includes the following expectations:\n• Be an active contributor to Tericsoft's culture.\n• Collaborate closely with other team members.\n• Provide support in varied areas beyond the job description, as needed."

        _save_fulltime_data(name, full_name, email, final_role, reporting_to, joining_date,
                            probation, monthly_salary, ctc, letter_date, responsibilities, comp_table_data)
        st.info("➡️ Proceed to **Editor & Preview** in the sidebar.")

    if use_placeholder:
        if not name or not full_name:
            st.error("Please fill at least Name and Full Name.")
            return
        final_role = custom_role.strip() if custom_role.strip() else role
        responsibilities = (
            f"This role covers several key areas:\n\n"
            f"{final_role} Core Responsibilities:\n"
            f"• Lead and execute key initiatives aligned with business goals.\n"
            f"• Develop strategies and workflows to support the team's objectives.\n"
            f"• Collaborate with stakeholders to identify opportunities for growth.\n"
            f"• Monitor key metrics and provide regular reporting.\n"
            f"• Drive innovation and continuous improvement in your domain.\n\n"
            f"Beyond the specific mentioned core areas, the role also includes the following expectations:\n"
            f"• Be an active contributor to Tericsoft's culture.\n"
            f"• Collaborate closely with other team members.\n"
            f"• Provide support in varied areas beyond the job description, as needed."
        )
        _save_fulltime_data(name, full_name, email, final_role, reporting_to, joining_date,
                            probation, monthly_salary, ctc, letter_date, responsibilities, comp_table_data)
        st.success("✅ Template draft created!")
        st.info("➡️ Proceed to **Editor & Preview** in the sidebar.")


def _save_fulltime_data(name, full_name, email, role, reporting_to, joining_date,
                        probation, monthly_salary, ctc, letter_date, responsibilities, comp_table_data):
    joining_str = joining_date.strftime("%-d %B %Y") if hasattr(joining_date, 'strftime') else str(joining_date)
    ld = letter_date if hasattr(letter_date, 'strftime') else datetime.strptime(str(letter_date), "%Y-%m-%d").date()
    letter_date_str = ld.strftime("%d-%m-%Y")

    st.session_state["offer_data"] = {
        "type": "fulltime",
        "name": name,
        "full_name": full_name,
        "email": email,
        "role": role,
        "reporting_to": reporting_to if reporting_to else "the Director",
        "joining_date": joining_str,
        "probation_period": probation,
        "monthly_salary": monthly_salary,
        "ctc": ctc,
        "letter_date": letter_date_str,
        "responsibilities": responsibilities,
        "comp_table_data": comp_table_data,
    }
