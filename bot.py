import os
import asyncio
import requests
from datetime import datetime
from telegram import Bot
from telegram.request import HTTPXRequest

=========================

SETTINGS

=========================

BOT_TOKEN = os.environ["BOT_TOKEN"]
BRS_API_KEY = os.environ["BRS_API_KEY"]

CHANNEL = "@dollarpriced"

API_URL = "https://api.brsapi.ir/Market/Gold_Currency.php"

=========================

GET MARKET DATA

=========================

def get_market_data():

headers_list = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://brsapi.ir/"
    },
    {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*"
    }
]

last_error = None

for attempt, headers in enumerate(headers_list, start=1):

    try:

        response = requests.get(
            API_URL,
            params={"key": BRS_API_KEY},
            headers=headers,
            timeout=30
        )

        print(f"BRS API attempt {attempt}")
        print(f"BRS API status: {response.status_code}")

        if response.status_code != 200:
            print(f"BRS response: {response.text[:500]}")
            continue

        data = response.json()

        if not isinstance(data, dict):
            raise ValueError("BRS API returned invalid JSON structure.")

        if "gold" not in data or "currency" not in data:
            raise ValueError("BRS API response does not contain gold/currency data.")

        return data

    except Exception as error:
        last_error = error
        print(f"API attempt {attempt} failed: {error}")

raise RuntimeError(
    f"BRS API failed after all attempts. Last error: {last_error}"
)

=========================

FIND PRICE

=========================

def find_item(items, symbol):

for item in items:

    if item.get("symbol") == symbol:
        return item

raise ValueError(f"Symbol not found: {symbol}")

=========================

SEND TELEGRAM MESSAGE

=========================

async def send_message():

data = get_market_data()

# Dollar
dollar = find_item(
    data["currency"],
    "USD"
)

# Gold 18K
gold = find_item(
    data["gold"],
    "IR_GOLD_18K"
)

# Emami Coin
coin = find_item(
    data["gold"],
    "IR_COIN_EMAMI"
)

dollar_price = int(dollar["price"])
gold_price = int(gold["price"])
coin_price = int(coin["price"])

update_time = datetime.now().strftime("%H:%M")

text = f"""💰 قیمت لحظه‌ای بازار

💵 دلار آزاد: {dollar_price:,} تومان

🟡 طلای ۱۸ عیار: {gold_price:,} تومان

🪙 سکه امامی: {coin_price:,} تومان

⏰ آخرین بروزرسانی: {update_time}

📊 منبع: BRS API
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

=========================

RUN

=========================

if name == "main":
asyncio.run(send_message())
