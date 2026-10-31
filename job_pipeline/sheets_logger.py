"""
Google Sheets Logger — Abiola Ajao Job Pipeline
Logs new jobs to the tracker sheet and returns only new (not already logged) jobs.
Sheet columns: Title | Company | Salary | Location | Deadline | Apply Link | Source | Date Found | Status
"""

import gspread
from google.oauth2.service_account import Credentials
import logging

logger = logging.getLogger(__name__)

SHEET_ID = '1XAPA7erJKnRiMyOjrpcThb_8sPlNg542YQkTNphOwOk'
CREDS_PATH = '/mnt/user-data/attachments/2d6fc4ab-a847-5e81-a2fa-a1c6d6deb538/8cb0392e-capstonbee-f2f9a5bc5914.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]

COLUMNS = ['Title', 'Company', 'Salary', 'Location', 'Deadline', 'Apply Link', 'Source', 'Date Found', 'Status']


def get_sheet():
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(SHEET_ID)
    # Use first worksheet or create it
    try:
        ws = sh.worksheet('Job Tracker')
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title='Job Tracker', rows=1000, cols=len(COLUMNS))
    return ws


def ensure_headers(ws):
    """Add column headers if sheet is empty."""
    existing = ws.row_values(1)
    if not existing or existing[0] != 'Title':
        ws.update('A1', [COLUMNS])
        # Format header row — bold, dark blue fill
        ws.format('A1:I1', {
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
            'backgroundColor': {'red': 0.122, 'green': 0.306, 'blue': 0.475},
        })
        logger.info('Sheet headers created.')


def get_existing_links(ws):
    """Return set of all apply_link values already in the sheet."""
    try:
        col_idx = COLUMNS.index('Apply Link') + 1  # 1-based
        values = ws.col_values(col_idx)
        return set(v.strip() for v in values[1:] if v.strip())  # skip header
    except Exception as e:
        logger.warning(f'Could not read existing links: {e}')
        return set()


def log_new_jobs(jobs):
    """
    Log jobs not already in the sheet. Returns list of truly new jobs appended.
    """
    try:
        ws = get_sheet()
        ensure_headers(ws)
        existing_links = get_existing_links(ws)

        new_jobs = [j for j in jobs if j.get('apply_link', '').strip() not in existing_links]

        if not new_jobs:
            logger.info('No new jobs to log — all already in sheet.')
            return []

        rows = []
        for j in new_jobs:
            rows.append([
                j.get('title', ''),
                j.get('company', ''),
                j.get('salary', 'Not stated'),
                j.get('location', ''),
                j.get('deadline', ''),
                j.get('apply_link', ''),
                j.get('source', ''),
                j.get('date_found', ''),
                j.get('status', 'New'),
            ])

        ws.append_rows(rows, value_input_option='USER_ENTERED')
        logger.info(f'Logged {len(new_jobs)} new jobs to Google Sheets.')
        return new_jobs

    except Exception as e:
        logger.error(f'Google Sheets error: {e}')
        return jobs  # fall back: treat all as new for email purposes


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Test with a dummy job
    test = [{
        'title': 'Test Research Analyst', 'company': 'Test Co',
        'salary': '₦400,000', 'location': 'Lagos', 'deadline': '',
        'apply_link': 'https://example.com/test-job-001',
        'source': 'Test', 'date_found': '2026-10-31', 'status': 'New'
    }]
    result = log_new_jobs(test)
    print(f'Logged: {len(result)} jobs')
