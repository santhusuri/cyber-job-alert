import csv
import datetime

def save_jobs(jobs):
    today = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"jobs_{today}.csv"
    keys = jobs[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Saved {len(jobs)} jobs to {filename}")
    return filename
