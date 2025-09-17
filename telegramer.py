# telegramer.py
import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message_if_configured(jobs):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured")
        return
    text = "<b>Cybersecurity Jobs (India+Remote)</b>\n\n"
    for j in jobs[:12]:
        title = j.get("title","")[:120]
        company = j.get("company","")
        location = j.get("location","")
        link = j.get("link","")
        text += f"{title} — {company} ({location})\n{link}\n\n"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=15)
    if resp.status_code == 200:
        print("Telegram sent")
    else:
        print("Telegram error:", resp.text)
