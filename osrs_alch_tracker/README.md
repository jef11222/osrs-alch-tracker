# OSRS High Alchemy & Crafting Profit Dashboard

A standalone desktop companion application for Old School RuneScape that tracks live Grand Exchange prices, finds the best high alchemy profit margins, compares craft-then-alch recipes, tracks your profit sessions, and alerts you when 4-hour GE buy limits expire.

---

## 🚀 How to Launch
* **1-Click:** Double-click [`run.bat`](file:///c:/Users/jef11/Documents/antigravity/noble-volta/osrs_alch_tracker/run.bat).
* **Or via Terminal:** Run `python main.py` inside this folder.

---

## ⚡ Features & Controls

### 1. Top Controls & Live Filters
* **Members / F2P Toggles:** Switch between full game alchables and F2P-only items.
* **Cash Stack:** Type in your current gold (e.g. `5M` or `5000000`). Automatically calculates how many of each item you can afford.
* **Max Item Price:** Filter out expensive alchables (e.g. `50k`) so your cash stack doesn't get tied up in high-ticket items.
* **Min Volume:** Filters out dead/illiquid items.
* **Strategy:** Toggle between **Patient (Bid)** for maximum profit offers, or **Instant (Ask)** for instant fills.
* **Auto-Refresh:** Configurable timer (`1m`, `2m`, `5m`, `10m`, `Off`) with a live countdown clock.
* **Explorer's Ring Toggle:** Check `Explorer Ring (0 Nat)` to calculate profits assuming free daily casts.

### 2. Nature Rune Buy Tracker & Override
* Displays live **Bid**, **Ask**, and **18,000 / 4h GE Buy Limit** for Nature Runes.
* **Custom Nat Cost:** If you bought a stack of Nature Runes at e.g. `165 gp`, enter it into the box and press Enter. All alch and craft profit calculations instantly update to reflect your exact purchase price!

### 3. Shopping Cart & GE Slot Counter
* **Slots Used (X / 8):** Keeps track of your available Grand Exchange offer slots.
* **Double-click any item** in the High Alch tab to add it to your shopping cart with the max affordable quantity.
* Shows **Total Invested**, **Remaining Cash Stack**, and **Expected Batch Profit**.
* Click **"✓ Log Cart & Start Timers"** to automatically record the alchs into your session log and start their 4-hour GE limit countdowns!

### 4. 🔨 Craft & Alch Tab
* Compares buying materials, crafting the item, and alching it vs. buying pre-made finished items.
* **Stats Filter:** Enter your Crafting, Fletching, and Magic levels.
* Check **"Only Show Usable Recipes"** to hide recipes you don't have the stats for, or uncheck it to see all recipes with level requirements clearly displayed.

### 5. ⏱️ 4-Hour GE Limit Reset Timers
* Automatically counts down the 4-hour Grand Exchange limit for items you've bought.
* **Persistent:** Timers are saved locally in `data/timers.json`. If you close the app or restart your PC, your timers resume accurately!
* **Desktop Notifications & Chimes:** When a 4-hour limit resets, you receive a desktop popup alert and sound notification:
  > *"⏰ GE 4-Hour Limit Reset! You can now buy Rune 2h swords on the GE again!"*

### 6. 📊 Session Profit Tracker
* Displays **Total Casts Done**, **Realized Net Profit**, **Magic XP Gained**, and **Nature Runes Burnt**.
* Keeps a timestamped log history of every batch you complete.

### 7. Click-to-Copy Quick Actions
* **Single Click:** Copies the exact item name to your Windows clipboard so you can immediately `Ctrl + V` into the Grand Exchange search bar.
