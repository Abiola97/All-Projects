# DataPrep — Survey Data Preparation Tool

> A free, browser-based tool that automates SPSS syntax generation and XLSForm scripting from survey questionnaires — powered by the Gemini API, with no server, no installation, and no data leaving your machine.

---

## What It Does

Survey researchers typically spend hours manually writing SPSS variable dictionaries and XLSForm scripts after a questionnaire is finalised. DataPrep eliminates that by reading your questionnaire (DOCX, PDF, or pasted text) and generating production-ready output in under 2 minutes.

| Feature | Input | Output |
|---|---|---|
| **SPSS Syntax Generator** | Questionnaire (DOCX/PDF/text) | `.sps` file — full variable dictionary, value labels, MRSETS, INPUT PROGRAM bootstrap |
| **XLSForm Generator** | Questionnaire (DOCX/PDF/text) | `.xlsx` file — survey + choices + settings sheets, KoboToolbox/SurveyCTO ready |
| **File Converter** | Excel / CSV | CSV or Excel |

---

## Key Features

### SPSS Syntax
- `INPUT PROGRAM` bootstrap — no `NEW FILE`, no `DATA LIST FREE` errors
- Nigeria geo variables: `DEM_GEO_ZONE` (F1.0), `DEM_STATE` (F2.0), `DEM_LGA` (F3.0) with all 37 states + FCT Abuja and full value labels
- Standard demographic variables: gender, age, religion, ethnicity, education, occupation
- `A1000` string fields for all open-ended responses (never `A255`)
- `MRSETS` for multiple-response questions, without `VALUE=1` warning
- `SET LOCALE='en_US'` — compatible with all SPSS versions
- Clustered themes fields (`_clustered_themes`) for open-ended coding

### XLSForm (2-pass generation)
- **Pass 1** — generates the full survey sheet: question types, variable names, labels, skip logic (`relevant`), constraints, `required=yes`
- **Pass 2** — generates the choices sheet using Pass 1 as context, eliminating truncation on long questionnaires
- Standard geo cascade hardcoded (not sent to AI): Zone → State → LGA with `choice_filter`
- All 37 Nigerian states + FCT with geopolitical zone column (integers 1–6)
- Standard demographic choice lists hardcoded: gender, age, education, religion, ethnicity
- Outputs a real `.xlsx` file (SheetJS) with separate survey, choices, and settings worksheets
- Compatible with KoboToolbox, SurveyCTO, and ODK

---

## How to Use

### Option 1 — Run locally (recommended)
1. Download `DataPrep.html`
2. Double-click to open in Chrome, Edge, or Firefox
3. No installation, no server, no internet connection required beyond the Gemini API call

### Option 2 — Deploy to Cloudflare Pages
1. Create a new Cloudflare Pages project
2. Upload `DataPrep.html` as your only file
3. Your tool is live at a public URL

### Getting a Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a free API key
3. Paste it into DataPrep and click **Save** — it is stored in your browser only

---

## Privacy & Security

- Your API key is stored in `localStorage` in your own browser — it is never sent to any server other than Google's Gemini API (`generativelanguage.googleapis.com`)
- Your questionnaire text is sent to the Gemini API for processing — do not upload documents containing personally identifiable information of survey respondents
- No data is stored, logged, or transmitted anywhere else
- The tool runs entirely client-side; there is no backend

---

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| [Mammoth.js](https://github.com/mwilliamson/mammoth.js) | 1.6.0 | Client-side DOCX text extraction |
| [SheetJS (xlsx)](https://sheetjs.com/) | 0.18.5 | Building real `.xlsx` files in-browser |
| [Gemini API](https://ai.google.dev/) | gemini-3.8-flash | Two-pass XLSForm and SPSS generation |

No frameworks, no build step, no `node_modules` — a single `.html` file.

---

## Validated On

- **Campaign survey tool** — contraception awareness study, NOI Polls 2026
  - 25 questions across 8 sections
  - 335-row XLSForm output (survey + choices + settings)
  - Full skip logic, geo cascade, agree/confidence/barrier scales, multiple-response questions
  - Uploaded to KoboToolbox without errors

---

## Limitations

- PDF extraction is basic (Tj operator parsing) — complex or scanned PDFs should be converted to DOCX first
- Gemini's free tier has rate limits; very long questionnaires (50+ questions) may occasionally require a retry
- XLSForm `relevant` expressions assume ODK/KoboToolbox syntax — test before deploying to SurveyCTO if your form uses SurveyCTO-specific functions

---

## Author

**Ajao Abiola Olanrewaju**  
Senior Research & Data Analyst, NOI Polls  
[linkedin.com/in/abiola-ajao](https://linkedin.com/in/abiola-ajao) · [github.com/Abiola97](https://github.com/Abiola97)

---

## License

MIT — free to use, modify, and distribute.
