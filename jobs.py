import datetime
from storage import save_jobs
from emailer import send_email_with_csv
from telegramer import send_telegram_message_if_configured

# --- Job Fetcher (placeholder) ---
def fetch_jobs():
    today = datetime.date.today().strftime("%Y-%m-%d")
    # Example dummy results (replace with scrapers/APIs later)
    jobs = [
        {
            "title": "Entry Level SOC Analyst",
            "company": "XYZ Corp",
            "location": "Remote",
            "link": "https://example.com/job1",
            "posted_date": today
        },
        {
            "title": "Junior Security Analyst",
            "company": "ABC Ltd",
            "location": "Bangalore",
            "link": "https://example.com/job2",
            "posted_date": today
        }
    ]
    csv_file = save_jobs(jobs)
    return jobs, csv_file


if __name__ == "__main__":
    jobs, csv_file = fetch_jobs()

    if jobs:
        body = "<h2>Cybersecurity Jobs (Last 24h)</h2><br>"
        for j in jobs:
            body += f"<b>{j['title']}</b><br>{j['company']} | {j['location']}<br>"
            body += f"<a href='{j['link']}'>Apply Here</a><br><br>"

        send_email_with_csv("Daily Cybersecurity Jobs", body, csv_file)
        send_telegram_message_if_configured(jobs)
    else:
        send_email_with_csv("Daily Cybersecurity Jobs", "<p>No new jobs found today.</p>")
