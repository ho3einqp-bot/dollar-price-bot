
import os
import requests
from datetime import datetime
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@dollarpriced"

def get_prices():
    # فعلاً تستی؛ بعد از اتصال API واقعی جایگزین می‌کنیم
    return {
        "dollar": "95,000",
        "gold": "7,200,000",
        "coin": "82,000,000"
    }

def send_message():
    prices = get_prices()

    text = f"""
💵 دلار آزاد: {prices['dollar']} تومان

🟡 طلای ۱۸ عیار: {prices['gold']} تومان

🪙 سکه امامی: {prices['coin']} تومان

⏰ بروزرسانی: {datetime.now().strftime('%H:%M')}
"""

    bot = Bot(token=TOKEN)
    bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

send_message()
