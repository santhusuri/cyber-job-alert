# scrapers/freshersworld_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_freshersworld(keywords, location, max_pages=1):
    jobs = []
    q = "-".join(keywords)
    url = f"https://www.freshersworld.com/jobs/search?search={urllib.parse.quote_plus(' '.join(keywords))}&location={urllib.parse.quote_plus(location)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("Freshersworld status:", resp.status_code)
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.jobCard") or soup.select("li.job")
        for c in cards:
            title_tag = c.select_one("h3 a") or c.select_one("h4 a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            company_tag = c.select_one("div.company") or c.select_one("span.company")
            company = company_tag.get_text(strip=True) if company_tag else ""
            loc_tag = c.select_one("p.location") or c.select_one("div.loc")
            location_text = loc_tag.get_text(strip=True) if loc_tag else location
            link = title_tag.get('href') if title_tag and title_tag.get('href') else ""
            posted_date = datetime.utcnow().date().isoformat()
            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": link,
                "posted_date": posted_date,
                "source": "freshersworld"
            })
            time.sleep(0.1)
    except Exception as e:
        print("Freshersworld error:", e)
    return jobs
