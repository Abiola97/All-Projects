# CATI Contact Intelligence System

> **Browser-based call-prioritisation tool for CATI survey teams.**  
> Scores respondent phone numbers by completion propensity, enforces NDPA 2023-compliant anonymisation, and runs entirely in the browser — no server, no database, no IT dependency.

---

## Overview

Nigerian survey organisations running Computer-Assisted Telephone Interviewing (CATI) panels accumulate large call-outcome histories. Without tooling, interviewers manually scan spreadsheets to decide who to call next, leading to wasted attempts on unreachable numbers and missed callbacks on high-propensity contacts.

This system solves that by:

- Loading your call-outcome data directly from a **Google Sheet** (published as CSV)
- **Scoring every contact** with a Bayesian propensity model calibrated on your organisation's own completion rate
- Giving interviewers a **one-click phone lookup** with a priority tier, scorecard, and full call history
- **Never storing real phone numbers** — all identifiers are SHA-256 hashed in-browser before any use

---

## Features

| Feature | Detail |
|---|---|
| 📊 **Dashboard** | Outcome distribution chart, total contacts loaded, recent activity |
| 🔍 **Phone Lookup** | Type any number → instant priority score, scorecard (attempts, success %, fail %), call history with Date, Outcome, Project, Interviewer, State, LGA |
| 📋 **Batch Score** | Upload a list of numbers and export prioritised call sheet |
| 📁 **Data Table** | Browse and filter all loaded contacts |
| ⚙️ **Settings** | Paste your Google Sheets CSV URL, configure column mappings |
| 🔒 **Privacy-first** | SHA-256 hashing via Web Crypto API; raw phones never leave the device |

---

## Priority Tiers

| Tier | Score | Meaning |
|---|---|---|
| 🟢 PRIORITY CALL | ≥ 65 | High completion history, call immediately |
| 🟢 RECOMMENDED | ≥ 45 | Above-average propensity |
| 🟡 NORMAL PRIORITY | ≥ 30 | Average likelihood |
| 🟡 LOW PRIORITY | ≥ 15 | Below-average, attempt if capacity allows |
| 🔴 SKIP / RETRY LATER | < 15 | Poor history, deprioritise |
| 🔵 SCHEDULED CALLBACK | — | Has a rescheduled entry, call at agreed time |
| 🔵 NEW NUMBER | — | No prior call history |

Scores blend individual call history with the organisation's overall completion rate using Bayesian smoothing (prior weight = 5, default org rate = 13.8%).

---

## Data Privacy & NDPA 2023 Compliance

Publishing a spreadsheet containing real respondent phone numbers to Google Sheets constitutes a cross-border personal data transfer under Nigeria's **National Data Protection Act 2023 (NDPA)**. This system provides a compliant path:

1. **Anonymise before upload** using the included Python pipeline
2. The Sheet contains only 64-character SHA-256 `Contact_Code` values — no phone numbers
3. The app hashes any number an interviewer types in-browser using the same formula
4. Lookup works without real numbers ever touching Google's infrastructure

---

## Anonymisation Pipeline

A Jupyter notebook (`anonymise_cati.ipynb`) and standalone script (`anonymise_cati.py`) are included.

```bash
pip install pandas openpyxl
python anonymise_cati.py --input your_data.xlsx --phone-col Contacts
```

**Outputs:**

| File | Contents | Action |
|---|---|---|
| `cati_public.csv` | Contact codes + all other columns | ✅ Upload to Google Sheets |
| `PRIVATE_phone_mapping.csv` | Phone ↔ Contact Code lookup | 🔒 Keep on internal drive only |

The same normalisation logic runs in both Python and JavaScript — same input always produces the same hash, so lookups are fully deterministic.

**Phone normalisation** handles all common Nigerian formats:

```
08031234567    →  +2348031234567
8031234567     →  +2348031234567  (Excel strips leading zero)
+2348031234567 →  +2348031234567
2348031234567  →  +2348031234567
```

---

## Getting Started

### 1 — Prepare your Google Sheet

Your Sheet must have at minimum these columns (names are configurable in Settings):

| Column | Description |
|---|---|
| `Contact_Code` | SHA-256 hash of phone number (or raw phone for testing) |
| `Outcome` | Call outcome string |
| `Call_Date` | Date of call (string or Excel serial number — both handled) |
| `Project` | Survey project name |
| `Interviewer` | Interviewer name or ID |
| `Attempt` | Attempt number |
| `State` | Respondent state |
| `LGA` | Respondent LGA |

### 2 — Publish the Sheet

In Google Sheets: **File → Share → Publish to web → Sheet → CSV → Publish**

Copy the generated URL.

### 3 — Deploy the app

No build step required. The app is a single `.html` file.

**Option A — Netlify (recommended)**
1. Drag `cati_sheets.html` into [netlify.com/drop](https://netlify.com/drop)
2. Share the generated URL with your team

**Option B — Any static host**
Upload `cati_sheets.html` to GitHub Pages, Vercel, or any web server.

**Option C — Run locally**
Open `cati_sheets.html` directly in a browser. Note: Chrome may block the Google Sheets fetch on a `file://` URL — use a local server (`python -m http.server`) if so.

### 4 — Connect your Sheet

1. Open the app → **Settings** tab
2. Paste your published CSV URL
3. Click **Load Data**

---

## Technology Stack

| Layer | Technology |
|---|---|
| UI | Vanilla HTML/CSS/JS (dark theme, amber accent) |
| Charts | Chart.js 4.4.1 |
| CSV parsing | SheetJS (xlsx 0.18.5) |
| Hashing | Web Crypto API (`crypto.subtle.digest`) |
| Scoring | Bayesian smoothing (custom, no dependencies) |
| Data source | Google Sheets published CSV |
| Hosting | Any static host (Netlify, GitHub Pages, etc.) |

No framework. No build tool. No backend. No API keys.

---

## Scoring Model

The priority score is a weighted blend of two signals:

```
smoothed_completion = (completed + PRIOR_WEIGHT × ORG_PRIOR_RATE) / (total + PRIOR_WEIGHT)
reach_rate          = 1 - (not_reachable + switched_off) / total
score               = round(smoothed_completion × 70 + reach_rate × 30)
```

| Parameter | Default | How to change |
|---|---|---|
| `ORG_PRIOR_RATE` | `0.138` (13.8%) | Edit in Settings or source |
| `PRIOR_WEIGHT` | `5` | Edit in source |

The prior weight determines how quickly new evidence overrides the organisational baseline. At weight 5, a contact needs roughly 10+ calls before their personal history dominates.

---

## File Structure

```
cati_sheets.html          # Main app (single file, self-contained)
anonymise_cati.py         # CLI anonymisation script
anonymise_cati.ipynb      # Jupyter notebook version
cati_mock_10k.csv         # 10,000-row mock dataset for testing
README.md                 # This file
```

---

## Roadmap

- [ ] Phase 2: Supabase backend for persistent storage and multi-user access
- [ ] Rescheduled callback extraction and calendar integration
- [ ] ML-based scoring as repeat-call data accumulates
- [ ] Interviewer performance analytics panel
- [ ] LLM-assisted QC (contact IDs only — no phone numbers sent to any external AI)

---

## Author

**Ajao Abiola Olanrewaju**  
Senior Research & Data Analyst, NOI Polls  
[linkedin.com/in/abiola-ajao](https://linkedin.com/in/abiola-ajao) · [github.com/Abiola97](https://github.com/Abiola97)

---

## Licence

MIT — free to use, adapt, and distribute with attribution.
