# scrapers/naukri_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_naukri(keywords, location, max_pages=1):
    """
    Naukri search. Returns list of jobs.
    """
    jobs = []
    q = "+".join(keywords)  # Naukri query formatting is flexible
    # use naugri.co.in search
    base = f"https://www.naukri.com/{urllib.parse.quote_plus(' '.join(keywords))}-jobs-in-{urllib.parse.quote_plus(location)}"
    # fallback: use their generic search URL with query param
    search_url = f"https://www.naukri.com/{urllib.parse.quote_plus(' '.join(keywords))}-jobs"
    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("Naukri status:", resp.status_code)
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("article.jobTuple") or soup.select("div.list")
        for c in cards[:50]:
            try:
                title_tag = c.select_one("a.title") or c.select_one("a.jobTitle")
                title = title_tag.get_text(strip=True) if title_tag else ""
                company_tag = c.select_one("a.subTitle") or c.select_one("div.company")
                company = company_tag.get_text(strip=True) if company_tag else ""
                loc_tag = c.select_one("li.location") or c.select_one("span.loc")
                location_text = loc_tag.get_text(strip=True) if loc_tag else location
                link = title_tag.get('href') if title_tag and title_tag.get('href') else ""
                posted_date = datetime.utcnow().date().isoformat()
                jobs.append({
                    "title": title,
                    "company": company,
                    "location": location_text,
                    "link": link,
                    "posted_date": posted_date,
                    "source": "naukri"
                })
            except Exception:
                continue
            time.sleep(0.2)
    except Exception as e:
        print("Naukri error:", e)
    return jobs
