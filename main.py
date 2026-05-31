import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.pokemoncenter.com/en-gb/category/new-releases"

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
    "Pokémon Center Elite Trainer Box",
    "Prismatic Evolutions",
    "Team Rocket",
    "Destined Rivals"
]

SEEN = set()

async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )

async def check_site():
    try:
        r = requests.get(
            URL,
            timeout=30,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(r.text, "html.parser")
        page_text = soup.get_text(" ", strip=True)

        found = []

        for keyword in KEYWORDS:
            if keyword.lower() in page_text.lower():
                found.append(keyword)

        new_items = []

        for item in found:
            if item not in SEEN:
                SEEN.add(item)
                new_items.append(item)

        if new_items:
            await send_message(
                "🚨 Pokémon Center UK Alert!\n\n"
                + "\n".join(new_items)
                + f"\n\n{URL}"
            )

    except Exception as e:
        await send_message(f"❌ Bot error:\n{e}")

async def runner():
    while True:
        await check_site()
        await asyncio.sleep(300)

asyncio.run(runner())