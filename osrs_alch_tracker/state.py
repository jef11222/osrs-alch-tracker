import os
import sys
import json
import time
import shutil

def get_app_data_dir():
    if getattr(sys, "frozen", False):
        base = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
        return os.path.join(base, "OSRS_Alch_Tracker", "data")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

STATE_DIR = get_app_data_dir()
CONFIG_FILE = os.path.join(STATE_DIR, "config.json")
TIMERS_FILE = os.path.join(STATE_DIR, "timers.json")
SESSION_FILE = os.path.join(STATE_DIR, "session.json")

DEFAULT_CONFIG = {
    "members": True,
    "f2p": False,
    "cash_stack": 5000000,
    "min_volume": 5000,
    "max_item_cost": 500000,
    "strategy": "patient",  # 'patient' (bid) or 'instant' (ask)
    "auto_refresh_mins": 2,
    "alert_threshold_alch": 200,
    "sound_enabled": True,
    "desktop_alerts": True,
    "free_alchs_mode": False,
    "custom_nature_price": 0, # 0 = use live price
    "alch_speed": 1200,
    "player_levels": {
        "Crafting": 99,
        "Fletching": 99,
        "Magic": 99
    },
    "only_usable_recipes": False,
    "use_cash_stack": True,
    "min_profit": None, # None or 0 = show everything
    "owned_nature_runes": 0,
    "speed_filter": "All"
}

class AppState:
    def __init__(self):
        os.makedirs(STATE_DIR, exist_ok=True)
        # Migrate existing state if transitioning to user AppData
        old_local_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
        if STATE_DIR != old_local_dir and os.path.exists(old_local_dir):
            for fname in ("config.json", "timers.json", "session.json"):
                old_f = os.path.join(old_local_dir, fname)
                new_f = os.path.join(STATE_DIR, fname)
                if os.path.exists(old_f) and not os.path.exists(new_f):
                    try:
                        shutil.copy2(old_f, new_f)
                    except Exception:
                        pass
        self.config = dict(DEFAULT_CONFIG)
        self.timers = {} # item_id -> {"name": ..., "bought_time": ..., "qty": ...}
        self.session = {
            "total_alchs": 0,
            "total_profit": 0,
            "total_xp": 0,
            "history": []
        }
        self.cart_items = {} # item_id -> qty
        self.alert_history = [] # list of recent alert strings
        self.notified_timers = set() # track timers already notified
        self.last_alerted_profits = {} # item_id -> profit_ea

        self.load_all()

    def load_all(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
            except Exception:
                pass

        if os.path.exists(TIMERS_FILE):
            try:
                with open(TIMERS_FILE, "r", encoding="utf-8") as f:
                    self.timers = json.load(f)
            except Exception:
                pass

        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    self.session.update(json.load(f))
            except Exception:
                pass

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def save_timers(self):
        try:
            with open(TIMERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.timers, f, indent=2)
        except Exception as e:
            print(f"Error saving timers: {e}")

    def save_session(self):
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump(self.session, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")

    def add_timer(self, item_id, item_name, qty):
        now = time.time()
        iid_str = str(item_id)
        existing = self.timers.get(iid_str)
        if existing and (now - existing.get("bought_time", 0)) < 14400:
            # Active timer already running within 4 hours: keep original anchor time, add qty!
            existing["qty"] = existing.get("qty", 0) + qty
            existing["name"] = item_name
        else:
            self.timers[iid_str] = {
                "name": item_name,
                "bought_time": now,
                "qty": qty
            }
        if iid_str in self.notified_timers:
            self.notified_timers.remove(iid_str)
        self.save_timers()

    def get_remaining_limit(self, item_id, base_limit):
        """Returns (remaining_qty, seconds_left, is_on_cooldown)"""
        if not base_limit or base_limit <= 0:
            return 1000, 0, False

        iid_str = str(item_id)
        tinfo = self.timers.get(iid_str)
        if not tinfo:
            return base_limit, 0, False

        now = time.time()
        elapsed = now - tinfo.get("bought_time", 0)
        if elapsed >= 14400: # Expired
            return base_limit, 0, False

        bought_qty = tinfo.get("qty", 0)
        remaining = max(0, base_limit - bought_qty)
        seconds_left = max(0, 14400 - elapsed)
        return remaining, seconds_left, True

    def remove_timer(self, item_id):
        if str(item_id) in self.timers:
            del self.timers[str(item_id)]
            self.save_timers()

    def check_expired_timers(self):
        now = time.time()
        expired = []
        for iid, tinfo in list(self.timers.items()):
            elapsed = now - tinfo["bought_time"]
            if elapsed >= 14400: # 4 hours
                if iid not in self.notified_timers:
                    expired.append(tinfo["name"])
                    self.notified_timers.add(iid)
        return expired

    def log_alch_batch(self, item_id, item_name, qty, buy_price, nat_price, alch_val):
        entry_id = str(int(time.time() * 1000)) + f"_{item_id}"
        profit_ea = alch_val - (buy_price + nat_price)
        total_profit = qty * profit_ea

        entry = {
            "id": entry_id,
            "item_id": item_id,
            "time": time.strftime("%H:%M:%S"),
            "item": item_name,
            "qty": qty,
            "buy_price": buy_price,
            "nat_price": nat_price,
            "alch_val": alch_val,
            "profit": total_profit
        }

        self.session["history"].insert(0, entry)
        self.session["history"] = self.session["history"][:200]
        self._recalc_session_totals()

        # Deduct nature runes from stockpile if tracked
        owned = self.config.get("owned_nature_runes", 0)
        if owned > 0:
            self.config["owned_nature_runes"] = max(0, owned - qty)
            self.save_config()
        self.save_session()
        return entry

    def update_session_entry(self, entry_id, new_qty, new_buy_price, new_nat_price):
        for entry in self.session["history"]:
            if entry["id"] == entry_id:
                entry["qty"] = new_qty
                entry["buy_price"] = new_buy_price
                entry["nat_price"] = new_nat_price
                alch_val = entry["alch_val"]
                entry["profit"] = new_qty * (alch_val - (new_buy_price + new_nat_price))
                break
        self._recalc_session_totals()
        self.save_session()

    def delete_session_entry(self, entry_id):
        self.session["history"] = [e for e in self.session["history"] if e["id"] != entry_id]
        self._recalc_session_totals()
        self.save_session()

    def _recalc_session_totals(self):
        total_alchs = 0
        total_profit = 0
        for entry in self.session["history"]:
            total_alchs += entry.get("qty", 0)
            total_profit += entry.get("profit", 0)
        self.session["total_alchs"] = total_alchs
        self.session["total_profit"] = total_profit
        self.session["total_xp"] = total_alchs * 65.0

    def reset_session(self):
        self.session = {
            "total_alchs": 0,
            "total_profit": 0,
            "total_xp": 0,
            "history": []
        }
        self.save_session()
