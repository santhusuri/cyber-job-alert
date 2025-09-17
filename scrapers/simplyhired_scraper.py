# scrapers/simplyhired_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_simplyhired(keywords, location, max_pages=1):
    jobs = []
    q = "+".join(keywords)
    url = f"https://www.simplyhired.co.in/search?q={urllib.parse.quote_plus(' '.join(keywords))}&l={urllib.parse.quote_plus(location)}&days=1"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("SimplyHired status:", resp.status_code)
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.SerpJob-jobCard") or soup.select("div.card")
        for c in cards:
            title_tag = c.select_one("a.SerpJob-link")
            title = title_tag.get_text(strip=True) if title_tag else ""
            company_tag = c.select_one("span.JobPosting-labelWithIcon")
            company = company_tag.get_text(strip=True) if company_tag else ""
            loc_tag = c.select_one("span.JobPosting-labelWithIcon+span")
            location_text = loc_tag.get_text(strip=True) if loc_tag else location
            link = "https://www.simplyhired.co.in" + title_tag.get('href') if title_tag and title_tag.get('href') else ""
            posted_date = datetime.utcnow().date().isoformat()
            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": link,
                "posted_date": posted_date,
                "source": "simplyhired"
            })
            time.sleep(0.1)
    except Exception as e:
        print("SimplyHired error:", e)
    return jobs
