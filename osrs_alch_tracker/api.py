import os
import json
import time
import urllib.request
import urllib.error

USER_AGENT = "OSRS-Alch-Dashboard/1.0 (Windows; Contact: osrs-tools)"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
MAPPING_CACHE_FILE = os.path.join(CACHE_DIR, "mapping.json")
MAPPING_CACHE_TTL = 86400 * 3 # 3 days cache for static mapping

NATURE_RUNE_ID = 561
FIRE_RUNE_ID = 554

def fetch_url_json(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

class OSRSPricesAPI:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.mapping = {} # id -> item metadata
        self.latest_prices = {} # id -> {high, highTime, low, lowTime}
        self.volumes_24h = {} # id -> volume
        self.nature_rune_price = 170
        self.nature_rune_bid = 168
        self.nature_rune_ask = 172
        self.last_sync_time = 0

    def load_mapping(self, force_refresh=False):
        """Loads items mapping from local cache or API."""
        now = time.time()
        if not force_refresh and os.path.exists(MAPPING_CACHE_FILE):
            try:
                with open(MAPPING_CACHE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    cache_time = data.get("_timestamp", 0)
                    if now - cache_time < MAPPING_CACHE_TTL:
                        self.mapping = data.get("items", {})
                        return len(self.mapping)
            except Exception:
                pass

        try:
            url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
            raw_list = fetch_url_json(url)
            self.mapping = {
                str(item["id"]): {
                    "id": item["id"],
                    "name": item.get("name", "Unknown"),
                    "highalch": item.get("highalch", 0),
                    "lowalch": item.get("lowalch", 0),
                    "limit": item.get("limit", 0) or 0,
                    "members": item.get("members", False),
                    "value": item.get("value", 0)
                }
                for item in raw_list
                if "id" in item
            }
            # Cache locally
            with open(MAPPING_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"_timestamp": now, "items": self.mapping}, f)
            return len(self.mapping)
        except Exception as e:
            print(f"Error fetching mapping: {e}")
            # If fetch fails, try to load stale cache
            if os.path.exists(MAPPING_CACHE_FILE):
                with open(MAPPING_CACHE_FILE, "r", encoding="utf-8") as f:
                    self.mapping = json.load(f).get("items", {})
            return len(self.mapping)

    def fetch_latest_and_volumes(self):
        """Fetches /latest prices and /24h volume data."""
        try:
            latest_url = "https://prices.runescape.wiki/api/v1/osrs/latest"
            latest_res = fetch_url_json(latest_url)
            self.latest_prices = latest_res.get("data", {})

            # Update Nature Rune live prices
            nat_data = self.latest_prices.get(str(NATURE_RUNE_ID), {})
            high = nat_data.get("high")
            low = nat_data.get("low")
            if high and low:
                self.nature_rune_bid = min(low, high)
                self.nature_rune_ask = max(low, high)
                self.nature_rune_price = self.nature_rune_bid
            elif high:
                self.nature_rune_ask = high
                self.nature_rune_bid = max(1, high - 2)
                self.nature_rune_price = self.nature_rune_bid
            elif low:
                self.nature_rune_ask = low + 2
                self.nature_rune_bid = low
                self.nature_rune_price = low
        except Exception as e:
            print(f"Error fetching latest prices: {e}")

        try:
            vol_url = "https://prices.runescape.wiki/api/v1/osrs/24h"
            vol_res = fetch_url_json(vol_url)
            vol_data = vol_res.get("data", {})
            self.volumes_24h = {}
            for item_id_str, vinfo in vol_data.items():
                high_vol = vinfo.get("highPriceVolume", 0) or 0
                low_vol = vinfo.get("lowPriceVolume", 0) or 0
                self.volumes_24h[item_id_str] = high_vol + low_vol
        except Exception as e:
            print(f"Error fetching 24h volumes: {e}")

        self.last_sync_time = time.time()

    def get_price(self, item_id, strategy="patient"):
        """Returns price based on strategy: 'patient' (bid) or 'instant' (ask)."""
        bid, ask = self.get_bid_ask(item_id)
        if strategy == "instant":
            return ask or bid or 0
        else: # patient
            return bid or ask or 0

    def get_bid_ask(self, item_id):
        """Returns (bid, ask) tuple for an item ensuring bid <= ask."""
        pdata = self.latest_prices.get(str(item_id), {})
        low = pdata.get("low")
        high = pdata.get("high")
        if low and high:
            bid = min(low, high)
            ask = max(low, high)
        elif low:
            bid = low
            ask = low
        elif high:
            bid = high
            ask = high
        else:
            bid = 0
            ask = 0
        return bid, ask
