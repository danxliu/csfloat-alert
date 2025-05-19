import os
from dotenv import load_dotenv
import time
import requests
import toml
import asyncio
from desktop_notifier import DesktopNotifier

load_dotenv()

API_KEY = os.getenv('API_KEY')
config = toml.load("config.toml")

update_interval = config["general"]["update_interval"]
def_indexes = config["items"]["def_indexes"]
paint_indexes = config["items"]["paint_indexes"]
alert_prices = config["items"]["alert_prices"]


def get_lowest_price_item(def_index, paint_index):
    try:
        url = f"https://csfloat.com/api/v1/listings?sort_by=lowest_price&def_index={def_index}&paint_index={paint_index}&sort_by=lowest_price&type=buy_now&limit=1"
        res = requests.get(url, headers={'Authorization': API_KEY}).json()
        data = res["data"]
        if (not data):
            return None
        best = res["data"][0]
        return best
    except:
        print("[ERROR]: Unable to get listings.")
        return None


async def main():
    notifier = DesktopNotifier()

    while True:
        for def_index, paint_index, alert_price in zip(def_indexes, paint_indexes, alert_prices):
            item = get_lowest_price_item(def_index, paint_index)
            if (not item):
                continue

            if (item["price"] <= alert_price * 100):
                url = f"https://csfloat.com/item/{item['id']}"
                await notifier.send(title=f"CSFloat Item Alert", message=url)

        time.sleep(update_interval)

asyncio.run(main())
