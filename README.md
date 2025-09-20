# 🚀 Neoo – AI Tech Bot  

## 📌 Overview  
**Neoo** is an AI-powered Telegram bot that delivers **daily tech updates** on programming languages, tools, AI advancements, and development resources.  
It automatically sends curated news twice a day (at **9:00 AM** and **6:00 PM** IST) directly to your Telegram chat.  

The project also includes a **futuristic landing page** with a solar-system-themed UI and glowing glassmorphism design, responsive for desktop and mobile users.  

---

## ✨ Features  

### 🔧 Backend (Python)
- 🤖 **Automated News Fetching** – Scrapes the latest dev news from Google News & other sources.
- ⏱ **Daily Scheduler** – Sends messages automatically at 9:00 AM & 6:00 PM.
- 🔑 **Environment Variables** – Securely loads API keys & tokens from `.env`.
- ☁️ **Deployment Ready** – Runs continuously on Railway (or any cloud platform).

### 🎨 Frontend (HTML + CSS)
- 🌌 **Solar System Theme** – Animated planets orbiting a glowing sun.
- 💎 **Glassmorphism Design** – Modern glowing UI with a neon effect.
- 📱 **Responsive Layout** – Looks great on desktop, tablet, and mobile.
- 🔗 **Quick Access Buttons** – Links to Telegram bot, GitHub repo, and LinkedIn.

---

## 🛠 Tech Stack  

| Part          | Technology |
|--------------|-----------|
| **Backend**  | Python, Requests, BeautifulSoup4, APScheduler, python-dotenv |
| **Frontend** | HTML5, CSS3 (Glassmorphism + Animations) |
| **Hosting**  | Railway (Backend), Vercel (Frontend) |
| **Version Control** | Git & GitHub |

---

## 📂 Project Structure  

```bash
Neoo.bot/
│
├── bot.py              # Main bot logic
├── config.json         # News topics & sources
├── requirements.txt    # Python dependencies
├── Procfile            # Railway entrypoint
├── .gitignore          # Ignored files (like .env, venv)
└── frontend/
    └── index.html      # Landing page
