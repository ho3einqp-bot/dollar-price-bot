import os
import asyncio
import requests
from datetime import datetime
from telegram import Bot
from telegram.request import HTTPXRequest

BOT_TOKEN = os.environ["BOT_TOKEN"]
BRS_API_KEY = os.environ["BRS_API_KEY"]

CHANNEL = "@dollarpriced"

API_URL = "https://api.brsapi.ir/Market/Gold_Currency.php"


def get_market_data():
    response = requests.get(
        API_URL,
        params={"key": BRS_API_KEY},
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        },
        timeout=30
    )

    print("BRS API status:", response.status_code)

    if response.status_code != 200:
        print("BRS API response:", response.text[:500])
        raise RuntimeError(
            f"BRS API returned HTTP {response.status_code}"
        )

    return response.json()


def find_item(items, symbol):
    for item in items:
        if item.get("symbol") == symbol:
            return item

    raise ValueError(f"Symbol not found: {symbol}")


async def send_message():

    data = get_market_data()

    dollar = find_item(data["currency"], "USD")
    gold = find_item(data["gold"], "IR_GOLD_18K")
    coin = find_item(data["gold"], "IR_COIN_EMAMI")

    dollar_price = int(dollar["price"])
    gold_price = int(gold["price"])
    coin_price = int(coin["price"])

    update_time = datetime.now().strftime("%H:%M")

    text = f"""💰 قیمت لحظه‌ای بازار

💵 دلار آزاد: {dollar_price:,} تومان

🟡 طلای ۱۸ عیار: {gold_price:,} تومان

🪙 سکه امامی: {coin_price:,} تومان

⏰ آخرین بروزرسانی: {update_time}
"""

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    bot = Bot(
        token=BOT_TOKEN,
        request=request
    )

    await bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

    print("Message sent successfully!")


if __name__ == "__main__":
    asyncio.run(send_message())
