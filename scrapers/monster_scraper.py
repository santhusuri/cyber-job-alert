# scrapers/monster_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_monster(keywords, location, max_pages=1):
    """
    Monster India scraper - best-effort.
    """
    jobs = []
    q = "-".join(keywords)  # monster uses hyphen sometimes
    url = f"https://www.monsterindia.com/srp/results?query={'%20'.join(keywords)}&locations={urllib.parse.quote_plus(location)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("Monster status:", resp.status_code)
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("div.card-layout") or soup.select("section.card")
        for c in cards:
            title_tag = c.select_one("h3.title") or c.select_one("a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            company_tag = c.select_one("div.company") or c.select_one("span.company")
            company = company_tag.get_text(strip=True) if company_tag else ""
            loc_tag = c.select_one("div.location") or c.select_one("span.location")
            location_text = loc_tag.get_text(strip=True) if loc_tag else location
            link_tag = c.select_one("a")
            link = link_tag.get('href') if link_tag else ""
            posted_date = datetime.utcnow().date().isoformat()
            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": link,
                "posted_date": posted_date,
                "source": "monster"
            })
            time.sleep(0.1)
    except Exception as e:
        print("Monster error:", e)
    return jobs
