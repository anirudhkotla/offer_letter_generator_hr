"""
HR Offer Letter Automation System — Tericsoft Technology
Entry point: runs the Streamlit multi-page app.
"""
import streamlit as st

st.set_page_config(
    page_title="Tericsoft HR Portal",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A3C6B 0%, #0f2444 100%);
}
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] .stRadio label { color: #fff !important; }

/* Main background */
.main { background: #F5F7FA; }

/* Card-style containers */
.block-container { padding-top: 1.5rem; }

/* Buttons */
.stButton > button {
    background: #1A3C6B;
    color: white;
    border-radius: 6px;
    border: none;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
}
.stButton > button:hover { background: #2a5298; }

/* Section headers */
h1, h2, h3 { color: #1A3C6B !important; }

/* Input labels */
label { font-weight: 600 !important; color: #333 !important; }

/* Success / Info boxes */
.stSuccess, .stInfo { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Navigation ───────────────────────────────────────────────────────────────
st.sidebar.markdown("## 📄 Tericsoft HR Portal")
st.sidebar.markdown("---")

pages = {
    "1️⃣  Offer Letter Form": "form",
    "2️⃣  Editor & Preview": "editor",
    "3️⃣  Download & Export": "export",
}

selection = st.sidebar.radio("Navigate", list(pages.keys()), key="nav")
page_key = pages[selection]

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small style='color:#aaa'>Tericsoft Technology Solutions Pvt. Ltd.<br>"
    "CIN: U72900TG2018PTC125275</small>",
    unsafe_allow_html=True,
)

# ── Route to pages ───────────────────────────────────────────────────────────
if page_key == "form":
    from pages.page1_form import render
    render()
elif page_key == "editor":
    from pages.page2_editor import render
    render()
elif page_key == "export":
    from pages.page3_export import render
    render()
