# jobs.py
import os
from datetime import datetime, timedelta
from storage import save_jobs
from emailer import send_email_with_csv
from telegramer import send_telegram_message_if_configured

# import scrapers
from scrapers.indeed_scraper import fetch_indeed
from scrapers.naukri_scraper import fetch_naukri
from scrapers.monster_scraper import fetch_monster
from scrapers.timesjobs_scraper import fetch_timesjobs
from scrapers.simplyhired_scraper import fetch_simplyhired
from scrapers.freshersworld_scraper import fetch_freshersworld

# Filters
TITLE_KEYWORDS = ["Entry Level", "Junior", "Associate", "Trainee", "Fresher"]
KEYWORDS = ["Cybersecurity", "Information Security", "SOC Analyst", "Security Analyst", "Cyber Defense"]
# Location preference (set via GitHub Actions env SECRET PREFERRED_LOCATION or default Remote)
LOCATION = os.environ.get("PREFERRED_LOCATION", "Remote")

def title_matches(title):
    t = (title or "").lower()
    return any(k.lower() in t for k in TITLE_KEYWORDS)

def keyword_matches(title, company, location):
    text = " ".join([title or "", company or "", location or ""]).lower()
    return any(k.lower() in text for k in KEYWORDS)

def dedupe_jobs(jobs):
    seen = set()
    out = []
    for j in jobs:
        key = (j.get("title","").lower(), j.get("company","").lower(), j.get("location","").lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(j)
    return out

def run_all_scrapers():
    all_jobs = []
    # Each returns list of jobs
    try:
        all_jobs += fetch_indeed(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("Indeed failed", e)
    try:
        all_jobs += fetch_naukri(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("Naukri failed", e)
    try:
        all_jobs += fetch_monster(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("Monster failed", e)
    try:
        all_jobs += fetch_timesjobs(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("TimesJobs failed", e)
    try:
        all_jobs += fetch_simplyhired(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("SimplyHired failed", e)
    try:
        all_jobs += fetch_freshersworld(KEYWORDS, LOCATION, max_pages=1)
    except Exception as e:
        print("Freshersworld failed", e)

    print(f"Fetched total {len(all_jobs)} raw job entries from scrapers")
    # filter by title and keywords
    filtered = []
    for j in all_jobs:
        if not j.get("title"):
            continue
        if not title_matches(j["title"]):
            # still allow if keyword present in title/company/location (catch cases where title lacks explicit 'Entry Level' but job is relevant)
            if not keyword_matches(j["title"], j.get("company",""), j.get("location","")):
                continue
        # posted_date: most scrapers set to today; keep all from last 2 days to be safe
        filtered.append(j)

    print(f"After filters: {len(filtered)} entries")
    filtered = dedupe_jobs(filtered)
    print(f"After dedupe: {len(filtered)} entries")
    return filtered

if __name__ == "__main__":
    jobs = run_all_scrapers()
    if not jobs:
        send_email_with_csv("Daily Cybersecurity Jobs", "<p>No new jobs found today.</p>")
        print("No jobs found")
    else:
        csv_path = save_jobs(jobs)
        # Build HTML body
        body = "<h2>Cybersecurity Jobs (India + Remote) — Last 24h</h2><br>"
        for j in jobs[:50]:
            body += f"<b>{j.get('title')}</b><br>{j.get('company')} | {j.get('location')}<br>"
            body += f"<a href='{j.get('link')}'>Apply</a> — {j.get('source')}<br><br>"

        send_email_with_csv("Daily Cybersecurity Jobs", body, csv_path)
        send_telegram_message_if_configured(jobs)
        print("Done")
