import os
import sys
import time
import math
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Sound support on Windows
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

from api import OSRSPricesAPI, NATURE_RUNE_ID
from crafting import CRAFTING_RECIPES
from skilling_guide import SKILLING_GUIDES, get_xp_for_level, get_level_for_xp
from state import AppState
from updater import APP_VERSION, check_for_updates, UpdateDialog, WhatsNewDialog
from bridge_server import BridgeServer
import datetime
import webbrowser

# Hall-of-Fame All-Time Workhorses (The gold standards of OSRS High Alchemy)
WORKHORSE_ITEMS = [
    {
        "id": 1079,
        "name": "Rune platelegs",
        "limit": 70,
        "members": False,
        "verdict": "👑 All-Time King: Highest alch floor (38.4k), zero price risk, instant liquidity."
    },
    {
        "id": 1093,
        "name": "Rune plateskirt",
        "limit": 70,
        "members": False,
        "verdict": "👑 Platelegs Twin: Identical 38.4k alch value, massive supply from smithers."
    },
    {
        "id": 1319,
        "name": "Rune 2h sword",
        "limit": 70,
        "members": False,
        "verdict": "⚔️ Top Volume Weapon: Constant supply from smithing & clue scrolls, fills fast."
    },
    {
        "id": 1201,
        "name": "Rune kiteshield",
        "limit": 70,
        "members": False,
        "verdict": "🛡️ High Alch Staple: Very steady 32.6k value, rock-solid profit margins."
    },
    {
        "id": 1113,
        "name": "Rune chainbody",
        "limit": 70,
        "members": False,
        "verdict": "🛡️ Solid 30k Floor: Reliable slayer drop supply, high profit spreads."
    },
    {
        "id": 1373,
        "name": "Rune battleaxe",
        "limit": 70,
        "members": False,
        "verdict": "🪓 Slayer Classic: Consistently traded at 24.9k floor with rapid turnover."
    },
    {
        "id": 1347,
        "name": "Rune warhammer",
        "limit": 70,
        "members": False,
        "verdict": "🔨 High Turnover: Frequent undercut sellers create wide profit spreads."
    },
    {
        "id": 1185,
        "name": "Rune sq shield",
        "limit": 70,
        "members": False,
        "verdict": "🛡️ Steady Earner: Reliable 23k floor with steady patient fills."
    },
    {
        "id": 1123,
        "name": "Adamant platebody",
        "limit": 125,
        "members": False,
        "verdict": "📦 High 125 Limit: Low capital (~1M batch), great F2P/P2P staple."
    },
    {
        "id": 1163,
        "name": "Rune full helm",
        "limit": 70,
        "members": False,
        "verdict": "🪖 Steady Volume: Reliable 21.1k alch value, quick fill cycles."
    },
    {
        "id": 1333,
        "name": "Rune scimitar",
        "limit": 70,
        "members": False,
        "verdict": "🗡️ High Liquidity: F2P/P2P staple, fast trading velocity."
    },
    {
        "id": 1213,
        "name": "Rune dagger",
        "limit": 70,
        "members": False,
        "verdict": "🗡️ Low Capital: Low buy price (~4.3k), high volume from monster drops."
    },
    {
        "id": 1397,
        "name": "Air battlestaff",
        "limit": 18000,
        "members": True,
        "verdict": "⚡ Massive 18k Limit: Premier crafting & bulk alch item with huge daily turnover."
    },
    {
        "id": 1135,
        "name": "Green d'hide body",
        "limit": 125,
        "members": False,
        "verdict": "🏹 Bulk Crafting Staple: Low buy price, high 125 limit, safe margins."
    },
    {
        "id": 1215,
        "name": "Dragon dagger",
        "limit": 70,
        "members": True,
        "verdict": "🗡️ Slayer Favorite: 18k alch value with deep undercut sell volume."
    }
]

def get_market_timing_info():
    """
    Analyzes global OSRS market liquidity based on UTC time and concurrent player activity curves.
    Peak player activity occurs between 14:00 and 22:00 UTC (~120k-165k players).
    Off-peak / sleepers window occurs between 02:00 and 10:00 UTC (~45k-75k players).
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    hour = now_utc.hour + now_utc.minute / 60.0
    time_str = now_utc.strftime("%H:%M UTC")

    if 14.0 <= hour < 22.0:
        pct = int(75 + 25 * (1.0 - abs(hour - 18.0) / 4.0))
        pct = max(75, min(100, pct))
        est_players = f"~{int(115000 + (pct - 75) * 1800):,} online"
        bar_n = int(round(pct / 10))
        bar = "█" * bar_n + "░" * (10 - bar_n)
        return {
            "time_str": time_str,
            "badge": "🟢 Peak Liquidity Window (Fast Fills & High Volume)",
            "badge_color": "#2ecc71",
            "activity": f"Activity: [{bar}] {pct}% ({est_players})",
            "advice": "💡 Market Tip: Prime EU/US trading hours! Buy orders fill in 2-5m. Best time for Fast Fills & Workhorses.",
            "rec_cat": "fast"
        }
    elif 22.0 <= hour or hour < 2.0:
        pct = 65
        est_players = "~95,000 online"
        bar = "██████░░░░"
        return {
            "time_str": time_str,
            "badge": "🟡 Evening Wind-Down (Good for Setting Overnight Orders)",
            "badge_color": "#f1c40f",
            "activity": f"Activity: [{bar}] 65% ({est_players})",
            "advice": "💡 Market Tip: US late evening. Volume tapering off. Queue up high-profit overnight bids.",
            "rec_cat": "overnight"
        }
    elif 2.0 <= hour < 10.0:
        pct = 40
        est_players = "~55,000 online"
        bar = "████░░░░░░"
        return {
            "time_str": time_str,
            "badge": "🌙 Off-Peak / Sleepers Window (Wide Overnight Margins)",
            "badge_color": "#9b59b6",
            "activity": f"Activity: [{bar}] 40% ({est_players})",
            "advice": "💡 Market Tip: Lowest global player count. Patient low bids fill with zero competition from undercut sellers.",
            "rec_cat": "overnight"
        }
    else: # 10.0 <= hour < 14.0
        pct = 60
        est_players = "~85,000 online"
        bar = "██████░░░░"
        return {
            "time_str": time_str,
            "badge": "🌅 Morning Ramp-Up (Volume Building)",
            "badge_color": "#3498db",
            "activity": f"Activity: [{bar}] 60% ({est_players})",
            "advice": "💡 Market Tip: European morning. Market liquidity is steadily accelerating towards afternoon peak.",
            "rec_cat": "workhorse"
        }

def format_gp(val):
    if val is None:
        return "0 gp"
    try:
        val = int(val)
        if abs(val) >= 1_000_000:
            return f"{val / 1_000_000:.2f}M gp"
        elif abs(val) >= 1_000:
            return f"{val:,} gp"
        else:
            return f"{val} gp"
    except Exception:
        return f"{val} gp"

def parse_cash_input(text):
    text = str(text).strip().upper().replace(",", "").replace(" ", "").replace("GP", "")
    if not text:
        return 0
    multiplier = 1
    if text.endswith("K"):
        multiplier = 1_000
        text = text[:-1]
    elif text.endswith("M"):
        multiplier = 1_000_000
        text = text[:-1]
    elif text.endswith("B"):
        multiplier = 1_000_000_000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return 0

class FloatingToast(tk.Toplevel):
    def __init__(self, parent, title, message, duration=5000):
        super().__init__(parent)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#2d2d30", highlightthickness=1, highlightbackground="#f39c12")

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        w = 340
        h = 85
        x = screen_w - w - 25
        y = screen_h - h - 60
        self.geometry(f"{w}x{h}+{x}+{y}")

        title_lbl = tk.Label(self, text=title, font=("Segoe UI", 10, "bold"), fg="#f39c12", bg="#2d2d30")
        title_lbl.pack(anchor="w", padx=12, pady=(8, 2))

        msg_lbl = tk.Label(self, text=message, font=("Segoe UI", 9), fg="#ffffff", bg="#2d2d30", wraplength=310, justify="left")
        msg_lbl.pack(anchor="w", padx=12, pady=(0, 8))

        self.after(duration, self.destroy)
        self.bind("<Button-1>", lambda e: self.destroy())

class EditSessionDialog(tk.Toplevel):
    def __init__(self, parent, entry, on_save_callback):
        super().__init__(parent)
        self.title("Edit Session Entry")
        self.geometry("380x300")
        self.resizable(False, False)
        self.configure(bg="#252528")
        self.transient(parent)
        self.grab_set()

        self.entry = entry
        self.on_save_callback = on_save_callback

        # Center dialog
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 190
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 150
        self.geometry(f"+{x}+{y}")

        lbl_title = tk.Label(self, text=f"Edit: {entry['item']}", font=("Segoe UI", 11, "bold"), fg="#f39c12", bg="#252528")
        lbl_title.pack(pady=(12, 10))

        form = tk.Frame(self, bg="#252528")
        form.pack(padx=20, fill="x")

        # Qty
        tk.Label(form, text="Quantity Bought:", fg="#cccccc", bg="#252528").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_qty = tk.Entry(form, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        self.ent_qty.insert(0, str(entry.get("qty", 1)))
        self.ent_qty.grid(row=0, column=1, pady=5, padx=5)

        # Buy Price
        tk.Label(form, text="Bought At (ea):", fg="#cccccc", bg="#252528").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_buy = tk.Entry(form, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        self.ent_buy.insert(0, str(entry.get("buy_price", 0)))
        self.ent_buy.grid(row=1, column=1, pady=5, padx=5)

        # Nat Cost
        tk.Label(form, text="Nature Cost (ea):", fg="#cccccc", bg="#252528").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_nat = tk.Entry(form, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        self.ent_nat.insert(0, str(entry.get("nat_price", 0)))
        self.ent_nat.grid(row=2, column=1, pady=5, padx=5)

        # Alch Val (Readonly)
        tk.Label(form, text="High Alch Val:", fg="#888888", bg="#252528").grid(row=3, column=0, sticky="w", pady=5)
        lbl_alch = tk.Label(form, text=f"{entry.get('alch_val', 0):,} gp (Fixed)", fg="#888888", bg="#252528")
        lbl_alch.grid(row=3, column=1, sticky="w", pady=5, padx=5)

        # 4h Cooldown auto-sync note
        tk.Label(form, text="💡 4h GE buy limit cooldown will auto-sync with this quantity.",
                 fg="#888888", bg="#252528", font=("Segoe UI", 8, "italic")).grid(row=4, column=0, columnspan=2, pady=(4, 0))

        # Dynamic Profit preview
        self.lbl_profit_preview = tk.Label(self, text="Realized Profit: ...", font=("Segoe UI", 10, "bold"), fg="#2ecc71", bg="#252528")
        self.lbl_profit_preview.pack(pady=8)

        self.ent_qty.bind("<KeyRelease>", self.update_preview)
        self.ent_buy.bind("<KeyRelease>", self.update_preview)
        self.ent_nat.bind("<KeyRelease>", self.update_preview)
        self.update_preview()

        # Buttons
        btn_box = tk.Frame(self, bg="#252528")
        btn_box.pack(pady=10)

        tk.Button(btn_box, text="Save Changes", command=self.save, bg="#27ae60", fg="#ffffff", relief="flat", padx=10, cursor="hand2").pack(side="left", padx=6)
        tk.Button(btn_box, text="Cancel", command=self.destroy, bg="#7f8c8d", fg="#ffffff", relief="flat", padx=10, cursor="hand2").pack(side="left", padx=6)

    def update_preview(self, event=None):
        try:
            q = int(self.ent_qty.get().strip().replace(",", ""))
            b = int(self.ent_buy.get().strip().replace(",", ""))
            n = int(self.ent_nat.get().strip().replace(",", ""))
            alch_v = self.entry.get("alch_val", 0)
            profit_ea = alch_v - (b + n)
            total = q * profit_ea
            color = "#2ecc71" if total >= 0 else "#e74c3c"
            self.lbl_profit_preview.config(text=f"Realized Profit: {total:+,} gp ({profit_ea:+,} ea)", fg=color)
        except Exception:
            self.lbl_profit_preview.config(text="Realized Profit: [Invalid Input]", fg="#e74c3c")

    def save(self):
        try:
            q = int(self.ent_qty.get().strip().replace(",", ""))
            b = int(self.ent_buy.get().strip().replace(",", ""))
            n = int(self.ent_nat.get().strip().replace(",", ""))
            if q < 0 or b < 0 or n < 0:
                messagebox.showerror("Invalid Input", "Quantity and prices cannot be negative.")
                return
            self.on_save_callback(self.entry["id"], q, b, n)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid whole numbers.")


class EditTimerDialog(tk.Toplevel):
    """Dialog to manually adjust quantity bought on an active 4h GE cooldown timer."""
    def __init__(self, parent, item_id, tinfo, on_save_callback):
        super().__init__(parent)
        self.title("Edit 4h GE Limit Timer")
        self.geometry("380x190")
        self.configure(bg="#252528")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.item_id = item_id
        self.tinfo = tinfo
        self.on_save_callback = on_save_callback

        lbl_title = tk.Label(self, text=f"Edit Timer: {tinfo.get('name', 'Item')}", font=("Segoe UI", 11, "bold"), fg="#f39c12", bg="#252528")
        lbl_title.pack(pady=(15, 8))

        form = tk.Frame(self, bg="#252528")
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Quantity Bought:", fg="#cccccc", bg="#252528").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_qty = tk.Entry(form, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff")
        self.ent_qty.insert(0, str(tinfo.get("qty", 0)))
        self.ent_qty.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form, text="💡 Set to 0 to clear this cooldown timer.", fg="#888888", bg="#252528", font=("Segoe UI", 8, "italic")).grid(row=1, column=0, columnspan=2, pady=(4, 0))

        btn_box = tk.Frame(self, bg="#252528")
        btn_box.pack(pady=15)

        tk.Button(btn_box, text="Save Changes", command=self.save, bg="#27ae60", fg="#ffffff", relief="flat", padx=10, cursor="hand2").pack(side="left", padx=6)
        tk.Button(btn_box, text="Cancel", command=self.destroy, bg="#7f8c8d", fg="#ffffff", relief="flat", padx=10, cursor="hand2").pack(side="left", padx=6)

        self.ent_qty.focus_set()
        self.ent_qty.select_range(0, tk.END)
        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.destroy())

    def save(self):
        try:
            q = int(self.ent_qty.get().strip().replace(",", ""))
            if q < 0:
                messagebox.showerror("Invalid Input", "Quantity cannot be negative.")
                return
            self.on_save_callback(self.item_id, q)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

class ToolTip:
    """Lightweight hover tooltip for widgets."""
    def __init__(self, widget, text, delay=350):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hide_tip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.delay, self.show_tip)

    def unschedule(self):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def show_tip(self):
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 15
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify="left",
                         background="#181818", foreground="#f1f1f1",
                         relief="solid", borderwidth=1,
                         font=("Segoe UI", 8), padx=7, pady=4)
        label.pack()
        tw.lift()

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class HeadingToolTip:
    """Dynamic hover tooltip for Treeview column headings."""
    def __init__(self, tree, col_tooltips_map, delay=300):
        self.tree = tree
        self.tooltips = col_tooltips_map
        self.delay = delay
        self.tip_window = None
        self.curr_col = None
        self.id = None
        self.tree.bind("<Motion>", self.on_motion, add="+")
        self.tree.bind("<Leave>", self.on_leave, add="+")

    def on_motion(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if col != self.curr_col:
                self.curr_col = col
                self.hide_tip()
                tip_text = self.tooltips.get(col)
                if tip_text:
                    x = self.tree.winfo_rootx() + event.x + 10
                    y = self.tree.winfo_rooty() + 25
                    if self.id:
                        self.tree.after_cancel(self.id)
                    self.id = self.tree.after(self.delay, lambda: self.show_tip(x, y, tip_text))
        else:
            self.on_leave()

    def on_leave(self, event=None):
        if self.id:
            self.tree.after_cancel(self.id)
            self.id = None
        self.curr_col = None
        self.hide_tip()

    def show_tip(self, x, y, text):
        if self.tip_window or not text:
            return
        self.tip_window = tw = tk.Toplevel(self.tree)
        tw.wm_overrideredirect(True)
        tw.attributes("-topmost", True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=text, justify="left",
                         background="#181818", foreground="#f1f1f1",
                         relief="solid", borderwidth=1,
                         font=("Segoe UI", 8), padx=7, pady=4)
        label.pack()
        tw.lift()

    def hide_tip(self):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

class RowToolTip:
    """Dynamic hover tooltip card for Treeview data rows."""
    def __init__(self, tree, get_tooltip_callback, delay=400):
        self.tree = tree
        self.get_tooltip_callback = get_tooltip_callback
        self.delay = delay
        self.tip_window = None
        self.curr_iid = None
        self.id = None
        self.tree.bind("<Motion>", self.on_motion, add="+")
        self.tree.bind("<Leave>", self.on_leave, add="+")
        self.tree.bind("<ButtonPress>", self.on_leave, add="+")
        self.tree.bind("<MouseWheel>", self.on_leave, add="+")

    def on_motion(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region in ("cell", "tree"):
            iid = self.tree.identify_row(event.y)
            if iid and iid != self.curr_iid:
                self.curr_iid = iid
                self.hide_tip()
                if self.id:
                    self.tree.after_cancel(self.id)
                gx = event.x_root
                gy = event.y_root
                self.id = self.tree.after(self.delay, lambda: self.show_tip(gx, gy, iid))
            elif not iid:
                self.on_leave()
        else:
            self.on_leave()

    def on_leave(self, event=None):
        if self.id:
            self.tree.after_cancel(self.id)
            self.id = None
        self.curr_iid = None
        self.hide_tip()

    def show_tip(self, mouse_x, mouse_y, iid):
        if self.tip_window or not iid:
            return
        tip_info = self.get_tooltip_callback(iid)
        if not tip_info:
            return

        try:
            self.tip_window = tw = tk.Toplevel(self.tree)
            tw.wm_overrideredirect(True)
            tw.attributes("-topmost", True)

            border_col = "#e67e22" if tip_info.get("has_warning") else "#4a4a52"
            card = tk.Frame(tw, bg="#1a1a1d", highlightthickness=1,
                            highlightbackground=border_col, padx=12, pady=9)
            card.pack()

            # Title
            title_box = tk.Frame(card, bg="#1a1a1d")
            title_box.pack(fill="x", pady=(0, 4))
            tk.Label(title_box, text=tip_info.get("title", ""), font=("Segoe UI", 9, "bold"),
                     fg=tip_info.get("title_color", "#f1c40f"), bg="#1a1a1d").pack(side="left")
            if tip_info.get("subtitle"):
                tk.Label(title_box, text=f" ({tip_info['subtitle']})", font=("Segoe UI", 8),
                         fg="#888888", bg="#1a1a1d").pack(side="left")

            tk.Frame(card, bg="#2f2f35", height=1).pack(fill="x", pady=(2, 6))

            # Metric Rows
            for label_text, val_text, val_color in tip_info.get("rows", []):
                rf = tk.Frame(card, bg="#1a1a1d")
                rf.pack(fill="x", pady=1)
                tk.Label(rf, text=label_text, font=("Segoe UI", 8), fg="#9e9ea7",
                         bg="#1a1a1d", width=23, anchor="w").pack(side="left")
                is_num = any(char.isdigit() for char in val_text)
                tk.Label(rf, text=val_text, font=("Segoe UI", 8, "bold" if is_num else "normal"),
                         fg=val_color, bg="#1a1a1d", anchor="e").pack(side="right")

            # Warnings
            warnings = tip_info.get("warnings", [])
            if warnings:
                tk.Frame(card, bg="#2f2f35", height=1).pack(fill="x", pady=(5, 5))
                for w in warnings:
                    tk.Label(card, text=f"⚠️ {w}", font=("Segoe UI", 8, "bold"),
                             fg="#e67e22", bg="#1a1a1d", wraplength=340, justify="left", anchor="w").pack(fill="x", pady=1)

            # Footer
            if tip_info.get("hint"):
                tk.Frame(card, bg="#2f2f35", height=1).pack(fill="x", pady=(5, 3))
                tk.Label(card, text=tip_info["hint"], font=("Segoe UI", 7, "italic"),
                         fg="#6e6e77", bg="#1a1a1d", anchor="w").pack(fill="x")

            tw.update_idletasks()
            w = tw.winfo_reqwidth()
            h = tw.winfo_reqheight()

            # Bound STRICTLY inside the application window boundaries across multi-monitors
            app = self.tree.winfo_toplevel()
            app_x = app.winfo_rootx()
            app_y = app.winfo_rooty()
            app_w = app.winfo_width()
            app_h = app.winfo_height()

            # Default offset: slightly to the right and below the cursor
            x = mouse_x + 18
            y = mouse_y + 12

            # Keep inside horizontal bounds of app
            if x + w > app_x + app_w - 15:
                x = mouse_x - w - 15
            if x < app_x + 10:
                x = app_x + 10

            # Keep inside vertical bounds of app
            if y + h > app_y + app_h - 15:
                y = mouse_y - h - 10
            if y < app_y + 35:
                y = app_y + 35

            tw.wm_geometry(f"+{x}+{y}")
            tw.lift()
        except Exception:
            self.hide_tip()

    def hide_tip(self):
        if self.tip_window:
            try:
                self.tip_window.destroy()
            except Exception:
                pass
            self.tip_window = None

class SetQuantityDialog(tk.Toplevel):
    def __init__(self, parent, item_name, current_qty, max_allowed, on_save):
        super().__init__(parent)
        self.title(f"Set Quantity - {item_name}")
        self.geometry("320x165")
        self.configure(bg="#252528")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.on_save = on_save
        self.max_allowed = max_allowed

        # Center dialog
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 160
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 85
        self.geometry(f"+{x}+{y}")

        tk.Label(self, text="Set Cart Quantity for:", fg="#aaaaaa", bg="#252528", font=("Segoe UI", 9)).pack(pady=(10, 2))
        tk.Label(self, text=item_name, fg="#f39c12", bg="#252528", font=("Segoe UI", 10, "bold")).pack()
        tk.Label(self, text=f"(Max allowed: {max_allowed:,})", fg="#888888", bg="#252528", font=("Segoe UI", 8)).pack(pady=(0, 6))

        f = tk.Frame(self, bg="#252528")
        f.pack(pady=4)
        self.ent = tk.Entry(f, width=10, bg="#1e1e1e", fg="#2ecc71", font=("Segoe UI", 10, "bold"), insertbackground="#ffffff", justify="center")
        self.ent.insert(0, str(current_qty))
        self.ent.pack()
        self.ent.focus_set()
        self.ent.select_range(0, tk.END)

        btn_box = tk.Frame(self, bg="#252528")
        btn_box.pack(pady=10)
        tk.Button(btn_box, text="Set Quantity", command=self.save, bg="#27ae60", fg="#ffffff", relief="flat", padx=8, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_box, text="Remove", command=self.remove, bg="#c0392b", fg="#ffffff", relief="flat", padx=6, cursor="hand2").pack(side="left", padx=4)
        tk.Button(btn_box, text="Cancel", command=self.destroy, bg="#7f8c8d", fg="#ffffff", relief="flat", padx=6, cursor="hand2").pack(side="left", padx=4)

        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.destroy())

    def save(self):
        try:
            val = int(self.ent.get().strip().replace(",", ""))
            if val <= 0:
                self.on_save(0)
            else:
                val = min(val, self.max_allowed)
                self.on_save(val)
            self.destroy()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid whole number.")

    def remove(self):
        self.on_save(0)
        self.destroy()

class OSRSAlchDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OSRS High Alchemy & Crafting Profit Dashboard")
        self.geometry("1280x780")
        self.minsize(1020, 620)

        # App state & API
        self.state = AppState()
        self.api = OSRSPricesAPI()

        # Runtime data
        self.alch_rows = []
        self.craft_rows = []
        self.rec_rows = []
        self.is_fetching = False
        self.seconds_until_refresh = self.state.config.get("auto_refresh_mins", 2) * 60

        # Sorting states: {col_name: descending_bool}
        self.alch_sort_col = "profit_ea"
        self.alch_sort_desc = True

        self.craft_sort_col = "profit_ea"
        self.craft_sort_desc = True

        self.rec_sort_col = "profit_ea"
        self.rec_sort_desc = True

        # Clipboard copy feedback
        self.clipboard_clear_timer = None

        self.setup_styles()
        self.build_ui()

        # Keyboard shortcuts
        self.bind("<F5>", lambda e: self.trigger_refresh())
        self.bind("<Control-f>", lambda e: self.focus_search())
        self.bind("<Control-F>", lambda e: self.focus_search())

        # Start timer tick
        self.after(1000, self.timer_tick)

        # Window close protocol (prompts if update available)
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Update checker
        self.latest_update_info = None
        self.after(2000, lambda: threading.Thread(target=self._check_update_startup, daemon=True).start())

        # Check if app was just updated to show "What's New" popup
        self.after(800, self._check_first_run_after_update)

        # Ensure plugin is deployed to .runelite/microbot-plugins if present
        self._ensure_plugin_deployed()

        # Bridge Server for RuneLite / Microbot live sync
        self._logged_ge_offers = set()
        self._ge_cart_slots = {}
        self._ge_tracked_items = set()
        self.bridge_server = BridgeServer(port=18833, event_callback=self._on_bridge_event_async)
        self.bridge_server.start()

    def _ensure_plugin_deployed(self):
        """Ensures AlchBridgePlugin.jar is deployed into .runelite/microbot-plugins if present."""
        try:
            user_home = os.path.expanduser("~")
            dest_dir = os.path.join(user_home, ".runelite", "microbot-plugins")
            if not os.path.exists(dest_dir):
                return

            dest_jar = os.path.join(dest_dir, "AlchBridgePlugin.jar")
            app_dir = os.path.dirname(os.path.abspath(__file__))
            exe_dir = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, "frozen", False) else app_dir

            sources = [
                os.path.join(app_dir, "bridge_plugin", "AlchBridgePlugin.jar"),
                os.path.join(exe_dir, "plugins", "AlchBridgePlugin.jar"),
                os.path.join(exe_dir, "bridge_plugin", "AlchBridgePlugin.jar")
            ]

            for src in sources:
                if os.path.exists(src):
                    if not os.path.exists(dest_jar) or (os.path.getmtime(src) > os.path.getmtime(dest_jar)):
                        shutil.copy2(src, dest_jar)
                    break
        except Exception:
            pass

        # Initial load in background thread
        self.trigger_refresh()

    def setup_styles(self):
        self.configure(bg="#1e1e1e")
        style = ttk.Style(self)
        style.theme_use("clam")

        # Global Dark Theme Options
        style.configure(".", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 9))
        style.configure("TFrame", background="#1e1e1e")
        style.configure("Card.TFrame", background="#252528", relief="solid", borderwidth=1)
        style.configure("TopBar.TFrame", background="#252528")

        # High Contrast Combobox Theme (Fixes unreadable white text)
        style.configure("TCombobox",
            background="#2d2d30",
            foreground="#ffffff",
            fieldbackground="#1e1e1e",
            darkcolor="#1e1e1e",
            lightcolor="#3e3e42",
            bordercolor="#3e3e42",
            arrowcolor="#f39c12",
            padding=[4, 2]
        )
        style.map("TCombobox",
            fieldbackground=[("readonly", "#1e1e1e"), ("active", "#252528")],
            foreground=[("readonly", "#ffffff"), ("active", "#ffffff")],
            selectbackground=[("readonly", "#38383e")],
            selectforeground=[("readonly", "#f39c12")]
        )

        # Force dark listbox for dropdown menus
        self.option_add("*TCombobox*Listbox.background", "#252528")
        self.option_add("*TCombobox*Listbox.foreground", "#ffffff")
        self.option_add("*TCombobox*Listbox.selectBackground", "#f39c12")
        self.option_add("*TCombobox*Listbox.selectForeground", "#000000")
        self.option_add("*TCombobox*Listbox.font", ("Segoe UI", 9))

        # Tabs
        style.configure("TNotebook", background="#1e1e1e", borderwidth=0)
        style.configure("TNotebook.Tab", background="#2d2d30", foreground="#cccccc", padding=[16, 6], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
            background=[("selected", "#3e3e42"), ("active", "#353538")],
            foreground=[("selected", "#f39c12"), ("active", "#ffffff")]
        )

        # Treeview (Tables)
        style.configure("Treeview",
            background="#252528",
            foreground="#f1f1f1",
            fieldbackground="#252528",
            rowheight=26,
            bordercolor="#3e3e42",
            font=("Segoe UI", 9)
        )
        style.configure("Treeview.Heading",
            background="#2d2d30",
            foreground="#f39c12",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=[4, 6]
        )
        style.map("Treeview",
            background=[("selected", "#38383e")],
            foreground=[("selected", "#f39c12")]
        )
        style.map("Treeview.Heading",
            background=[("active", "#3a3a3e")]
        )

        style.configure("Vertical.TScrollbar", background="#2d2d30", troughcolor="#1e1e1e", borderwidth=0, arrowcolor="#cccccc")
        style.configure("Horizontal.TScrollbar", background="#2d2d30", troughcolor="#1e1e1e", borderwidth=0, arrowcolor="#cccccc")
        style.configure("TScrollbar", background="#2d2d30", troughcolor="#1e1e1e", borderwidth=0, arrowcolor="#cccccc")

    def build_ui(self):
        # 1. Top Control Strip
        self.top_frame = ttk.Frame(self, style="TopBar.TFrame")
        self.top_frame.pack(fill="x", padx=10, pady=(10, 5))
        self.build_top_controls()

        # 2. Prominent Nature Rune & Shopping Cart Bar
        self.sub_bar = ttk.Frame(self, style="Card.TFrame")
        self.sub_bar.pack(fill="x", padx=10, pady=5)
        self.build_sub_bar()

        # 3. Main Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Tab 1: Pure High Alch
        self.tab_alch = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alch, text="🔮 Pure High Alch")
        self.build_alch_tab()

        # Tab 2: Smart Picks (Recommendations)
        self.tab_rec = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_rec, text="⭐ Smart Picks")
        self.build_rec_tab()

        # Tab 3: Craft & Alch
        self.tab_craft = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_craft, text="🔨 Craft & Alch")
        self.build_craft_tab()

        # Tab 4: Skilling & Level Training Guide
        self.tab_guide = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_guide, text="🎓 Level Guide")
        self.build_guide_tab()

        # Tab 5: 4h GE Limit Timers
        self.tab_timers = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_timers, text="⏱️ 4h GE Timers")
        self.build_timers_tab()

        # Tab 6: Session Profit Tracker
        self.tab_session = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_session, text="📊 Session Tracker")
        self.build_session_tab()

        # Tab 7: Alert Log
        self.tab_alerts = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alerts, text="🔔 Alert Feed")
        self.build_alerts_tab()

        # 4. Bottom Status Bar
        self.status_bar = tk.Frame(self, bg="#181818", height=28)
        self.status_bar.pack(fill="x", side="bottom")
        self.build_status_bar()

    def build_top_controls(self):
        # Row 1: Item & Market Filters
        p1 = tk.Frame(self.top_frame, bg="#252528")
        p1.pack(fill="x", padx=8, pady=(4, 2))

        # Filters: Members / F2P
        self.var_members = tk.BooleanVar(value=self.state.config.get("members", True))
        self.var_f2p = tk.BooleanVar(value=self.state.config.get("f2p", False))

        cb_mem = tk.Checkbutton(p1, text="Members", variable=self.var_members, command=self.on_members_clicked,
                                bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30", activebackground="#252528", activeforeground="#f39c12")
        cb_mem.pack(side="left", padx=2)
        ToolTip(cb_mem, "Members Mode (P2P):\nShows all tradeable items and skilling methods (both P2P items and F2P staples).")

        cb_f2p = tk.Checkbutton(p1, text="F2P Only", variable=self.var_f2p, command=self.on_f2p_clicked,
                                bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30", activebackground="#252528", activeforeground="#2ecc71")
        cb_f2p.pack(side="left", padx=2)
        ToolTip(cb_f2p, "Free-to-Play Mode (F2P Only):\nStrictly filters to F2P items, recipes, quests, and brackets only.\nAll Members items and quests are completely hidden across all tabs.\nGE slots cap at 3.")

        # Cash Stack (Toggleable on/off)
        self.var_use_cash = tk.BooleanVar(value=self.state.config.get("use_cash_stack", True))
        self.cb_cash = tk.Checkbutton(p1, text="Cash Stack:", variable=self.var_use_cash, command=self.on_cash_toggle_changed,
                                      bg="#252528", fg="#cccccc", selectcolor="#2d2d30", activebackground="#252528", activeforeground="#2ecc71")
        self.cb_cash.pack(side="left", padx=(4, 0))
        ToolTip(self.cb_cash, "Toggle budget constraint. Uncheck for unlimited cash.")

        self.ent_cash = tk.Entry(p1, width=8, bg="#1e1e1e", fg="#2ecc71", insertbackground="#ffffff", relief="flat")
        self.ent_cash.insert(0, format_gp(self.state.config.get("cash_stack", 5000000)))
        if not self.var_use_cash.get():
            self.ent_cash.config(state="disabled")
        self.ent_cash.pack(side="left", padx=(1, 6))
        self.ent_cash.bind("<FocusOut>", self.on_cash_changed)
        self.ent_cash.bind("<Return>", self.on_cash_changed)
        ToolTip(self.ent_cash, "Your current in-game cash stack. Supports 900k, 1.5m, etc.")

        # Max Item Spend
        tk.Label(p1, text="Max Spend:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_max_spend = tk.Entry(p1, width=7, bg="#1e1e1e", fg="#f1f1f1", insertbackground="#ffffff", relief="flat")
        self.ent_max_spend.insert(0, format_gp(self.state.config.get("max_item_cost", 500000)))
        self.ent_max_spend.pack(side="left", padx=(2, 6))
        self.ent_max_spend.bind("<FocusOut>", self.on_filter_changed)
        self.ent_max_spend.bind("<Return>", self.on_filter_changed)
        ToolTip(self.ent_max_spend, "Maximum buy price of a single item to display.")

        # Min 24h Volume
        tk.Label(p1, text="Min Vol:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_min_vol = tk.Entry(p1, width=6, bg="#1e1e1e", fg="#f1f1f1", insertbackground="#ffffff", relief="flat")
        self.ent_min_vol.insert(0, str(self.state.config.get("min_volume", 5000)))
        self.ent_min_vol.pack(side="left", padx=(2, 6))
        self.ent_min_vol.bind("<FocusOut>", self.on_filter_changed)
        self.ent_min_vol.bind("<Return>", self.on_filter_changed)
        ToolTip(self.ent_min_vol, "Minimum 24-hour traded volume on Grand Exchange.")

        # Min Profit per alch (Empty = show everything!)
        tk.Label(p1, text="Min Profit:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_min_profit = tk.Entry(p1, width=5, bg="#1e1e1e", fg="#2ecc71", insertbackground="#ffffff", relief="flat")
        m_prof = self.state.config.get("min_profit")
        if m_prof is not None and m_prof > 0:
            self.ent_min_profit.insert(0, str(m_prof))
        self.ent_min_profit.pack(side="left", padx=(2, 6))
        self.ent_min_profit.bind("<KeyRelease>", lambda e: self.recalculate_alch_table())
        ToolTip(self.ent_min_profit, "Minimum GP profit per alch. Leave blank to show all items (even 0 or negative for XP).")

        # Live Search Bar (Universal across ALL tabs)
        tk.Label(p1, text="🔍", fg="#f39c12", bg="#252528").pack(side="left", padx=(2, 1))
        self.ent_search = tk.Entry(p1, width=13, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.ent_search.pack(side="left", padx=(1, 8))
        self.ent_search.bind("<KeyRelease>", self.on_global_search_changed)
        self.ent_search.bind("<Escape>", lambda e: self.clear_search())
        ToolTip(self.ent_search, "Universal search across ALL tabs (Alch, Smart Picks, Craft, Guide, Timers, History). Press Esc to clear, Ctrl+F to focus.")

        # Strategy Combobox
        lbl_strat = tk.Label(p1, text="Strategy:", fg="#cccccc", bg="#252528")
        lbl_strat.pack(side="left")
        ToolTip(lbl_strat, "Select your buy pricing strategy on the Grand Exchange.")

        curr_strat = self.state.config.get("strategy", "patient")
        strat_display = "smart (Bid+1)" if curr_strat == "smart" else ("instant (Ask)" if curr_strat == "instant" else "patient (Bid)")
        self.var_strat = tk.StringVar(value=strat_display)
        cb_strat = ttk.Combobox(p1, textvariable=self.var_strat, values=["patient (Bid)", "smart (Bid+1)", "instant (Ask)"], width=13, state="readonly")
        cb_strat.pack(side="left", padx=(2, 8))
        cb_strat.bind("<<ComboboxSelected>>", self.on_strategy_changed)
        ToolTip(cb_strat, "patient (Bid) = Lowest price, maximum profit.\nsmart (Bid+1) = Bid + 1 gp for top queue priority (much faster fills!).\ninstant (Ask) = Instant fill from active sellers.")

        # Speed Filter Combobox
        lbl_spd = tk.Label(p1, text="Speed:", fg="#cccccc", bg="#252528")
        lbl_spd.pack(side="left")
        ToolTip(lbl_spd, "Filter items by estimated transaction fill wait time.")

        self.var_speed = tk.StringVar(value=self.state.config.get("speed_filter", "All"))
        cb_spd = ttk.Combobox(p1, textvariable=self.var_speed, values=["All", "⚡ Fast (<15m)", "⏱️ Steady (<1h)"], width=12, state="readonly")
        cb_spd.pack(side="left", padx=(2, 4))
        cb_spd.bind("<<ComboboxSelected>>", self.on_speed_filter_changed)
        ToolTip(cb_spd, "Filter by buy fill speed:\n⚡ Fast (<15m) = Active sales happening right now (fills in minutes!)\n⏱️ Steady (<1h) = Consistent volume\nAll = Show all items regardless of wait time")

        # Row 2: Toggles, Alerts, Auto-Sync & Action Buttons
        p2 = tk.Frame(self.top_frame, bg="#252528")
        p2.pack(fill="x", padx=8, pady=(2, 4))

        # Toggles on Left
        self.var_free_alch = tk.BooleanVar(value=self.state.config.get("free_alchs_mode", False))
        self.var_sound = tk.BooleanVar(value=self.state.config.get("sound_enabled", True))
        self.var_desktop = tk.BooleanVar(value=self.state.config.get("desktop_alerts", True))
        self.var_hide_maxed = tk.BooleanVar(value=self.state.config.get("hide_maxed_cooldown", True))

        cb_free = tk.Checkbutton(p2, text="🌿 Ring (0 Nat)", variable=self.var_free_alch, command=self.on_filter_changed,
                                 bg="#252528", fg="#3498db", selectcolor="#2d2d30", activebackground="#252528")
        cb_free.pack(side="left", padx=(0, 6))
        ToolTip(cb_free, "Explorer's Ring Mode: Calculates profit assuming 0 Nature Rune cost.")

        cb_snd = tk.Checkbutton(p2, text="🔊 Sound Alerts", variable=self.var_sound, command=self.save_preferences,
                                bg="#252528", fg="#cccccc", selectcolor="#2d2d30", activebackground="#252528")
        cb_snd.pack(side="left", padx=6)
        ToolTip(cb_snd, "Play audio chime when a 4h limit resets or a high margin alert triggers.")

        cb_dsk = tk.Checkbutton(p2, text="🔔 Desktop Popups", variable=self.var_desktop, command=self.save_preferences,
                                bg="#252528", fg="#cccccc", selectcolor="#2d2d30", activebackground="#252528")
        cb_dsk.pack(side="left", padx=6)
        ToolTip(cb_dsk, "Show desktop popup notifications on 4h limit resets.")

        cb_max = tk.Checkbutton(p2, text="⏳ Hide Maxed", variable=self.var_hide_maxed, command=self.on_hide_maxed_changed,
                                bg="#252528", fg="#cccccc", selectcolor="#2d2d30", activebackground="#252528")
        cb_max.pack(side="left", padx=6)
        ToolTip(cb_max, "Hide Maxed (4h GE Limit):\nTemporarily removes items from the table when your 4-hour GE limit is reached (0 remaining), and mutes their alerts.\nItems automatically reappear when the 4h cooldown expires.")

        tk.Label(p2, text="|", fg="#444444", bg="#252528").pack(side="left", padx=5)

        tk.Label(p2, text="Basis:", fg="#cccccc", bg="#252528").pack(side="left", padx=(2, 2))
        curr_basis = self.state.config.get("price_basis", "5m")
        basis_display = "5m Volume Avg" if curr_basis == "5m" else "1-Trade Tick"
        self.var_price_basis = tk.StringVar(value=basis_display)
        cb_basis = ttk.Combobox(p2, textvariable=self.var_price_basis, values=["5m Volume Avg", "1-Trade Tick"], width=13, state="readonly")
        cb_basis.pack(side="left", padx=(0, 6))
        cb_basis.bind("<<ComboboxSelected>>", self.on_price_basis_changed)
        ToolTip(cb_basis, "Price Calculation Basis:\n- 5m Volume Avg (Recommended): Volume-weighted average across real trades over the last 5 minutes. Eliminates 1-item freak dumps and provides prices that actually fill on the GE.\n- 1-Trade Tick: Instant single-trade tick from /latest.")

        tk.Label(p2, text="|", fg="#444444", bg="#252528").pack(side="left", padx=5)

        tk.Label(p2, text="⏱️ Auto-Sync:", fg="#888888", bg="#252528", font=("Segoe UI", 8)).pack(side="left")
        self.var_refresh = tk.StringVar(value=f"{self.state.config.get('auto_refresh_mins', 2)} min")
        cb_ref = ttk.Combobox(p2, textvariable=self.var_refresh, values=["1 min", "2 min", "5 min", "10 min", "Off"], width=6, state="readonly")
        cb_ref.pack(side="left", padx=(2, 6))
        cb_ref.bind("<<ComboboxSelected>>", self.on_refresh_rate_changed)
        ToolTip(cb_ref, "Configure how often market prices automatically refresh.")

        # Multi-Account Selector & Live Bridge Indicator
        tk.Label(p2, text="|", fg="#444444", bg="#252528").pack(side="left", padx=4)
        tk.Label(p2, text="Monitor:", fg="#3498db", bg="#252528", font=("Segoe UI", 8, "bold")).pack(side="left", padx=(2, 2))
        saved_char = self.state.config.get("monitored_character", "All Accounts")
        self.var_account = tk.StringVar(value=saved_char)
        init_accs = ["All Accounts"] + sorted(list(self.state.accounts.keys()))
        if saved_char not in init_accs:
            init_accs.append(saved_char)
        self.cb_account = ttk.Combobox(p2, textvariable=self.var_account, values=init_accs, width=13, state="readonly")
        self.cb_account.pack(side="left", padx=(0, 4))
        self.cb_account.bind("<<ComboboxSelected>>", self.on_account_selected)
        ToolTip(self.cb_account, "Character Lock / Multi-Instance Monitor:\nChoose an account to lock dashboard monitoring to (Cash, Nats, Levels, GE Cart, Session, Timers).\nAlt accounts will update silently in the background without stealing focus or disrupting your view.")

        self.lbl_bridge_status = tk.Label(p2, text="🟢 Bridge", fg="#2ecc71", bg="#252528", font=("Segoe UI", 8, "bold"))
        self.lbl_bridge_status.pack(side="left", padx=(2, 6))
        ToolTip(self.lbl_bridge_status, "Microbot / RuneLite Bridge:\nListening on 127.0.0.1:18833 for live GE trades, 4h cooldown timers, coins, and nature runes.")

        # Action Buttons on Right
        self.btn_update = tk.Button(p2, text=f"⚡ v{APP_VERSION}", command=self.on_update_button_click,
                                    bg="#2d2d30", fg="#3498db", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=1, cursor="hand2")
        self.btn_update.pack(side="right", padx=(4, 0))
        ToolTip(self.btn_update, f"OSRS Tracker v{APP_VERSION}.\nClick to check GitHub for updates.")

        self.btn_refresh = tk.Button(p2, text="🔄 Refresh Now", command=self.trigger_refresh,
                                     bg="#f39c12", fg="#000000", font=("Segoe UI", 8, "bold"), relief="flat", padx=10, pady=1, cursor="hand2")
        self.btn_refresh.pack(side="right", padx=(4, 2))
        ToolTip(self.btn_refresh, "Fetch latest live prices from OSRS Wiki API. Shortcut: F5")

        self.lbl_countdown = tk.Label(p2, text="(Next: 02:00)", fg="#888888", bg="#252528", font=("Segoe UI", 8))
        self.lbl_countdown.pack(side="right", padx=(0, 4))
        ToolTip(self.lbl_countdown, "Time until next automatic price sync with OSRS Wiki.")

    def build_sub_bar(self):
        p = tk.Frame(self.sub_bar, bg="#252528")
        p.pack(fill="x", padx=8, pady=3)

        # Dedicated Nature Rune Card
        nat_card = tk.Frame(p, bg="#1e1e1e", relief="solid", borderwidth=1, padx=6, pady=2)
        nat_card.pack(side="left")

        tk.Label(nat_card, text="🌿 NATURE RUNE", font=("Segoe UI", 9, "bold"), fg="#2ecc71", bg="#1e1e1e").pack(side="left", padx=(0, 4))

        self.lbl_nat_target = tk.Label(nat_card, text="🎯 Offer: 168 gp", font=("Segoe UI", 9, "bold"), bg="#27ae60", fg="#ffffff", padx=5, pady=1, cursor="hand2")
        self.lbl_nat_target.pack(side="left", padx=2)
        ToolTip(self.lbl_nat_target, "Live GE patient buy offer for Nature Runes. Click to copy price!")
        self.lbl_nat_target.bind("<Button-1>", lambda e: self.copy_to_clipboard(str(self.api.nature_rune_bid), f"Copied Nature Rune Bid: {self.api.nature_rune_bid} gp"))

        self.lbl_nat_details = tk.Label(nat_card, text="Ask: 172 gp | Limit: 18k", font=("Segoe UI", 8), fg="#aaaaaa", bg="#1e1e1e")
        self.lbl_nat_details.pack(side="left", padx=3)
        ToolTip(self.lbl_nat_details, "Nature Rune instant buy (Ask) price and 4h GE buy limit (18,000).")

        tk.Label(nat_card, text="Lock:", font=("Segoe UI", 8), fg="#888888", bg="#1e1e1e").pack(side="left", padx=(2, 1))
        self.ent_custom_nat = tk.Entry(nat_card, width=4, bg="#252528", fg="#f39c12", relief="flat")
        self.ent_custom_nat.pack(side="left", padx=(1, 2))
        c_price = self.state.config.get("custom_nature_price", 0)
        if c_price > 0:
            self.ent_custom_nat.insert(0, str(c_price))
        self.ent_custom_nat.bind("<FocusOut>", self.on_custom_nat_changed)
        self.ent_custom_nat.bind("<Return>", self.on_custom_nat_changed)
        ToolTip(self.ent_custom_nat, "Optional fixed Nature Rune price. Leave blank to use live GE market price.")

        tk.Label(nat_card, text="Owned:", font=("Segoe UI", 8), fg="#888888", bg="#1e1e1e").pack(side="left", padx=(2, 1))
        self.ent_owned_nat = tk.Entry(nat_card, width=5, bg="#252528", fg="#2ecc71", relief="flat")
        self.ent_owned_nat.pack(side="left", padx=(1, 2))
        owned = self.state.config.get("owned_nature_runes", 0)
        if owned > 0:
            self.ent_owned_nat.insert(0, str(owned))
        self.ent_owned_nat.bind("<FocusOut>", self.on_owned_nat_changed)
        self.ent_owned_nat.bind("<Return>", self.on_owned_nat_changed)
        ToolTip(self.ent_owned_nat, "Your Nature Rune bank stockpile. Cart tells you if you need to buy more.")

        # Action Buttons pinned to Right
        btn_frame = tk.Frame(p, bg="#252528")
        btn_frame.pack(side="right")

        btn_master_tag = tk.Button(btn_frame, text="📋 Master Tag", command=self.export_master_bank_tag,
                                   bg="#8e44ad", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=6, cursor="hand2")
        btn_master_tag.pack(side="right", padx=2)
        ToolTip(btn_master_tag, "Export all profitable items as a RuneLite bank tag tab.")

        btn_cart_tag = tk.Button(btn_frame, text="🛒 Cart Tag", command=self.export_cart_bank_tag,
                                 bg="#2980b9", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=6, cursor="hand2")
        btn_cart_tag.pack(side="right", padx=2)
        ToolTip(btn_cart_tag, "Export only items currently in your cart as a RuneLite bank tag tab.")

        btn_log_cart = tk.Button(btn_frame, text="✓ Log Cart", command=self.log_cart_session,
                                 bg="#27ae60", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=6, cursor="hand2")
        btn_log_cart.pack(side="right", padx=2)
        ToolTip(btn_log_cart, "Record cart into Session Tracker and start 4h GE cooldown timers.")

        btn_clear_cart = tk.Button(btn_frame, text="✕ Clear", command=self.clear_cart,
                                   bg="#c0392b", fg="#ffffff", font=("Segoe UI", 8), relief="flat", padx=5, cursor="hand2")
        btn_clear_cart.pack(side="right", padx=2)
        ToolTip(btn_clear_cart, "Clear all items from your shopping cart.")

        # Separator
        tk.Label(p, text="|", fg="#444444", bg="#252528").pack(side="left", padx=6)

        # Shopping Cart Summary in center
        self.lbl_cart_status = tk.Label(p, text="🛒 Slots: 0/8 | Allocated: 0 gp | Left: 5.00M gp | Profit: +0 gp",
                                        font=("Segoe UI", 8, "bold"), fg="#2ecc71", bg="#252528")
        self.lbl_cart_status.pack(side="left", padx=2)
        ToolTip(self.lbl_cart_status, "Shopping cart status: slots used, gold budget allocated, projected profit, and casting time.")

    def build_alch_tab(self):
        container = ttk.Frame(self.tab_alch)
        container.pack(fill="both", expand=True)

        cols = ("cart", "name", "offer_bid", "instant_ask", "alch_val", "profit_ea", "profit_hr", "speed", "limit", "batch_profit", "max_afford", "volume")
        self.tree_alch = ttk.Treeview(container, columns=cols, show="headings", selectmode="browse")

        self.tree_alch.heading("cart", text="Cart", command=lambda: self.toggle_sort_alch("cart"))
        self.tree_alch.heading("name", text="Item Name", command=lambda: self.toggle_sort_alch("name"))
        self.tree_alch.heading("offer_bid", text="Target Offer (Bid)", command=lambda: self.toggle_sort_alch("offer_bid"))
        self.tree_alch.heading("instant_ask", text="Instant Buy (Ask)", command=lambda: self.toggle_sort_alch("instant_ask"))
        self.tree_alch.heading("alch_val", text="Alch Value", command=lambda: self.toggle_sort_alch("alch_val"))
        self.tree_alch.heading("profit_ea", text="Profit / Alch ▼", command=lambda: self.toggle_sort_alch("profit_ea"))
        self.tree_alch.heading("profit_hr", text="Profit / Hr (1.2k)", command=lambda: self.toggle_sort_alch("profit_hr"))
        self.tree_alch.heading("speed", text="Fill Speed", command=lambda: self.toggle_sort_alch("speed"))
        self.tree_alch.heading("limit", text="4h Limit", command=lambda: self.toggle_sort_alch("limit"))
        self.tree_alch.heading("batch_profit", text="4h Batch Profit", command=lambda: self.toggle_sort_alch("batch_profit"))
        self.tree_alch.heading("max_afford", text="Max Afford", command=lambda: self.toggle_sort_alch("max_afford"))
        self.tree_alch.heading("volume", text="24h Volume", command=lambda: self.toggle_sort_alch("volume"))

        self.tree_alch.column("cart", width=46, anchor="center")
        self.tree_alch.column("name", width=170, anchor="w")
        self.tree_alch.column("offer_bid", width=105, anchor="e")
        self.tree_alch.column("instant_ask", width=105, anchor="e")
        self.tree_alch.column("alch_val", width=85, anchor="e")
        self.tree_alch.column("profit_ea", width=100, anchor="e")
        self.tree_alch.column("profit_hr", width=110, anchor="e")
        self.tree_alch.column("speed", width=128, anchor="center")
        self.tree_alch.column("limit", width=95, anchor="center")
        self.tree_alch.column("batch_profit", width=110, anchor="e")
        self.tree_alch.column("max_afford", width=85, anchor="center")
        self.tree_alch.column("volume", width=115, anchor="e")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree_alch.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree_alch.xview)
        self.tree_alch.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.tree_alch.pack(side="left", fill="both", expand=True)

        self.tree_alch.bind("<Button-1>", self.on_alch_click)
        self.tree_alch.bind("<Double-1>", self.on_alch_double_click)
        self.tree_alch.bind("<Button-3>", self.on_alch_right_click)

        # Hover descriptions for every table column header
        alch_col_tooltips = {
            "#1": "Shopping Cart:\nShows items in cart. Click row cell to copy quantity number to clipboard.\nRight-click row to set custom cart quantity.",
            "#2": "Item Name:\nGrand Exchange item name. Click row cell to copy name to clipboard for GE search.",
            "#3": "Target Offer (Bid):\nBest patient buy price from active sellers. Click cell to copy price.\nIf using Smart strategy, bids Bid + 1 gp for queue priority.",
            "#4": "Instant Buy (Ask):\nInstant purchase price from active sellers. Fills immediately. Click cell to copy.",
            "#5": "High Alch Value:\nFixed gold returned by casting the High Level Alchemy spell.",
            "#6": "Profit / Alch:\nNet GP profit per cast = High Alch Value - Item Buy Price - Nature Rune Cost.\nClick column header to sort.",
            "#7": "Profit / Hr:\nEstimated profit per hour at standard 1,200 casts/hour rate.\nClick column header to sort.",
            "#8": "Fill Speed & 5m Sold:\nEstimated wait time or live 5-minute sales velocity.\nIn 1-Trade Tick mode, shows exact quantity sold into bids in the past 5 minutes (e.g. '3 sold') to verify real market activity.\nClick column header to sort.",
            "#9": "4h GE Buy Limit:\nOfficial Grand Exchange purchase limit every 4 hours.\n⚠️ Volume Capped: If 24h market volume is lower than GE limit, shows 'Volume / Limit ⚠️' to avoid illiquid paper profit traps.",
            "#10": "4h Batch Profit:\nRealistic profit achievable for a full 4-hour batch (Profit ea * Effective volume-capped limit).\nClick column header to sort.",
            "#11": "Max Afford:\nMaximum quantity your current cash stack can afford out of remaining available limit.\nClick column header to sort.",
            "#12": "24h Volume & 5m Sold:\nTotal units traded on Grand Exchange over the last 24 hours.\nIn 1-Trade Tick mode, displays '24h Vol (5m Sold)' to verify active trades.\nClick column header to sort."
        }
        HeadingToolTip(self.tree_alch, alch_col_tooltips)
        RowToolTip(self.tree_alch, self.get_alch_row_tooltip)

    def build_rec_tab(self):
        container = ttk.Frame(self.tab_rec)
        container.pack(fill="both", expand=True, padx=6, pady=4)

        # 1. Market Clock & Timing Banner Card
        self.market_clock_card = tk.Frame(container, bg="#202023", relief="solid", borderwidth=1, padx=10, pady=6)
        self.market_clock_card.pack(fill="x", pady=(2, 6))

        clock_top = tk.Frame(self.market_clock_card, bg="#202023")
        clock_top.pack(fill="x")

        self.lbl_market_time = tk.Label(clock_top, text="🕒 --:-- UTC", font=("Segoe UI", 11, "bold"), fg="#f1c40f", bg="#202023")
        self.lbl_market_time.pack(side="left", padx=(0, 10))
        ToolTip(self.lbl_market_time, "Current Grand Exchange server time (UTC).\nOSRS market activity cycles strictly follow UTC time zones.")

        self.lbl_market_badge = tk.Label(clock_top, text="🟢 Peak Trading Hours", font=("Segoe UI", 10, "bold"), fg="#2ecc71", bg="#202023")
        self.lbl_market_badge.pack(side="left", padx=(0, 12))

        self.lbl_market_activity = tk.Label(clock_top, text="Activity: [████████░░] 80%", font=("Segoe UI", 9), fg="#3498db", bg="#202023")
        self.lbl_market_activity.pack(side="left")

        self.lbl_market_advice = tk.Label(self.market_clock_card, text="💡 Tip: Market is active. Place smart bids on high-volume staples.",
                                          font=("Segoe UI", 9, "italic"), fg="#e0e0e0", bg="#202023")
        self.lbl_market_advice.pack(anchor="w", pady=(4, 0))

        # 2. Controls & Categories Row
        rec_ctrl = tk.Frame(container, bg="#252528", relief="solid", borderwidth=1, padx=8, pady=5)
        rec_ctrl.pack(fill="x", pady=(0, 6))

        tk.Label(rec_ctrl, text="Category:", font=("Segoe UI", 9, "bold"), fg="#f39c12", bg="#252528").pack(side="left", padx=(2, 8))

        self.var_rec_cat = tk.StringVar(value="workhorse")
        cat_options = [
            ("🏆 All-Time Workhorses", "workhorse", "Proven high-volume alch staples that rarely fail (Rune armor, weapons, battlestaves)."),
            ("⚡ Fast Fills (<5m)", "fast", "Items with rapid transaction velocity and live 5m sales activity that fill in under 5 minutes."),
            ("💰 Top 4h Batch Profit", "batch", "Items ranked by total profit achievable in a single 4-hour GE limit cycle."),
            ("🌙 Overnight Sleepers", "overnight", "High-margin items ideal for leaving patient bids overnight during off-peak hours.")
        ]
        for label, val, tip in cat_options:
            rb = tk.Radiobutton(rec_ctrl, text=label, variable=self.var_rec_cat, value=val,
                                command=self.recalculate_rec_table,
                                bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30",
                                activebackground="#252528", activeforeground="#f39c12",
                                font=("Segoe UI", 9))
            rb.pack(side="left", padx=4)
            ToolTip(rb, f"{label}:\n{tip}")

        # Action Buttons on right
        btn_auto_fill = tk.Button(rec_ctrl, text="⚡ Auto-Fill Empty GE Slots", command=self.auto_fill_ge_slots,
                                  bg="#27ae60", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=2, cursor="hand2")
        btn_auto_fill.pack(side="right", padx=3)
        ToolTip(btn_auto_fill, "⚡ Auto-Fill Empty GE Slots:\nInspects your remaining empty GE slots (up to 8) and automatically allocates\nthe top recommended items into your shopping cart, fitted to your cash stack budget!")

        btn_copy_all = tk.Button(rec_ctrl, text="📋 Copy All", command=self.copy_all_recs,
                                 bg="#2980b9", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=2, cursor="hand2")
        btn_copy_all.pack(side="right", padx=3)
        ToolTip(btn_copy_all, "Copy All:\nCopy formatted text list of all displayed recommendations to clipboard.")

        btn_refresh = tk.Button(rec_ctrl, text="🔄 Refresh", command=self.recalculate_rec_table,
                                bg="#3e3e42", fg="#f1f1f1", font=("Segoe UI", 8), relief="flat", padx=6, pady=2, cursor="hand2")
        btn_refresh.pack(side="right", padx=3)
        ToolTip(btn_refresh, "Refresh recommendations using latest live GE prices.")

        # 3. Recommendations Table Container
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill="both", expand=True)

        cols = ("badge", "name", "category", "offer_bid", "alch_val", "profit_ea", "limit", "batch_profit", "speed", "batch_cost", "verdict")
        self.tree_rec = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_rec.heading("badge", text="Rank", command=lambda: self.toggle_sort_rec("badge"))
        self.tree_rec.heading("name", text="Item Name", command=lambda: self.toggle_sort_rec("name"))
        self.tree_rec.heading("category", text="Category", command=lambda: self.toggle_sort_rec("category"))
        self.tree_rec.heading("offer_bid", text="Target Bid", command=lambda: self.toggle_sort_rec("offer_bid"))
        self.tree_rec.heading("alch_val", text="Alch Value", command=lambda: self.toggle_sort_rec("alch_val"))
        self.tree_rec.heading("profit_ea", text="Profit / Alch ▼", command=lambda: self.toggle_sort_rec("profit_ea"))
        self.tree_rec.heading("limit", text="4h Limit", command=lambda: self.toggle_sort_rec("limit"))
        self.tree_rec.heading("batch_profit", text="4h Batch Profit", command=lambda: self.toggle_sort_rec("batch_profit"))
        self.tree_rec.heading("speed", text="Fill Speed", command=lambda: self.toggle_sort_rec("speed"))
        self.tree_rec.heading("batch_cost", text="Batch Spend", command=lambda: self.toggle_sort_rec("batch_cost"))
        self.tree_rec.heading("verdict", text="Why Buy? / Verdict", command=lambda: self.toggle_sort_rec("verdict"))

        self.tree_rec.column("badge", width=55, anchor="center")
        self.tree_rec.column("name", width=165, anchor="w")
        self.tree_rec.column("category", width=130, anchor="center")
        self.tree_rec.column("offer_bid", width=95, anchor="e")
        self.tree_rec.column("alch_val", width=85, anchor="e")
        self.tree_rec.column("profit_ea", width=95, anchor="e")
        self.tree_rec.column("limit", width=95, anchor="center")
        self.tree_rec.column("batch_profit", width=105, anchor="e")
        self.tree_rec.column("speed", width=120, anchor="center")
        self.tree_rec.column("batch_cost", width=100, anchor="e")
        self.tree_rec.column("verdict", width=290, anchor="w")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_rec.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_rec.xview)
        self.tree_rec.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree_rec.pack(side="left", fill="both", expand=True)

        self.tree_rec.bind("<Button-1>", self.on_rec_click)
        self.tree_rec.bind("<Double-1>", self.on_rec_double_click)
        self.tree_rec.bind("<Button-3>", self.on_rec_right_click)

        rec_col_tooltips = {
            "#1": "Rank & Badge:\nRank position within this recommendation list.",
            "#2": "Item Name:\nGrand Exchange item name. Click to copy name to clipboard.",
            "#3": "Category:\nStrategy category: All-Time Workhorse, Fast Fill, Batch Profit, or Overnight Sleeper.",
            "#4": "Target Bid:\nBest buy offer price. Click to copy.",
            "#5": "Alch Value:\nHigh Alchemy gold value.",
            "#6": "Profit / Alch:\nNet gold profit per High Alch cast (Alch Value - Buy Price - Nature Rune Cost).",
            "#7": "4h GE Buy Limit:\nMaximum Grand Exchange units purchasable every 4 hours.",
            "#8": "4h Batch Profit:\nTotal profit earned for a full 4h limit batch (Profit ea * Available limit).",
            "#9": "Fill Speed:\nLive transaction velocity badge (⚡ Fast, ⏱️ Steady, 🐢 Slow).",
            "#10": "Batch Spend:\nTotal gold required to purchase a full batch of this item.",
            "#11": "Why Buy? / Verdict:\nStrategic summary explaining why this item is recommended."
        }
        HeadingToolTip(self.tree_rec, rec_col_tooltips)

    def build_craft_tab(self):
        sub_top = tk.Frame(self.tab_craft, bg="#252528")
        sub_top.pack(fill="x", padx=6, pady=(6, 2))

        tk.Label(sub_top, text="Your Stats:", font=("Segoe UI", 9, "bold"), fg="#f39c12", bg="#252528").pack(side="left", padx=4)

        levels = self.state.config.get("player_levels", {})
        tk.Label(sub_top, text="Crafting:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_craft_lvl = tk.Entry(sub_top, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat")
        self.ent_craft_lvl.insert(0, str(levels.get("Crafting", 99)))
        self.ent_craft_lvl.pack(side="left", padx=(2, 6))
        self.ent_craft_lvl.bind("<FocusOut>", self.on_levels_changed)
        ToolTip(self.ent_craft_lvl, "Your in-game Crafting level. Recipes above this level are flagged or hidden.")

        tk.Label(sub_top, text="Smithing:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_smith_lvl = tk.Entry(sub_top, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat")
        self.ent_smith_lvl.insert(0, str(levels.get("Smithing", 99)))
        self.ent_smith_lvl.pack(side="left", padx=(2, 6))
        self.ent_smith_lvl.bind("<FocusOut>", self.on_levels_changed)
        ToolTip(self.ent_smith_lvl, "Your in-game Smithing level. Recipes above this level are flagged or hidden.")

        tk.Label(sub_top, text="Fletching:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_fletch_lvl = tk.Entry(sub_top, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat")
        self.ent_fletch_lvl.insert(0, str(levels.get("Fletching", 99)))
        self.ent_fletch_lvl.pack(side="left", padx=(2, 6))
        self.ent_fletch_lvl.bind("<FocusOut>", self.on_levels_changed)
        ToolTip(self.ent_fletch_lvl, "Your in-game Fletching level.")

        tk.Label(sub_top, text="Magic:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_mage_lvl = tk.Entry(sub_top, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat")
        self.ent_mage_lvl.insert(0, str(levels.get("Magic", 99)))
        self.ent_mage_lvl.pack(side="left", padx=(2, 10))
        self.ent_mage_lvl.bind("<FocusOut>", self.on_levels_changed)
        ToolTip(self.ent_mage_lvl, "Your in-game Magic level.")

        self.var_only_usable = tk.BooleanVar(value=self.state.config.get("only_usable_recipes", False))
        cb_usable = tk.Checkbutton(sub_top, text="Only Show Usable Recipes", variable=self.var_only_usable, command=self.on_levels_changed,
                                   bg="#252528", fg="#2ecc71", selectcolor="#2d2d30", activebackground="#252528")
        cb_usable.pack(side="left", padx=6)
        ToolTip(cb_usable, "Filter out recipes that exceed your current Crafting, Smithing, Fletching, or Magic levels.")

        # Recipe Search Box
        tk.Label(sub_top, text="🔍", fg="#f39c12", bg="#252528").pack(side="left", padx=(12, 2))
        self.ent_craft_search = tk.Entry(sub_top, width=14, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.ent_craft_search.pack(side="left", padx=(0, 6))
        self.ent_craft_search.bind("<KeyRelease>", self.on_craft_search_changed)
        ToolTip(self.ent_craft_search, "Filter recipes by name or ingredients (e.g. 'rune', 'diamond', 'ring', 'body', 'bow', 'cosmic').")

        # Category Skill Toggle Buttons Row
        sub_filters = tk.Frame(self.tab_craft, bg="#202023")
        sub_filters.pack(fill="x", padx=6, pady=(0, 6))

        tk.Label(sub_filters, text="Categories:", font=("Segoe UI", 9, "bold"), fg="#3498db", bg="#202023").pack(side="left", padx=(4, 6))

        self.var_filter_craft = tk.BooleanVar(value=self.state.config.get("filter_craft", True))
        self.var_filter_smith = tk.BooleanVar(value=self.state.config.get("filter_smith", True))
        self.var_filter_fletch = tk.BooleanVar(value=self.state.config.get("filter_fletch", True))
        self.var_filter_magic = tk.BooleanVar(value=self.state.config.get("filter_magic", True))

        cb_craft = tk.Checkbutton(sub_filters, text="🔨 Crafting", variable=self.var_filter_craft, command=self.on_skill_filter_changed,
                                  bg="#202023", fg="#e67e22", selectcolor="#2d2d30", activebackground="#202023", activeforeground="#e67e22", font=("Segoe UI", 9, "bold"))
        cb_craft.pack(side="left", padx=4)
        ToolTip(cb_craft, "Toggle Crafting recipes (Gold/Silver Jewellery, D'hide Armour, Battlestaves).")

        cb_smith = tk.Checkbutton(sub_filters, text="⚒️ Smithing", variable=self.var_filter_smith, command=self.on_skill_filter_changed,
                                  bg="#202023", fg="#95a5a6", selectcolor="#2d2d30", activebackground="#202023", activeforeground="#bdc3c7", font=("Segoe UI", 9, "bold"))
        cb_smith.pack(side="left", padx=4)
        ToolTip(cb_smith, "Toggle Smithing recipes (Rune, Adamant, Mithril weapons & armour from bars at an anvil).")

        cb_fletch = tk.Checkbutton(sub_filters, text="🏹 Fletching", variable=self.var_filter_fletch, command=self.on_skill_filter_changed,
                                   bg="#202023", fg="#2ecc71", selectcolor="#2d2d30", activebackground="#202023", activeforeground="#2ecc71", font=("Segoe UI", 9, "bold"))
        cb_fletch.pack(side="left", padx=4)
        ToolTip(cb_fletch, "Toggle Fletching recipes (Bows, Crossbows, and Shields from logs).")

        cb_magic = tk.Checkbutton(sub_filters, text="✨ Magic", variable=self.var_filter_magic, command=self.on_skill_filter_changed,
                                  bg="#202023", fg="#9b59b6", selectcolor="#2d2d30", activebackground="#202023", activeforeground="#9b59b6", font=("Segoe UI", 9, "bold"))
        cb_magic.pack(side="left", padx=4)
        ToolTip(cb_magic, "Toggle Magic Enchanting recipes (Enchanting jewellery with Cosmic runes).")

        btn_all = tk.Button(sub_filters, text="All", command=self.select_all_skill_filters, bg="#2d2d30", fg="#f1f1f1", relief="flat", padx=6, font=("Segoe UI", 8))
        btn_all.pack(side="left", padx=(10, 2))
        btn_none = tk.Button(sub_filters, text="None", command=self.clear_all_skill_filters, bg="#2d2d30", fg="#888888", relief="flat", padx=6, font=("Segoe UI", 8))
        btn_none.pack(side="left", padx=2)

        container = ttk.Frame(self.tab_craft)
        container.pack(fill="both", expand=True)

        # Uses tree and headings for +/- hierarchical recipe expansion!
        cols = ("skill_req", "mat_cost", "alch_val", "profit_ea", "extra_vs_buy", "xp_ea", "profit_hr")
        self.tree_craft = ttk.Treeview(container, columns=cols, show="tree headings", selectmode="browse")

        self.tree_craft.heading("#0", text="Recipe / Ingredient Breakdown", command=lambda: self.toggle_sort_craft("recipe"))
        self.tree_craft.heading("skill_req", text="Skill & Req", command=lambda: self.toggle_sort_craft("skill_req"))
        self.tree_craft.heading("mat_cost", text="Materials Cost", command=lambda: self.toggle_sort_craft("mat_cost"))
        self.tree_craft.heading("alch_val", text="Alch Value", command=lambda: self.toggle_sort_craft("alch_val"))
        self.tree_craft.heading("profit_ea", text="Profit (Craft + Alch) ▼", command=lambda: self.toggle_sort_craft("profit_ea"))
        self.tree_craft.heading("extra_vs_buy", text="Bonus vs Buying Finished", command=lambda: self.toggle_sort_craft("bonus"))
        self.tree_craft.heading("xp_ea", text="XP / Item", command=lambda: self.toggle_sort_craft("xp"))
        self.tree_craft.heading("profit_hr", text="Est Craft+Alch GP/Hr", command=lambda: self.toggle_sort_craft("hr_profit"))

        self.tree_craft.column("#0", width=250, anchor="w")
        self.tree_craft.column("skill_req", width=120, anchor="center")
        self.tree_craft.column("mat_cost", width=110, anchor="e")
        self.tree_craft.column("alch_val", width=100, anchor="e")
        self.tree_craft.column("profit_ea", width=140, anchor="e")
        self.tree_craft.column("extra_vs_buy", width=160, anchor="e")
        self.tree_craft.column("xp_ea", width=90, anchor="center")
        self.tree_craft.column("profit_hr", width=140, anchor="e")

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree_craft.yview)
        h_scrollbar = ttk.Scrollbar(container, orient="horizontal", command=self.tree_craft.xview)
        self.tree_craft.configure(yscrollcommand=scrollbar.set, xscrollcommand=h_scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.tree_craft.pack(side="left", fill="both", expand=True)

        self.tree_craft.bind("<Button-1>", self.on_craft_click)

        craft_col_tooltips = {
            "#0": "Recipe / Ingredient Breakdown:\nItem to create. Click row expander [+] to see required raw materials breakdown.\nClick item name to copy to clipboard.",
            "#1": "Skill & Req:\nSkill and minimum level required to craft this item.",
            "#2": "Materials Cost:\nTotal purchase cost of raw materials needed to craft one item.",
            "#3": "Alch Value:\nHigh Alchemy gold value returned upon casting.",
            "#4": "Profit (Craft + Alch):\nTotal profit earned by buying raw materials, crafting, and alching the finished item.\nClick column header to sort.",
            "#5": "Bonus vs Buying Finished:\nExtra profit gained compared to buying the finished item directly on the GE.\nClick column header to sort.",
            "#6": "XP / Item:\nCrafting or Fletching experience granted per created item.\nClick column header to sort.",
            "#7": "Est Craft+Alch GP/Hr:\nProjected hourly profit accounting for crafting + alching speed.\nClick column header to sort."
        }
        HeadingToolTip(self.tree_craft, craft_col_tooltips)
        RowToolTip(self.tree_craft, self.get_craft_row_tooltip)

    def build_guide_tab(self):
        container = ttk.Frame(self.tab_guide)
        container.pack(fill="both", expand=True, padx=6, pady=4)

        # 1. Top Controls Bar: Skill Selector Buttons + Level Inputs + Dynamic Target Banner
        guide_ctrl = tk.Frame(container, bg="#252528", relief="solid", borderwidth=1, padx=8, pady=5)
        guide_ctrl.pack(fill="x", pady=(2, 4))

        tk.Label(guide_ctrl, text="Skill:", font=("Segoe UI", 9, "bold"), fg="#f39c12", bg="#252528").pack(side="left", padx=(2, 6))

        self.var_guide_skill = tk.StringVar(value="Smithing")
        self.btn_guide_skills = {}
        skills_info = [
            ("Smithing", "⚒️ Smithing"),
            ("Fletching", "🏹 Fletching"),
            ("Crafting", "🔨 Crafting"),
            ("Magic", "✨ Magic")
        ]
        for sk_key, sk_label in skills_info:
            b = tk.Button(guide_ctrl, text=sk_label, command=lambda k=sk_key: self.set_guide_skill(k),
                          bg="#f39c12" if sk_key == "Smithing" else "#2d2d30",
                          fg="#000000" if sk_key == "Smithing" else "#cccccc",
                          font=("Segoe UI", 9, "bold" if sk_key == "Smithing" else "normal"),
                          relief="flat", padx=8, pady=1, cursor="hand2")
            b.pack(side="left", padx=2)
            self.btn_guide_skills[sk_key] = b
            ToolTip(b, f"Switch Skilling & Level Training Guide to {sk_key}.")

        tk.Label(guide_ctrl, text="|", fg="#444444", bg="#252528").pack(side="left", padx=6)

        # Current Level & Target Level Inputs
        tk.Label(guide_ctrl, text="Current Lvl:", fg="#cccccc", bg="#252528", font=("Segoe UI", 8)).pack(side="left", padx=(2, 2))
        self.ent_guide_cur_lvl = tk.Entry(guide_ctrl, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat", justify="center")
        init_smith = self.state.config.get("player_levels", {}).get("Smithing", 1)
        self.ent_guide_cur_lvl.insert(0, str(init_smith))
        self.ent_guide_cur_lvl.pack(side="left", padx=(0, 6))
        self.ent_guide_cur_lvl.bind("<FocusOut>", lambda e: self.on_guide_levels_changed())
        self.ent_guide_cur_lvl.bind("<Return>", lambda e: self.on_guide_levels_changed())
        ToolTip(self.ent_guide_cur_lvl, "Your current skill level.\nAutomatically updates when logged into RuneLite / Microbot bridge, or edit manually.")

        tk.Label(guide_ctrl, text="Goal Lvl:", fg="#cccccc", bg="#252528", font=("Segoe UI", 8)).pack(side="left", padx=(2, 2))
        self.ent_guide_target_lvl = tk.Entry(guide_ctrl, width=4, bg="#1e1e1e", fg="#2ecc71", relief="flat", justify="center")
        self.ent_guide_target_lvl.insert(0, str(self.state.config.get("guide_target_level", 99)))
        self.ent_guide_target_lvl.pack(side="left", padx=(0, 6))
        self.ent_guide_target_lvl.bind("<FocusOut>", lambda e: self.on_guide_levels_changed())
        self.ent_guide_target_lvl.bind("<Return>", lambda e: self.on_guide_levels_changed())
        ToolTip(self.ent_guide_target_lvl, "Target level goal (e.g. 50, 70, 85, 99).\nCalculates total remaining XP, actions, and cost required.")

        tk.Label(guide_ctrl, text="|", fg="#444444", bg="#252528").pack(side="left", padx=6)

        # Style & Strategy Radio / Filter
        self.var_guide_style = tk.StringVar(value="all")
        style_radios = [
            ("All", "all", "Show all training methods."),
            ("💰 Profitable", "profit", "Filter to methods that yield net gold profit or minimal loss."),
            ("⚡ Fast XP", "fast", "Filter to high XP/hr progression methods."),
            ("☕ AFK", "afk", "Filter to low-click, relaxed methods.")
        ]
        for slab, sval, stip in style_radios:
            r = tk.Radiobutton(guide_ctrl, text=slab, variable=self.var_guide_style, value=sval,
                               command=self.recalculate_guide_table,
                               bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30",
                               activebackground="#252528", activeforeground="#f39c12",
                               font=("Segoe UI", 8))
            r.pack(side="left", padx=3)
            ToolTip(r, stip)

        init_guide_p2p = (not self.var_f2p.get()) if hasattr(self, "var_f2p") else self.state.config.get("guide_members", True)
        self.var_guide_members = tk.BooleanVar(value=init_guide_p2p)
        self.cb_guide_mem = tk.Checkbutton(guide_ctrl, text="P2P Methods", variable=self.var_guide_members, command=self.on_guide_p2p_toggled,
                                           bg="#252528", fg="#3498db", selectcolor="#2d2d30", activebackground="#252528", font=("Segoe UI", 8))
        self.cb_guide_mem.pack(side="left", padx=3)
        ToolTip(self.cb_guide_mem, "Include Members-only (P2P) skilling brackets and quests.\nUncheck if training on Free-to-play (F2P).")

        # Target Profit Margin per item (Breakeven if 0)
        tk.Label(guide_ctrl, text="|", fg="#444444", bg="#252528").pack(side="left", padx=4)
        tk.Label(guide_ctrl, text="Target Margin:", fg="#cccccc", bg="#252528", font=("Segoe UI", 8)).pack(side="left", padx=(2, 2))
        self.var_guide_margin = tk.StringVar(value=str(self.state.config.get("guide_margin", 0)))
        self.ent_guide_margin = tk.Entry(guide_ctrl, textvariable=self.var_guide_margin, width=5, bg="#1e1e1e", fg="#2ecc71",
                                         insertbackground="#ffffff", relief="flat", font=("Segoe UI", 8))
        self.ent_guide_margin.pack(side="left", padx=(0, 4))
        self.ent_guide_margin.bind("<KeyRelease>", lambda e: self.on_guide_margin_changed())
        ToolTip(self.ent_guide_margin, "Target Safety Profit Margin per item (GP):\n• 0 gp = Exact Breakeven buy price (0 gp loss).\n• 50 / 100 / 200 gp = Max buy price needed to guarantee that profit margin.")

        # Right Action Buttons
        btn_guide_batch = tk.Button(guide_ctrl, text="🛒 Add Batch to Cart", command=self.add_guide_batch_to_cart,
                                    bg="#27ae60", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=2, cursor="hand2")
        btn_guide_batch.pack(side="right", padx=3)
        ToolTip(btn_guide_batch, "🛒 Add Training Batch to Cart:\nAdds materials or alchables for the active or selected step into your shopping cart.")

        btn_shop_list = tk.Button(guide_ctrl, text="📋 Shopping List", command=self.copy_guide_shopping_list,
                                  bg="#2980b9", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=6, pady=2, cursor="hand2")
        btn_shop_list.pack(side="right", padx=3)
        ToolTip(btn_shop_list, "📋 Copy Shopping List:\nCopies formatted materials and cost list for this bracket to clipboard.")

        btn_bank_tag = tk.Button(guide_ctrl, text="🏷️ Bank Tag", command=self.copy_guide_bank_tag,
                                 bg="#8e44ad", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=6, pady=2, cursor="hand2")
        btn_bank_tag.pack(side="right", padx=3)
        ToolTip(btn_bank_tag, "🏷️ Copy RuneLite Bank Tag:\nCopies a RuneLite Bank Tag Tab string to organize all training materials in your bank.")

        # 2. Dynamic Progress & XP Summary Banner
        self.banner_guide_xp = tk.Frame(container, bg="#202023", relief="solid", borderwidth=1, padx=8, pady=4)
        self.banner_guide_xp.pack(fill="x", pady=(0, 4))
        self.lbl_guide_xp_summary = tk.Label(self.banner_guide_xp, text="🎯 Calculating progression...", font=("Segoe UI", 9), fg="#e0e0e0", bg="#202023")
        self.lbl_guide_xp_summary.pack(anchor="w")

        # 3. Early Quest Skips & Shortcuts Card
        self.frame_guide_quests = tk.Frame(container, bg="#202023", relief="solid", borderwidth=1, padx=8, pady=4)
        self.frame_guide_quests.pack(fill="x", pady=(0, 4))

        q_top = tk.Frame(self.frame_guide_quests, bg="#202023")
        q_top.pack(fill="x")
        tk.Label(q_top, text="📜 Essential Early Quest Skips & Shortcuts (Click 🌐 to view Wiki Guide):",
                 font=("Segoe UI", 8, "bold"), fg="#f1c40f", bg="#202023").pack(side="left")

        self.frame_quest_inner = tk.Frame(self.frame_guide_quests, bg="#202023")
        self.frame_quest_inner.pack(fill="x", pady=(3, 0))

        # 4. Skilling Progression Treeview Table
        tree_frame = ttk.Frame(container)
        tree_frame.pack(fill="both", expand=True)

        cols = ("status", "level_range", "name", "materials", "tot_mats", "needed", "max_buy", "xp_ea", "gp_xp", "bracket_cost", "action_rec", "xp_rate", "time_est", "verdict")
        self.tree_guide = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_guide.heading("status", text="Status", command=lambda: self.toggle_sort_guide("status"))
        self.tree_guide.heading("level_range", text="Level Range", command=lambda: self.toggle_sort_guide("level_range"))
        self.tree_guide.heading("name", text="Training Method", command=lambda: self.toggle_sort_guide("name"))
        self.tree_guide.heading("materials", text="Materials (ea)", command=lambda: self.toggle_sort_guide("materials"))
        self.tree_guide.heading("tot_mats", text="Total Mats Needed", command=lambda: self.toggle_sort_guide("tot_mats"))
        self.tree_guide.heading("needed", text="Units Needed", command=lambda: self.toggle_sort_guide("needed"))
        self.tree_guide.heading("max_buy", text="🎯 Max Mat Buy", command=lambda: self.toggle_sort_guide("max_buy"))
        self.tree_guide.heading("xp_ea", text="XP / Act", command=lambda: self.toggle_sort_guide("xp_ea"))
        self.tree_guide.heading("gp_xp", text="Live GP/XP", command=lambda: self.toggle_sort_guide("gp_xp"))
        self.tree_guide.heading("bracket_cost", text="Net Profit / Loss", command=lambda: self.toggle_sort_guide("bracket_cost"))
        self.tree_guide.heading("action_rec", text="Best Disposal", command=lambda: self.toggle_sort_guide("action_rec"))
        self.tree_guide.heading("xp_rate", text="XP / Hour", command=lambda: self.toggle_sort_guide("xp_rate"))
        self.tree_guide.heading("time_est", text="Est. Time", command=lambda: self.toggle_sort_guide("time_est"))
        self.tree_guide.heading("verdict", text="Strategy Tips / Verdict", command=lambda: self.toggle_sort_guide("verdict"))

        self.tree_guide.column("status", width=110, anchor="center")
        self.tree_guide.column("level_range", width=75, anchor="center")
        self.tree_guide.column("name", width=175, anchor="w")
        self.tree_guide.column("materials", width=130, anchor="w")
        self.tree_guide.column("tot_mats", width=145, anchor="w")
        self.tree_guide.column("needed", width=85, anchor="e")
        self.tree_guide.column("max_buy", width=110, anchor="e")
        self.tree_guide.column("xp_ea", width=65, anchor="e")
        self.tree_guide.column("gp_xp", width=85, anchor="e")
        self.tree_guide.column("bracket_cost", width=100, anchor="e")
        self.tree_guide.column("action_rec", width=100, anchor="center")
        self.tree_guide.column("xp_rate", width=80, anchor="e")
        self.tree_guide.column("time_est", width=70, anchor="center")
        self.tree_guide.column("verdict", width=260, anchor="w")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_guide.yview)
        h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_guide.xview)
        self.tree_guide.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")
        self.tree_guide.pack(side="left", fill="both", expand=True)

        self.tree_guide.tag_configure("current", foreground="#f1c40f", font=("Segoe UI", 9, "bold"))
        self.tree_guide.tag_configure("completed", foreground="#7f8c8d")
        self.tree_guide.tag_configure("locked", foreground="#666666")
        self.tree_guide.tag_configure("profit", foreground="#2ecc71")
        self.tree_guide.tag_configure("mild_loss", foreground="#f39c12")
        self.tree_guide.tag_configure("loss", foreground="#e74c3c")
        self.tree_guide.tag_configure("quest", foreground="#3498db", font=("Segoe UI", 9, "bold"))

        self.tree_guide.bind("<Button-1>", self.on_guide_click)
        self.tree_guide.bind("<Double-1>", self.on_guide_double_click)
        self.tree_guide.bind("<Button-3>", self.on_guide_right_click)

        guide_col_tooltips = {
            "#1": "Status:\n📍 YOU ARE HERE (Current training step for your level)\n✅ Completed (Already passed this level)\n🔒 Locked (Requires higher level).",
            "#2": "Level Range:\nRecommended level bracket for this skilling method.",
            "#3": "Training Method:\nSpecific item to smith/fletch/craft or quest to complete.",
            "#4": "Materials Needed (ea):\nRaw ingredients required per single action.",
            "#5": "Total Mats Needed:\nTotal raw materials / bars needed to complete this bracket (or remaining for your level goal).",
            "#6": "Units Needed:\nNumber of actions required to complete this bracket (or reach your target goal).",
            "#7": "🎯 Max Mat Buy:\nMaximum GE buy price to pay for raw materials to break even (or meet target margin).",
            "#8": "XP / Act:\nExperience granted per single crafted/smithed item or cast.",
            "#9": "Live GP/XP:\nNet gold profit/cost per experience point based on live Grand Exchange market prices.",
            "#10": "Net Profit / Loss:\nTotal projected gold profit (+) or loss (-) to complete all needed units in this bracket.",
            "#11": "Best Disposal:\nOptimal way to dispose of finished products: 🪄 High Alch vs 🏪 Sell on GE vs 📜 Quest Turn-in.",
            "#12": "XP / Hour:\nRealistic hourly experience rate attainable with this method.",
            "#13": "Est. Time:\nProjected grind time to finish this bracket at standard XP/hr rates.",
            "#14": "Strategy Tips / Verdict:\nPro tips, quest skips, and strategy breakdown."
        }
        HeadingToolTip(self.tree_guide, guide_col_tooltips)
        RowToolTip(self.tree_guide, self.get_guide_row_tooltip)

        self.guide_rows = []
        self.guide_sort_col = "level_range"
        self.guide_sort_asc = True
        self.update_guide_quests_card("Smithing")

    def set_guide_skill(self, skill_name):
        self.var_guide_skill.set(skill_name)
        for sk_key, b in self.btn_guide_skills.items():
            if sk_key == skill_name:
                b.config(bg="#f39c12", fg="#000000", font=("Segoe UI", 9, "bold"))
            else:
                b.config(bg="#2d2d30", fg="#cccccc", font=("Segoe UI", 9))

        curr_char = self.var_account.get() if hasattr(self, "var_account") else "All Accounts"
        player_levels = self.state.config.get("player_levels", {})
        if curr_char != "All Accounts" and curr_char in self.state.accounts:
            char_lvls = self.state.accounts[curr_char].get("levels", {})
            lvl = char_lvls.get(skill_name, player_levels.get(skill_name, 1))
        else:
            lvl = player_levels.get(skill_name, 1)

        self.ent_guide_cur_lvl.delete(0, tk.END)
        self.ent_guide_cur_lvl.insert(0, str(lvl))

        self.update_guide_quests_card(skill_name)
        self.recalculate_guide_table()

    def is_guide_p2p_allowed(self):
        # Strict F2P mode: if top bar F2P is checked and Members is not checked, or guide P2P is unchecked
        if hasattr(self, "var_f2p") and self.var_f2p.get() and hasattr(self, "var_members") and not self.var_members.get():
            return False
        if hasattr(self, "var_guide_members"):
            return self.var_guide_members.get()
        return True

    def on_guide_p2p_toggled(self):
        p2p_on = self.var_guide_members.get()
        if hasattr(self, "var_members") and hasattr(self, "var_f2p"):
            self.var_members.set(p2p_on)
            self.var_f2p.set(not p2p_on)
            self.state.config["members"] = p2p_on
            self.state.config["f2p"] = not p2p_on
        self.state.config["guide_members"] = p2p_on
        self.save_preferences()
        self.update_guide_quests_card(self.var_guide_skill.get())
        self.recalculate_all()

    def update_guide_quests_card(self, skill_name):
        for w in self.frame_quest_inner.winfo_children():
            w.destroy()

        sdata = SKILLING_GUIDES.get(skill_name, {})
        quests = sdata.get("quests", [])
        p2p_allowed = self.is_guide_p2p_allowed()

        filtered_quests = [q for q in quests if p2p_allowed or not q.get("members", True)]

        if not filtered_quests:
            msg = "ℹ️ No F2P quest skips for this skill (All quest skips require Members)." if not p2p_allowed else "No early quest skips registered for this skill."
            tk.Label(self.frame_quest_inner, text=msg, fg="#888888", bg="#202023", font=("Segoe UI", 8)).pack(side="left")
            return

        for q in filtered_quests:
            q_btn = tk.Button(self.frame_quest_inner, text=f"📜 {q['name']} ({q['skip'].split('!')[0]}) 🌐",
                              command=lambda slug=q['wiki_slug']: webbrowser.open(f"https://oldschool.runescape.wiki/w/{slug}"),
                              bg="#2d2d30", fg="#3498db", activebackground="#3498db", activeforeground="#ffffff",
                              relief="flat", padx=6, pady=1, font=("Segoe UI", 8, "bold"), cursor="hand2")
            q_btn.pack(side="left", padx=3)
            mem_tag = " (Members)" if q.get("members", True) else " (F2P)"
            q_tip = (
                f"Quest: {q['name']}{mem_tag}\n"
                f"XP Reward: {q['xp']:,} XP\n"
                f"Benefit: {q['skip']}\n"
                f"Requirements: {q['reqs']}\n\n"
                f"Tip: {q['tip']}\n"
                "Click to open the full OSRS Wiki Guide in your browser."
            )
            ToolTip(q_btn, q_tip)

    def on_guide_levels_changed(self):
        try:
            cur_lvl = int(self.ent_guide_cur_lvl.get().strip())
            cur_lvl = max(1, min(99, cur_lvl))
        except ValueError:
            cur_lvl = 1
            self.ent_guide_cur_lvl.delete(0, tk.END)
            self.ent_guide_cur_lvl.insert(0, "1")

        try:
            target_lvl = int(self.ent_guide_target_lvl.get().strip())
            target_lvl = max(cur_lvl, min(99, target_lvl))
        except ValueError:
            target_lvl = 99
            self.ent_guide_target_lvl.delete(0, tk.END)
            self.ent_guide_target_lvl.insert(0, "99")

        active_skill = self.var_guide_skill.get()
        self.state.config.setdefault("player_levels", {})[active_skill] = cur_lvl
        self.state.config["guide_target_level"] = target_lvl
        self.state.save_config()

        self.recalculate_guide_table()

    def on_guide_margin_changed(self):
        try:
            val = parse_cash_input(self.var_guide_margin.get())
            self.state.config["guide_margin"] = max(0, val)
            self.save_preferences()
        except Exception:
            pass
        self.recalculate_guide_table()

    def recalculate_guide_table(self):
        if not hasattr(self, "tree_guide"):
            return

        active_skill = self.var_guide_skill.get()
        try:
            cur_lvl = int(self.ent_guide_cur_lvl.get().strip())
        except ValueError:
            cur_lvl = 1

        try:
            target_lvl = int(self.ent_guide_target_lvl.get().strip())
        except ValueError:
            target_lvl = 99

        cur_xp = get_xp_for_level(cur_lvl)
        target_xp = get_xp_for_level(target_lvl)
        rem_xp = max(0, target_xp - cur_xp)
        pct_done = (1.0 - (rem_xp / max(1, target_xp))) * 100.0 if target_xp > 0 else 100.0

        summary_txt = f"🎯 Goal: Level {target_lvl} ({target_xp:,} XP)  |  Current: Level {cur_lvl} ({cur_xp:,} XP)  |  XP Remaining: {rem_xp:,} XP ({pct_done:.1f}% Complete)"
        if hasattr(self, "lbl_guide_xp_summary"):
            self.lbl_guide_xp_summary.config(text=summary_txt)

        self.tree_guide.delete(*self.tree_guide.get_children())
        self.guide_rows = []
        search_query = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""

        sdata = SKILLING_GUIDES.get(active_skill, {})
        brackets = sdata.get("brackets", [])
        style_filter = self.var_guide_style.get()
        mem_ok = self.is_guide_p2p_allowed()

        # Update local checkbutton visual state if needed
        if hasattr(self, "cb_guide_mem") and hasattr(self, "var_guide_members"):
            if self.var_guide_members.get() != mem_ok:
                self.var_guide_members.set(mem_ok)

        # If skill is strictly members-only (like Fletching) and mem_ok is False:
        if active_skill == "Fletching" and not mem_ok:
            if hasattr(self, "lbl_guide_xp_summary"):
                self.lbl_guide_xp_summary.config(text="⚠️ Fletching is a Members-only skill in Old School RuneScape. Enable P2P Methods to view recipes.")
            self.tree_guide.insert("", "end", iid="fletch_p2p_warn", values=(
                "🔒 P2P Only",
                "1 - 99",
                "Fletching is Members-only",
                "None (P2P)",
                "--",
                "0",
                "--",
                "0",
                "--",
                "--",
                "Enable P2P",
                "--",
                "--",
                "⚠️ Fletching cannot be trained on Free-to-play worlds."
            ), tags=("locked",))
            return

        strat = self.var_strat.get().split()[0] if hasattr(self, "var_strat") else "smart"
        nat_price = self.get_effective_nature_price()

        current_step_found = False

        for b in brackets:
            b_mem = b.get("members", True)
            if not mem_ok and b_mem:
                continue

            b_style = b.get("style", "standard")
            if style_filter == "profit" and b_style not in ("profit", "quest"):
                continue
            if style_filter == "fast" and b_style not in ("fast", "quest"):
                continue
            if style_filter == "afk" and b_style not in ("afk", "quest"):
                continue

            min_l = b["min_lvl"]
            max_l = b["max_lvl"]

            # Status determination
            if cur_lvl >= max_l:
                status = "✅ Completed"
                status_tag = "completed"
            elif min_l <= cur_lvl < max_l:
                status = "📍 YOU ARE HERE"
                status_tag = "current"
                current_step_found = True
            elif not current_step_found and cur_lvl < min_l:
                status = "🔒 Locked"
                status_tag = "locked"
            else:
                status = "🔒 Locked"
                status_tag = "locked"

            if b_style == "quest":
                status_tag = "quest"

            # Actions needed
            xp_ea = b.get("xp_per_action", 1.0)
            if cur_lvl >= max_l:
                xp_needed_bracket = 0
                actions_needed = 0
            else:
                step_start_xp = max(get_xp_for_level(cur_lvl), get_xp_for_level(min_l))
                step_end_xp = min(get_xp_for_level(max_l), target_xp)
                xp_needed_bracket = max(0, step_end_xp - step_start_xp)
                actions_needed = math.ceil(xp_needed_bracket / xp_ea) if (xp_ea > 0 and xp_needed_bracket > 0) else 0

            # Material cost & total materials needed calculation
            mat_cost_ea = 0
            mat_str_list = []
            mats = b.get("materials", [])
            for m in mats:
                p = self.api.get_price(m["id"], strat)
                mat_cost_ea += p * m["qty"]
                mat_str_list.append(f"{m['qty']}x {m['name']}")
            materials_str = ", ".join(mat_str_list) if mat_str_list else "None / Quest"

            # Total materials needed across the bracket
            tot_mats_str = "--"
            tot_mat_qty = 0
            primary_mat_name = mats[0]["name"] if mats else ""

            display_actions = actions_needed
            if display_actions == 0 and cur_lvl < min_l:
                # Locked / upcoming bracket: calculate full bracket requirement
                bracket_xp = min(get_xp_for_level(max_l), target_xp) - get_xp_for_level(min_l)
                display_actions = math.ceil(bracket_xp / xp_ea) if (xp_ea > 0 and bracket_xp > 0) else 0

            if mats:
                if display_actions > 0:
                    tot_mat_qty = mats[0]["qty"] * display_actions
                    tot_mats_list = [f"{m['qty'] * display_actions:,}x {m['name']}" for m in mats]
                    tot_mats_str = ", ".join(tot_mats_list)
                elif cur_lvl >= max_l:
                    tot_mats_str = "0 (Completed)"
                else:
                    tot_mats_str = "0"
            elif b_style == "quest":
                tot_mats_str = "None (Quest)"

            # Output valuation & disposal recommendation
            out_id = b.get("output_id", 0)
            alch_val = self.api.mapping.get(str(out_id), {}).get("highalch", 0) if b.get("can_alch") else 0
            nat_cost = nat_price if b.get("nature_cost", 0) > 0 else 0
            total_act_cost = mat_cost_ea + nat_cost

            profit_alch = (alch_val - total_act_cost) if b.get("can_alch") else -99999999
            ge_sell = self.api.get_price(out_id, "instasell") if b.get("can_sell_ge") and out_id > 0 else 0
            profit_ge = (int(ge_sell * 0.99) - mat_cost_ea) if b.get("can_sell_ge") and out_id > 0 else -99999999

            if b_style == "quest":
                action_rec = "📜 Quest Turn-in"
                best_profit_ea = 0
                gp_per_xp = 0.0
                gp_xp_str = "FREE (0 GP)"
                bracket_cost_str = "0 gp"
                total_cost = 0
            elif profit_alch >= profit_ge and b.get("can_alch"):
                action_rec = "🪄 High Alch"
                best_profit_ea = profit_alch
                gp_per_xp = best_profit_ea / xp_ea if xp_ea > 0 else 0.0
                gp_xp_str = f"+{gp_per_xp:.2f} GP/XP" if gp_per_xp >= 0 else f"{gp_per_xp:.2f} GP/XP"
                total_cost = best_profit_ea * (actions_needed if actions_needed > 0 else 100)
                bracket_cost_str = f"+{format_gp(total_cost)}" if total_cost >= 0 else f"-{format_gp(abs(total_cost))}"
            elif b.get("can_sell_ge"):
                action_rec = "🏪 Sell on GE"
                best_profit_ea = profit_ge
                gp_per_xp = best_profit_ea / xp_ea if xp_ea > 0 else 0.0
                gp_xp_str = f"+{gp_per_xp:.2f} GP/XP" if gp_per_xp >= 0 else f"{gp_per_xp:.2f} GP/XP"
                total_cost = best_profit_ea * (actions_needed if actions_needed > 0 else 100)
                bracket_cost_str = f"+{format_gp(total_cost)}" if total_cost >= 0 else f"-{format_gp(abs(total_cost))}"
            else:
                action_rec = "⚔️ Train / Consume"
                best_profit_ea = -mat_cost_ea
                gp_per_xp = best_profit_ea / xp_ea if xp_ea > 0 else 0.0
                gp_xp_str = f"{gp_per_xp:.2f} GP/XP"
                total_cost = best_profit_ea * (actions_needed if actions_needed > 0 else 100)
                bracket_cost_str = f"-{format_gp(abs(total_cost))}"

            # Breakeven & Target Material Buy Calculation
            target_margin = 0
            if hasattr(self, "ent_guide_margin"):
                try:
                    target_margin = max(0, parse_cash_input(self.ent_guide_margin.get()))
                except Exception:
                    target_margin = 0

            out_qty = b.get("output_qty", 1)
            eff_alch_rev = (alch_val - nat_cost) if (b.get("can_alch") and alch_val > 0) else -99999999
            eff_ge_rev = (int(ge_sell * 0.99) * out_qty) if (b.get("can_sell_ge") and out_id > 0) else -99999999
            best_rev = max(eff_alch_rev, eff_ge_rev)

            curr_mat_p = 0
            breakeven_p = 0
            target_buy_p = 0
            margin_at_curr = 0
            max_buy_str = "--"

            if mats and best_rev > -99999999:
                primary_mat = mats[0]
                primary_qty = primary_mat.get("qty", 1)
                curr_mat_p = self.api.get_price(primary_mat["id"], strat)

                # Secondary materials cost (e.g. gems or bow strings)
                secondary_cost = sum(self.api.get_price(m["id"], strat) * m["qty"] for m in mats[1:])
                net_alloc_rev = best_rev - secondary_cost

                breakeven_p = math.floor(net_alloc_rev / primary_qty) if primary_qty > 0 else 0
                target_buy_p = math.floor((net_alloc_rev - target_margin) / primary_qty) if primary_qty > 0 else 0
                margin_at_curr = target_buy_p - curr_mat_p

                if target_margin > 0:
                    max_buy_str = f"≤ {target_buy_p:,} gp"
                else:
                    max_buy_str = f"≤ {breakeven_p:,} gp"
            elif b_style == "quest":
                max_buy_str = "FREE (Quest)"

            verdict_text = b.get("verdict", "")
            if breakeven_p > 0:
                if target_margin > 0:
                    verdict_text = f"{verdict_text} [🎯 Buy @ ≤ {target_buy_p:,} gp ea (+{target_margin:,} margin | Breakeven: ≤ {breakeven_p:,} gp)]"
                else:
                    verdict_text = f"{verdict_text} [🎯 Breakeven Buy: ≤ {breakeven_p:,} gp ea (Market: {curr_mat_p:,} gp)]"

            # Time estimate
            xp_rate = b.get("xp_rate", 50000)
            if xp_needed_bracket > 0 and xp_rate > 0:
                hrs = xp_needed_bracket / xp_rate
                time_est_str = f"{int(hrs)}h {int((hrs % 1) * 60):02d}m" if hrs >= 1 else f"{max(1, int(hrs * 60))}m"
            elif xp_needed_bracket == 0:
                time_est_str = "0m"
            else:
                time_est_str = "--"

            # Row tag priority
            if status_tag == "current":
                final_tag = "current"
            elif status_tag == "quest":
                final_tag = "quest"
            elif status_tag == "completed":
                final_tag = "completed"
            elif gp_per_xp >= 0:
                final_tag = "profit"
            elif gp_per_xp >= -2.0:
                final_tag = "mild_loss"
            else:
                final_tag = "loss"

            row_obj = {
                "id": f"{min_l}_{max_l}_{b['name']}",
                "status": status,
                "level_range": f"{min_l} - {max_l}",
                "name": b["name"],
                "materials": materials_str,
                "materials_raw": b.get("materials", []),
                "tot_mats": tot_mats_str,
                "tot_mat_qty": tot_mat_qty,
                "max_buy": max_buy_str,
                "max_buy_val": target_buy_p if target_buy_p > 0 else breakeven_p,
                "breakeven_ea": breakeven_p,
                "target_buy_p": target_buy_p,
                "curr_mat_price": curr_mat_p,
                "margin_ea": margin_at_curr,
                "primary_mat_name": primary_mat_name,
                "xp_ea": xp_ea,
                "needed": actions_needed,
                "gp_xp": gp_xp_str,
                "gp_xp_val": gp_per_xp,
                "bracket_cost": bracket_cost_str,
                "bracket_cost_val": total_cost,
                "action_rec": action_rec,
                "xp_rate": f"{xp_rate // 1000}k/hr" if xp_rate >= 1000 else f"{xp_rate}/hr",
                "xp_rate_val": xp_rate,
                "time_est": time_est_str,
                "verdict": verdict_text,
                "output_id": out_id,
                "nature_cost": b.get("nature_cost", 0),
                "tag": final_tag,
                "min_lvl": min_l,
                "max_lvl": max_l,
                "wiki_slug": b.get("wiki_slug", "")
            }

            if search_query:
                name_match = search_query in b["name"].lower()
                mat_match = search_query in materials_str.lower()
                verdict_match = search_query in verdict_text.lower()
                action_match = search_query in action_rec.lower()
                if not (name_match or mat_match or verdict_match or action_match):
                    continue

            self.guide_rows.append(row_obj)

        for r in self.guide_rows:
            self.tree_guide.insert("", "end", iid=r["id"], values=(
                r["status"],
                r["level_range"],
                r["name"],
                r["materials"],
                r["tot_mats"],
                f"{r['needed']:,}",
                r["max_buy"],
                f"{r['xp_ea']:,.1f}" if r["xp_ea"] % 1 else f"{int(r['xp_ea']):,}",
                r["gp_xp"],
                r["bracket_cost"],
                r["action_rec"],
                r["xp_rate"],
                r["time_est"],
                r["verdict"]
            ), tags=(r["tag"],))

        # Append current step target buy info to XP summary banner if available
        curr_step = next((r for r in self.guide_rows if "YOU ARE HERE" in r.get("status", "")), None)
        if curr_step and curr_step.get("breakeven_ea", 0) > 0 and hasattr(self, "lbl_guide_xp_summary"):
            cur_summary = self.lbl_guide_xp_summary.cget("text")
            if "Target Buy:" not in cur_summary:
                self.lbl_guide_xp_summary.config(text=f"{cur_summary}  |  🎯 Current Step Buy: {curr_step['max_buy']} ({curr_step.get('primary_mat_name', 'bars')})")

    def get_selected_guide_row(self):
        sel = self.tree_guide.selection()
        if not sel:
            return None
        row_id = sel[0]
        return next((r for r in self.guide_rows if r["id"] == row_id), None)

    def on_guide_click(self, event):
        row_id = self.tree_guide.identify_row(event.y)
        if not row_id:
            return
        row = next((r for r in self.guide_rows if r["id"] == row_id), None)
        if not row:
            return
        col_id = self.tree_guide.identify_column(event.x)
        if col_id == "#3":
            self.copy_to_clipboard(row["name"], f"Copied '{row['name']}' to clipboard!")
        elif col_id == "#4":
            self.copy_to_clipboard(row["materials"], f"Copied materials for '{row['name']}' to clipboard!")
        elif col_id == "#5":
            qty = row.get("tot_mat_qty", 0)
            if qty > 0:
                mat_n = row.get("primary_mat_name", "materials")
                self.copy_to_clipboard(str(qty), f"📋 Copied Total Material Quantity ({qty:,}) for {mat_n} to clipboard!")
            elif row.get("tot_mats"):
                self.copy_to_clipboard(row["tot_mats"], f"Copied '{row['tot_mats']}' to clipboard!")
        elif col_id == "#6":
            self.copy_to_clipboard(str(row["needed"]), f"Copied needed units ({row['needed']:,}) to clipboard!")
        elif col_id == "#7":
            p = row.get("target_buy_p", 0) or row.get("breakeven_ea", 0)
            if p > 0:
                mat_n = row.get("primary_mat_name", "materials")
                self.copy_to_clipboard(str(p), f"📋 Copied Max Buy Price ({p:,} gp) for {mat_n} to clipboard!")

    def on_guide_double_click(self, event):
        row_id = self.tree_guide.identify_row(event.y)
        if not row_id:
            return
        self.tree_guide.selection_set(row_id)
        self.add_guide_batch_to_cart()

    def on_guide_right_click(self, event):
        row_id = self.tree_guide.identify_row(event.y)
        if not row_id:
            return
        self.tree_guide.selection_set(row_id)
        row = next((r for r in self.guide_rows if r["id"] == row_id), None)
        if not row:
            return

        menu = tk.Menu(self, tearoff=0, bg="#2d2d30", fg="#ffffff", activebackground="#f39c12", activeforeground="#000000")
        menu.add_command(label=f"🛒 Add Training Batch to Cart ({row['needed']:,} units)", command=self.add_guide_batch_to_cart)
        p_buy = row.get("target_buy_p", 0) or row.get("breakeven_ea", 0)
        if p_buy > 0:
            mat_n = row.get("primary_mat_name", "materials")
            menu.add_command(label=f"🎯 Copy Max Buy Price ({p_buy:,} gp for {mat_n})",
                             command=lambda pb=p_buy, mn=mat_n: self.copy_to_clipboard(str(pb), f"Copied {pb:,} gp for {mn}!"))
        tot_qty = row.get("tot_mat_qty", 0)
        if tot_qty > 0:
            mat_n = row.get("primary_mat_name", "materials")
            menu.add_command(label=f"📦 Copy Total Material Qty ({tot_qty:,}x {mat_n})",
                             command=lambda tq=tot_qty, mn=mat_n: self.copy_to_clipboard(str(tq), f"Copied {tq:,} for {mn}!"))
        menu.add_separator()
        menu.add_command(label="📋 Copy Shopping List for this Step", command=self.copy_guide_shopping_list)
        menu.add_command(label="🏷️ Copy RuneLite Bank Tag Tab", command=self.copy_guide_bank_tag)
        menu.add_command(label=f"📋 Copy Method Name ('{row['name']}')", command=lambda: self.copy_to_clipboard(row["name"], f"Copied '{row['name']}'!"))
        if row.get("output_id", 0) > 0:
            menu.add_separator()
            menu.add_command(label="🌐 Open in OSRS Wiki Prices", command=lambda: self.open_wiki_url(row["output_id"]))
        elif row.get("wiki_slug"):
            menu.add_separator()
            menu.add_command(label="🌐 Open Quest Guide on OSRS Wiki", command=lambda: webbrowser.open(f"https://oldschool.runescape.wiki/w/{row['wiki_slug']}"))
        menu.post(event.x_root, event.y_root)

    def add_guide_batch_to_cart(self):
        row = self.get_selected_guide_row()
        if not row:
            row = next((r for r in self.guide_rows if "YOU ARE HERE" in r.get("status", "")), None)
        if not row or (row.get("output_id", 0) == 0 and not row.get("materials_raw")):
            row = next((r for r in self.guide_rows if r.get("materials_raw") or r.get("output_id", 0) > 0), None)
        if not row:
            return

        needed_actions = max(1, row.get("needed", 100))
        mats = row.get("materials_raw", [])
        if mats:
            primary_mat = mats[0]
            mat_id = str(primary_mat["id"])
            total_needed = primary_mat["qty"] * needed_actions
            mdata = self.api.mapping.get(mat_id, {})
            base_limit = mdata.get("limit", 10000)
            batch_qty = min(total_needed, base_limit)

            self.state.cart_items[mat_id] = batch_qty
            self.recalculate_alch_table()
            self.update_cart_display()
            self.lbl_status_right.config(text=f"🛒 Added {batch_qty:,}x {primary_mat['name']} to cart for {row['name']}", fg="#2ecc71")
        elif row.get("output_id", 0) > 0:
            item_id = str(row["output_id"])
            mdata = self.api.mapping.get(item_id, {})
            base_limit = mdata.get("limit", 70)
            batch_qty = min(needed_actions, base_limit)
            self.state.cart_items[item_id] = batch_qty
            self.recalculate_alch_table()
            self.update_cart_display()
            self.lbl_status_right.config(text=f"🛒 Added {batch_qty:,}x {row['name']} to cart", fg="#2ecc71")

    def copy_guide_shopping_list(self):
        row = self.get_selected_guide_row()
        if not row:
            row = next((r for r in self.guide_rows if "YOU ARE HERE" in r.get("status", "")), None)
        if not row or (row.get("output_id", 0) == 0 and not row.get("materials_raw")):
            row = next((r for r in self.guide_rows if r.get("materials_raw") or r.get("output_id", 0) > 0), None)
        if not row:
            return

        needed_units = max(1, row["needed"]) if row["needed"] > 0 else 100
        lines = [
            f"========================================",
            f"🎓 OSRS SKILLING SHOPPING LIST: {self.var_guide_skill.get()}",
            f"Method: {row['name']}",
            f"Level Bracket: {row['level_range']}",
            f"Actions Required: {needed_units:,} units",
            f"----------------------------------------",
            f"Required Materials:"
        ]
        total_mat_cost = 0
        strat = self.var_strat.get().split()[0] if hasattr(self, "var_strat") else "smart"
        for m in row.get("materials_raw", []):
            p = self.api.get_price(m["id"], strat)
            tot_qty = m["qty"] * needed_units
            sub = p * tot_qty
            total_mat_cost += sub
            lines.append(f"  • {tot_qty:,}x {m['name']} (~{format_gp(sub)})")

        if row.get("nature_cost", 0) > 0 and row.get("action_rec") == "🪄 High Alch":
            nat_price = self.get_effective_nature_price()
            tot_nats = row["nature_cost"] * needed_units
            sub_nat = nat_price * tot_nats
            total_mat_cost += sub_nat
            lines.append(f"  • {tot_nats:,}x Nature rune (~{format_gp(sub_nat)})")

        if row.get("breakeven_ea", 0) > 0:
            lines.append(f"----------------------------------------")
            lines.append(f"🎯 Target GE Buy: {row['max_buy']} ea (for {row.get('primary_mat_name', 'materials')})")
            lines.append(f"   (Breakeven ceiling: ≤ {row['breakeven_ea']:,} gp ea)")

        lines.append(f"Total Est. Cost: {format_gp(total_mat_cost)}")
        lines.append(f"Disposal Strategy: {row['action_rec']}")
        lines.append(f"Net Est. Outcome: {row['bracket_cost']} ({row['gp_xp']})")
        lines.append(f"Est. Training Time: {row['time_est']} ({row['xp_rate']})")
        lines.append(f"========================================")

        text = "\n".join(lines)
        self.copy_to_clipboard(text, f"📋 Copied Skilling Shopping List for {row['name']}!")

    def copy_guide_bank_tag(self):
        row = self.get_selected_guide_row()
        if not row:
            row = next((r for r in self.guide_rows if "YOU ARE HERE" in r.get("status", "")), None)
        if not row or (row.get("output_id", 0) == 0 and not row.get("materials_raw")):
            row = next((r for r in self.guide_rows if r.get("materials_raw") or r.get("output_id", 0) > 0), None)
        if not row:
            return

        skill_tag = self.var_guide_skill.get().lower()[:5]
        bracket_tag = row['level_range'].replace(' ', '').replace('-', '_')
        tag_name = f"{skill_tag}_{bracket_tag}"

        item_ids = []
        for m in row.get("materials_raw", []):
            item_ids.append(str(m["id"]))
        if row.get("output_id", 0) > 0:
            item_ids.append(str(row["output_id"]))
        if row.get("nature_cost", 0) > 0:
            item_ids.append("561")

        if not item_ids:
            self.lbl_status_right.config(text=f"No item IDs associated with this step.", fg="#f1c40f")
            return

        icon_id = item_ids[0]
        tag_str = f"banktags,1,{tag_name},{icon_id}," + ",".join(item_ids)
        self.copy_to_clipboard(tag_str, f"📋 Copied RuneLite Bank Tag tab '{tag_name}' to clipboard!")
        messagebox.showinfo("Bank Tag Copied",
            f"Successfully copied Bank Tag tab '{tag_name}' to clipboard!\n\n"
            f"Items included: {len(item_ids)}\n"
            "In RuneLite, right-click the '+' tab icon in your bank and click 'Import tag tab'.")

    def get_guide_row_tooltip(self, row_id):
        if row_id == "fletch_p2p_warn":
            return {
                "title": "🔒 Members-Only Skill",
                "subtitle": "Fletching",
                "title_color": "#e74c3c",
                "rows": [
                    ("Restriction:", "Members Only", "#e74c3c"),
                    ("How to Train:", "Enable P2P Methods checkbox", "#3498db")
                ],
                "warnings": ["Fletching cannot be trained on Free-to-play worlds."],
                "has_warning": True,
                "hint": "Check 'P2P Methods' at the top to unlock Fletching guides."
            }

        row = next((r for r in self.guide_rows if str(r.get("id")) == str(row_id)), None)
        if not row:
            return None

        is_here = "HERE" in row.get("status", "")
        title_col = "#f1c40f" if is_here else ("#2ecc71" if "profit" in row.get("tag", "") else "#3498db")

        rows = [
            ("Current Status:", row.get("status", "--"), "#f1c40f" if is_here else "#cccccc"),
            ("Level Range:", f"Levels {row.get('level_range', '--')}", "#f1f1f1"),
            ("XP per Action:", f"{row.get('xp_ea', 0):,.1f} XP" if row.get("xp_ea", 0) % 1 else f"{int(row.get('xp_ea', 0)):,} XP", "#3498db"),
            ("Units Needed:", f"{row.get('needed', 0):,} units", "#f1f1f1"),
            ("Total Materials:", row.get("tot_mats", "--"), "#e67e22" if row.get("tot_mat_qty", 0) > 0 else "#888888"),
        ]

        if row.get("breakeven_ea", 0) > 0:
            rows.append(("Target GE Buy Price:", row.get("max_buy", "--"), "#2ecc71"))
            rows.append(("Breakeven Ceiling:", f"≤ {row['breakeven_ea']:,} gp ea", "#f1c40f"))
            if row.get("curr_mat_price", 0) > 0:
                rows.append(("Current Market Price:", f"{row['curr_mat_price']:,} gp ea", "#cccccc"))
                m_ea = row.get("margin_ea", 0)
                m_col = "#2ecc71" if m_ea >= 0 else "#e74c3c"
                rows.append(("Margin at Market:", f"{m_ea:+,} gp ea", m_col))

        rows.extend([
            ("Live GP / XP:", row.get("gp_xp", "--"), "#2ecc71" if "+" in row.get("gp_xp", "") else ("#f1c40f" if "-0." in row.get("gp_xp", "") else "#e74c3c")),
            ("Net Profit / Loss:", row.get("bracket_cost", "--"), "#2ecc71" if "+" in row.get("bracket_cost", "") else "#e74c3c"),
            ("Disposal Strategy:", row.get("action_rec", "--"), "#3498db"),
            ("XP Rate / Hour:", row.get("xp_rate", "--"), "#f1f1f1"),
            ("Est. Grind Time:", row.get("time_est", "--"), "#f1c40f"),
        ])

        warnings = []
        if row.get("verdict"):
            warnings.append(row["verdict"])

        return {
            "title": f"🎓 {row['name']}",
            "subtitle": f"Lvl {row.get('level_range', '')} ({self.var_guide_skill.get()})",
            "title_color": title_col,
            "rows": rows,
            "warnings": warnings,
            "has_warning": bool("loss" in row.get("tag", "") or "Loss" in row.get("bracket_cost", "")),
            "hint": "💡 Click 'Total Mats' for quantity | Click 'Max Buy' for price | Right-click for Shopping List & Bank Tag"
        }

    def toggle_sort_guide(self, col):
        if self.guide_sort_col == col:
            self.guide_sort_asc = not self.guide_sort_asc
        else:
            self.guide_sort_col = col
            self.guide_sort_asc = True

        if col == "level_range":
            self.guide_rows.sort(key=lambda r: r["min_lvl"], reverse=not self.guide_sort_asc)
        elif col == "tot_mats":
            self.guide_rows.sort(key=lambda r: r.get("tot_mat_qty", 0), reverse=not self.guide_sort_asc)
        elif col == "max_buy":
            self.guide_rows.sort(key=lambda r: r.get("max_buy_val", 0), reverse=not self.guide_sort_asc)
        elif col == "xp_ea":
            self.guide_rows.sort(key=lambda r: r["xp_ea"], reverse=not self.guide_sort_asc)
        elif col == "needed":
            self.guide_rows.sort(key=lambda r: r["needed"], reverse=not self.guide_sort_asc)
        elif col == "gp_xp":
            self.guide_rows.sort(key=lambda r: r["gp_xp_val"], reverse=not self.guide_sort_asc)
        elif col == "bracket_cost":
            self.guide_rows.sort(key=lambda r: r["bracket_cost_val"], reverse=not self.guide_sort_asc)
        elif col == "xp_rate":
            self.guide_rows.sort(key=lambda r: r["xp_rate_val"], reverse=not self.guide_sort_asc)
        else:
            self.guide_rows.sort(key=lambda r: str(r.get(col, "")), reverse=not self.guide_sort_asc)

        self.tree_guide.delete(*self.tree_guide.get_children())
        for r in self.guide_rows:
            self.tree_guide.insert("", "end", iid=r["id"], values=(
                r["status"],
                r["level_range"],
                r["name"],
                r["materials"],
                r["tot_mats"],
                f"{r['needed']:,}",
                r["max_buy"],
                f"{r['xp_ea']:,.1f}" if r["xp_ea"] % 1 else f"{int(r['xp_ea']):,}",
                r["gp_xp"],
                r["bracket_cost"],
                r["action_rec"],
                r["xp_rate"],
                r["time_est"],
                r["verdict"]
            ), tags=(r["tag"],))

    def build_timers_tab(self):
        container = ttk.Frame(self.tab_timers)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_info = tk.Label(container, text="Active 4-Hour GE Buy Limit Watchlist. Alerts you when 4h expires!",
                            fg="#cccccc", bg="#1e1e1e", font=("Segoe UI", 9, "italic"))
        top_info.pack(anchor="w", pady=(0, 6))

        cols = ("account", "item", "qty", "time_left", "status")
        self.tree_timers = ttk.Treeview(container, columns=cols, show="headings", height=12)

        self.tree_timers.heading("account", text="Account")
        self.tree_timers.heading("item", text="Item Name")
        self.tree_timers.heading("qty", text="Quantity Bought")
        self.tree_timers.heading("time_left", text="Time Remaining")
        self.tree_timers.heading("status", text="Status")

        self.tree_timers.column("account", width=120, anchor="center")
        self.tree_timers.column("item", width=220, anchor="w")
        self.tree_timers.column("qty", width=120, anchor="center")
        self.tree_timers.column("time_left", width=140, anchor="center")
        self.tree_timers.column("status", width=160, anchor="center")

        self.tree_timers.pack(fill="both", expand=True)

        timers_col_tooltips = {
            "#1": "Account:\nIn-game character name for this 4-hour cooldown timer.",
            "#2": "Item Name:\nItem currently on 4-hour Grand Exchange buy limit cooldown.",
            "#3": "Quantity Bought:\nNumber of units purchased in this 4-hour limit window.",
            "#4": "Time Remaining:\nCount down until the 4-hour Grand Exchange limit completely resets.",
            "#5": "Status:\nShows whether cooldown is actively ticking or ready to purchase again."
        }
        HeadingToolTip(self.tree_timers, timers_col_tooltips)

        btn_bar = tk.Frame(container, bg="#1e1e1e")
        btn_bar.pack(fill="x", pady=6)

        btn_edit_timer = tk.Button(btn_bar, text="✏️ Edit Quantity Bought", command=self.edit_selected_timer,
                                   bg="#f39c12", fg="#000000", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=4, cursor="hand2")
        btn_edit_timer.pack(side="left")
        ToolTip(btn_edit_timer, "Edit Quantity Bought:\nAdjust the purchased amount for this 4h cooldown timer.")

        btn_reset_all = tk.Button(btn_bar, text="⚡ Reset All Timers", command=self.reset_all_timers,
                                  bg="#d35400", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=4, cursor="hand2")
        btn_reset_all.pack(side="left", padx=6)
        ToolTip(btn_reset_all, "Reset All Timers:\n1-click reset to clear active 4h GE cooldown timers.")

        btn_ge_sync_timers = tk.Button(btn_bar, text="🔄 Sync with GE", command=self.manual_ge_sync,
                                       bg="#2980b9", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=4, cursor="hand2")
        btn_ge_sync_timers.pack(side="left", padx=6)
        ToolTip(btn_ge_sync_timers, "Sync with GE:\nAuthoritatively fetch live 4-hour buy limits and trades directly from RuneLite / Microbot.")

        btn_del = tk.Button(btn_bar, text="🗑️ Remove Selected Timer", command=self.remove_selected_timer,
                            bg="#c0392b", fg="#ffffff", relief="flat", padx=8, pady=4, cursor="hand2")
        btn_del.pack(side="right")
        ToolTip(btn_del, "Remove selected item cooldown timer from active watchlist.")

        self.tree_timers.bind("<Double-1>", lambda e: self.edit_selected_timer())

    def build_session_tab(self):
        container = ttk.Frame(self.tab_session)
        container.pack(fill="both", expand=True, padx=15, pady=15)

        cards_frame = tk.Frame(container, bg="#1e1e1e")
        cards_frame.pack(fill="x", pady=(0, 15))

        self.card_alchs = self.create_stat_card(cards_frame, "Total Casts Done", "0", "#3498db", "Total High Alchemy casts completed during this session.")
        self.card_profit = self.create_stat_card(cards_frame, "Realized Profit", "0 gp", "#2ecc71", "Total net profit realized across all logged alch batches.")
        self.card_xp = self.create_stat_card(cards_frame, "Magic XP Gained", "0 XP", "#9b59b6", "Total Magic experience gained (65 XP per High Alchemy cast).")
        self.card_nats = self.create_stat_card(cards_frame, "Natures Used", "0", "#f39c12", "Total Nature Runes consumed during this session.")

        # Top of History table with Action Buttons
        hist_bar = tk.Frame(container, bg="#1e1e1e")
        hist_bar.pack(fill="x", pady=(5, 4))

        lbl_hist = tk.Label(hist_bar, text="Session Log History (Immutable to GE Fluctuations):", font=("Segoe UI", 10, "bold"), fg="#f39c12", bg="#1e1e1e")
        lbl_hist.pack(side="left")

        btn_edit = tk.Button(hist_bar, text="✏️ Edit Selected Entry", command=self.open_edit_session_dialog,
                             bg="#f39c12", fg="#000000", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, cursor="hand2")
        btn_edit.pack(side="right", padx=4)
        ToolTip(btn_edit, "Edit Selected Entry:\nManually adjust buy price, nature cost, or quantity if actual GE purchase differed.")

        btn_del = tk.Button(hist_bar, text="🗑️ Delete Entry", command=self.delete_session_entry,
                            bg="#c0392b", fg="#ffffff", font=("Segoe UI", 8), relief="flat", padx=8, cursor="hand2")
        btn_del.pack(side="right", padx=4)
        ToolTip(btn_del, "Delete Entry:\nRemove the selected transaction from your session history log.")

        cols = ("time", "account", "item", "qty", "buy_price", "nat_price", "alch_val", "profit")
        self.tree_session = ttk.Treeview(container, columns=cols, show="headings", height=10)
        self.tree_session.heading("time", text="Time")
        self.tree_session.heading("account", text="Account")
        self.tree_session.heading("item", text="Item Name")
        self.tree_session.heading("qty", text="Quantity")
        self.tree_session.heading("buy_price", text="Bought At (ea)")
        self.tree_session.heading("nat_price", text="Nat Cost (ea)")
        self.tree_session.heading("alch_val", text="Alch Value (Fixed)")
        self.tree_session.heading("profit", text="Realized Profit")

        self.tree_session.column("time", width=75, anchor="center")
        self.tree_session.column("account", width=95, anchor="center")
        self.tree_session.column("item", width=190, anchor="w")
        self.tree_session.column("qty", width=85, anchor="center")
        self.tree_session.column("buy_price", width=105, anchor="e")
        self.tree_session.column("nat_price", width=95, anchor="e")
        self.tree_session.column("alch_val", width=105, anchor="e")
        self.tree_session.column("profit", width=130, anchor="e")

        self.tree_session.pack(fill="both", expand=True)
        self.tree_session.bind("<Double-1>", lambda e: self.open_edit_session_dialog())

        session_col_tooltips = {
            "#1": "Time:\nTimestamp when this alch batch was recorded.",
            "#2": "Account:\nIn-game character name that bought/alched this batch.",
            "#3": "Item Name:\nName of the alched item.",
            "#4": "Quantity:\nNumber of items alched in this batch.",
            "#5": "Bought At (ea):\nGold price paid per item on the Grand Exchange.",
            "#6": "Nat Cost (ea):\nPrice paid per Nature Rune.",
            "#7": "Alch Value (Fixed):\nFixed High Alchemy gold payout per item.",
            "#8": "Realized Profit:\nNet profit earned = (Alch Value - Buy Price - Nat Cost) * Quantity."
        }
        HeadingToolTip(self.tree_session, session_col_tooltips)

        session_btn_bar = tk.Frame(container, bg="#1e1e1e")
        session_btn_bar.pack(fill="x", pady=8)

        btn_ge_sync_sess = tk.Button(session_btn_bar, text="🔄 Sync with GE", command=self.manual_ge_sync,
                                     bg="#2980b9", fg="#ffffff", font=("Segoe UI", 8, "bold"), relief="flat", padx=10, pady=4, cursor="hand2")
        btn_ge_sync_sess.pack(side="left")
        ToolTip(btn_ge_sync_sess, "Sync with GE:\nImport any completed GE trades from RuneLite / Microbot history into this session.")

        btn_reset = tk.Button(session_btn_bar, text="Reset Session", command=self.reset_session,
                              bg="#7f8c8d", fg="#ffffff", relief="flat", padx=10, pady=4, cursor="hand2")
        btn_reset.pack(side="right")
        ToolTip(btn_reset, "Reset Session:\nClears all session stats and history log back to zero.")

    def create_stat_card(self, parent, title, initial_val, val_color, tooltip=""):
        card = tk.Frame(parent, bg="#252528", relief="solid", borderwidth=1, padx=14, pady=10)
        card.pack(side="left", expand=True, fill="both", padx=6)

        lbl_t = tk.Label(card, text=title, font=("Segoe UI", 9), fg="#aaaaaa", bg="#252528")
        lbl_t.pack(anchor="w")

        lbl_v = tk.Label(card, text=initial_val, font=("Segoe UI", 14, "bold"), fg=val_color, bg="#252528")
        lbl_v.pack(anchor="w", pady=(4, 0))
        if tooltip:
            ToolTip(card, tooltip)
            ToolTip(lbl_t, tooltip)
            ToolTip(lbl_v, tooltip)
        return lbl_v

    def build_alerts_tab(self):
        container = ttk.Frame(self.tab_alerts)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(container, text="Recent High Margin Alerts (Only Fires on >=2 gp Shift):", font=("Segoe UI", 10, "bold"), fg="#f39c12", bg="#1e1e1e").pack(anchor="w", pady=(0, 6))

        self.lst_alerts = tk.Listbox(container, bg="#252528", fg="#f1f1f1", font=("Segoe UI", 10), selectbackground="#3e3e42", relief="flat", highlightthickness=0)
        self.lst_alerts.pack(fill="both", expand=True)
        ToolTip(self.lst_alerts, "Feed of real-time high margin price alerts detected while running.")

    def build_status_bar(self):
        self.lbl_status_left = tk.Label(self.status_bar, text="Initializing...", font=("Segoe UI", 8), fg="#888888", bg="#181818")
        self.lbl_status_left.pack(side="left", padx=10)

        self.lbl_status_right = tk.Label(self.status_bar, text="Ready", font=("Segoe UI", 8), fg="#888888", bg="#181818")
        self.lbl_status_right.pack(side="right", padx=10)

    # ------------------ LOGIC & HANDLERS ------------------

    def get_effective_nature_price(self):
        if self.var_free_alch.get():
            return 0
        custom = self.state.config.get("custom_nature_price", 0)
        if custom > 0:
            return custom
        return self.api.nature_rune_price

    def trigger_refresh(self):
        if self.is_fetching:
            return
        self.is_fetching = True
        self.btn_refresh.config(state="disabled", text="⏳ Syncing...")
        self.lbl_status_left.config(text="Fetching live prices from OSRS Wiki API...")

        threading.Thread(target=self._worker_fetch, daemon=True).start()

    def _worker_fetch(self):
        try:
            if not self.api.mapping:
                self.api.load_mapping()
            self.api.fetch_latest_and_volumes()
        except Exception as e:
            print(f"Worker fetch error: {e}")

        try:
            self.after(0, self._on_fetch_complete)
        except Exception:
            pass

    def _on_fetch_complete(self):
        self.is_fetching = False
        self.btn_refresh.config(state="normal", text="🔄 Refresh Now")
        self.seconds_until_refresh = self.state.config.get("auto_refresh_mins", 2) * 60

        # Update Nature Rune labels
        bid = self.api.nature_rune_bid
        ask = self.api.nature_rune_ask
        self.lbl_nat_target.config(text=f"🎯 Offer: {bid} gp")
        self.lbl_nat_details.config(text=f"Ask: {ask} gp | Limit: 18,000")

        # Recalculate tables
        self.recalculate_all()

        # Authoritatively reconcile 4h timers and past trades from RuneLite profiles
        try:
            ge_res = self.state.sync_from_runelite_ge(self.api.mapping, self.get_effective_nature_price())
            if ge_res.get("timers_updated", 0) > 0 or ge_res.get("session_imported", 0) > 0:
                self.update_timers_display()
                self.update_session_display()
        except Exception:
            pass

        # Check for alerts ONLY on fresh fetch!
        self._check_alerts_on_sync()

        sync_str = time.strftime("%H:%M:%S")
        self.lbl_status_left.config(text=f"Live Nature Rune: {self.get_effective_nature_price()} gp | Items Monitored: {len(self.api.latest_prices):,} | Last Sync: {sync_str}")

    def _check_alerts_on_sync(self):
        """Runs strictly when new API data arrives to avoid alert spam on UI interactions."""
        threshold = self.state.config.get("alert_threshold_alch", 200)
        min_vol = self.state.config.get("min_volume", 5000)

        alerts_fired = 0
        for row in self.alch_rows:
            iid = str(row["id"])
            profit = row["profit_ea"]
            vol = row["volume"]

            # Mute popup and sound alerts if item has reached its 4h GE buy limit!
            base_limit = row.get("base_limit", row.get("limit", 0))
            rem_limit, _, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
            if is_cd and rem_limit <= 0:
                continue

            # Proper Sell Boundary:
            # Require at least min_alert_vol (3+) items sold in the 5m window to confirm a real selling market.
            # Avoids spamming alerts on 1-off freak single-sell dumps!
            min_alert_vol = self.state.config.get("min_alert_5m_vol", 3)
            v5 = self.api.volumes_5m.get(iid, {})
            vol_5m_low = v5.get("low", 0) or 0
            vol_5m_total = v5.get("total", 0) or 0
            if vol_5m_low < min_alert_vol and vol_5m_total < (min_alert_vol * 2):
                continue

            if profit >= threshold and vol >= min_vol:
                last_profit = self.state.last_alerted_profits.get(iid)
                # Only alert if brand new OR margin shifted by >= 2 gp
                if last_profit is None or abs(profit - last_profit) >= 2:
                    self.state.last_alerted_profits[iid] = profit
                    alert_msg = f"{row['name']} margin: +{profit:,} gp/ea ({row['profit_hr']/1000:.0f}k/hr) | 5m: {vol_5m_low} sold"
                    self.state.alert_history.insert(0, f"[{time.strftime('%H:%M:%S')}] 🚨 {alert_msg}")
                    self.state.alert_history = self.state.alert_history[:60]
                    self.update_alerts_display()
                    if alerts_fired < 2:
                        self.trigger_alert_notification(row['name'], f"+{profit:,} gp/ea (+{row['profit_hr']/1000:.0f}k/hr) | 5m: {vol_5m_low} sold", item_id=row["id"])
                        alerts_fired += 1

    # ------------------ GITHUB AUTO-UPDATER ------------------

    def _check_update_startup(self):
        try:
            has_up, remote_v, dl_url, notes = check_for_updates(APP_VERSION)
            if has_up:
                self.latest_update_info = (remote_v, dl_url, notes)
                try:
                    self.after(0, self._render_update_available)
                except Exception:
                    pass
        except Exception as e:
            print(f"Startup update check: {e}")
        finally:
            # Automatically re-checks GitHub every 30 minutes while running
            try:
                self.after(30 * 60 * 1000, lambda: threading.Thread(target=self._check_update_startup, daemon=True).start())
            except Exception:
                pass

    def _render_update_available(self):
        if self.latest_update_info:
            remote_v, _, _ = self.latest_update_info
            self.btn_update.config(
                text=f"✨ Update {remote_v}",
                bg="#27ae60",
                fg="#ffffff",
                font=("Segoe UI", 8, "bold")
            )
            self.lbl_status_right.config(text=f"Update {remote_v} available!", fg="#2ecc71")

    def on_update_button_click(self):
        if self.latest_update_info:
            remote_v, dl_url, notes = self.latest_update_info
            UpdateDialog(self, remote_v, dl_url, notes)
        else:
            self.btn_update.config(text="Checking...", state="disabled")
            def worker():
                try:
                    has_up, remote_v, dl_url, notes = check_for_updates(APP_VERSION)
                    self.after(0, lambda: self._on_manual_check_done(has_up, remote_v, dl_url, notes))
                except Exception as e:
                    self.after(0, lambda: self._on_manual_check_done(False, APP_VERSION, None, str(e)))
            threading.Thread(target=worker, daemon=True).start()

    def _on_manual_check_done(self, has_up, remote_v, dl_url, notes):
        self.btn_update.config(state="normal")
        if has_up:
            self.latest_update_info = (remote_v, dl_url, notes)
            self._render_update_available()
            UpdateDialog(self, remote_v, dl_url, notes)
        else:
            self.btn_update.config(text=f"v{APP_VERSION}", bg="#2d2d30", fg="#888888")
            messagebox.showinfo("Up to Date", f"You are running the latest version (v{APP_VERSION})!")

    def _check_first_run_after_update(self):
        last_v = self.state.config.get("last_seen_version")
        if last_v is None:
            # Initial setup: mark current version
            self.state.config["last_seen_version"] = APP_VERSION
            self.state.save_config()
        elif last_v != APP_VERSION:
            # App was just updated! Show "What's New" modal
            self.state.config["last_seen_version"] = APP_VERSION
            self.state.save_config()
            WhatsNewDialog(self, APP_VERSION)

    def on_app_close(self):
        if self.latest_update_info:
            remote_v, dl_url, notes = self.latest_update_info
            ans = messagebox.askyesnocancel(
                "Update Available",
                f"A new version ({remote_v}) is ready to install!\n\n"
                f"Would you like to install the update now before exiting?\n\n"
                f"• Click YES to update & restart into {remote_v}\n"
                f"• Click NO to exit without updating\n"
                f"• Click CANCEL to stay in the app"
            )
            if ans is True:
                UpdateDialog(self, remote_v, dl_url, notes)
                return
            elif ans is False:
                if hasattr(self, "bridge_server") and self.bridge_server:
                    self.bridge_server.stop()
                self.destroy()
                return
            else:
                return # Cancelled, stay in app
        if hasattr(self, "bridge_server") and self.bridge_server:
            self.bridge_server.stop()
        self.destroy()

    def update_owned_nat_display(self):
        if hasattr(self, "ent_owned_nat"):
            self.ent_owned_nat.delete(0, tk.END)
            owned = self.state.config.get("owned_nature_runes", 0)
            if owned > 0:
                self.ent_owned_nat.insert(0, str(owned))

    def recalculate_all(self):
        self.recalculate_alch_table()
        self.recalculate_rec_table()
        self.recalculate_craft_table()
        if hasattr(self, "recalculate_guide_table"):
            if hasattr(self, "var_guide_skill"):
                self.update_guide_quests_card(self.var_guide_skill.get())
            self.recalculate_guide_table()
        self.update_cart_display()
        self.update_session_display()
        self.update_timers_display()
        self.update_owned_nat_display()

    def focus_search(self):
        self.ent_search.focus_set()
        self.ent_search.select_range(0, tk.END)
        return "break"

    def clear_search(self):
        self.ent_search.delete(0, tk.END)
        if hasattr(self, "ent_craft_search"):
            self.ent_craft_search.delete(0, tk.END)
        self.on_global_search_changed()

    def on_global_search_changed(self, event=None):
        if hasattr(self, "ent_craft_search") and hasattr(self, "ent_search"):
            val = self.ent_search.get()
            if self.ent_craft_search.get() != val:
                self.ent_craft_search.delete(0, tk.END)
                self.ent_craft_search.insert(0, val)
        self.recalculate_alch_table()
        if hasattr(self, "recalculate_rec_table"):
            self.recalculate_rec_table()
        if hasattr(self, "recalculate_craft_table"):
            self.recalculate_craft_table()
        if hasattr(self, "recalculate_guide_table"):
            self.recalculate_guide_table()
        if hasattr(self, "update_timers_display"):
            self.update_timers_display()
        if hasattr(self, "update_session_display"):
            self.update_session_display()
        if hasattr(self, "update_alerts_display"):
            self.update_alerts_display()

    def on_craft_search_changed(self, event=None):
        if hasattr(self, "ent_craft_search") and hasattr(self, "ent_search"):
            val = self.ent_craft_search.get()
            if self.ent_search.get() != val:
                self.ent_search.delete(0, tk.END)
                self.ent_search.insert(0, val)
        self.on_global_search_changed()

    def on_tab_changed(self, event=None):
        search_query = self.ent_search.get().strip() if hasattr(self, "ent_search") else ""
        if search_query:
            self.on_global_search_changed()

    def recalculate_alch_table(self):
        nat_cost = self.get_effective_nature_price()
        strat = self.var_strat.get().split()[0]
        cash_stack = self.state.config.get("cash_stack", 5000000)
        max_spend = self.state.config.get("max_item_cost", 500000)
        min_vol = self.state.config.get("min_volume", 5000)
        mem_ok = self.var_members.get()
        f2p_ok = self.var_f2p.get()
        speed_filter = self.var_speed.get() if hasattr(self, "var_speed") else "All"

        # Parse user min profit filter (leave blank to show ALL items)
        min_p_val = None
        min_p_raw = self.ent_min_profit.get().strip().replace(",", "")
        if min_p_raw:
            try:
                min_p_val = int(min_p_raw)
            except ValueError:
                pass

        search_query = self.ent_search.get().strip().lower()

        new_rows = []

        if hasattr(self, "var_price_basis"):
            basis = "5m" if "5m" in self.var_price_basis.get() else "latest"
        else:
            basis = self.state.config.get("price_basis", "5m")

        for item_id_str, mdata in self.api.mapping.items():
            high_alch = mdata.get("highalch", 0)
            if not high_alch or high_alch <= 10:
                continue

            if search_query and search_query not in mdata["name"].lower():
                continue

            is_mem = mdata.get("members", False)
            if f2p_ok and not mem_ok and is_mem:
                continue
            if not f2p_ok and not mem_ok:
                continue

            bid, ask = self.api.get_bid_ask(item_id_str, basis=basis)
            buy_price = self.api.get_price(item_id_str, strat, basis=basis)
            if not buy_price or buy_price <= 0:
                continue
            if buy_price > max_spend:
                continue

            vol = self.api.volumes_24h.get(item_id_str, 0)
            if vol < min_vol:
                continue

            cost = buy_price + nat_cost
            profit = high_alch - cost

            # User filter cutoff: if blank, shows all items!
            if min_p_val is not None and profit < min_p_val:
                continue

            base_limit = mdata.get("limit", 0) or 0
            rem_limit, secs_left, is_cd = self.state.get_remaining_limit(mdata["id"], base_limit)

            # Hide Maxed (4h GE limit reached): temporarily remove from table while cooldown is active
            if getattr(self, "var_hide_maxed", None) and self.var_hide_maxed.get() and is_cd and rem_limit <= 0:
                continue

            speed_cat, speed_badge, est_mins, speed_score = self.api.get_fill_speed_info(mdata["id"], base_limit if base_limit > 0 else 70)

            # Detect 1-item freak spike vs 5m volume average & format 1-tick sold count
            is_spike, spike_pct, lat_low, avg_low_p, vol_5m_l = self.api.get_spike_info(mdata["id"])
            if basis == "latest":
                if is_spike:
                    speed_badge = f"⚠️ Spike ({vol_5m_l} sold)"
                elif vol_5m_l > 0:
                    badge_prefix = "⚡ Fast" if speed_cat == "fast" else "⏱️ Steady"
                    speed_badge = f"{badge_prefix} ({vol_5m_l} sold)"
                elif str(speed_badge).startswith("⚠️ Stale"):
                    speed_badge = "⚠️ Stale (0 sold)"
                else:
                    speed_badge = f"🐢 Slow ({vol_5m_l} sold)"

            # Apply Speed Filter
            if "Fast" in speed_filter and speed_cat != "fast":
                continue
            if "Steady" in speed_filter and speed_cat not in ("fast", "steady"):
                continue

            # Realistic Volume Capping (inspired by QuantScapers analysis engine)
            avail_limit = rem_limit if is_cd else base_limit
            is_vol_capped = False
            if vol > 0 and avail_limit > 0 and vol < avail_limit:
                effective_limit = vol
                is_vol_capped = True
            elif avail_limit > 0:
                effective_limit = avail_limit
            else:
                effective_limit = min(vol, 125) if vol > 0 else 125
                if vol > 0 and vol < 125:
                    is_vol_capped = True

            if is_cd:
                hours = int(secs_left // 3600)
                mins = int((secs_left % 3600) // 60)
                time_tag = f" ({hours}h {mins:02d}m)"
                if rem_limit > 0:
                    limit_str = f"{effective_limit}/{base_limit} ⚠️" if is_vol_capped else f"{rem_limit}/{base_limit}{time_tag}"
                else:
                    limit_str = f"0/{base_limit}{time_tag}"
            else:
                if base_limit > 0:
                    limit_str = f"{effective_limit}/{base_limit} ⚠️" if is_vol_capped else f"{base_limit}"
                else:
                    limit_str = f"{effective_limit} (Cap)" if is_vol_capped else "-"

            profit_hr = profit * 1200
            batch_profit = profit * effective_limit

            if self.var_use_cash.get():
                afford_qty = min(effective_limit, cash_stack // buy_price) if buy_price > 0 else 0
            else:
                afford_qty = effective_limit

            cart_qty = self.state.cart_items.get(str(mdata["id"]), 0)

            row_dict = {
                "id": mdata["id"],
                "cart": cart_qty,
                "name": mdata["name"],
                "bid": bid,
                "ask": ask,
                "buy_at": buy_price,
                "alch_val": high_alch,
                "profit_ea": profit,
                "profit_hr": profit_hr,
                "speed_cat": speed_cat,
                "speed_badge": speed_badge,
                "est_mins": est_mins,
                "speed_score": speed_score,
                "limit": effective_limit,
                "base_limit": base_limit,
                "effective_limit": effective_limit,
                "is_vol_capped": is_vol_capped,
                "is_spike": is_spike,
                "spike_pct": spike_pct,
                "latest_low": lat_low,
                "avg_low": avg_low_p,
                "vol_5m_low": vol_5m_l,
                "limit_str": limit_str,
                "is_cd": is_cd,
                "batch_profit": batch_profit,
                "max_afford": afford_qty,
                "volume": vol
            }
            new_rows.append(row_dict)

        # Sort based on active sorting column and direction
        sort_key_map = {
            "cart": "cart",
            "offer_bid": "bid",
            "instant_ask": "ask",
            "speed": "speed_score",
            "limit": "limit",
            "batch_profit": "batch_profit",
            "max_afford": "max_afford",
            "volume": "volume"
        }
        k = sort_key_map.get(self.alch_sort_col, self.alch_sort_col)
        if k == "name":
            new_rows.sort(key=lambda x: str(x.get("name", "")).lower(), reverse=self.alch_sort_desc)
        else:
            new_rows.sort(key=lambda x: x.get(k, 0), reverse=self.alch_sort_desc)
        self.alch_rows = new_rows

        # Dynamically sync column headings with active pricing basis
        arrow = " ▼" if self.alch_sort_desc else " ▲"
        speed_header = "Fill Speed (5m Sold)" if basis == "latest" else "Fill Speed"
        vol_header = "24h Vol (5m Sold)" if basis == "latest" else "24h Volume"
        self.tree_alch.heading("speed", text=speed_header + (arrow if self.alch_sort_col == "speed" else ""))
        self.tree_alch.heading("volume", text=vol_header + (arrow if self.alch_sort_col == "volume" else ""))

        self.tree_alch.delete(*self.tree_alch.get_children())
        for row in self.alch_rows[:300]:
            cart_str = f"{row['cart']}x" if row['cart'] > 0 else ""
            vol_base = f"{row['volume']/1000:.0f}k" if row['volume'] >= 100000 else f"{row['volume']:,}"
            if basis == "latest":
                vol_str = f"{vol_base} ({row['vol_5m_low']} sold)"
            else:
                vol_str = vol_base
            limit_str = row["limit_str"]

            p_ea_str = f"+{row['profit_ea']:,} gp" if row['profit_ea'] >= 0 else f"{row['profit_ea']:,} gp"
            p_hr_str = f"+{row['profit_hr']/1000:.1f}k/hr" if row['profit_hr'] >= 0 else f"{row['profit_hr']/1000:.1f}k/hr"
            b_p_str = f"+{row['batch_profit']:,} gp" if row['batch_profit'] >= 0 else f"{row['batch_profit']:,} gp"

            item_tag = "profit" if row['profit_ea'] >= 200 else ("mild" if row['profit_ea'] >= 0 else "loss")
            tags = (item_tag, "incart") if row['cart'] > 0 else (item_tag,)

            self.tree_alch.insert("", "end", iid=str(row["id"]), values=(
                cart_str,
                row["name"],
                f"{row['bid']:,} gp",
                f"{row['ask']:,} gp",
                f"{row['alch_val']:,} gp",
                p_ea_str,
                p_hr_str,
                row["speed_badge"],
                limit_str,
                b_p_str,
                f"{row['max_afford']:,}",
                vol_str
            ), tags=tags)

        self.tree_alch.tag_configure("profit", foreground="#2ecc71")
        self.tree_alch.tag_configure("mild", foreground="#f1c40f")
        self.tree_alch.tag_configure("loss", foreground="#e74c3c")
        self.tree_alch.tag_configure("incart", font=("Segoe UI", 9, "bold"))

        # Update BridgeServer with Top 10 recommendations for in-game plugin
        if hasattr(self, "bridge_server") and self.bridge_server:
            top_list = []
            for r in self.alch_rows:
                if r["profit_ea"] > 0 and r["limit"] > 0:
                    metrics = self.api.get_quote_metrics(r["id"])
                    top_list.append({
                        "id": r["id"],
                        "name": r["name"],
                        "buy_price": r["buy_at"],
                        "alch_value": r["alch_val"],
                        "profit_ea": r["profit_ea"],
                        "profit_hr": r["profit_hr"],
                        "limit": r["limit"],
                        "speed": r["speed_badge"],
                        "vol_5m": metrics.get("vol_5m_low", 0),
                        "vol_5m_price": metrics.get("avg_low", 0),
                        "vol_24h": r["volume"]
                    })
                if len(top_list) >= 10:
                    break
            self.bridge_server.set_top_items(top_list)

    def toggle_sort_alch(self, col):
        if self.alch_sort_col == col:
            if col == "name":
                if self.alch_sort_desc:
                    # 3rd click on name (was Z-A) -> reset to default
                    self.alch_sort_col = "profit_ea"
                    self.alch_sort_desc = True
                else:
                    # 2nd click on name -> Z-A
                    self.alch_sort_desc = True
            else:
                if not self.alch_sort_desc:
                    # 3rd click (was ascending / lowest first) -> reset to default
                    self.alch_sort_col = "profit_ea"
                    self.alch_sort_desc = True
                else:
                    # 2nd click -> ascending / lowest first
                    self.alch_sort_desc = False
        else:
            # 1st click on new column
            self.alch_sort_col = col
            self.alch_sort_desc = False if col == "name" else True

        arrow = " ▼" if self.alch_sort_desc else " ▲"
        if hasattr(self, "var_price_basis"):
            basis = "5m" if "5m" in self.var_price_basis.get() else "latest"
        else:
            basis = self.state.config.get("price_basis", "5m")
        speed_header = "Fill Speed (5m Sold)" if basis == "latest" else "Fill Speed"
        vol_header = "24h Vol (5m Sold)" if basis == "latest" else "24h Volume"
        headers = {
            "cart": "Cart",
            "name": "Item Name",
            "offer_bid": "Target Offer (Bid)",
            "instant_ask": "Instant Buy (Ask)",
            "alch_val": "Alch Value",
            "profit_ea": "Profit / Alch",
            "profit_hr": "Profit / Hr (1.2k)",
            "speed": speed_header,
            "limit": "4h Limit",
            "batch_profit": "4h Batch Profit",
            "max_afford": "Max Afford",
            "volume": vol_header
        }
        for c, title in headers.items():
            self.tree_alch.heading(c, text=title + (arrow if c == self.alch_sort_col else ""))

        self.recalculate_alch_table()

    def recalculate_rec_table(self):
        if not hasattr(self, "tree_rec"):
            return

        timing = get_market_timing_info()
        self.lbl_market_time.config(text=f"🕒 {timing['time_str']}")
        self.lbl_market_badge.config(text=timing['badge'], fg=timing['badge_color'])
        self.lbl_market_activity.config(text=timing['activity'])
        self.lbl_market_advice.config(text=timing['advice'])

        cat = self.var_rec_cat.get() if hasattr(self, "var_rec_cat") else "workhorse"
        nat_cost = self.get_effective_nature_price()
        strat = self.var_strat.get().split()[0] if hasattr(self, "var_strat") else "smart"
        cash_stack = self.state.config.get("cash_stack", 5000000)
        max_spend = self.state.config.get("max_item_cost", 500000)
        mem_ok = self.var_members.get() if hasattr(self, "var_members") else True
        f2p_ok = self.var_f2p.get() if hasattr(self, "var_f2p") else False

        basis = "5m" if hasattr(self, "var_price_basis") and "5m" in self.var_price_basis.get() else self.state.config.get("price_basis", "5m")
        search_query = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""

        rows = []

        if cat == "workhorse":
            for spec in WORKHORSE_ITEMS:
                iid_str = str(spec["id"])
                mdata = self.api.mapping.get(iid_str, {})
                item_name = mdata.get("name", spec["name"])
                if search_query:
                    if (search_query not in item_name.lower() and
                        search_query not in spec.get("verdict", "").lower() and
                        search_query not in "workhorse"):
                        continue

                high_alch = mdata.get("highalch", 0)
                if not high_alch or high_alch <= 10:
                    continue

                is_mem = mdata.get("members", spec.get("members", False))
                if f2p_ok and not mem_ok and is_mem:
                    continue
                if not f2p_ok and not mem_ok:
                    continue

                bid, ask = self.api.get_bid_ask(iid_str, basis=basis)
                buy_price = self.api.get_price(iid_str, strat, basis=basis)
                if not buy_price or buy_price <= 0:
                    continue
                if buy_price > max_spend:
                    continue

                profit = high_alch - buy_price - nat_cost
                base_limit = spec.get("limit", mdata.get("limit", 70))
                rem_limit, secs_left, is_cd = self.state.get_remaining_limit(spec["id"], base_limit)

                vol = self.api.volumes_24h.get(iid_str, 0)
                speed_cat, speed_badge, est_mins, speed_score = self.api.get_fill_speed_info(spec["id"], base_limit)

                avail_limit = rem_limit if is_cd else base_limit
                eff_limit = avail_limit if (vol <= 0 or vol >= avail_limit) else vol
                batch_profit = profit * eff_limit if eff_limit > 0 else 0
                batch_cost = buy_price * eff_limit

                if is_cd:
                    hours = int(secs_left // 3600)
                    mins = int((secs_left % 3600) // 60)
                    time_tag = f" ({hours}h {mins:02d}m)"
                    limit_str = f"{rem_limit}/{base_limit}{time_tag}" if rem_limit > 0 else f"0/{base_limit}{time_tag}"
                else:
                    limit_str = f"{base_limit}"

                rows.append({
                    "id": spec["id"],
                    "name": mdata.get("name", spec["name"]),
                    "category": "🏆 Workhorse",
                    "bid": bid or buy_price,
                    "ask": ask or buy_price,
                    "buy_at": buy_price,
                    "alch_val": high_alch,
                    "profit_ea": profit,
                    "profit_hr": profit * 1200,
                    "limit": base_limit,
                    "rem_limit": rem_limit,
                    "eff_limit": eff_limit,
                    "limit_str": limit_str,
                    "batch_profit": batch_profit,
                    "batch_cost": batch_cost,
                    "speed_cat": speed_cat,
                    "speed_badge": speed_badge,
                    "verdict": spec["verdict"]
                })

        else:
            for iid_str, mdata in self.api.mapping.items():
                high_alch = mdata.get("highalch", 0)
                if not high_alch or high_alch <= 10:
                    continue

                is_mem = mdata.get("members", False)
                if f2p_ok and not mem_ok and is_mem:
                    continue
                if not f2p_ok and not mem_ok:
                    continue

                bid, ask = self.api.get_bid_ask(iid_str, basis=basis)
                buy_price = self.api.get_price(iid_str, strat, basis=basis)
                if not buy_price or buy_price <= 0 or buy_price > max_spend:
                    continue

                profit = high_alch - buy_price - nat_cost
                if profit <= 0:
                    continue

                base_limit = mdata.get("limit", 0) or 0
                if base_limit <= 0:
                    continue

                vol = self.api.volumes_24h.get(iid_str, 0)
                rem_limit, secs_left, is_cd = self.state.get_remaining_limit(mdata["id"], base_limit)
                avail_limit = rem_limit if is_cd else base_limit
                eff_limit = avail_limit if (vol <= 0 or vol >= avail_limit) else vol
                if eff_limit <= 0:
                    continue

                batch_profit = profit * eff_limit
                batch_cost = buy_price * eff_limit
                speed_cat, speed_badge, est_mins, speed_score = self.api.get_fill_speed_info(mdata["id"], base_limit)

                if is_cd:
                    hours = int(secs_left // 3600)
                    mins = int((secs_left % 3600) // 60)
                    time_tag = f" ({hours}h {mins:02d}m)"
                    limit_str = f"{rem_limit}/{base_limit}{time_tag}" if rem_limit > 0 else f"0/{base_limit}{time_tag}"
                else:
                    limit_str = f"{base_limit}"

                v5 = self.api.volumes_5m.get(iid_str, {})
                sold_5m = v5.get("low", 0) or 0

                if cat == "fast":
                    if speed_cat != "fast" and sold_5m < 8:
                        continue
                    cat_label = "⚡ Fast Fill"
                    verdict = f"⚡ Instant velocity: {sold_5m} sold in 5m into bids. Fills in ~{est_mins}m."
                elif cat == "batch":
                    if eff_limit < 10 or batch_profit < 10000:
                        continue
                    cat_label = "💰 Batch Profit"
                    verdict = f"💰 Top Batch Yield: Earns +{batch_profit:,} gp for full {base_limit} batch."
                elif cat == "overnight":
                    if profit < 250 or eff_limit < 15:
                        continue
                    cat_label = "🌙 Overnight"
                    verdict = f"🌙 Patient sleeper: +{profit:,} gp/ea. Queue low bid overnight during off-peak hours."
                else:
                    cat_label = "Smart Pick"
                    verdict = "Solid alch margin."

                if search_query:
                    if (search_query not in mdata["name"].lower() and
                        search_query not in cat_label.lower() and
                        search_query not in verdict.lower()):
                        continue

                rows.append({
                    "id": mdata["id"],
                    "name": mdata["name"],
                    "category": cat_label,
                    "bid": bid or buy_price,
                    "ask": ask or buy_price,
                    "buy_at": buy_price,
                    "alch_val": high_alch,
                    "profit_ea": profit,
                    "profit_hr": profit * 1200,
                    "limit": base_limit,
                    "rem_limit": rem_limit,
                    "eff_limit": eff_limit,
                    "limit_str": limit_str,
                    "batch_profit": batch_profit,
                    "batch_cost": batch_cost,
                    "speed_cat": speed_cat,
                    "speed_badge": speed_badge,
                    "verdict": verdict
                })

        sort_col = getattr(self, "rec_sort_col", "profit_ea")
        sort_desc = getattr(self, "rec_sort_desc", True)
        if cat == "batch" and sort_col == "profit_ea" and sort_desc:
            sort_col = "batch_profit"
        elif cat == "fast" and sort_col == "profit_ea" and sort_desc:
            sort_col = "profit_hr"

        if sort_col == "name":
            rows.sort(key=lambda x: str(x.get("name", "")).lower(), reverse=sort_desc)
        elif sort_col == "badge":
            pass
        else:
            rows.sort(key=lambda x: x.get(sort_col, 0), reverse=sort_desc)

        self.rec_rows = rows[:25]

        self.tree_rec.delete(*self.tree_rec.get_children())
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        for idx, r in enumerate(self.rec_rows):
            badge = medals[idx] if idx < len(medals) else f"#{idx+1}"
            r["badge"] = badge

            p_ea_str = f"+{r['profit_ea']:,} gp" if r['profit_ea'] >= 0 else f"{r['profit_ea']:,} gp"
            b_p_str = f"+{r['batch_profit']:,} gp" if r['batch_profit'] >= 0 else f"{r['batch_profit']:,} gp"
            b_cost_str = format_gp(r['batch_cost'])

            in_cart = str(r["id"]) in self.state.cart_items
            tags = ("incart",) if in_cart else ("profit",)

            self.tree_rec.insert("", "end", iid=str(r["id"]), values=(
                badge,
                r["name"],
                r["category"],
                f"{r['bid']:,} gp",
                f"{r['alch_val']:,} gp",
                p_ea_str,
                r["limit_str"],
                b_p_str,
                r["speed_badge"],
                b_cost_str,
                r["verdict"]
            ), tags=tags)

        self.tree_rec.tag_configure("profit", foreground="#2ecc71")
        self.tree_rec.tag_configure("incart", font=("Segoe UI", 9, "bold"), foreground="#f39c12")

    def toggle_sort_rec(self, col):
        if getattr(self, "rec_sort_col", "") == col:
            self.rec_sort_desc = not self.rec_sort_desc
        else:
            self.rec_sort_col = col
            self.rec_sort_desc = False if col in ("name", "category", "badge") else True
        self.recalculate_rec_table()

    def recalculate_craft_table(self):
        nat_cost = self.get_effective_nature_price()
        strat = self.var_strat.get().split()[0]
        levels = self.state.config.get("player_levels", {})
        only_usable = self.var_only_usable.get()
        craft_query = self.ent_craft_search.get().strip().lower() if hasattr(self, "ent_craft_search") else ""
        if not craft_query and hasattr(self, "ent_search"):
            craft_query = self.ent_search.get().strip().lower()
        mem_ok = self.var_members.get() if hasattr(self, "var_members") else True
        f2p_ok = self.var_f2p.get() if hasattr(self, "var_f2p") else False

        self.tree_craft.delete(*self.tree_craft.get_children())
        rows = []

        for r in CRAFTING_RECIPES:
            if craft_query:
                name_match = craft_query in r["name"].lower()
                mat_match = any(craft_query in m["name"].lower() for m in r.get("materials", []))
                skill_match = craft_query in r.get("skill", "").lower()
                if not name_match and not mat_match and not skill_match:
                    continue

            is_mem = r.get("members", True)
            if f2p_ok and not mem_ok and is_mem:
                continue
            if not f2p_ok and not mem_ok:
                continue

            req_skill = r["skill"]
            if req_skill == "Crafting" and hasattr(self, "var_filter_craft") and not self.var_filter_craft.get():
                continue
            if req_skill == "Smithing" and hasattr(self, "var_filter_smith") and not self.var_filter_smith.get():
                continue
            if req_skill == "Fletching" and hasattr(self, "var_filter_fletch") and not self.var_filter_fletch.get():
                continue
            if req_skill == "Magic" and hasattr(self, "var_filter_magic") and not self.var_filter_magic.get():
                continue

            req_lvl = r["level"]
            player_lvl = levels.get(req_skill, 99)
            can_make = player_lvl >= req_lvl

            if only_usable and not can_make:
                continue

            mat_cost = 0
            valid_mats = True
            mat_breakdown = []
            for m in r["materials"]:
                p = self.api.get_price(m["id"], strat)
                if not p:
                    valid_mats = False
                    break
                sub_total = p * m["qty"]
                mat_cost += sub_total
                mat_breakdown.append({
                    "name": m["name"],
                    "qty": m["qty"],
                    "price_ea": p,
                    "total": sub_total
                })

            if not valid_mats:
                continue

            out_meta = self.api.mapping.get(str(r["output_id"]), {})
            alch_val = out_meta.get("highalch", 0)
            if not alch_val:
                continue

            total_recipe_cost = mat_cost + nat_cost
            craft_alch_profit = alch_val - total_recipe_cost

            finished_buy_price = self.api.get_price(r["output_id"], strat)
            direct_alch_profit = (alch_val - (finished_buy_price + nat_cost)) if finished_buy_price else 0
            bonus_vs_buy = craft_alch_profit - direct_alch_profit

            hr_profit = craft_alch_profit * 1200

            rows.append({
                "recipe": r["name"],
                "skill_req": f"{req_skill} {req_lvl}" + ("" if can_make else " ⚠️"),
                "mat_cost": mat_cost,
                "alch_val": alch_val,
                "profit_ea": craft_alch_profit,
                "bonus": bonus_vs_buy,
                "xp": r["xp"],
                "hr_profit": hr_profit,
                "can_make": can_make,
                "materials": mat_breakdown,
                "nat_cost": nat_cost
            })

        rows.sort(key=lambda x: x.get(self.craft_sort_col, 0), reverse=self.craft_sort_desc)
        self.craft_rows = rows

        for cr in rows:
            p_ea_str = f"+{cr['profit_ea']:,} gp" if cr['profit_ea'] >= 0 else f"{cr['profit_ea']:,} gp"
            bonus_str = f"+{cr['bonus']:,} gp" if cr['bonus'] >= 0 else f"{cr['bonus']:,} gp"
            hr_str = f"+{cr['hr_profit']/1000:.1f}k/hr" if cr['hr_profit'] >= 0 else f"{cr['hr_profit']/1000:.1f}k/hr"

            tag = "profit" if cr['profit_ea'] >= 250 else ("mild" if cr['profit_ea'] >= 0 else "loss")
            if not cr["can_make"]:
                tag = "unusable"

            # Insert Parent Recipe Row
            parent_id = self.tree_craft.insert("", "end", text=f" {cr['recipe']}", values=(
                cr["skill_req"],
                f"{cr['mat_cost']:,} gp",
                f"{cr['alch_val']:,} gp",
                p_ea_str,
                bonus_str,
                f"{cr['xp']} xp",
                hr_str
            ), tags=(tag,), open=False)

            # Insert Breakdown Sub-rows (+ / -)
            for m in cr["materials"]:
                self.tree_craft.insert(parent_id, "end", text=f"  ↳ {m['name']} (x{m['qty']})", values=(
                    "-",
                    f"{m['total']:,} gp ({m['price_ea']:,} ea)",
                    "-",
                    "-",
                    "-",
                    "-",
                    "-"
                ), tags=("subrow",))

            self.tree_craft.insert(parent_id, "end", text=f"  ↳ Nature rune (x1)", values=(
                "-",
                f"{cr['nat_cost']:,} gp",
                "-",
                "-",
                "-",
                "-",
                "-"
            ), tags=("subrow",))

        self.tree_craft.tag_configure("profit", foreground="#2ecc71")
        self.tree_craft.tag_configure("mild", foreground="#f1c40f")
        self.tree_craft.tag_configure("loss", foreground="#e74c3c")
        self.tree_craft.tag_configure("unusable", foreground="#777777")
        self.tree_craft.tag_configure("subrow", foreground="#95a5a6")

    def toggle_sort_craft(self, col):
        if self.craft_sort_col == col:
            if col == "recipe":
                if self.craft_sort_desc:
                    # 3rd click on recipe (was Z-A) -> reset to default
                    self.craft_sort_col = "profit_ea"
                    self.craft_sort_desc = True
                else:
                    # 2nd click on recipe -> Z-A
                    self.craft_sort_desc = True
            else:
                if not self.craft_sort_desc:
                    # 3rd click (was ascending / lowest first) -> reset to default
                    self.craft_sort_col = "profit_ea"
                    self.craft_sort_desc = True
                else:
                    # 2nd click -> ascending / lowest first
                    self.craft_sort_desc = False
        else:
            # 1st click on new column
            self.craft_sort_col = col
            self.craft_sort_desc = False if col == "recipe" else True

        arrow = " ▼" if self.craft_sort_desc else " ▲"
        headers = {
            "recipe": "Recipe / Ingredient Breakdown",
            "skill_req": "Skill & Req",
            "mat_cost": "Materials Cost",
            "alch_val": "Alch Value",
            "profit_ea": "Profit (Craft + Alch)",
            "bonus": "Bonus vs Buying Finished",
            "xp": "XP / Item",
            "hr_profit": "Est Craft+Alch GP/Hr"
        }
        for c, title in headers.items():
            if c == "recipe":
                self.tree_craft.heading("#0", text=title + (arrow if self.craft_sort_col == "recipe" else ""))
            else:
                self.tree_craft.heading(c, text=title + (arrow if c == self.craft_sort_col else ""))

        self.recalculate_craft_table()

    def on_owned_nat_changed(self, event=None):
        raw = self.ent_owned_nat.get().strip().replace(",", "")
        try:
            val = int(raw) if raw else 0
            self.state.config["owned_nature_runes"] = max(0, val)
            self.save_preferences()
            self.update_cart_display()
        except ValueError:
            pass

    def update_cart_display(self):
        use_cash = self.var_use_cash.get()
        cash_stack = self.state.config.get("cash_stack", 5000000)
        strat = self.var_strat.get().split()[0]
        total_cost = 0
        total_exp_profit = 0
        slots_used = len(self.state.cart_items)
        total_alchs = sum(self.state.cart_items.values())

        for iid_str, qty in self.state.cart_items.items():
            row = next((r for r in self.alch_rows if str(r["id"]) == iid_str), None)
            if row:
                total_cost += row["buy_at"] * qty
                total_exp_profit += row["profit_ea"] * qty
            else:
                p = self.api.get_price(iid_str, strat)
                total_cost += p * qty

        # F2P vs Members GE slot cap
        max_slots = 3 if (self.var_f2p.get() and not self.var_members.get()) else 8

        if use_cash:
            remaining = cash_stack - total_cost
            slot_color = "#e74c3c" if (slots_used > max_slots or remaining < 0) else "#2ecc71"
            budget_str = f"Left: {format_gp(remaining)}"
        else:
            slot_color = "#e74c3c" if slots_used > max_slots else "#2ecc71"
            budget_str = "Budget: Unlimited"

        # Estimated Alch Time at 1,200 alchs/hr (20 alchs/min)
        time_part = ""
        if total_alchs > 0:
            alch_mins = math.ceil(total_alchs / 20)
            if alch_mins >= 60:
                h = alch_mins // 60
                m = alch_mins % 60
                time_part = f"  |  ⏱️ ~{h}h {m}m ({total_alchs:,} alchs)"
            else:
                time_part = f"  |  ⏱️ ~{alch_mins}m ({total_alchs:,} alchs)"

        # Nature Rune Stockpile check
        nat_part = ""
        if total_alchs > 0:
            owned_nats = self.state.config.get("owned_nature_runes", 0)
            if owned_nats >= total_alchs:
                nat_part = f"  |  🌿 Nats: {total_alchs:,}/{owned_nats:,} OK"
            else:
                shortage = total_alchs - owned_nats
                nat_part = f"  |  ⚠️ Buy {shortage:,} Nats"

        if slots_used == 0:
            cart_text = f"🛒 0/{max_slots} Slots  |  Budget: {format_gp(cash_stack) if use_cash else 'Unlimited'}"
        else:
            p_sign = "+" if total_exp_profit >= 0 else "-"
            cart_text = f"🛒 {slots_used}/{max_slots}  |  Cost: {format_gp(total_cost)}  |  {budget_str}  |  {p_sign}{format_gp(abs(total_exp_profit))}{time_part}{nat_part}"

        self.lbl_cart_status.config(
            text=cart_text,
            fg=slot_color
        )

    def update_session_display(self):
        history = self.state.session.get("history", [])
        curr_sel = self.var_account.get() if getattr(self, "var_account", None) else "All Accounts"
        search_query = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""

        if curr_sel != "All Accounts":
            filtered = [h for h in history if h.get("account", "Default") == curr_sel]
            total_alchs = sum(h.get("qty", 0) for h in filtered)
            total_profit = sum(h.get("profit", 0) for h in filtered)
            total_xp = total_alchs * 65.0
        else:
            filtered = history
            total_alchs = self.state.session.get("total_alchs", 0)
            total_profit = self.state.session.get("total_profit", 0)
            total_xp = self.state.session.get("total_xp", 0)

        self.card_alchs.config(text=f"{total_alchs:,}")
        self.card_profit.config(text=format_gp(total_profit))
        self.card_xp.config(text=f"{total_xp:,.0f} XP")
        self.card_nats.config(text=f"{total_alchs:,}")

        self.tree_session.delete(*self.tree_session.get_children())
        table_rows = [h for h in filtered if not search_query or (search_query in h.get("item", "").lower() or search_query in h.get("account", "").lower())]
        for h in table_rows:
            prof = h.get('profit', 0)
            prof_str = f"+{format_gp(prof)}" if prof >= 0 else f"-{format_gp(abs(prof))}"
            self.tree_session.insert("", "end", iid=h.get("id"), values=(
                h.get("time"),
                h.get("account", "Default"),
                h.get("item"),
                f"{h.get('qty', 0):,}",
                f"{h.get('buy_price', 0):,} gp",
                f"{h.get('nat_price', 0):,} gp",
                f"{h.get('alch_val', 0):,} gp",
                prof_str
            ))

    def update_timers_display(self):
        self.tree_timers.delete(*self.tree_timers.get_children())
        now = time.time()
        curr_sel = self.var_account.get() if getattr(self, "var_account", None) else "All Accounts"
        search_query = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""

        expired_keys = []
        for iid, tinfo in list(self.state.timers.items()):
            elapsed = now - tinfo.get("bought_time", 0)
            if elapsed >= 14400: # Has hit 0 / expired
                expired_keys.append(iid)
                continue

            acc = tinfo.get("account", "Default")
            if curr_sel != "All Accounts" and acc != curr_sel:
                continue

            item_name = tinfo.get("name", "Item")
            if search_query and search_query not in item_name.lower() and search_query not in acc.lower():
                continue

            left = max(0, 14400 - elapsed)
            hours = int(left // 3600)
            mins = int((left % 3600) // 60)
            secs = int(left % 60)
            time_left_str = f"{hours:02d}h {mins:02d}m {secs:02d}s"

            self.tree_timers.insert("", "end", iid=iid, values=(
                acc,
                item_name,
                f"{tinfo.get('qty', 0):,}",
                time_left_str,
                "Cooldown Active"
            ))

        if expired_keys:
            for k in expired_keys:
                if k in self.state.timers:
                    del self.state.timers[k]
                self.state.notified_timers.discard(k)
            self.state.save_timers()

    def update_alerts_display(self):
        self.lst_alerts.delete(0, tk.END)
        search_query = self.ent_search.get().strip().lower() if hasattr(self, "ent_search") else ""
        for a in self.state.alert_history:
            if search_query and search_query not in a.lower():
                continue
            self.lst_alerts.insert(tk.END, a)

    # ------------------ HOVER ROW TOOLTIPS (QuantScapers Inspired) ------------------

    def get_alch_row_tooltip(self, iid):
        try:
            row = next((r for r in self.alch_rows if str(r["id"]) == str(iid)), None)
            if not row:
                return None

            m_id = row["id"]
            metrics = self.api.get_quote_metrics(m_id)
            nat_cost = self.get_effective_nature_price()
            buy_at = row["buy_at"]
            total_cost = buy_at + nat_cost
            profit_ea = row["profit_ea"]
            roi_pct = (profit_ea / max(1, total_cost) * 100.0) if total_cost > 0 else 0.0

            title_col = "#2ecc71" if profit_ea >= 200 else ("#f1c40f" if profit_ea >= 0 else "#e74c3c")
            speed_badge = row["speed_badge"]
            if "Fast" in speed_badge:
                speed_col = "#2ecc71"
            elif "Steady" in speed_badge:
                speed_col = "#3498db"
            elif "Stale" in speed_badge:
                speed_col = "#e67e22"
            else:
                speed_col = "#95a5a6"

            limit_info = f"{row['effective_limit']:,}"
            if row.get("is_vol_capped"):
                limit_info = f"{row['effective_limit']:,} (Capped from {row['base_limit']:,})"

            p_hr_k = row["profit_hr"] / 1000.0

            rows = [
                ("Target Offer (Bid):", f"{row['bid']:,} gp", "#f1f1f1"),
                ("Instant Buy (Ask):", f"{row['ask']:,} gp ({metrics['spread_pct']:.1f}% sprd)", "#f1f1f1"),
                ("Nature Rune Cost:", f"{nat_cost:,} gp", "#95a5a6"),
                ("High Alch Value:", f"{row['alch_val']:,} gp", "#f1c40f"),
                ("Net Profit / Alch:", f"{profit_ea:+,} gp ({roi_pct:+.1f}%)", "#2ecc71" if profit_ea >= 0 else "#e74c3c"),
                ("Profit / Hr (1.2k):", f"{p_hr_k:+.1f}k GP/hr", "#2ecc71" if p_hr_k >= 0 else "#e74c3c"),
                ("Fill Velocity:", speed_badge, speed_col),
                ("24h Traded Volume:", f"{row['volume']:,} items", "#f1f1f1"),
                ("5m Sells into Bids:", f"{metrics['vol_5m_low']:,} items @ ~{metrics['avg_low']:,} gp" if metrics['vol_5m_low'] > 0 else "0 items", "#2ecc71" if metrics['vol_5m_low'] >= 3 else ("#f1c40f" if metrics['vol_5m_low'] > 0 else "#e74c3c")),
                ("5m Buys from Asks:", f"{metrics['vol_5m_high']:,} items @ ~{metrics['avg_high']:,} gp" if metrics['vol_5m_high'] > 0 else "0 items", "#3498db" if metrics['vol_5m_high'] > 0 else "#95a5a6"),
                ("5m Total Traded:", f"{metrics['vol_5m_total']:,} items (~{metrics['vol_5m_total'] * 12:,}/hr)", "#2ecc71" if metrics['vol_5m_total'] >= 10 else "#f1f1f1"),
                ("4h Buy Limit:", limit_info, "#e67e22" if row.get("is_vol_capped") else "#f1f1f1"),
                ("4h Batch Profit:", f"{row['batch_profit']:+,} gp", "#2ecc71" if row["batch_profit"] >= 0 else "#e74c3c"),
                ("Quote Freshness:", metrics["age_str"], "#e67e22" if metrics["is_stale"] else "#95a5a6"),
            ]

            if hasattr(self, "var_price_basis"):
                basis = "5m" if "5m" in self.var_price_basis.get() else "latest"
            else:
                basis = self.state.config.get("price_basis", "5m")
            if basis == "latest":
                if metrics['vol_5m_low'] >= 3:
                    verdict_txt = f"✓ Real Activity ({metrics['vol_5m_low']} sold in 5m) - Worth bidding!"
                    verdict_col = "#2ecc71"
                elif metrics['vol_5m_low'] in (1, 2):
                    verdict_txt = f"⚠️ Low Activity ({metrics['vol_5m_low']} sold in 5m) - Small batch recommended"
                    verdict_col = "#f1c40f"
                else:
                    verdict_txt = "⚠️ No 5m Sales Recorded (0 sold) - Potential outlier tick"
                    verdict_col = "#e74c3c"
                rows.insert(7, ("1-Tick Activity:", verdict_txt, verdict_col))

            warnings = []
            if metrics.get("is_spike"):
                warnings.append(
                    f"1-Item Spike Detected: Latest 1-trade price ({metrics['latest_low']:,} gp) is {metrics['spike_pct']:.1f}% below 5m volume average ({metrics['avg_low']:,} gp with only {metrics['vol_5m_low']} sold). Unlikely to fill full batch."
                )
            if metrics["is_stale"]:
                warnings.append(f"Stale Quote: Last GE trade was {metrics['age_str']}. Check in-game GE price.")
            if row.get("is_vol_capped"):
                warnings.append(f"Volume Capped: 24h volume ({row['volume']:,}) < 4h limit ({row['base_limit']:,}). Batch profit adjusted.")
            if metrics["is_wide_spread"]:
                warnings.append(f"Wide Spread ({metrics['spread_pct']:.1f}%): Low liquidity. Offer may take long to fill.")

            return {
                "title": row["name"],
                "subtitle": f"ID: {m_id}",
                "title_color": title_col,
                "rows": rows,
                "warnings": warnings,
                "has_warning": bool(warnings),
                "hint": "💡 Click Bid/Ask to copy price | Double-click row to add to cart"
            }
        except Exception:
            return None

    def get_craft_row_tooltip(self, iid):
        try:
            item_text = self.tree_craft.item(iid, "text").strip()
        except Exception:
            return None
        if not item_text:
            return None

        # If it's a sub-ingredient row
        if item_text.startswith("↳"):
            clean_name = item_text.lstrip("↳").strip()
            parent_id = self.tree_craft.parent(iid)
            parent_text = self.tree_craft.item(parent_id, "text").strip() if parent_id else "Recipe"
            return {
                "title": f"Ingredient: {clean_name}",
                "subtitle": f"For {parent_text}",
                "title_color": "#95a5a6",
                "rows": [("Material:", clean_name, "#f1f1f1")],
                "warnings": [],
                "has_warning": False,
                "hint": "💡 Click cell to copy ingredient name to clipboard"
            }

        # Parent Recipe row
        cr = next((r for r in self.craft_rows if r["recipe"] == item_text), None)
        if not cr:
            return None

        p_ea = cr["profit_ea"]
        bonus = cr["bonus"]
        hr_p = cr["hr_profit"] / 1000.0

        rows = [
            ("Skill Required:", cr["skill_req"], "#f1c40f" if not cr["can_make"] else "#f1f1f1"),
            ("Materials Total:", f"{cr['mat_cost']:,} gp", "#f1f1f1"),
            ("Nature Rune Cost:", f"{cr['nat_cost']:,} gp", "#95a5a6"),
            ("High Alch Value:", f"{cr['alch_val']:,} gp", "#f1c40f"),
            ("Craft + Alch Profit:", f"{p_ea:+,} gp ea", "#2ecc71" if p_ea >= 0 else "#e74c3c"),
            ("Bonus vs Buy Finished:", f"{bonus:+,} gp", "#2ecc71" if bonus >= 0 else "#e74c3c"),
            ("Est GP / Hr:", f"{hr_p:+.1f}k GP/hr", "#2ecc71" if hr_p >= 0 else "#e74c3c"),
            ("XP Earned / Item:", f"{cr['xp']} Craft/Fletch + 65 Magic", "#3498db")
        ]

        warnings = []
        if not cr["can_make"]:
            warnings.append(f"Level Requirement Unmet: You need {cr['skill_req']} to craft this item.")

        return {
            "title": f"Recipe: {cr['recipe']}",
            "subtitle": cr["skill_req"],
            "title_color": "#2ecc71" if p_ea >= 250 else ("#f1c40f" if p_ea >= 0 else "#e74c3c"),
            "rows": rows,
            "warnings": warnings,
            "has_warning": bool(warnings),
            "hint": "💡 Click row to copy name | Click [+] to expand ingredient breakdown"
        }

    # ------------------ CLICKS, EXPORTS & ACTIONS ------------------

    def on_alch_click(self, event):
        item_id = self.tree_alch.identify_row(event.y)
        if not item_id:
            return
        col_id = self.tree_alch.identify_column(event.x)
        row = next((r for r in self.alch_rows if str(r["id"]) == item_id), None)
        if not row:
            return

        # col_id corresponds to display column: #1 (Cart), #2 (Name), #3 (Bid), #4 (Ask)
        if col_id == "#1":
            qty_in_cart = self.state.cart_items.get(item_id, 0)
            if qty_in_cart > 0:
                self.copy_to_clipboard(str(qty_in_cart), f"Copied Quantity: {qty_in_cart:,} ({row['name']})")
            else:
                max_aff = row.get("max_afford", 1)
                self.copy_to_clipboard(str(max_aff), f"Copied Quantity: {max_aff:,} ({row['name']})")
        elif col_id == "#3":
            self.copy_to_clipboard(str(row["bid"]), f"Copied Bid Price: {row['bid']:,} gp ({row['name']})")
        elif col_id == "#4":
            self.copy_to_clipboard(str(row["ask"]), f"Copied Ask Price: {row['ask']:,} gp ({row['name']})")
        else:
            self.copy_to_clipboard(row["name"], f"Copied '{row['name']}' to clipboard!")

    def on_alch_double_click(self, event):
        item_id = self.tree_alch.identify_row(event.y)
        if not item_id:
            return
        if item_id in self.state.cart_items:
            del self.state.cart_items[item_id]
            self.lbl_status_right.config(text="Removed item from cart", fg="#888888")
        else:
            row = next((r for r in self.alch_rows if str(r["id"]) == item_id), None)
            if row:
                base_limit = row.get("base_limit", row["limit"]) if row.get("base_limit", 0) > 0 else (row["limit"] if row["limit"] > 0 else 70)
                rem_limit, secs_left, is_cd = self.state.get_remaining_limit(row["id"], base_limit)

                if is_cd and rem_limit <= 0:
                    hours = int(secs_left // 3600)
                    mins = int((secs_left % 3600) // 60)
                    self.lbl_status_right.config(
                        text=f"Cannot add {row['name']}: 4h GE cooldown active for {hours}h {mins:02d}m!",
                        fg="#e74c3c"
                    )
                    return

                limit_cap = row.get("effective_limit", rem_limit if is_cd else (base_limit if base_limit > 0 else 70))
                use_cash = self.var_use_cash.get()

                if use_cash:
                    cash_stack = self.state.config.get("cash_stack", 5000000)
                    strat = self.var_strat.get().split()[0]
                    allocated_so_far = sum(
                        self.api.get_price(iid, strat) * q
                        for iid, q in self.state.cart_items.items()
                    )
                    remaining_budget = max(0, cash_stack - allocated_so_far)
                    buy_price = max(1, row["buy_at"])

                    afford_with_remaining = remaining_budget // buy_price
                    qty = min(limit_cap, afford_with_remaining)

                    if qty <= 0:
                        if remaining_budget < buy_price:
                            self.lbl_status_right.config(
                                text=f"Cannot add {row['name']}: remaining budget ({format_gp(remaining_budget)}) < item price ({format_gp(buy_price)})! (Uncheck Cash Stack for unlimited)",
                                fg="#e74c3c"
                            )
                            return
                        qty = 1
                else:
                    qty = limit_cap

                self.state.cart_items[item_id] = qty
                self.lbl_status_right.config(
                    text=f"Added {qty:,}x {row['name']} to cart ({format_gp(qty * row['buy_at'])})",
                    fg="#2ecc71"
                )

        self.recalculate_alch_table()
        self.update_cart_display()

    def on_alch_right_click(self, event):
        item_id = self.tree_alch.identify_row(event.y)
        if not item_id:
            return
        row = next((r for r in self.alch_rows if str(r["id"]) == item_id), None)
        if not row:
            return

        current_qty = self.state.cart_items.get(item_id, 0)
        base_limit = row.get("base_limit", row["limit"]) if row.get("base_limit", 0) > 0 else (row["limit"] if row["limit"] > 0 else 1000)
        rem_limit, _, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
        max_allowed = rem_limit if is_cd else base_limit
        if max_allowed <= 0:
            max_allowed = 1000

        def save_qty(new_qty):
            if new_qty <= 0:
                if item_id in self.state.cart_items:
                    del self.state.cart_items[item_id]
                self.lbl_status_right.config(text=f"Removed {row['name']} from cart", fg="#888888")
            else:
                self.state.cart_items[item_id] = new_qty
                self.lbl_status_right.config(text=f"Set {new_qty:,}x {row['name']} in cart", fg="#2ecc71")
            self.recalculate_alch_table()
            self.update_cart_display()

        SetQuantityDialog(self, row["name"], current_qty, max_allowed, save_qty)

    def auto_fill_ge_slots(self):
        curr_cart_count = len(self.state.cart_items)
        empty_slots = 8 - curr_cart_count
        if empty_slots <= 0:
            messagebox.showinfo(
                "GE Slots Full",
                f"All 8 Grand Exchange slots are already filled in your Shopping Cart ({curr_cart_count}/8)!\n\n"
                "Clear or remove items from your cart before auto-filling."
            )
            return

        strat = self.var_strat.get().split()[0] if hasattr(self, "var_strat") else "smart"
        cash_stack = self.state.config.get("cash_stack", 5000000)
        use_cash = self.var_use_cash.get() if hasattr(self, "var_use_cash") else True

        allocated_so_far = sum(
            self.api.get_price(iid, strat) * q
            for iid, q in self.state.cart_items.items()
        )
        remaining_budget = max(0, cash_stack - allocated_so_far) if use_cash else 999_999_999

        if use_cash and remaining_budget < 5000:
            messagebox.showwarning(
                "Budget Fully Allocated",
                f"Your Cash Stack budget ({format_gp(cash_stack)}) is already fully allocated across existing cart items ({format_gp(allocated_so_far)}).\n\n"
                "Increase your Cash Stack or remove cart items to allocate more slots."
            )
            return

        if not self.rec_rows:
            self.recalculate_rec_table()

        candidates = []
        for r in self.rec_rows:
            iid_str = str(r["id"])
            if iid_str in self.state.cart_items:
                continue
            if r["profit_ea"] <= 0:
                continue

            base_limit = r.get("limit", 70)
            rem_limit, _, is_cd = self.state.get_remaining_limit(r["id"], base_limit)
            if rem_limit <= 0:
                continue

            buy_price = max(1, r["buy_at"])
            if use_cash and buy_price > remaining_budget:
                continue

            candidates.append(r)

        if not candidates:
            messagebox.showinfo(
                "No Available Recommendations",
                "No eligible items found to auto-fill.\n\n"
                "Items may already be in your cart, on 4-hour cooldown, or exceed your remaining budget."
            )
            return

        added_count = 0
        total_spent = 0
        total_profit = 0
        budget_left = remaining_budget

        for r in candidates:
            if added_count >= empty_slots:
                break

            iid_str = str(r["id"])
            buy_price = max(1, r["buy_at"])
            rem_limit = r["rem_limit"]

            if use_cash:
                max_units = budget_left // buy_price
                qty = min(rem_limit, max_units)
            else:
                qty = rem_limit

            if qty <= 0:
                continue

            self.state.cart_items[iid_str] = qty
            cost = qty * buy_price
            budget_left -= cost
            total_spent += cost
            total_profit += qty * r["profit_ea"]
            added_count += 1

        self.recalculate_alch_table()
        self.update_cart_display()
        self.recalculate_rec_table()

        msg = f"Auto-filled {added_count} empty GE slots! Allocated {format_gp(total_spent)} (Est. Profit: +{format_gp(total_profit)})"
        self.lbl_status_right.config(text=f"⚡ {msg}", fg="#2ecc71")
        if self.state.config.get("desktop_alerts"):
            FloatingToast(self, "⚡ GE Slots Auto-Filled", msg)
        else:
            messagebox.showinfo("Auto-Fill Completed", f"Successfully added {added_count} items to your shopping cart!\n\n• Gold Allocated: {format_gp(total_spent)}\n• Projected Profit: +{format_gp(total_profit)}\n• Slots Used: {len(self.state.cart_items)}/8")

    def copy_all_recs(self):
        if not self.rec_rows:
            return
        cat = self.var_rec_cat.get() if hasattr(self, "var_rec_cat") else "workhorse"
        timing = get_market_timing_info()
        lines = [
            f"=== OSRS Smart Picks ({cat.title()}) [{timing['time_str']}] ===",
            f"Status: {timing['badge']}",
            ""
        ]
        for r in self.rec_rows[:15]:
            lines.append(f"{r['badge']} {r['name']} | Bid: {r['bid']:,} gp | Alch: {r['alch_val']:,} gp | Profit: +{r['profit_ea']:,} gp | Limit: {r['limit']} (Batch: +{r['batch_profit']:,} gp) | {r['speed_badge']}")
        text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(text)
        self.lbl_status_right.config(text=f"📋 Copied {len(self.rec_rows[:15])} recommendations to clipboard!", fg="#3498db")

    def on_rec_click(self, event):
        item_id = self.tree_rec.identify_row(event.y)
        if not item_id:
            return
        row = next((r for r in self.rec_rows if str(r["id"]) == item_id), None)
        if not row:
            return
        col_id = self.tree_rec.identify_column(event.x)
        if col_id == "#4":
            self.copy_to_clipboard(str(row["bid"]), f"Copied Bid Price: {row['bid']:,} gp ({row['name']})")
        else:
            self.copy_to_clipboard(row["name"], f"Copied '{row['name']}' to clipboard!")

    def on_rec_double_click(self, event):
        item_id = self.tree_rec.identify_row(event.y)
        if not item_id:
            return
        if item_id in self.state.cart_items:
            del self.state.cart_items[item_id]
            self.lbl_status_right.config(text="Removed item from cart", fg="#888888")
        else:
            row = next((r for r in self.rec_rows if str(r["id"]) == item_id), None)
            if row:
                base_limit = row.get("limit", 70)
                rem_limit, secs_left, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
                if is_cd and rem_limit <= 0:
                    hours = int(secs_left // 3600)
                    mins = int((secs_left % 3600) // 60)
                    self.lbl_status_right.config(
                        text=f"Cannot add {row['name']}: 4h GE cooldown active for {hours}h {mins:02d}m!",
                        fg="#e74c3c"
                    )
                    return
                limit_cap = rem_limit if is_cd else base_limit
                use_cash = self.var_use_cash.get() if hasattr(self, "var_use_cash") else True
                if use_cash:
                    cash_stack = self.state.config.get("cash_stack", 5000000)
                    strat = self.var_strat.get().split()[0] if hasattr(self, "var_strat") else "smart"
                    allocated_so_far = sum(
                        self.api.get_price(iid, strat) * q
                        for iid, q in self.state.cart_items.items()
                    )
                    remaining_budget = max(0, cash_stack - allocated_so_far)
                    buy_price = max(1, row["buy_at"])
                    afford = remaining_budget // buy_price
                    qty = min(limit_cap, afford)
                    if qty <= 0:
                        qty = 1 if remaining_budget >= buy_price else 0
                        if qty == 0:
                            self.lbl_status_right.config(
                                text=f"Cannot add {row['name']}: remaining budget ({format_gp(remaining_budget)}) < item price ({format_gp(buy_price)})!",
                                fg="#e74c3c"
                            )
                            return
                else:
                    qty = limit_cap
                self.state.cart_items[item_id] = qty
                self.lbl_status_right.config(
                    text=f"Added {qty:,}x {row['name']} to cart ({format_gp(qty * row['buy_at'])})",
                    fg="#2ecc71"
                )

        self.recalculate_alch_table()
        self.update_cart_display()
        self.recalculate_rec_table()

    def on_rec_right_click(self, event):
        item_id = self.tree_rec.identify_row(event.y)
        if not item_id:
            return
        row = next((r for r in self.rec_rows if str(r["id"]) == item_id), None)
        if not row:
            return

        menu = tk.Menu(self, tearoff=0, bg="#2d2d30", fg="#ffffff", activebackground="#f39c12", activeforeground="#000000")
        menu.add_command(label=f"🛒 Add Full Limit ({row['limit']}x) to Cart", command=lambda: self._rec_add_full(row))
        menu.add_command(label="✏️ Set Custom Quantity in Cart...", command=lambda: self._rec_set_custom_qty(row))
        menu.add_separator()
        menu.add_command(label=f"📋 Copy Item Name ('{row['name']}')", command=lambda: self.copy_to_clipboard(row["name"], f"Copied '{row['name']}'!"))
        menu.add_command(label=f"💰 Copy Target Bid ({row['bid']:,} gp)", command=lambda: self.copy_to_clipboard(str(row["bid"]), f"Copied {row['bid']:,} gp!"))
        menu.add_separator()
        menu.add_command(label="🌐 Open in OSRS Wiki Prices", command=lambda: self.open_wiki_url(row["id"]))
        menu.post(event.x_root, event.y_root)

    def _rec_add_full(self, row):
        item_id = str(row["id"])
        base_limit = row.get("limit", 70)
        rem_limit, _, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
        qty = rem_limit if (is_cd and rem_limit > 0) else base_limit
        self.state.cart_items[item_id] = qty
        self.recalculate_alch_table()
        self.update_cart_display()
        self.recalculate_rec_table()
        self.lbl_status_right.config(text=f"Added {qty}x {row['name']} to cart", fg="#2ecc71")

    def _rec_set_custom_qty(self, row):
        item_id = str(row["id"])
        curr_qty = self.state.cart_items.get(item_id, 0)
        base_limit = row.get("limit", 70)
        rem_limit, _, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
        max_allowed = rem_limit if is_cd else base_limit
        if max_allowed <= 0:
            max_allowed = 1000

        def save_qty(new_qty):
            if new_qty <= 0:
                if item_id in self.state.cart_items:
                    del self.state.cart_items[item_id]
                self.lbl_status_right.config(text=f"Removed {row['name']} from cart", fg="#888888")
            else:
                self.state.cart_items[item_id] = new_qty
                self.lbl_status_right.config(text=f"Set {new_qty:,}x {row['name']} in cart", fg="#2ecc71")
            self.recalculate_alch_table()
            self.update_cart_display()
            self.recalculate_rec_table()

        SetQuantityDialog(self, row["name"], curr_qty if curr_qty > 0 else (rem_limit if rem_limit > 0 else base_limit), max_allowed, save_qty)

    def open_wiki_url(self, item_id):
        url = f"https://prices.runescape.wiki/osrs/item/{item_id}"
        webbrowser.open(url)

    def on_craft_click(self, event):
        item = self.tree_craft.identify_row(event.y)
        if not item:
            return
        text_val = self.tree_craft.item(item, "text").strip().lstrip("+").lstrip("↳").strip()
        if text_val:
            # Strip extra quantity text if clicking a sub-ingredient
            clean_name = text_val.split("(")[0].strip()
            self.copy_to_clipboard(clean_name, f"Copied '{clean_name}' to clipboard!")

    def show_status_message(self, message, fg="#f39c12", duration_ms=3000):
        if not hasattr(self, "lbl_status_right"):
            return
        self.lbl_status_right.config(text=message, fg=fg)
        if self.clipboard_clear_timer:
            self.after_cancel(self.clipboard_clear_timer)
        self.clipboard_clear_timer = self.after(duration_ms, lambda: self.lbl_status_right.config(text="Ready", fg="#888888"))

    def copy_to_clipboard(self, text, message=""):
        self.clipboard_clear()
        self.clipboard_append(text)
        if message:
            self.show_status_message(message)

    def export_master_bank_tag(self):
        """Exports all currently profitable items matching active filters as a RuneLite bank tag."""
        profitable_ids = [str(r["id"]) for r in self.alch_rows if r["profit_ea"] > 0]
        if not profitable_ids:
            messagebox.showinfo("No Items", "No profitable items found matching your current filters.")
            return

        # Prepend Nature Rune (561) as icon and item
        tag_str = f"banktags,1,alch,561,561," + ",".join(profitable_ids)
        self.copy_to_clipboard(tag_str, f"Copied Master Alch Tag ({len(profitable_ids)} items) to clipboard!")
        messagebox.showinfo("Master Tag Exported",
            f"Successfully copied Master Tag with {len(profitable_ids)} profitable items to clipboard!\n\n"
            "In RuneLite, right-click the '+' tab icon in your bank and click 'Import tag tab'.")

    def export_cart_bank_tag(self):
        """Exports items currently in your shopping cart as a RuneLite bank tag."""
        if not self.state.cart_items:
            messagebox.showinfo("Cart Empty", "Your shopping cart is currently empty. Double-click items to add them first.")
            return

        cart_ids = list(self.state.cart_items.keys())
        tag_str = f"banktags,1,cart,561,561," + ",".join(cart_ids)
        self.copy_to_clipboard(tag_str, f"Copied Cart Tag ({len(cart_ids)} items) to clipboard!")
        messagebox.showinfo("Cart Tag Exported",
            f"Successfully copied Cart Tag ({len(cart_ids)} items) to clipboard!\n\n"
            "In RuneLite, right-click the '+' tab icon in your bank and click 'Import tag tab'.")

    def log_cart_session(self):
        if not self.state.cart_items:
            messagebox.showinfo("Cart Empty", "Double-click items in the High Alch tab to add them to your cart first!")
            return

        count = len(self.state.cart_items)
        nat_cost = self.get_effective_nature_price()

        active_acc = getattr(self.state, "active_account", "Default")
        if not active_acc or active_acc in ("All", "All Accounts"):
            active_acc = self.var_account.get() if getattr(self, "var_account", None) and self.var_account.get() != "All Accounts" else "Default"

        for iid_str, qty in list(self.state.cart_items.items()):
            row = next((r for r in self.alch_rows if str(r["id"]) == iid_str), None)
            if row:
                self.state.log_alch_batch(
                    item_id=row["id"],
                    item_name=row["name"],
                    qty=qty,
                    buy_price=row["buy_at"],
                    nat_price=nat_cost,
                    alch_val=row["alch_val"],
                    account=active_acc
                )
                self.state.add_timer(row["id"], row["name"], qty, account=active_acc)

        self.state.cart_items.clear()
        self.recalculate_all()

        messagebox.showinfo("Logged Successfully", f"Logged {count} items into your session tracker and started their 4-hour GE limit timers!\n\nYou can click 'Edit Selected Entry' in the Session Tracker anytime if your actual buy price was different.")

    def open_edit_session_dialog(self):
        selected_id = self.tree_session.selection()
        if not selected_id:
            messagebox.showinfo("Select Entry", "Please select a session history entry to edit.")
            return

        entry_id = selected_id[0]
        entry = next((e for e in self.state.session.get("history", []) if e["id"] == entry_id), None)
        if entry:
            EditSessionDialog(self, entry, self._on_entry_edited)

    def _on_entry_edited(self, entry_id, new_qty, new_buy_price, new_nat_price):
        self.state.update_session_entry(entry_id, new_qty, new_buy_price, new_nat_price)
        self.recalculate_all()
        self.show_status_message(f"Session entry updated ({new_qty:,} bought) & 4h GE timer synced!")

    def delete_session_entry(self):
        selected_id = self.tree_session.selection()
        if not selected_id:
            return
        if messagebox.askyesno("Delete Entry", "Delete this history entry from your session?"):
            self.state.delete_session_entry(selected_id[0])
            self.recalculate_all()
            self.show_status_message("Session entry deleted & 4h GE timer updated.")

    def clear_cart(self):
        self._ge_cart_slots.clear()
        if hasattr(self, "_ge_tracked_items"):
            self._ge_tracked_items.clear()
        self.state.cart_items.clear()
        self.recalculate_alch_table()
        self.update_cart_display()

    def edit_selected_timer(self):
        selected = self.tree_timers.selection()
        if not selected:
            messagebox.showinfo("Select Timer", "Please select a timer from the list to edit.")
            return

        item_id = selected[0]
        tinfo = self.state.timers.get(item_id)
        if not tinfo:
            return

        EditTimerDialog(self, item_id, tinfo, self._on_timer_edited)

    def _on_timer_edited(self, item_id, new_qty):
        tinfo = self.state.timers.get(item_id)
        item_name = tinfo.get("name", "Item") if tinfo else "Item"
        if new_qty <= 0:
            self.state.remove_timer(item_id)
            self.show_status_message(f"Cleared timer for {item_name} (cooldown reset).")
        else:
            if item_id in self.state.timers:
                self.state.timers[item_id]["qty"] = new_qty
                self.state.save_timers()
                self.show_status_message(f"Updated timer for {item_name} to {new_qty:,} bought.")
        self.recalculate_all()

    def remove_selected_timer(self):
        selected = self.tree_timers.selection()
        if selected:
            for item_id in selected:
                self.state.remove_timer(item_id)
            self.recalculate_all()
            self.show_status_message("Selected cooldown timer(s) removed.")

    def reset_all_timers(self):
        curr_sel = self.var_account.get() if getattr(self, "var_account", None) else "All Accounts"
        prompt_txt = f"Reset all active 4-hour GE cooldown timers for {curr_sel}?" if curr_sel != "All Accounts" else "Reset all active 4-hour GE cooldown timers across all accounts?"
        if messagebox.askyesno("Reset Timers", prompt_txt):
            self.state.reset_all_timers(account=curr_sel)
            self.recalculate_all()
            self.show_status_message(f"All 4h GE timers reset for {curr_sel}.")

    def reset_session(self):
        if messagebox.askyesno("Reset Session", "Are you sure you want to reset all session statistics?"):
            self.state.reset_session()
            self.update_session_display()

    def manual_ge_sync(self):
        """Authoritatively syncs 4-hour buy limits and past trades directly from RuneLite / Microbot."""
        try:
            res = self.state.sync_from_runelite_ge(self.api.mapping, self.get_effective_nature_price())
            self.update_timers_display()
            self.update_session_display()
            self.recalculate_all()
            t_up = res.get("timers_updated", 0)
            s_up = res.get("session_imported", 0)
            msg = f"GE Sync Complete: {t_up} active timer(s) synced, {s_up} missing trade(s) imported."
            self.show_status_message(msg)
            FloatingToast(self, "🔄 GE Synced", msg)
        except Exception as e:
            self.show_status_message(f"GE Sync Error: {e}")

    def trigger_alert_notification(self, item_name, details, item_id=None):
        if item_id:
            rem_limit, _, is_cd = self.state.get_remaining_limit(item_id, 1000)
            if is_cd and rem_limit <= 0:
                return

        if self.state.config.get("sound_enabled") and HAS_WINSOUND:
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except Exception:
                pass

        if self.state.config.get("desktop_alerts"):
            try:
                FloatingToast(self, "🚨 OSRS High Alch Opportunity!", f"{item_name} spiked to {details}")
            except Exception:
                pass

    # ------------------ TIMERS & SETTINGS ------------------

    def timer_tick(self):
        if self.state.config.get("auto_refresh_mins", 2) > 0 and not self.is_fetching:
            self.seconds_until_refresh -= 1
            if self.seconds_until_refresh <= 0:
                self.trigger_refresh()
            else:
                m = self.seconds_until_refresh // 60
                s = self.seconds_until_refresh % 60
                self.lbl_countdown.config(text=f"(Next: {m:02d}:{s:02d})")

        expired = self.state.check_expired_timers()
        if expired:
            for exp in expired:
                item_name = exp.get("name") if isinstance(exp, dict) else exp
                acc = exp.get("account", "Default") if isinstance(exp, dict) else "Default"
                acc_tag = f"[{acc}] " if acc != "Default" else ""
                if self.state.config.get("sound_enabled") and HAS_WINSOUND:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                if self.state.config.get("desktop_alerts"):
                    FloatingToast(self, f"⏰ {acc_tag}GE 4-Hour Limit Reset!", f"You can now buy {item_name} on the GE again!")
            # Unhide expired items and refresh active watchlists
            self.recalculate_all()
        else:
            self.update_timers_display()

        self.after(1000, self.timer_tick)

    def on_cash_toggle_changed(self):
        use = self.var_use_cash.get()
        self.state.config["use_cash_stack"] = use
        self.save_preferences()
        if use:
            self.ent_cash.config(state="normal")
        else:
            self.ent_cash.config(state="disabled")
        self.recalculate_all()

    def on_cash_changed(self, event=None):
        raw = self.ent_cash.get()
        val = parse_cash_input(raw)
        if val > 0:
            self.state.config["cash_stack"] = val
            self.ent_cash.delete(0, tk.END)
            self.ent_cash.insert(0, format_gp(val))
            self.save_preferences()
            self.recalculate_all()

    def on_custom_nat_changed(self, event=None):
        raw = self.ent_custom_nat.get().strip()
        try:
            val = int(raw) if raw else 0
            self.state.config["custom_nature_price"] = val
            self.save_preferences()
            self.recalculate_all()
        except ValueError:
            pass

    def on_members_clicked(self):
        if self.var_members.get():
            self.var_f2p.set(False)
            if hasattr(self, "var_guide_members"):
                self.var_guide_members.set(True)
        else:
            self.var_f2p.set(True)
            if hasattr(self, "var_guide_members"):
                self.var_guide_members.set(False)
        self.on_filter_changed()

    def on_f2p_clicked(self):
        if self.var_f2p.get():
            self.var_members.set(False)
            if hasattr(self, "var_guide_members"):
                self.var_guide_members.set(False)
        else:
            self.var_members.set(True)
            if hasattr(self, "var_guide_members"):
                self.var_guide_members.set(True)
        self.on_filter_changed()

    def on_filter_changed(self, event=None):
        self.state.config["members"] = self.var_members.get()
        self.state.config["f2p"] = self.var_f2p.get()
        if hasattr(self, "var_guide_members"):
            self.state.config["guide_members"] = self.var_guide_members.get()
        self.state.config["free_alchs_mode"] = self.var_free_alch.get()

        max_s = parse_cash_input(self.ent_max_spend.get())
        if max_s > 0:
            self.state.config["max_item_cost"] = max_s

        min_v = parse_cash_input(self.ent_min_vol.get())
        if min_v >= 0:
            self.state.config["min_volume"] = min_v

        self.save_preferences()
        self.recalculate_all()

    def on_strategy_changed(self, event=None):
        strat = self.var_strat.get().split()[0]
        self.state.config["strategy"] = strat
        self.save_preferences()
        self.recalculate_all()

    def on_speed_filter_changed(self, event=None):
        self.state.config["speed_filter"] = self.var_speed.get()
        self.save_preferences()
        self.recalculate_alch_table()

    def on_refresh_rate_changed(self, event=None):
        val = self.var_refresh.get()
        if "1" in val:
            mins = 1
        elif "2" in val:
            mins = 2
        elif "5" in val:
            mins = 5
        elif "10" in val:
            mins = 10
        else:
            mins = 0
        self.state.config["auto_refresh_mins"] = mins
        self.seconds_until_refresh = mins * 60
        self.save_preferences()

    def on_levels_changed(self, event=None):
        try:
            c = int(self.ent_craft_lvl.get())
            s = int(self.ent_smith_lvl.get()) if hasattr(self, "ent_smith_lvl") else 99
            f = int(self.ent_fletch_lvl.get())
            m = int(self.ent_mage_lvl.get())
            self.state.config["player_levels"] = {"Crafting": c, "Smithing": s, "Fletching": f, "Magic": m}
        except ValueError:
            pass
        self.state.config["only_usable_recipes"] = self.var_only_usable.get()
        self.save_preferences()
        self.recalculate_craft_table()
        if hasattr(self, "var_guide_skill") and hasattr(self, "ent_guide_cur_lvl"):
            g_sk = self.var_guide_skill.get()
            cur_p_lvls = self.state.config.get("player_levels", {})
            if g_sk in cur_p_lvls:
                self.ent_guide_cur_lvl.delete(0, tk.END)
                self.ent_guide_cur_lvl.insert(0, str(cur_p_lvls[g_sk]))
                self.recalculate_guide_table()

    def on_skill_filter_changed(self):
        self.state.config["filter_craft"] = self.var_filter_craft.get()
        self.state.config["filter_smith"] = self.var_filter_smith.get()
        self.state.config["filter_fletch"] = self.var_filter_fletch.get()
        self.state.config["filter_magic"] = self.var_filter_magic.get()
        self.save_preferences()
        self.recalculate_craft_table()

    def select_all_skill_filters(self):
        self.var_filter_craft.set(True)
        self.var_filter_smith.set(True)
        self.var_filter_fletch.set(True)
        self.var_filter_magic.set(True)
        self.on_skill_filter_changed()

    def clear_all_skill_filters(self):
        self.var_filter_craft.set(False)
        self.var_filter_smith.set(False)
        self.var_filter_fletch.set(False)
        self.var_filter_magic.set(False)
        self.on_skill_filter_changed()

    def on_hide_maxed_changed(self):
        self.state.config["hide_maxed_cooldown"] = self.var_hide_maxed.get()
        self.save_preferences()
        self.recalculate_alch_table()

    def on_price_basis_changed(self, event=None):
        val = "5m" if "5m" in self.var_price_basis.get() else "latest"
        self.state.config["price_basis"] = val
        self.save_preferences()
        self.recalculate_all()

    def save_preferences(self):
        self.state.config["sound_enabled"] = self.var_sound.get()
        self.state.config["desktop_alerts"] = self.var_desktop.get()
        if hasattr(self, "var_hide_maxed"):
            self.state.config["hide_maxed_cooldown"] = self.var_hide_maxed.get()
        if hasattr(self, "var_price_basis"):
            self.state.config["price_basis"] = "5m" if "5m" in self.var_price_basis.get() else "latest"
        self.state.save_config()

    # ------------------ MICROBOT / RUNELITE BRIDGE HANDLERS ------------------

    def _on_bridge_event_async(self, data):
        try:
            self.after(0, lambda: self.handle_bridge_event(data))
        except Exception:
            pass

    def _register_account(self, account):
        if not account or account == "Unknown":
            return
        if hasattr(self, "cb_account"):
            curr_vals = list(self.cb_account["values"])
            if account not in curr_vals:
                curr_vals.append(account)
                self.cb_account["values"] = sorted(curr_vals, key=lambda x: (x != "All Accounts", x))

    def on_account_selected(self, event=None):
        sel = self.var_account.get()
        self.state.active_account = "All" if sel == "All Accounts" else sel
        self.state.config["monitored_character"] = sel
        self.state.save_config()
        self._apply_active_account_data()
        self.recalculate_all()
        if hasattr(self, "recalculate_guide_table"):
            self.recalculate_guide_table()

    def _apply_active_account_data(self):
        sel = self.var_account.get() if hasattr(self, "var_account") else "All Accounts"
        if sel == "All Accounts":
            if self.state.accounts:
                total_coins = sum(acc.get("coins", 0) for acc in self.state.accounts.values())
                total_nats = sum(acc.get("nature_runes", 0) for acc in self.state.accounts.values())
                if total_coins > 0 and self.var_use_cash.get():
                    self.ent_cash.delete(0, tk.END)
                    self.ent_cash.insert(0, format_gp(total_coins))
                    self.state.config["cash_stack"] = total_coins
                if total_nats > 0:
                    self.ent_owned_nat.delete(0, tk.END)
                    self.ent_owned_nat.insert(0, str(total_nats))
                    self.state.config["owned_nature_runes"] = total_nats
        else:
            acc = self.state.accounts.get(sel)
            if acc:
                coins = acc.get("coins", 0)
                nats = acc.get("nature_runes", 0)
                is_mem = acc.get("is_members", True)
                levels = acc.get("levels", {})

                if coins > 0 and self.var_use_cash.get():
                    self.ent_cash.delete(0, tk.END)
                    self.ent_cash.insert(0, format_gp(coins))
                    self.state.config["cash_stack"] = coins

                if nats > 0:
                    self.ent_owned_nat.delete(0, tk.END)
                    self.ent_owned_nat.insert(0, str(nats))
                    self.state.config["owned_nature_runes"] = nats


                if hasattr(self, "ent_craft_lvl") and "Crafting" in levels:
                    self.ent_craft_lvl.delete(0, tk.END)
                    self.ent_craft_lvl.insert(0, str(levels["Crafting"]))
                    self.state.config.setdefault("player_levels", {})["Crafting"] = levels["Crafting"]

                if hasattr(self, "ent_smith_lvl") and "Smithing" in levels:
                    self.ent_smith_lvl.delete(0, tk.END)
                    self.ent_smith_lvl.insert(0, str(levels["Smithing"]))
                    self.state.config.setdefault("player_levels", {})["Smithing"] = levels["Smithing"]

                if hasattr(self, "ent_fletch_lvl") and "Fletching" in levels:
                    self.ent_fletch_lvl.delete(0, tk.END)
                    self.ent_fletch_lvl.insert(0, str(levels["Fletching"]))
                    self.state.config.setdefault("player_levels", {})["Fletching"] = levels["Fletching"]

                if hasattr(self, "ent_mage_lvl") and "Magic" in levels:
                    self.ent_mage_lvl.delete(0, tk.END)
                    self.ent_mage_lvl.insert(0, str(levels["Magic"]))
                    self.state.config.setdefault("player_levels", {})["Magic"] = levels["Magic"]

                if hasattr(self, "ent_guide_cur_lvl") and hasattr(self, "var_guide_skill"):
                    g_sk = self.var_guide_skill.get()
                    if g_sk in levels:
                        self.ent_guide_cur_lvl.delete(0, tk.END)
                        self.ent_guide_cur_lvl.insert(0, str(levels[g_sk]))

        self._sync_cart_from_ge()

    def _sync_cart_from_ge(self):
        curr_sel = self.var_account.get() if getattr(self, "var_account", None) else "All Accounts"
        active_ge_items = {}
        for k, info in self._ge_cart_slots.items():
            acc = k.split("_")[0]
            if curr_sel == "All Accounts" or acc == curr_sel:
                iid = info["item_id"]
                active_ge_items[iid] = active_ge_items.get(iid, 0) + info["qty"]

        # Cleanly remove previous GE-driven items that are no longer actively buying
        if not hasattr(self, "_ge_tracked_items"):
            self._ge_tracked_items = set()

        for iid in list(self._ge_tracked_items):
            if iid not in active_ge_items:
                if iid in self.state.cart_items:
                    del self.state.cart_items[iid]
                self._ge_tracked_items.discard(iid)

        # Add or update currently active GE items
        for iid, qty in active_ge_items.items():
            self.state.cart_items[iid] = qty
            self._ge_tracked_items.add(iid)

        self.recalculate_alch_table()
        self.update_cart_display()

    def handle_bridge_event(self, data):
        event_type = data.get("event")
        account = data.get("account", "Default")
        if not account or account == "Unknown":
            account = "Default"

        self._register_account(account)
        active_monitored = self.var_account.get() if hasattr(self, "var_account") else "All Accounts"
        is_active = (active_monitored == "All Accounts" or account == active_monitored)

        if event_type in ("ACCOUNT_LOGIN", "ACCOUNT_SNAPSHOT"):
            world = data.get("world")
            is_mem = data.get("isMembers", True)
            levels = {
                "Crafting": data.get("crafting", 99),
                "Smithing": data.get("smithing", 99),
                "Fletching": data.get("fletching", 99),
                "Magic": data.get("magic", 99)
            }
            coins = data.get("coins")
            nats = data.get("natureRunes")
            self.state.update_account(account, coins=coins, nature_runes=nats, world=world, is_members=is_mem, levels=levels)
            if is_active:
                self._apply_active_account_data()
                if hasattr(self, "lbl_bridge_status"):
                    self.lbl_bridge_status.config(text=f"🟢 {account}", fg="#2ecc71")
                self.recalculate_all()
                if hasattr(self, "recalculate_guide_table"):
                    self.recalculate_guide_table()

        elif event_type == "INVENTORY_SYNC":
            coins = data.get("coins")
            nats = data.get("natureRunes")
            self.state.update_account(account, coins=coins, nature_runes=nats)
            if is_active:
                self._apply_active_account_data()
                self.recalculate_alch_table()

        elif event_type == "BANK_SYNC":
            bank_coins = data.get("bankCoins")
            bank_nats = data.get("bankNatureRunes")
            acc = self.state.accounts.get(account, {})
            if bank_coins is not None:
                acc["bank_coins"] = bank_coins
            if bank_nats is not None:
                acc["bank_nats"] = bank_nats
            if is_active:
                self._apply_active_account_data()

        elif event_type == "SKILLS_SYNC":
            levels = {
                "Crafting": data.get("crafting"),
                "Smithing": data.get("smithing"),
                "Fletching": data.get("fletching"),
                "Magic": data.get("magic")
            }
            self.state.update_account(account, levels={k: v for k, v in levels.items() if v is not None})
            if is_active:
                self._apply_active_account_data()
                self.recalculate_craft_table()
                if hasattr(self, "recalculate_guide_table"):
                    self.recalculate_guide_table()

        elif event_type == "GE_OFFER":
            item_id = data.get("itemId", 0)
            item_name = data.get("itemName", "")
            qty_sold = data.get("quantitySold", 0)
            total_qty = data.get("totalQuantity", 0)
            spent = data.get("spent", 0)
            price = data.get("price", 0)
            state = data.get("state", "")
            slot = data.get("slot", 0)

            slot_key = f"{account}_{slot}"

            # 1. Live GE Sync into Shopping Cart
            if state == "BUYING" and item_id > 0 and total_qty > 0:
                self._ge_cart_slots[slot_key] = {"item_id": str(item_id), "qty": total_qty}
                self._sync_cart_from_ge()
            elif state in ("BOUGHT", "CANCELLED_BUY", "EMPTY"):
                if slot_key in self._ge_cart_slots:
                    del self._ge_cart_slots[slot_key]
                    self._sync_cart_from_ge()

            if item_id > 0:
                # 2. Automatically log finalized GE buy (completed or cancelled partial) to both 4h Timer and Session Tracker
                if state in ("BOUGHT", "CANCELLED_BUY") and qty_sold > 0:
                    finalize_key = f"{account}_{slot}_{item_id}_{qty_sold}_{state}"
                    if finalize_key not in self._logged_ge_offers:
                        self._logged_ge_offers.add(finalize_key)

                        # 1. 4-Hour GE Timer: Added exactly once with the true final quantity
                        self.state.add_timer(item_id, item_name, qty_sold, account=account)
                        self.update_timers_display()
                        self.recalculate_alch_table()

                        # 2. Session Tracker: Logged exactly once with the true final quantity
                        unit_buy_price = int(spent // qty_sold) if spent > 0 else int(price)
                        nat_price = self.get_effective_nature_price()
                        mdata = self.api.mapping.get(str(item_id), {})
                        high_alch = mdata.get("highalch", 0)
                        if high_alch > 0:
                            entry = self.state.log_alch_batch(item_id, item_name, qty_sold, unit_buy_price, nat_price, high_alch, account=account, timestamp=data.get("timestamp"))
                            self.update_session_display()
                            tag = "Completed" if state == "BOUGHT" else "Cancelled (Partial)"
                            if is_active:
                                self.lbl_status_right.config(text=f"🛒 Logged GE Buy ({tag}): {qty_sold}x {item_name} [{account}]", fg="#2ecc71")
                                if self.state.config.get("desktop_alerts"):
                                    FloatingToast(self, f"🛒 GE Buy {tag} [{account}]", f"Bought {qty_sold}x {item_name} at {unit_buy_price:,} gp (Profit: +{format_gp(entry['profit'])})")
                            else:
                                if self.state.config.get("desktop_alerts"):
                                    FloatingToast(self, f"🛒 Alt GE Buy [{account}]", f"Bought {qty_sold}x {item_name} at {unit_buy_price:,} gp")

                        # Immediately reconcile authoritative 4h buy limits and trades from RuneLite
                        try:
                            self.state.sync_from_runelite_ge(self.api.mapping, self.get_effective_nature_price())
                            self.update_timers_display()
                        except Exception:
                            pass

        elif event_type == "GE_SYNC":
            try:
                res = self.state.sync_from_runelite_ge(self.api.mapping, self.get_effective_nature_price(), raw_sync_data=data)
                self.update_timers_display()
                self.update_session_display()
                self.recalculate_alch_table()
                if is_active:
                    self.lbl_status_right.config(
                        text=f"🔄 GE Synced [{account}]: {res.get('timers_updated', 0)} timers, {res.get('session_imported', 0)} trades",
                        fg="#3498db"
                    )
            except Exception as e:
                print(f"Error handling GE_SYNC: {e}")

        elif event_type == "ALCH_CAST":
            if is_active:
                self.lbl_status_right.config(text=f"🪄 [{account}] High Alch Cast (+65 XP)", fg="#f39c12")

if __name__ == "__main__":
    app = OSRSAlchDashboard()
    app.mainloop()
