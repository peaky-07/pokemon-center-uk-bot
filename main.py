import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.pokemoncenter.com/en-gb/category/trading-card-game"

KEYWORDS = [
    "pre-order",
    "preorder",
    "Elite Trainer Box",
    "ETB",
    "Booster Bundle",
    "Booster Box",
    "Premium Collection",
    "Collection",
    "Tin",
    "Bundle",
    "Trainer Box",
    "Pokémon Center Elite Trainer Box"
]

async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    try:
        r = requests.get(URL, timeout=30)
        soup = BeautifulSoup(r.text, "html.parser")

        page_text = soup.get_text(" ", strip=True)

        matches = []

        for keyword in KEYWORDS:
            if keyword.lower() in page_text.lower():
                matches.append(keyword)

        if matches:
            await send_message(
                "Pokemon Center UK match found:\n\n" +
                "\n".join(matches)
            )

    except Exception as e:
        await send_message(f"Bot error: {e}")

async def runner():
    while True:
        await main()
        await asyncio.sleep(300)  # check every 5 minutes

asyncio.run(runner())