import os
import asyncio
import requests
from datetime import datetime
from telegram import Bot
from telegram.request import HTTPXRequest

TOKEN = os.environ["BOT_TOKEN"]
API_KEY = os.environ["BRS_API_KEY"]
CHANNEL = "@dollarpriced"


def get_price(data_list, symbol):
    for item in data_list:
        if item["symbol"] == symbol:
            return f"{item['price']:,}"
    return "---"


def get_market_data():
    url = "https://Api.BrsApi.ir/Market/Gold_Currency.php"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Connection": "keep-alive"
    }

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                params={"key": API_KEY},
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"API attempt {attempt + 1}/5 failed: {e}")

            if attempt < 4:
                time_to_wait = 5
                print(f"Retrying in {time_to_wait} seconds...")
                import time
                time.sleep(time_to_wait)
            else:
                raise


async def send_message():

    data = get_market_data()

    dollar = get_price(data["currency"], "USD")
    tether = get_price(data["currency"], "USDT_IRT")

    gold18 = get_price(data["gold"], "IR_GOLD_18K")
    emami = get_price(data["gold"], "IR_COIN_EMAMI")

    text = f"""💵 قیمت لحظه‌ای بازار

🇺🇸 دلار: {dollar} تومان

💲 تتر: {tether} تومان

🟡 طلای ۱۸ عیار: {gold18} تومان

🪙 سکه امامی: {emami} تومان

🕒 بروزرسانی:
{datetime.now().strftime('%Y/%m/%d - %H:%M')}
"""

    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=60,
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


asyncio.run(send_message())
