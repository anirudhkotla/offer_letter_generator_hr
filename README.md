# 📄 Tericsoft HR Offer Letter Automation System

A multi-page Streamlit application to automate generation of professional offer letters for Tericsoft Technology Solutions Pvt. Ltd.

---

## ✨ Features

- **Two offer letter types**: Internship & Full-Time
- **AI-powered content generation** via Mistral AI API
- **Live preview** on official Tericsoft letterhead
- **Rich text editing** of all letter sections
- **PDF export** with letterhead overlay (print-ready A4)
- **DOCX export** for further editing in Word/Google Docs
- **Compensation table** support (CSV upload)

---

## 🚀 Setup & Run

### 1. Prerequisites
- Python 3.10 or higher
- A [Mistral AI](https://console.mistral.ai/) API key

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Mistral API key
nano .env   # or use any text editor
```

Your `.env` file should look like:
```
MISTRAL_API_KEY=your_actual_mistral_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure

```
hr_offer_system/
├── app.py                          # Main entry point & navigation
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variable template
├── .env                            # Your API keys (create this)
│
├── assets/
│   └── letterhead.pdf              # Official Tericsoft letterhead
│
├── pages/
│   ├── page1_form.py               # Page 1: Candidate form + AI generation
│   ├── page2_editor.py             # Page 2: Editor + live preview
│   └── page3_export.py             # Page 3: PDF/DOCX download
│
├── templates/
│   └── role_definitions.py         # Role definitions, static clauses, templates
│
└── utils/
    ├── mistral_helper.py           # Mistral AI API integration
    ├── pdf_generator.py            # PDF generation with letterhead overlay
    └── docx_generator.py           # DOCX generation
```

---

## 🖥️ Usage Workflow

1. **Page 1 — Form**: Select Internship or Full-Time, fill candidate details, click **Generate with AI**
2. **Page 2 — Editor**: Edit any section, use AI Refine for specific paragraphs, save changes
3. **Page 3 — Export**: Download as PDF (with letterhead) or DOCX

---

## 📊 Compensation Table (Full-Time)

Upload a CSV file with these exact column headers:
```
Component, Percentage, Per Month, Per Annum
```

Example:
```csv
Component,Percentage,Per Month,Per Annum
Basic Salary,50% of Gross,58333,700000
HRA,40% of Basic or 8k,8000,96000
Other allowance,Remaining amount,50333,604000
Total Gross Salary,,116667,1400000
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `MISTRAL_API_KEY not set` | Create `.env` file with your API key |
| Letterhead not showing | Ensure `assets/letterhead.pdf` exists |
| PDF generation error | Check that `reportlab` and `pypdf` are installed |
| `streamlit-quill` error | Ignore — app uses native Streamlit text areas |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| streamlit | Web UI framework |
| mistralai | AI content generation |
| python-dotenv | Secure API key loading |
| reportlab | PDF generation |
| pypdf | PDF manipulation & letterhead overlay |
| python-docx | DOCX generation |
| pandas | Compensation CSV parsing |
| Pillow | Image handling |
