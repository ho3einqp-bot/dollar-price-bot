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


async def send_message():
    url = f"https://api.brsapi.ir/Market/Gold_Currency.php?key={API_KEY}"

    response = requests.get(url, timeout=20)
    data = response.json()

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
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30
    )

    bot = Bot(token=TOKEN, request=request)

    await bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

    print("Message sent successfully!")


asyncio.run(send_message())
