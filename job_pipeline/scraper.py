"""
Job Board Scraper — Abiola Ajao Job Pipeline
Scrapes: Jobberman, MyJobMag, HotNigerianJobs, RemoteOK
Returns list of job dicts with: title, company, salary, location, deadline, apply_link, source, date_found
"""

import requests
from bs4 import BeautifulSoup
import datetime
import time
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

SEARCH_TERMS = [
    'Research Analyst', 'Data Analyst', 'Market Research Analyst',
    'BI Analyst', 'Market Intelligence Analyst', 'AI Analyst',
    'Data Scientist', 'Research Associate', 'Analytics Consultant',
    'Marketing Analyst', 'Business Analyst'
]

TODAY = datetime.date.today().isoformat()


def clean(text):
    if not text:
        return ''
    return re.sub(r'\s+', ' ', text.strip())


# ──────────────────────────────────────────────────────────────────────────────
# JOBBERMAN
# ──────────────────────────────────────────────────────────────────────────────
def scrape_jobberman():
    jobs = []
    seen = set()
    for term in SEARCH_TERMS[:6]:  # limit to avoid rate limiting
        try:
            url = f'https://www.jobberman.com/jobs?q={requests.utils.quote(term)}&l=Nigeria'
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'Jobberman {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            # Jobberman job cards
            cards = soup.select('article.job-card, div[class*="job-item"], li[class*="job"]')
            if not cards:
                # Try alternate selectors
                cards = soup.select('a[href*="/jobs/"]')
            for card in cards[:10]:
                try:
                    title_el = card.select_one('h3, h2, [class*="title"], [class*="job-name"]')
                    company_el = card.select_one('[class*="company"], [class*="employer"]')
                    salary_el = card.select_one('[class*="salary"], [class*="pay"]')
                    location_el = card.select_one('[class*="location"], [class*="city"]')
                    link_el = card if card.name == 'a' else card.select_one('a[href*="/jobs/"]')

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    salary = clean(salary_el.get_text()) if salary_el else 'Not stated'
                    location = clean(location_el.get_text()) if location_el else 'Nigeria'
                    link = link_el.get('href', '') if link_el else ''
                    if link and not link.startswith('http'):
                        link = 'https://www.jobberman.com' + link

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': salary,
                        'location': location, 'deadline': '', 'apply_link': link,
                        'source': 'Jobberman', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'Jobberman card parse error: {e}')
            time.sleep(2)
        except Exception as e:
            logger.warning(f'Jobberman error for "{term}": {e}')
    logger.info(f'Jobberman: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# MYJOBMAG
# ──────────────────────────────────────────────────────────────────────────────
def scrape_myjobmag():
    jobs = []
    seen = set()
    for term in SEARCH_TERMS[:6]:
        try:
            url = f'https://www.myjobmag.com/jobs-by-title/{requests.utils.quote(term.replace(" ", "-").lower())}'
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'MyJobMag {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            cards = soup.select('li.job-item, div.job-listing, article[class*="job"]')
            if not cards:
                cards = soup.select('a[href*="/job/"]')
            for card in cards[:10]:
                try:
                    title_el = card.select_one('h2, h3, [class*="title"]')
                    company_el = card.select_one('[class*="company"], [class*="employer"], strong')
                    salary_el = card.select_one('[class*="salary"]')
                    location_el = card.select_one('[class*="location"]')
                    link_el = card if card.name == 'a' else card.select_one('a')

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    salary = clean(salary_el.get_text()) if salary_el else 'Not stated'
                    location = clean(location_el.get_text()) if location_el else 'Nigeria'
                    link = link_el.get('href', '') if link_el else ''
                    if link and not link.startswith('http'):
                        link = 'https://www.myjobmag.com' + link

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': salary,
                        'location': location, 'deadline': '', 'apply_link': link,
                        'source': 'MyJobMag', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'MyJobMag card parse error: {e}')
            time.sleep(2)
        except Exception as e:
            logger.warning(f'MyJobMag error for "{term}": {e}')
    logger.info(f'MyJobMag: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# HOTNIGERIANIJOBS
# ──────────────────────────────────────────────────────────────────────────────
def scrape_hotnigerianijobs():
    jobs = []
    seen = set()
    for term in SEARCH_TERMS[:5]:
        try:
            url = f'https://www.hotnigerianjobs.com/jobs/?s={requests.utils.quote(term)}'
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'HotNigerianJobs {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            cards = soup.select('div.job-list-item, article, div[class*="job-post"]')
            for card in cards[:10]:
                try:
                    title_el = card.select_one('h2, h3, a[href*="job"]')
                    company_el = card.select_one('[class*="company"], strong, b')
                    link_el = card.select_one('a[href*="job"], h2 a, h3 a')

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    link = link_el.get('href', '') if link_el else ''
                    if link and not link.startswith('http'):
                        link = 'https://www.hotnigerianjobs.com' + link

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': 'Not stated',
                        'location': 'Nigeria', 'deadline': '', 'apply_link': link,
                        'source': 'HotNigerianJobs', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'HotNigerianJobs card parse error: {e}')
            time.sleep(2)
        except Exception as e:
            logger.warning(f'HotNigerianJobs error for "{term}": {e}')
    logger.info(f'HotNigerianJobs: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# REMOTEOK
# ──────────────────────────────────────────────────────────────────────────────
def scrape_remoteok():
    jobs = []
    seen = set()
    remote_terms = ['research-analyst', 'data-analyst', 'business-analyst', 'market-research']
    for term in remote_terms:
        try:
            url = f'https://remoteok.com/remote-{term}-jobs'
            resp = requests.get(url, headers={**HEADERS, 'Accept': 'text/html'}, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'RemoteOK {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            rows = soup.select('tr.job[data-slug]')
            for row in rows[:8]:
                try:
                    title_el = row.select_one('h2[itemprop="title"]')
                    company_el = row.select_one('h3[itemprop="name"]')
                    salary_el = row.select_one('[class*="salary"]')
                    slug = row.get('data-slug', '')
                    link = f'https://remoteok.com/jobs/{slug}' if slug else ''

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    salary = clean(salary_el.get_text()) if salary_el else 'Not stated'

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': salary,
                        'location': 'Remote', 'deadline': '', 'apply_link': link,
                        'source': 'RemoteOK', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'RemoteOK row parse error: {e}')
            time.sleep(3)
        except Exception as e:
            logger.warning(f'RemoteOK error for "{term}": {e}')
    logger.info(f'RemoteOK: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# INDEED NIGERIA (via search)
# ──────────────────────────────────────────────────────────────────────────────
def scrape_indeed():
    jobs = []
    seen = set()
    for term in SEARCH_TERMS[:5]:
        try:
            url = f'https://ng.indeed.com/jobs?q={requests.utils.quote(term)}&l=Nigeria&fromage=1'
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'Indeed {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            cards = soup.select('div.job_seen_beacon, div[class*="result"], div[data-jk]')
            for card in cards[:8]:
                try:
                    title_el = card.select_one('h2.jobTitle, [class*="jobTitle"], a[id*="job"]')
                    company_el = card.select_one('[class*="companyName"], [data-testid="company-name"]')
                    salary_el = card.select_one('[class*="salary"], [data-testid="attribute_snippet_testid"]')
                    location_el = card.select_one('[class*="companyLocation"], [data-testid="text-location"]')
                    link_el = card.select_one('a[href*="/rc/clk"], a[href*="/pagead"]')
                    if not link_el:
                        link_el = card.select_one('a[href]')

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    salary = clean(salary_el.get_text()) if salary_el else 'Not stated'
                    location = clean(location_el.get_text()) if location_el else 'Nigeria'
                    href = link_el.get('href', '') if link_el else ''
                    link = ('https://ng.indeed.com' + href) if href and not href.startswith('http') else href

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': salary,
                        'location': location, 'deadline': '', 'apply_link': link,
                        'source': 'Indeed', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'Indeed card parse error: {e}')
            time.sleep(3)
        except Exception as e:
            logger.warning(f'Indeed error for "{term}": {e}')
    logger.info(f'Indeed: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# LINKEDIN (public search - no login required for basic results)
# ──────────────────────────────────────────────────────────────────────────────
def scrape_linkedin():
    jobs = []
    seen = set()
    for term in SEARCH_TERMS[:4]:
        try:
            url = (f'https://www.linkedin.com/jobs/search/?keywords={requests.utils.quote(term)}'
                   f'&location=Nigeria&f_TPR=r86400&position=1&pageNum=0')
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                logger.warning(f'LinkedIn {term}: HTTP {resp.status_code}')
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            cards = soup.select('div.job-search-card, li[class*="jobs-search-results"]')
            if not cards:
                cards = soup.select('div[class*="base-card"]')
            for card in cards[:8]:
                try:
                    title_el = card.select_one('h3.base-search-card__title, h3[class*="title"]')
                    company_el = card.select_one('h4.base-search-card__subtitle, [class*="company"]')
                    location_el = card.select_one('span.job-search-card__location, [class*="location"]')
                    link_el = card.select_one('a.base-card__full-link, a[href*="/jobs/view/"]')

                    title = clean(title_el.get_text()) if title_el else ''
                    company = clean(company_el.get_text()) if company_el else ''
                    location = clean(location_el.get_text()) if location_el else 'Nigeria'
                    link = link_el.get('href', '').split('?')[0] if link_el else ''

                    if not title or link in seen:
                        continue
                    seen.add(link)
                    jobs.append({
                        'title': title, 'company': company, 'salary': 'Not stated',
                        'location': location, 'deadline': '', 'apply_link': link,
                        'source': 'LinkedIn', 'date_found': TODAY, 'status': 'New'
                    })
                except Exception as e:
                    logger.debug(f'LinkedIn card parse error: {e}')
            time.sleep(3)
        except Exception as e:
            logger.warning(f'LinkedIn error for "{term}": {e}')
    logger.info(f'LinkedIn: {len(jobs)} jobs')
    return jobs


# ──────────────────────────────────────────────────────────────────────────────
# DEDUPLICATION
# ──────────────────────────────────────────────────────────────────────────────
def deduplicate(jobs):
    seen_keys = set()
    unique = []
    for j in jobs:
        key = (j['title'].lower().strip(), j['company'].lower().strip())
        if key not in seen_keys and j['title']:
            seen_keys.add(key)
            unique.append(j)
    return unique


# ──────────────────────────────────────────────────────────────────────────────
# MAIN SCRAPER
# ──────────────────────────────────────────────────────────────────────────────
def scrape_all():
    logger.info('=== Starting scrape run ===')
    all_jobs = []
    all_jobs += scrape_jobberman()
    all_jobs += scrape_myjobmag()
    all_jobs += scrape_hotnigerianijobs()
    all_jobs += scrape_remoteok()
    all_jobs += scrape_indeed()
    all_jobs += scrape_linkedin()
    unique = deduplicate(all_jobs)
    logger.info(f'=== Total unique jobs found: {len(unique)} ===')
    return unique


if __name__ == '__main__':
    jobs = scrape_all()
    for j in jobs[:5]:
        print(j)
