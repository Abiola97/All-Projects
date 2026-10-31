#!/usr/bin/env python3
"""
Abiola Ajao — Job Pipeline (GitHub Actions version)
Reads all credentials from environment variables set as GitHub Secrets.
"""

import logging
import subprocess
import json
import os
import sys
import datetime

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PIPELINE_DIR, 'outputs')
TODAY = datetime.date.today().isoformat()
MAX_CVS = 5

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

CV_BUILDER_JS = os.path.join(PIPELINE_DIR, 'cv_builder.js')


def build_cv_for_job(job):
    try:
        result = subprocess.run(
            ['node', CV_BUILDER_JS, json.dumps(job), OUTPUT_DIR],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            path = result.stdout.strip()
            logger.info(f'CV built: {os.path.basename(path)}')
            return path
        else:
            logger.error(f'CV build failed: {result.stderr[:200]}')
            return None
    except Exception as e:
        logger.error(f'CV build error: {e}')
        return None


def run_pipeline():
    logger.info('=' * 55)
    logger.info(f'Pipeline run — {TODAY}')
    logger.info('=' * 55)

    sys.path.insert(0, PIPELINE_DIR)

    # 1. Scrape
    from scraper import scrape_all
    all_jobs = scrape_all()
    logger.info(f'Scraped {len(all_jobs)} unique jobs')

    if not all_jobs:
        logger.info('No jobs found — done.')
        return

    # 2. Log to Google Sheets
    try:
        from sheets_logger import log_new_jobs
        new_jobs = log_new_jobs(all_jobs)
        logger.info(f'{len(new_jobs)} new jobs logged to sheet')
    except Exception as e:
        logger.error(f'Sheets error: {e}')
        new_jobs = all_jobs

    if not new_jobs:
        logger.info('No new jobs this run.')
        return

    # 3. Build CVs
    cv_paths = []
    for job in new_jobs[:MAX_CVS]:
        path = build_cv_for_job(job)
        cv_paths.append(path)

    # 4. Email digest
    try:
        from email_notifier import send_digest
        send_digest(new_jobs, attachments=[p for p in cv_paths if p])
    except Exception as e:
        logger.error(f'Email error: {e}')

    logger.info('Pipeline complete.')


if __name__ == '__main__':
    run_pipeline()
