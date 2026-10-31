"""
Email Notifier — Abiola Ajao Job Pipeline
Sends daily email digest of new jobs to ajaoabiola0812@gmail.com via Gmail SMTP.
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

GMAIL_USER = 'ajaoabiola0812@gmail.com'
GMAIL_APP_PASSWORD = 'jbsk ggmo gqlc bdxn'
TO_EMAIL = 'ajaoabiola0812@gmail.com'
SHEET_URL = 'https://docs.google.com/spreadsheets/d/1XAPA7erJKnRiMyOjrpcThb_8sPlNg542YQkTNphOwOk/edit'


def build_html_digest(new_jobs, cv_paths=None):
    """Build rich HTML email body."""
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
        cv_label = ''
        if cv_paths and i <= len(cv_paths) and cv_paths[i-1]:
            cv_label = '<span style="color:#1F4E79;font-size:11px;">📎 CV attached</span>'

        rows_html += f'''
        <tr style="background:{bg};">
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;font-weight:600;color:#1F4E79;">{title}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;">{company}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{salary}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{location}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;color:#595959;">{source}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #E0E0E0;">
            <a href="{link}" style="background:#1F4E79;color:#FFF;padding:5px 12px;border-radius:4px;text-decoration:none;font-size:12px;">Apply</a>
            {cv_label}
          </td>
        </tr>'''

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#F5F7FA;font-family:Calibri,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F7FA;">
    <tr><td align="center" style="padding:30px 20px;">
      <table width="680" cellpadding="0" cellspacing="0" style="background:#FFFFFF;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">

        <!-- Header -->
        <tr>
          <td style="background:#1F4E79;padding:24px 32px;">
            <h1 style="margin:0;color:#FFFFFF;font-size:22px;font-weight:700;">📊 Your Daily Job Digest</h1>
            <p style="margin:6px 0 0;color:#B8D4F0;font-size:14px;">{today} &nbsp;·&nbsp; {count} new role{'s' if count != 1 else ''} found</p>
          </td>
        </tr>

        <!-- Intro -->
        <tr>
          <td style="padding:20px 32px 8px;">
            <p style="margin:0;color:#333;font-size:14px;">
              Hi Abiola, here are <strong>{count} new analytical role{'s' if count != 1 else ''}</strong> matching your profile found today across Jobberman, MyJobMag, HotNigerianJobs, RemoteOK, Indeed, and LinkedIn.
              Where a tailored CV was generated, it is attached to this email for your review.
            </p>
          </td>
        </tr>

        <!-- Jobs Table -->
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
              <tbody>
                {rows_html}
              </tbody>
            </table>
          </td>
        </tr>

        <!-- Tracker link -->
        <tr>
          <td style="padding:0 32px 24px;">
            <p style="margin:0;font-size:13px;color:#595959;">
              View and update all applications in your&nbsp;
              <a href="{SHEET_URL}" style="color:#2E74B5;font-weight:600;">Google Sheets Tracker</a>.
            </p>
          </td>
        </tr>

        <!-- Footer -->
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
</body>
</html>
"""
    return html


def send_digest(new_jobs, attachments=None):
    """
    Send email digest.
    attachments: list of file paths (CVs, cover letters) to attach.
    """
    if not new_jobs:
        logger.info('No new jobs — skipping email.')
        return False

    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = GMAIL_USER
        msg['To'] = TO_EMAIL
        today = datetime.date.today().strftime('%d %b %Y')
        count = len(new_jobs)
        msg['Subject'] = f'🔍 {count} New Job Match{"es" if count != 1 else ""} – {today} | Abiola Ajao Job Tracker'

        cv_paths = attachments or []
        html_body = build_html_digest(new_jobs, cv_paths)
        msg.attach(MIMEText(html_body, 'html'))

        # Attach CV/cover letter files
        if attachments:
            for filepath in attachments:
                if filepath and os.path.exists(filepath):
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(filepath)
                    part.add_header('Content-Disposition', 'attachment', filename=filename)
                    msg.attach(part)
                    logger.info(f'Attached: {filename}')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD.replace(' ', ''))
            server.send_message(msg)

        logger.info(f'Email digest sent to {TO_EMAIL} with {count} jobs.')
        return True

    except Exception as e:
        logger.error(f'Email send failed: {e}')
        return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Test email
    test_jobs = [{
        'title': 'Research Analyst', 'company': 'TalentHub HRM',
        'salary': '₦400,000–600,000', 'location': 'Lagos',
        'source': 'LinkedIn', 'apply_link': 'https://linkedin.com/jobs/view/test',
        'date_found': '2026-10-31', 'status': 'New'
    }]
    send_digest(test_jobs)
