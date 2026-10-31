#!/usr/bin/env python3 -I
"""
Abiola Ajao — Job Application Pipeline
Orchestrates: scrape → deduplicate → log to Sheets → build CVs → email digest

Run: python3 pipeline.py
"""

import logging
import subprocess
import json
import os
import sys
import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/mnt/user-data/outputs/pipeline.log', mode='a'),
    ]
)
logger = logging.getLogger(__name__)

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
CV_BUILDER_JS = os.path.join(PIPELINE_DIR, 'cv_builder.js')
OUTPUT_DIR = '/mnt/user-data/outputs'
TODAY = datetime.date.today().isoformat()

# Max CVs to auto-generate per run (top N most relevant jobs)
MAX_CVS = 5


def install_node_deps():
    """Ensure docx npm package is available."""
    node_modules = os.path.join(PIPELINE_DIR, 'node_modules')
    if not os.path.exists(node_modules):
        logger.info('Installing Node.js dependencies (docx)...')
        result = subprocess.run(
            ['npm', 'install', 'docx@8.5.0'],
            cwd=PIPELINE_DIR,
            capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.error(f'npm install failed: {result.stderr}')
        else:
            logger.info('docx package installed.')


def build_cv_for_job(job):
    """Call cv_builder.js for a single job. Returns path to generated .docx or None."""
    try:
        job_json = json.dumps(job)
        result = subprocess.run(
            ['node', CV_BUILDER_JS, job_json, OUTPUT_DIR],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            logger.info(f'CV built: {path}')
            return path
        else:
            logger.error(f'CV build failed for {job.get("title")}: {result.stderr}')
            return None
    except Exception as e:
        logger.error(f'CV build error: {e}')
        return None


def run_pipeline():
    logger.info('=' * 60)
    logger.info(f'Pipeline run started — {TODAY}')
    logger.info('=' * 60)

    # 1. Install Node dependencies
    install_node_deps()

    # 2. Scrape all job boards
    sys.path.insert(0, PIPELINE_DIR)
    from scraper import scrape_all
    all_jobs = scrape_all()
    logger.info(f'Scraped {len(all_jobs)} unique jobs total')

    if not all_jobs:
        logger.info('No jobs scraped — pipeline complete.')
        return

    # 3. Log to Google Sheets (returns only truly new jobs)
    try:
        from sheets_logger import log_new_jobs
        new_jobs = log_new_jobs(all_jobs)
        logger.info(f'{len(new_jobs)} new jobs logged to Google Sheets')
    except Exception as e:
        logger.error(f'Sheets logging failed: {e}')
        new_jobs = all_jobs  # fall back to all jobs for email

    if not new_jobs:
        logger.info('No new jobs this run — nothing to email.')
        return

    # 4. Build tailored CVs for top N new jobs
    cv_paths = []
    for job in new_jobs[:MAX_CVS]:
        path = build_cv_for_job(job)
        cv_paths.append(path)

    # 5. Send email digest with CVs attached
    try:
        from email_notifier import send_digest
        success = send_digest(new_jobs, attachments=[p for p in cv_paths if p])
        if success:
            logger.info('Email digest sent successfully.')
        else:
            logger.warning('Email digest could not be sent.')
    except Exception as e:
        logger.error(f'Email notification failed: {e}')

    logger.info('=' * 60)
    logger.info('Pipeline run complete.')
    logger.info('=' * 60)


if __name__ == '__main__':
    run_pipeline()
