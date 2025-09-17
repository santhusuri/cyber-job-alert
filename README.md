# Cyber Job Alert (GitHub Actions Version)

This project fetches **entry-level cybersecurity jobs** daily at **12:00 IST** and sends results via **Email** and optionally **Telegram**.

---

## 🚀 Features
- Runs daily via **GitHub Actions** (free, no server needed).
- Emails you the latest jobs with a CSV attachment.
- Sends Telegram alerts (optional).
- Custom filters (titles, keywords, location) can be extended.

---

## ⚙️ Setup

### 1. Fork this repo

    git clone https://github.com/santhusuri/cyber-job-alert.git

### 2. Add GitHub Secrets

Go to Repo → Settings → Secrets and variables → Actions and add:

- SMTP_SERVER (e.g., smtp.gmail.com)

- SMTP_PORT (e.g., 465)

- SENDER_EMAIL

- SENDER_PASSWORD (App password for Gmail, NOT your real password)

- RECEIVER_EMAIL

- TELEGRAM_BOT_TOKEN (optional)

- TELEGRAM_CHAT_ID (optional)

### 3. Test workflow

- Go to Actions tab → Run workflow (manual trigger).

- Or wait for the daily schedule (12:00 IST).