import os
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHANNEL = "@dollarpriced"

async def send_message():
    bot = Bot(token=TOKEN)

    text = f"""
💵 دلار آزاد: 95,000 تومان

🟡 طلای ۱۸ عیار: 7,200,000 تومان

🪙 سکه امامی: 82,000,000 تومان

⏰ بروزرسانی: {datetime.now().strftime('%H:%M')}
"""

    await bot.send_message(
        chat_id=CHANNEL,
        text=text
    )

    print("Message sent successfully!")

asyncio.run(send_message())
