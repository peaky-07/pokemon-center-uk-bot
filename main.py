import os
import json
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

URL = "https://www.pokemoncenter.com/en-gb/category/trading-card-game"

SEEN_FILE = "seen_products.json"


async def send_message(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        disable_web_page_preview=False
    )


def load_seen():
    try:
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_seen(products):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(products), f)


def get_products():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/124 Safari/537.36"
        )
    }

def get_products():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/124 Safari/537.36"
        )
    }

    r = requests.get(
        URL,
        timeout=30,
        headers=headers
    )

    print(f"Status: {r.status_code}")
    print(f"HTML length: {len(r.text)}")
    print("FIRST 1000 CHARS:")
    print(r.text[:1000])

    soup = BeautifulSoup(r.text, "html.parser")

    products = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/product/" not in href:
            continue

        name = a.get_text(" ", strip=True)

        if not name:
            continue

        if href.startswith("/"):
            href = "https://www.pokemoncenter.com" + href

        products[href] = name

    return products

async def check_site():
    try:
        current_products = get_products()

        print(f"Found {len(current_products)} products")

        seen = load_seen()

        new_urls = set(current_products.keys()) - seen

        if new_urls:
            for url in new_urls:
                name = current_products[url]

                await send_message(
                    f"🚨 NEW POKÉMON CENTER UK PRODUCT\n\n"
                    f"{name}\n\n"
                    f"{url}"
                )

            seen.update(new_urls)
            save_seen(seen)

    except Exception as e:
        print(f"ERROR: {e}")

        try:
            await send_message(f"❌ Bot error:\n{e}")
        except:
            pass


async def heartbeat():
    try:
        await send_message("✅ Pokémon Center UK bot is alive")
    except:
        pass


async def runner():
    counter = 0

    while True:
        await check_site()

        counter += 1

        if counter >= 288:
            await heartbeat()
            counter = 0

        await asyncio.sleep(300)


asyncio.run(runner())