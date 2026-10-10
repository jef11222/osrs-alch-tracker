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

OVERNIGHT_CACHE_FILE = os.path.join(CACHE_DIR, "overnight_cache.json")
OVERNIGHT_CACHE_TTL = 1800 # 30 minutes cache for overnight timeseries dips

BOND_ITEM_ID = 13190
BOND_CACHE_FILE = os.path.join(CACHE_DIR, "bond_cache.json")
BOND_CACHE_TTL = 900 # 15 minutes cache for bond market stats

NATURE_RUNE_ID = 561
FIRE_RUNE_ID = 554

def fetch_url_json(url, timeout=10):
    if not str(url).startswith("https://prices.runescape.wiki/"):
        raise ValueError(f"Disallowed API host: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def calc_percentile(data, p):
    if not data:
        return 0
    s = sorted(data)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    d = k - f
    return int(round(s[f] + d * (s[c] - s[f])))

OVERNIGHT_CANDIDATE_SPECS = [
    # F2P Heavy Staples - Rune Gear
    {"id": 1163, "group": "rune", "verdict": "⭐ Top F2P Pick: Catches 3-6 AM dumps with massive volume"},
    {"id": 1347, "group": "rune", "verdict": "🔥 High Margin: Dips to ~24,200 gp in the middle of the night"},
    {"id": 1373, "group": "rune", "verdict": "⚔️ Reliable F2P Heavy: Sells at ~24,300 gp, alchs for 24,960 gp"},
    {"id": 1127, "group": "rune", "verdict": "🛡️ Heavy Tank Alch: Highest alch value in F2P (39k gp)"},
    {"id": 1079, "group": "rune", "verdict": "🦵 Consistent F2P Staple: Extremely flat price with ~100k daily volume"},
    {"id": 1093, "group": "rune", "verdict": "👗 Deep Discount: Same 38.4k alch as legs but currently cheaper"},
    {"id": 1319, "group": "rune", "verdict": "🗡️ Heavy 2H Weapon: High alch value staple"},
    {"id": 1113, "group": "rune", "verdict": "⛓️ Solid F2P Alch: 30k gp alch value with steady dips"},
    {"id": 1147, "group": "rune", "verdict": "🪖 Low-Cap F2P Pick: 11.5k alch with quick fill rate"},
    {"id": 1201, "group": "rune", "verdict": "🛡️ High Defense Alch: 32.6k alch value staple"},
    {"id": 1185, "group": "rune", "verdict": "🛡️ Fast F2P Shield: Steady 23k alch value"},
    {"id": 1333, "group": "rune", "verdict": "⚔️ Classic F2P Weapon: High turnover from smithers and f2p drops"},
    {"id": 1303, "group": "rune", "verdict": "🗡️ Clean F2P Weapon: 19.2k alch value with steady fill rate"},
    {"id": 1275, "group": "rune", "verdict": "⛏️ Skilling Tool: 19.2k alch value from clue hunters"},
    # F2P High-ROI Adamant & Crafting Staples
    {"id": 1123, "group": "adamant", "verdict": "⚡ Ultra-Fast Volume: 380k daily volume, fills in minutes"},
    {"id": 1111, "group": "adamant", "verdict": "📦 Cheap Budget Filler: Fast volume for remaining coins"},
    {"id": 1073, "group": "adamant", "verdict": "📦 High Volume Filler: Adamant armor alch staple"},
    {"id": 1135, "group": "dhide", "verdict": "🏹 Crafting Staple: 125 buy limit, high volume F2P/P2P"},
    # P2P High-Volume / High-Margin Staples
    {"id": 9342, "group": "bolt", "verdict": "👑 Best P2P Overnight: Stackable bolt with 11k buy limit"},
    {"id": 9341, "group": "bolt", "verdict": "💎 High Limit Stackable: 11k buy limit for huge overnight piles"},
    {"id": 1393, "group": "staff", "verdict": "🪄 Massive Crafter Dumps: High volume P2P battlestaff staple"},
    {"id": 1395, "group": "staff", "verdict": "🪄 High Volume Staff: 9.3k alch with continuous dumping"},
    {"id": 1397, "group": "staff", "verdict": "🪄 Pure Crafter Staff: Enormous daily turnover"},
    {"id": 1399, "group": "staff", "verdict": "🪄 Reliable Staff Alch: Steady margins overnight"},
    {"id": 2503, "group": "dhide", "verdict": "🐲 High Demand Leather: 8.0k alch with massive craft volume"},
    {"id": 2497, "group": "dhide", "verdict": "🐲 Quick Chaps Alch: High limit dragonhide filler"},
    {"id": 1305, "group": "dragon", "verdict": "🐉 Reliable P2P Heavy: Massive daily volume from slayer dumps"},
    {"id": 1149, "group": "dragon", "verdict": "🎯 Deep Dip Sniper: Giant +1,800+ gp profit per cast"},
    {"id": 4587, "group": "dragon", "verdict": "⚔️ Iconic P2P Weapon: 60k alch with continuous trading"},
    {"id": 1377, "group": "dragon", "verdict": "🪓 Ultra Heavy Alch: 120k gp alch value with deep margins"},
    {"id": 1215, "group": "dragon", "verdict": "🗡️ Slayer Dump Staple: 18k alch value with quick fills"},
    {"id": 4091, "group": "mystic", "verdict": "🧙‍♂️ High-Tier Robe: 72k alch value from clue hunters and PvM"},
    {"id": 4093, "group": "mystic", "verdict": "🧙‍♂️ High-Tier Skirt: 48k alch value with +900+ gp margins"},
]

class OSRSPricesAPI:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.mapping = {} # id -> item metadata
        self.latest_prices = {} # id -> {high, highTime, low, lowTime}
        self.volumes_24h = {} # id -> volume
        self.volumes_5m = {} # id -> {high, low, total}
        self.five_min_prices = {} # id -> {avg_high, avg_low, high_vol, low_vol}
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

        # Fetch 5-minute real-time transaction velocity & volume-weighted prices
        try:
            five_url = "https://prices.runescape.wiki/api/v1/osrs/5m"
            five_res = fetch_url_json(five_url)
            five_data = five_res.get("data", {})
            self.volumes_5m = {}
            self.five_min_prices = {}
            for item_id_str, vinfo in five_data.items():
                h_vol = vinfo.get("highPriceVolume", 0) or 0
                l_vol = vinfo.get("lowPriceVolume", 0) or 0
                avg_high = vinfo.get("avgHighPrice")
                avg_low = vinfo.get("avgLowPrice")
                self.volumes_5m[item_id_str] = {
                    "high": h_vol,
                    "low": l_vol,
                    "total": h_vol + l_vol
                }
                self.five_min_prices[item_id_str] = {
                    "avg_high": avg_high,
                    "avg_low": avg_low,
                    "high_vol": h_vol,
                    "low_vol": l_vol
                }
        except Exception as e:
            print(f"Error fetching 5m data: {e}")

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
        score: 3 (fast), 2 (steady), 1 (slow), 0 (stale) - for table sorting
        """
        iid_str = str(item_id)
        now = time.time()
        pdata = self.latest_prices.get(iid_str, {})
        low_time = pdata.get("lowTime", 0) or 0
        high_time = pdata.get("highTime", 0) or 0
        last_trade = max(low_time, high_time)
        secs_since_trade = (now - last_trade) if last_trade > 0 else 999999

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

        # Stale Detection: If quote has had no trades in >= 45m (2700s)
        if secs_since_trade >= 2700:
            return "slow", "⚠️ Stale (>45m)", 120, 0

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

    def get_quote_metrics(self, item_id):
        """
        Returns rich metadata for an item:
        - last_trade_time: float timestamp
        - age_secs: seconds since last recorded trade
        - age_str: human-readable time (e.g. '2m ago', '48m ago', '3h ago')
        - is_stale: bool (True if >= 45 minutes)
        - vol_5m_total: int
        - vol_5m_low: int
        - vol_5m_high: int
        - vol_24h: int
        - spread_gp: int (ask - bid)
        - spread_pct: float ((ask - bid) / ask * 100)
        - is_wide_spread: bool (True if spread >= 25% and vol_24h < 5000)
        """
        iid_str = str(item_id)
        now = time.time()
        pdata = self.latest_prices.get(iid_str, {})
        ht = pdata.get("highTime", 0) or 0
        lt = pdata.get("lowTime", 0) or 0
        last_trade_time = max(ht, lt)

        if last_trade_time > 0:
            age_secs = max(0, int(now - last_trade_time))
            if age_secs < 60:
                age_str = f"{age_secs}s ago"
            elif age_secs < 3600:
                age_str = f"{age_secs // 60}m ago"
            elif age_secs < 86400:
                age_str = f"{age_secs // 3600}h {(age_secs % 3600) // 60}m ago"
            else:
                age_str = ">24h ago"
            is_stale = age_secs >= 2700
        else:
            age_secs = 999999
            age_str = "No recent trades"
            is_stale = True

        v5 = self.volumes_5m.get(iid_str, {})
        vol_5m_low = v5.get("low", 0) or 0
        vol_5m_high = v5.get("high", 0) or 0
        vol_5m_total = v5.get("total", 0) or 0
        vol_24h = self.volumes_24h.get(iid_str, 0) or 0

        bid, ask = self.get_bid_ask(item_id)
        spread_gp = max(0, ask - bid) if (bid and ask) else 0
        spread_pct = (spread_gp / ask * 100.0) if ask > 0 else 0.0
        is_wide_spread = (spread_pct >= 25.0 and vol_24h < 5000) if ask > 0 else False

        spike_info = self.get_spike_info(item_id)
        is_spike, spike_pct, lat_low, avg_low_p, vol_5m_l = spike_info

        finfo = self.five_min_prices.get(iid_str, {}) if hasattr(self, "five_min_prices") else {}
        avg_high_p = finfo.get("avg_high") or 0

        return {
            "last_trade_time": last_trade_time,
            "age_secs": age_secs,
            "age_str": age_str,
            "is_stale": is_stale,
            "vol_5m_low": vol_5m_low,
            "vol_5m_high": vol_5m_high,
            "vol_5m_total": vol_5m_total,
            "vol_24h": vol_24h,
            "spread_gp": spread_gp,
            "spread_pct": spread_pct,
            "is_wide_spread": is_wide_spread,
            "is_spike": is_spike,
            "spike_pct": spike_pct,
            "latest_low": lat_low,
            "avg_low": avg_low_p,
            "avg_high": avg_high_p
        }

    def get_spike_info(self, item_id):
        """
        Detects if the latest 1-trade price is an unconfirmed 1-item spike compared to 5m VWAP.
        Returns: (is_spike: bool, spike_diff_pct: float, latest_price: int, vwap_price: int, low_vol_5m: int)
        """
        iid_str = str(item_id)
        pdata = self.latest_prices.get(iid_str, {})
        latest_low = pdata.get("low") or 0

        finfo = self.five_min_prices.get(iid_str, {}) if hasattr(self, "five_min_prices") else {}
        avg_low = finfo.get("avg_low") or 0
        low_vol = finfo.get("low_vol", 0) or 0

        if latest_low > 0 and avg_low > 0:
            diff_pct = ((avg_low - latest_low) / avg_low) * 100.0
            # If latest single trade is >= 4% cheaper than 5m volume average, but 5m sell volume is < 5 items:
            if diff_pct >= 4.0 and low_vol < 5:
                return True, diff_pct, latest_low, avg_low, low_vol
            elif diff_pct >= 8.0:
                return True, diff_pct, latest_low, avg_low, low_vol

        return False, 0.0, latest_low, avg_low, low_vol

    def get_price(self, item_id, strategy="patient", basis="5m"):
        """Returns price based on strategy: 'patient' (bid), 'smart' (bid+1), or 'instant' (ask), using specified basis."""
        bid, ask = self.get_bid_ask(item_id, basis=basis)
        strat_lower = str(strategy).lower()
        if "instant" in strat_lower:
            return ask or bid or 0
        elif "smart" in strat_lower:
            if bid and ask and ask > bid:
                return bid + 1
            return bid or ask or 0
        else: # patient
            return bid or ask or 0

    def get_bid_ask(self, item_id, basis="5m"):
        """
        Returns (bid, ask) tuple for an item ensuring bid <= ask.
        If basis == '5m' (default), uses 5-minute volume-weighted averages when available,
        falling back to /latest or merging seamlessly if one side (low/high) is missing.
        """
        iid_str = str(item_id)
        pdata = self.latest_prices.get(iid_str, {})
        lat_low = pdata.get("low")
        lat_high = pdata.get("high")

        finfo = self.five_min_prices.get(iid_str, {}) if hasattr(self, "five_min_prices") else {}
        avg_low = finfo.get("avg_low")
        avg_high = finfo.get("avg_high")

        if basis == "5m":
            # Prioritize 5m volume average, cleanly fall back to latest 1-tick trade
            bid = avg_low if avg_low is not None else lat_low
            ask = avg_high if avg_high is not None else lat_high
        else:
            # basis == "latest": prioritize latest 1-tick trade, fall back to 5m volume average
            bid = lat_low if lat_low is not None else avg_low
            ask = lat_high if lat_high is not None else avg_high

        if bid is not None and ask is not None:
            b = int(round(bid))
            a = int(round(ask))
            return min(b, a), max(b, a)
        elif bid is not None:
            b = int(round(bid))
            return b, b
        elif ask is not None:
            a = int(round(ask))
            return a, a
        else:
            return 0, 0

    def get_overnight_data(self, force_refresh=False):
        """
        Fetches and caches 48h and 7d historical timeseries data for prime overnight alch candidates.
        Calculates realistic 25th percentile (Safe Morning Fill) and 10th percentile (Deep-Dip Sniper)
        bids with 7-day floor support checks and fill confidence ratings.
        """
        now = time.time()
        if not force_refresh and os.path.exists(OVERNIGHT_CACHE_FILE):
            try:
                with open(OVERNIGHT_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    if now - cached.get("_timestamp", 0) < OVERNIGHT_CACHE_TTL:
                        return cached.get("items", [])
            except Exception:
                pass

        results = []
        for spec in OVERNIGHT_CANDIDATE_SPECS:
            iid = spec["id"]
            iid_str = str(iid)
            mdata = self.mapping.get(iid_str, {})
            name = mdata.get("name", f"Item #{iid}")
            alch = mdata.get("highalch", 0)
            if not alch or alch <= 0:
                continue

            limit = mdata.get("limit", 70) or 70
            is_mem = mdata.get("members", False)
            verdict = spec.get("verdict", "")

            # Fallback values from latest
            platest = self.latest_prices.get(iid_str, {})
            cur_low = platest.get("low") or platest.get("high") or 0
            cur_high = platest.get("high") or platest.get("low") or 0

            safe_bid = cur_low
            deep_bid = max(1, cur_low - 10)
            daily_vol = self.volumes_24h.get(iid_str, 0)

            # Try to fetch 1h timeseries for accurate percentiles
            try:
                url = f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=1h&id={iid}"
                res = fetch_url_json(url, timeout=5)
                data = res.get("data", [])
                if data:
                    h48 = data[-48:] if len(data) >= 48 else data
                    lows_48 = [c["avgLowPrice"] for c in h48 if c.get("avgLowPrice") and c["avgLowPrice"] > 0]
                    vols_48 = [c.get("lowPriceVolume", 0) + c.get("highPriceVolume", 0) for c in h48]

                    week_168 = data[-168:] if len(data) >= 168 else data
                    lows_week = [c["avgLowPrice"] for c in week_168 if c.get("avgLowPrice") and c["avgLowPrice"] > 0]
                    min_week = min(lows_week) if lows_week else 0

                    if lows_48:
                        safe_bid = calc_percentile(lows_48, 25) + 5
                        raw_deep = calc_percentile(lows_48, 10) + 5
                        deep_bid = max(raw_deep, min_week + 5) if min_week > 0 else raw_deep
                        total_v48 = sum(vols_48)
                        daily_vol = total_v48 // 2 if len(h48) >= 24 else total_v48
            except Exception:
                pass

            # Fill confidence
            if daily_vol >= 50000:
                conf_safe = "🟢 99% Very High"
                conf_deep = "🟢 92% High"
            elif daily_vol >= 20000:
                conf_safe = "🟢 95% High"
                conf_deep = "🟡 88% Solid"
            elif daily_vol >= 5000:
                conf_safe = "🟡 90% Solid"
                conf_deep = "🟠 80% Moderate"
            else:
                conf_safe = "🟡 85% Moderate"
                conf_deep = "🟠 75% Speculative"

            results.append({
                "id": iid,
                "name": name,
                "members": is_mem,
                "alch": alch,
                "limit": limit,
                "safe_bid": safe_bid,
                "deep_bid": deep_bid,
                "safe_profit": alch - safe_bid,
                "deep_profit": alch - deep_bid,
                "daily_vol": daily_vol,
                "conf_safe": conf_safe,
                "conf_deep": conf_deep,
                "group": spec.get("group", "general"),
                "verdict": verdict
            })

        # Save cache
        try:
            with open(OVERNIGHT_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"_timestamp": now, "items": results}, f)
        except Exception:
            pass

        return results

    def get_bond_data(self, force_refresh=False):
        """Fetches live Old School Bond (13190) prices, spread, and 7-day percentile dip analysis."""
        now = time.time()
        if not force_refresh and os.path.exists(BOND_CACHE_FILE):
            try:
                with open(BOND_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                if now - cached.get("_timestamp", 0) < BOND_CACHE_TTL:
                    return cached.get("data", {})
            except Exception:
                pass

        insta_buy = 0
        insta_sell = 0
        try:
            latest_res = fetch_url_json(f"https://prices.runescape.wiki/api/v1/osrs/latest?id={BOND_ITEM_ID}")
            item_data = latest_res.get("data", {}).get(str(BOND_ITEM_ID), {})
            insta_buy = item_data.get("high") or 0
            insta_sell = item_data.get("low") or 0
        except Exception as e:
            print(f"[API] Error fetching live bond latest: {e}")

        series = []
        floor_7d = 0
        peak_7d = 0
        daily_vol = 0
        safe_bid = 0
        deep_bid = 0
        try:
            ts_res = fetch_url_json(f"https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=1h&id={BOND_ITEM_ID}")
            series = ts_res.get("data", [])
            if series:
                # 48h data
                h48 = series[-48:] if len(series) >= 48 else series
                lows_48 = [c["avgLowPrice"] for c in h48 if c.get("avgLowPrice") and c["avgLowPrice"] > 0]
                vols_48 = [c.get("lowPriceVolume", 0) + c.get("highPriceVolume", 0) for c in h48]
                if vols_48:
                    daily_vol = sum(vols_48) // 2 if len(h48) >= 24 else sum(vols_48)

                # 7d data (168 hours)
                w168 = series[-168:] if len(series) >= 168 else series
                lows_7d = [c["avgLowPrice"] for c in w168 if c.get("avgLowPrice") and c["avgLowPrice"] > 0]
                highs_7d = [c["avgHighPrice"] for c in w168 if c.get("avgHighPrice") and c["avgHighPrice"] > 0]
                if lows_7d:
                    floor_7d = min(lows_7d)
                if highs_7d:
                    peak_7d = max(highs_7d)

                if lows_48:
                    safe_bid = calc_percentile(lows_48, 25) + 10_000
                    deep_bid = calc_percentile(lows_48, 10) + 10_000
                    if floor_7d > 0:
                        deep_bid = max(deep_bid, floor_7d + 10_000)
        except Exception as e:
            print(f"[API] Error fetching bond timeseries: {e}")

        # Fallbacks
        if insta_buy == 0 and series:
            for s in reversed(series):
                if s.get("avgHighPrice"):
                    insta_buy = s["avgHighPrice"]
                    break
        if insta_sell == 0 and series:
            for s in reversed(series):
                if s.get("avgLowPrice"):
                    insta_sell = s["avgLowPrice"]
                    break

        if safe_bid == 0:
            safe_bid = max(insta_sell + 10_000, int(insta_buy * 0.96)) if insta_buy > 0 else 11_000_000
        if deep_bid == 0:
            deep_bid = max(insta_sell - 50_000, int(insta_buy * 0.94)) if insta_buy > 0 else 10_700_000
        if floor_7d == 0:
            floor_7d = int(safe_bid * 0.97)
        if peak_7d == 0:
            peak_7d = int(insta_buy * 1.05) if insta_buy > 0 else 12_500_000
        if daily_vol == 0:
            daily_vol = 12_000

        patient_savings = max(0, insta_buy - safe_bid) if insta_buy > safe_bid else (insta_buy - insta_sell if insta_buy > insta_sell else 0)

        result_data = {
            "id": BOND_ITEM_ID,
            "name": "Old School Bond",
            "insta_buy": insta_buy,
            "insta_sell": insta_sell,
            "safe_bid": safe_bid,
            "deep_bid": deep_bid,
            "patient_savings": patient_savings,
            "floor_7d": floor_7d,
            "peak_7d": peak_7d,
            "daily_vol": daily_vol,
            "timestamp": now
        }

        try:
            with open(BOND_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"_timestamp": now, "data": result_data}, f)
        except Exception:
            pass

        return result_data


