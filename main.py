import os
import asyncio
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="Pokemon Center UK bot is working!"
    )

asyncio.run(main())