# scrapers/timesjobs_scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_timesjobs(keywords, location, max_pages=1):
    jobs = []
    q = "%20".join(keywords)
    url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={urllib.parse.quote_plus(' '.join(keywords))}&txtLocation={urllib.parse.quote_plus(location)}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            print("TimesJobs status:", resp.status_code)
            return jobs
        soup = BeautifulSoup(resp.text, "lxml")
        cards = soup.select("li.joindata") or soup.select("li.clearfix")
        for c in cards:
            title_tag = c.select_one("h2 a") or c.select_one("h3 a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            company_tag = c.select_one("h3 span") or c.select_one("h4")
            company = company_tag.get_text(strip=True) if company_tag else ""
            loc_tag = c.select_one("ul.job-info li") or c.select_one("span.job-location")
            location_text = loc_tag.get_text(strip=True) if loc_tag else location
            link = title_tag.get('href') if title_tag and title_tag.get('href') else ""
            posted_date = datetime.utcnow().date().isoformat()
            jobs.append({
                "title": title,
                "company": company,
                "location": location_text,
                "link": link,
                "posted_date": posted_date,
                "source": "timesjobs"
            })
            time.sleep(0.1)
    except Exception as e:
        print("TimesJobs error:", e)
    return jobs
