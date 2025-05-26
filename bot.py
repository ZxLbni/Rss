import os
import time
import threading
import requests
from flask import Flask
from telegram import Bot

# === Config from Environment Variables ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # e.g., "@your_channel" or "-1001234567890"
API_URL = "https://nsfw-noob-api.vercel.app/xnxx/10/desi"
DELAY_SECONDS = 20

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
sent_urls = set()

def fetch_and_send():
    global sent_urls
    while True:
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            data = response.json()

            for item in data:
                content_url = item.get("content_url")
                title = item.get("title", "No Title")
                thumb = item.get("thumb")

                if content_url and content_url not in sent_urls:
                    caption = f"{title}\n{content_url}"

                    try:
                        if thumb:
                            bot.send_photo(chat_id=CHANNEL_ID, photo=thumb, caption=caption)
                        else:
                            bot.send_message(chat_id=CHANNEL_ID, text=caption)
                    except Exception as send_err:
                        print(f"Send failed: {send_err}")

                    sent_urls.add(content_url)
                    time.sleep(2)

            print("Cycle complete. Sleeping...")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(DELAY_SECONDS)

# Simple health check for Render
@app.route('/')
def index():
    return "Bot is running 24/7."

# Run background thread on Flask start
def start_bot_thread():
    thread = threading.Thread(target=fetch_and_send)
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    start_bot_thread()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
  
