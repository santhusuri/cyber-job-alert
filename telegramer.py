import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message_if_configured(jobs):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram not configured — skipping telegram send")
        return

    text = "<b>Cybersecurity Jobs</b>\n\n"
    for j in jobs[:10]:  # send only first 10
        text += f"{j['title']} — {j['company']} ({j['location']})\n{j['link']}\n\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    if resp.status_code == 200:
        print("✅ Telegram message sent")
    else:
        print(f"⚠️ Telegram error: {resp.text}")
