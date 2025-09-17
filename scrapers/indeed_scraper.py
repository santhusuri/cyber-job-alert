# scrapers/indeed_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"}

def fetch_indeed(keywords, location, max_pages=1):
    """
    Fetch job cards from Indeed (India or Remote).
    returns list of job dicts.
    """
    jobs = []
    q = urllib.parse.quote_plus(" OR ".join(keywords))
    # Indeed 'fromage=1' filters 1 day postings
    base = f"https://www.indeed.co.in/jobs?q={q}&l={urllib.parse.quote_plus(location)}&fromage=1"
    # some pagination support
    for page in range(max_pages):
        url = base + (f"&start={page*10}" if page else "")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                print("Indeed status:", resp.status_code)
                break
            soup = BeautifulSoup(resp.text, "lxml")
            for a in soup.select("a.tapItem"):
                title_tag = a.select_one("h2 span")
                title = title_tag.get_text(strip=True) if title_tag else ""
                comp_tag = a.select_one("span.companyName")
                company = comp_tag.get_text(strip=True) if comp_tag else ""
                loc_tag = a.select_one("div.companyLocation")
                location_text = loc_tag.get_text(strip=True) if loc_tag else location
                href = a.get('href') or ""
                link = "https://www.indeed.co.in" + href if href.startswith("/") else href
                # posted date: often within a span with class date or by aria-label; default to today
                posted_date = datetime.utcnow().date().isoformat()
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link,
                    "posted_date": posted_date,
                    "source": "indeed"
                })
            time.sleep(1.0)
        except Exception as e:
            print("Indeed fetch error:", e)
            break
    return jobs
