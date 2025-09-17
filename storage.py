# storage.py
import csv
import datetime
import os

OUT_DIR = os.environ.get("OUT_DIR", ".")
os.makedirs(OUT_DIR, exist_ok=True)

def save_jobs(jobs):
    date = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"jobs_{date}.csv"
    path = os.path.join(OUT_DIR, filename)
    if not jobs:
        # create empty csv header
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("title,company,location,link,posted_date,source\n")
        return path
    keys = ["title","company","location","link","posted_date","source"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for j in jobs:
            row = {k: j.get(k,"") for k in keys}
            writer.writerow(row)
    print(f"Saved {len(jobs)} jobs to {path}")
    return path
