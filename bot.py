import os
import asyncio
import requests
from datetime import datetime
from telegram import Bot
from telegram.request import HTTPXRequest


TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["BRS_API_KEY"]
CHANNEL = "@dollarpriced"

API_URL = "https://brsapi.ir/Api/Market/Gold_Currency.php"


def get_market_data():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://brsapi.ir/",
    }

    response = requests.get(
        API_URL,
        params={"key": API_KEY},
        headers=headers,
        timeout=30
    )

    print("BRS API status:", response.status_code)
    print("BRS API URL:", response.url)

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise ValueError("BRS API returned unexpected data")

    return data


def find_price(data, symbol):
    for item in data.get("gold", []):
        if item.get("symbol") == symbol:
            return item.get("price")

    for item in data.get("currency", []):
        if item.get("symbol") == symbol:
            return item.get("price")

    return None


async def send_message():

    data = get_market_data()

    dollar = find_price(data, "USD")
    gold = find_price(data, "IR_GOLD_18K")
    coin = find_price(data, "IR_COIN_EMAMI")

    if dollar is None:
        raise ValueError("USD price not found")

    if gold is None:
        raise ValueError("18K gold price not found")

    if coin is None:
        raise ValueError("Emami coin price not found")

    now = datetime.now().strftime("%H:%M")

    text = f"""
💵 دلار آزاد: {dollar:,} تومان

🟡 طلای ۱۸ عیار: {gold:,} تومان

🪙 سکه امامی: {coin:,} تومان

⏰ بروزرسانی: {now}
"""

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    bot = Bot(
        token=TOKEN,
        request=request
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

    print("Message sent successfully!")


if __name__ == "__main__":
    asyncio.run(send_message())
