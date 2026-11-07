"""
Email Notifier — reads Gmail credentials from environment variables (GitHub Secrets).
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
import datetime

logger = logging.getLogger(__name__)

GMAIL_USER = os.environ.get('GMAIL_USER', 'ajaoabiola0812@gmail.com')
GMAIL_APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD', '').replace(' ', '')
TO_EMAIL = 'ajaoabiola0812@gmail.com'
CC_EMAIL = 'abiolaolanrewaju1@gmail.com'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1XAPA7erJKnRiMyOjrpcThb_8sPlNg542YQkTNphOwOk/edit'


def build_html_digest(new_jobs, cv_paths=None):
    today = datetime.date.today().strftime('%d %B %Y')
    count = len(new_jobs)
    rows_html = ''

    for i, job in enumerate(new_jobs, 1):
        bg = '#F0F4F8' if i % 2 == 0 else '#FFFFFF'
        title = job.get('title', 'N/A')
        company = job.get('company', 'N/A')
        salary = job.get('salary', 'Not stated')
        location = job.get('location', 'N/A')
        source = job.get('source', 'N/A')
        link = job.get('apply_link', '#')
        cv_note = '<br><span style="color:#1F4E79;font-size:11px;">📎 CV attached</span>' \
                  if cv_paths and i <= len(cv_paths) and cv_paths[i-1] else ''

        rows_html += f'''
        <tr style="background:{bg};">
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;font-weight:600;color:#1F4E79;">{title}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;">{company}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{salary}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{location}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{source}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;">
            <a href="{link}" style="background:#1F4E79;color:#FFF;padding:5px 12px;border-radius:4px;
               text-decoration:none;font-size:12px;">Apply</a>{cv_note}
          </td>
        </tr>'''

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#F5F7FA;font-family:Calibri,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F7FA;">
<tr><td align="center" style="padding:30px 20px;">
<table width="680" cellpadding="0" cellspacing="0"
  style="background:#FFFFFF;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
  <tr>
    <td style="background:#1F4E79;padding:24px 32px;">
      <h1 style="margin:0;color:#FFF;font-size:22px;">📊 Your Daily Job Digest</h1>
      <p style="margin:6px 0 0;color:#B8D4F0;font-size:14px;">{today} &nbsp;·&nbsp; {count} new role{'s' if count!=1 else ''} found</p>
    </td>
  </tr>
  <tr>
    <td style="padding:20px 32px 8px;">
      <p style="margin:0;color:#333;font-size:14px;">Hi Abiola, here are <strong>{count} new role{'s' if count!=1 else ''}</strong>
      found today. Tailored CVs for the top roles are attached.</p>
    </td>
  </tr>
  <tr>
    <td style="padding:12px 32px 20px;">
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="background:#2E74B5;color:#FFF;">
            <th style="padding:10px 12px;text-align:left;">Role</th>
            <th style="padding:10px 12px;text-align:left;">Company</th>
            <th style="padding:10px 12px;text-align:left;">Salary</th>
            <th style="padding:10px 12px;text-align:left;">Location</th>
            <th style="padding:10px 12px;text-align:left;">Source</th>
            <th style="padding:10px 12px;text-align:left;">Action</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:0 32px 24px;">
      <p style="margin:0;font-size:13px;color:#595959;">
        Track all applications: <a href="{SHEET_URL}" style="color:#2E74B5;font-weight:600;">Google Sheets Tracker</a>
      </p>
    </td>
  </tr>
  <tr>
    <td style="background:#F0F4F8;padding:16px 32px;border-top:1px solid #E0E0E0;">
      <p style="margin:0;font-size:11px;color:#999;">
        Abiola Ajao Job Pipeline · Auto-generated ·
        <a href="https://www.linkedin.com/in/abiola-ajao" style="color:#2E74B5;">LinkedIn</a> ·
        <a href="https://github.com/Abiola97/All-Projects" style="color:#2E74B5;">GitHub</a>
      </p>
    </td>
  </tr>
</table>
</td></tr>
</table>
</body></html>"""


def send_digest(new_jobs, attachments=None):
    if not new_jobs:
        logger.info('No new jobs — skipping email.')
        return False

    if not GMAIL_APP_PASSWORD:
        logger.error('GMAIL_APP_PASSWORD not set in environment.')
        return False

    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = GMAIL_USER
        msg['To'] = TO_EMAIL
        msg['Cc'] = CC_EMAIL
        today = datetime.date.today().strftime('%d %b %Y')
        count = len(new_jobs)
        msg['Subject'] = f'🔍 {count} New Job Match{"es" if count!=1 else ""} – {today} | Abiola Job Tracker'

        cv_paths = attachments or []
        msg.attach(MIMEText(build_html_digest(new_jobs, cv_paths), 'html'))

        for filepath in (attachments or []):
            if filepath and os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment',
                                filename=os.path.basename(filepath))
                msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [TO_EMAIL, CC_EMAIL], msg.as_string())

        logger.info(f'Email sent to {TO_EMAIL} (cc: {CC_EMAIL}) with {count} jobs.')
        return True

    except Exception as e:
        logger.error(f'Email failed: {e}')
        return False
