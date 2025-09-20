from dotenv import load_dotenv
import asyncio
import json
import os
import requests
import openai
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime
import schedule
import time

# ================================
# LOAD ENV
# ================================
load_dotenv()

# ================================
# CONFIG
# ================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CONFIG_FILE = "config.json"

openai.api_key = OPENAI_API_KEY
bot = Bot(token=TELEGRAM_TOKEN)

# ================================
# AUTO CHAT ID DETECTION
# ================================
async def get_chat_id():
    """Fetch chat ID from Telegram updates and store in config.json if not present."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            if "chat_id" in config:
                return config["chat_id"]

    updates = await bot.get_updates()
    if not updates:
        print("⚠️ No chat messages found. Send a message to your bot in Telegram first!")
        return None

    chat_id = updates[-1].message.chat.id
    with open(CONFIG_FILE, "w") as f:
        json.dump({"chat_id": chat_id}, f)
    print(f"✅ Saved chat_id: {chat_id} to {CONFIG_FILE}")
    return chat_id

# ================================
# DATA FETCHERS
# ================================
def fetch_hackernews():
    """Fetch top 5 Hacker News stories."""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        story_ids = requests.get(url, timeout=10).json()[:5]
        stories = []
        for sid in story_ids:
            story = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10).json()
            if "title" in story and "url" in story:
                stories.append({"title": story["title"], "url": story["url"]})
        return stories
    except Exception as e:
        print(f"⚠️ Failed to fetch Hacker News: {e}")
        return []

def fetch_github_trending():
    """Fetch top 5 GitHub trending repos."""
    try:
        url = "https://github.com/trending"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        repos = []
        for repo in soup.select("article.Box-row")[:5]:
            title = repo.h2.a.get_text(strip=True)
            link = "https://github.com" + repo.h2.a["href"]
            repos.append({"title": title, "url": link})
        return repos
    except Exception as e:
        print(f"⚠️ Failed to fetch GitHub Trending: {e}")
        return []


def fetch_google_news(query):
    """Fetch top 5 Google News results for a specific query."""
    url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "xml")
        items = soup.find_all("item")[:5]
        news = []
        for item in items:
            news.append({"title": item.title.text, "url": item.link.text})
        return news
    except Exception as e:
        print(f"⚠️ Failed to fetch Google News ({query}): {e}")
        return []

# ================================
# GPT SUMMARIZER
# ================================
def summarize_item(item):
    """Use GPT to make a catchy summary in one line."""
    prompt = f"""
Summarize this tech news into one catchy line for a Telegram message:
Title: {item['title']}
Link: {item['url']}
Make it short, engaging, and relevant for developers.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a witty tech news summarizer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return item['title']

# ================================
# ALERT SENDER
# ================================
async def send_alerts():
    chat_id = await get_chat_id()
    if not chat_id:
        return

    hn_news = fetch_hackernews()
    gh_news = fetch_github_trending()
    google_lang = fetch_google_news("programming+languages")
    google_tools = fetch_google_news("programming+tools")
    google_ai = fetch_google_news("AI+tools")
    google_dev = fetch_google_news("development+tools")

    messages = []
    messages.append("🚀 *Today's Tech Briefing*\n")

    if hn_news:
        messages.append("📰 *Top Hacker News:*")
        for news in hn_news:
            summary = summarize_item(news)
            messages.append(f"• [{summary}]({news['url']})")

    if gh_news:
        messages.append("\n💻 *GitHub Trending Repos:*")
        for repo in gh_news:
            summary = summarize_item(repo)
            messages.append(f"• [{summary}]({repo['url']})")

    if google_lang:
        messages.append("\n📚 *Programming Languages News:*")
        for news in google_lang:
            summary = summarize_item(news)
            messages.append(f"• [{summary}]({news['url']})")

    if google_tools:
        messages.append("\n🛠 *Programming Tools:*")
        for news in google_tools:
            summary = summarize_item(news)
            messages.append(f"• [{summary}]({news['url']})")

    if google_ai:
        messages.append("\n🤖 *AI Tools & Updates:*")
        for news in google_ai:
            summary = summarize_item(news)
            messages.append(f"• [{summary}]({news['url']})")

    if google_dev:
        messages.append("\n🧰 *Development Tools:*")
        for news in google_dev:
            summary = summarize_item(news)
            messages.append(f"• [{summary}]({news['url']})")

    full_message = "\n".join(messages)

    await bot.send_message(chat_id=chat_id, text=full_message, parse_mode="Markdown")
    print(f"✅ Sent Tech Briefing at {datetime.now().strftime('%H:%M:%S')}")

# ================================
# SCHEDULER
# ================================
def run_scheduler():
    """Run every morning at 9 AM & evening at 6 PM."""
    schedule.every().day.at("09:00").do(lambda: asyncio.run(send_alerts()))
    schedule.every().day.at("18:00").do(lambda: asyncio.run(send_alerts()))
    print("⏳ Scheduler started. Waiting for 09:00 AM & 06:00 PM daily...")
    while True:
        schedule.run_pending()
        time.sleep(30)

# ================================
# MAIN
# ================================
if __name__ == "__main__":
    # Manual run for testing
    asyncio.run(send_alerts())

    # Uncomment below line to enable daily scheduler
    run_scheduler()
