import os
import sys
import json
import time
import urllib.request
import urllib.error

USER_AGENT = "OSRS-Alch-Dashboard/1.0 (Windows; Contact: osrs-tools)"

def get_app_cache_dir():
    if getattr(sys, "frozen", False):
        base = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
        return os.path.join(base, "OSRS_Alch_Tracker", "cache")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

CACHE_DIR = get_app_cache_dir()
MAPPING_CACHE_FILE = os.path.join(CACHE_DIR, "mapping.json")
MAPPING_CACHE_TTL = 86400 * 3 # 3 days cache for static mapping

NATURE_RUNE_ID = 561
FIRE_RUNE_ID = 554

def fetch_url_json(url, timeout=10):
    if not str(url).startswith("https://prices.runescape.wiki/"):
        raise ValueError(f"Disallowed API host: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

class OSRSPricesAPI:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.mapping = {} # id -> item metadata
        self.latest_prices = {} # id -> {high, highTime, low, lowTime}
        self.volumes_24h = {} # id -> volume
        self.volumes_5m = {} # id -> {high, low, total}
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
        """Fetches /latest prices, /5m trade velocity, and /24h volume data."""
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

        # Fetch 5-minute real-time transaction velocity
        try:
            five_url = "https://prices.runescape.wiki/api/v1/osrs/5m"
            five_res = fetch_url_json(five_url)
            five_data = five_res.get("data", {})
            self.volumes_5m = {}
            for item_id_str, vinfo in five_data.items():
                h_vol = vinfo.get("highPriceVolume", 0) or 0
                l_vol = vinfo.get("lowPriceVolume", 0) or 0
                self.volumes_5m[item_id_str] = {
                    "high": h_vol,
                    "low": l_vol,
                    "total": h_vol + l_vol
                }
        except Exception as e:
            print(f"Error fetching 5m volumes: {e}")

        # Fetch 24-hour total volumes
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

    def get_fill_speed_info(self, item_id, target_qty=70):
        """
        Calculates transaction fill velocity based on 5m lowPriceVolume and trade timestamps.
        Returns: (category: str, badge: str, est_minutes: int, score: int)
        category: 'fast' | 'steady' | 'slow'
        score: 3 (fast), 2 (steady), 1 (slow) - for table sorting
        """
        iid_str = str(item_id)
        now = time.time()
        pdata = self.latest_prices.get(iid_str, {})
        low_time = pdata.get("lowTime", 0) or 0
        secs_since_trade = (now - low_time) if low_time > 0 else 999999

        v5 = self.volumes_5m.get(iid_str, {})
        bid_vol_5m = v5.get("low", 0)
        total_5m = v5.get("total", 0)
        v24 = self.volumes_24h.get(iid_str, 0)

        # Estimate hourly sell rate into bids
        if bid_vol_5m > 0:
            rate_per_hour = bid_vol_5m * 12
        elif total_5m > 0:
            rate_per_hour = (total_5m * 12) // 2
        else:
            rate_per_hour = (v24 // 24) // 2

        qty = max(1, target_qty)

        # Determine Category & Time Estimate
        if secs_since_trade < 600 and (bid_vol_5m >= 8 or rate_per_hour >= 60):
            mins = max(3, int(round((qty / max(1, rate_per_hour)) * 60)))
            mins = min(15, mins)
            return "fast", f"⚡ Fast (~{mins}m)", mins, 3
        elif secs_since_trade < 3600 and (rate_per_hour >= 15 or v24 >= 1000):
            mins = max(15, int(round((qty / max(1, rate_per_hour)) * 60)))
            mins = min(60, mins)
            return "steady", f"⏱️ Steady (~{mins}m)", mins, 2
        else:
            return "slow", "🐢 Slow (>1h)", 120, 1

    def get_price(self, item_id, strategy="patient"):
        """Returns price based on strategy: 'patient' (bid), 'smart' (bid+1), or 'instant' (ask)."""
        bid, ask = self.get_bid_ask(item_id)
        strat_lower = str(strategy).lower()
        if "instant" in strat_lower:
            return ask or bid or 0
        elif "smart" in strat_lower:
            if bid and ask and ask > bid:
                return bid + 1
            return bid or ask or 0
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
