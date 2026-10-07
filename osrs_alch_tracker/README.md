# 🧙‍♂️ OSRS High Alchemy & Crafting Profit Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](https://www.microsoft.com/windows)

A real-time, desktop companion tool for **Old School RuneScape (OSRS)** that monitors live Grand Exchange prices via the official OSRS Wiki Real-time Prices API. It tracks high-margin High Alchemy flips, evaluates Craft-then-Alch skilling recipes, manages 4-hour Grand Exchange buy limit timers, tracks Nature Rune bank stockpiles, and logs session profit and Magic XP.

---

## ✨ Key Features

- **⚡ Real-Time Price Sync:** Fetches live bid/ask margins and 24-hour traded volumes directly from the OSRS Wiki API.
- **⏱️ Dynamic 4-Hour GE Limit Tracking:**
  - Real-time limit depletion (e.g. buying 20 out of 70 items displays `50 / 70`).
  - Active cooldown indicators (e.g. `0 (3h 24m)`) that automatically reset when the 4-hour window expires.
  - Desktop toast alerts and audio chimes when limits reset.
- **🌿 Nature Rune Stockpile Tracker:**
  - Track owned Nature Runes in your bank.
  - Cart automatically alerts you if you need to purchase more runes before your alch session.
  - Automatically deducts used runes on session log.
  - Optional fixed cost override (leave empty to use live standard GE prices).
- **💰 Smart Cash Stack Baseline (`Max Afford`):**
  - Accurately calculates how many items you can afford based on your remaining budget and active limits without zeroing out table rows.
  - Easily toggle budget constraints on or off for unlimited calculations.
- **🛒 Grand Exchange Cart & Fast 1-Click Pasting:**
  - **Click Column #1:** Copies exact buy quantity.
  - **Click Column #2 (Name):** Copies item name for fast GE search.
  - **Click Column #3 (Bid):** Copies patient buy offer price.
  - **Click Column #4 (Ask):** Copies instant buy price.
  - **Right-Click:** Set custom quantities or remove items.
- **🔨 Craft & Alch Breakdown:**
  - Interactive recipe tree comparing the cost of buying raw materials, crafting, and alching vs. buying finished items.
  - Filter recipes by your in-game Crafting, Fletching, and Magic levels.
- **📋 RuneLite Bank Tag Exporter:**
  - 1-click export of your active cart or master profitable alch list as a RuneLite Bank Tag tab (`banktags,1,...`).
- **🔍 Instant Live Search & Filter:**
  - Filter items in real time as you type (`Ctrl + F`).
  - Min Profit threshold (leave blank to display all items including break-even and XP alchs).

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| **`F5`** | Immediately refresh live market prices |
| **`Ctrl + F`** | Jump to search bar |
| **`Esc`** | Clear active search |
| **`Enter`** | Apply cash stack or filter input |

---

## 🚀 Getting Started

### Option 1: Standalone Windows Executable (No Python Required)
1. Download `OSRS_Alch_Tracker.exe` from the latest [GitHub Releases](https://github.com/jef11222/osrs-alch-tracker/releases).
2. Double-click to run! All user settings, session history, and timers persist locally in a `data/` folder.

### Option 2: Running from Source
Ensure you have **Python 3.10+** installed:
```bash
# Clone the repository
git clone https://github.com/jef11222/osrs-alch-tracker.git
cd osrs-alch-tracker

# Run the application
python main.py
```

### Option 3: Building Standalone Executable with PyInstaller
```bash
pip install pyinstaller
python -m PyInstaller --noconsole --onefile --name "OSRS_Alch_Tracker" main.py
```

---

## 📁 Project Structure

```
osrs-alch-tracker/
├── api.py               # OSRS Wiki Real-time Prices API client
├── crafting.py          # Crafting & fletching recipe definitions
├── state.py             # State persistence (config, 4h timers, session log)
├── gui.py               # Tkinter GUI (custom dark theme, tooltips, tables)
├── main.py              # Application entry point
├── run.bat              # 1-click launch batch script
├── Launch_Dashboard.vbs # Silent background launcher
└── .gitignore           # Ignores build artifacts and local caches
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
