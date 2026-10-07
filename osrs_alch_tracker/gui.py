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
from state import AppState
from updater import APP_VERSION, check_for_updates, UpdateDialog, WhatsNewDialog

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
        self.is_fetching = False
        self.seconds_until_refresh = self.state.config.get("auto_refresh_mins", 2) * 60

        # Sorting states: {col_name: descending_bool}
        self.alch_sort_col = "profit_ea"
        self.alch_sort_desc = True

        self.craft_sort_col = "profit_ea"
        self.craft_sort_desc = True

        # Clipboard copy feedback
        self.clipboard_clear_timer = None

        self.setup_styles()
        self.build_ui()

        # Keyboard shortcuts
        self.bind("<F5>", lambda e: self.trigger_refresh())
        self.bind("<Control-f>", lambda e: self.focus_search())

        # Start timer tick
        self.after(1000, self.timer_tick)

        # Window close protocol (prompts if update available)
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Update checker
        self.latest_update_info = None
        self.after(2000, lambda: threading.Thread(target=self._check_update_startup, daemon=True).start())

        # Check if app was just updated to show "What's New" popup
        self.after(800, self._check_first_run_after_update)

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

        # Tab 1: Pure High Alch
        self.tab_alch = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_alch, text="🔮 Pure High Alch")
        self.build_alch_tab()

        # Tab 2: Craft & Alch
        self.tab_craft = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_craft, text="🔨 Craft & Alch")
        self.build_craft_tab()

        # Tab 3: 4h GE Limit Timers
        self.tab_timers = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_timers, text="⏱️ 4h GE Timers")
        self.build_timers_tab()

        # Tab 4: Session Profit Tracker
        self.tab_session = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_session, text="📊 Session Tracker")
        self.build_session_tab()

        # Tab 5: Alert Log
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

        cb_mem = tk.Checkbutton(p1, text="Members", variable=self.var_members, command=self.on_filter_changed,
                                bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30", activebackground="#252528", activeforeground="#f39c12")
        cb_mem.pack(side="left", padx=2)
        ToolTip(cb_mem, "Include Members items. Uncheck if you only want Free-to-play.")

        cb_f2p = tk.Checkbutton(p1, text="F2P", variable=self.var_f2p, command=self.on_filter_changed,
                                bg="#252528", fg="#f1f1f1", selectcolor="#2d2d30", activebackground="#252528", activeforeground="#f39c12")
        cb_f2p.pack(side="left", padx=2)
        ToolTip(cb_f2p, "Include Free-to-play items. When only F2P is active, GE slots cap at 3.")

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

        # Live Search Bar
        tk.Label(p1, text="🔍", fg="#f39c12", bg="#252528").pack(side="left", padx=(2, 1))
        self.ent_search = tk.Entry(p1, width=9, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        self.ent_search.pack(side="left", padx=(1, 8))
        self.ent_search.bind("<KeyRelease>", lambda e: self.recalculate_alch_table())
        self.ent_search.bind("<Escape>", lambda e: self.clear_search())
        ToolTip(self.ent_search, "Live search by item name (e.g. 'rune', 'bow'). Press Esc to clear, Ctrl+F to focus.")

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

        tk.Label(p2, text="|", fg="#444444", bg="#252528").pack(side="left", padx=6)

        tk.Label(p2, text="⏱️ Auto-Sync:", fg="#888888", bg="#252528", font=("Segoe UI", 8)).pack(side="left")
        self.var_refresh = tk.StringVar(value=f"{self.state.config.get('auto_refresh_mins', 2)} min")
        cb_ref = ttk.Combobox(p2, textvariable=self.var_refresh, values=["1 min", "2 min", "5 min", "10 min", "Off"], width=6, state="readonly")
        cb_ref.pack(side="left", padx=(2, 6))
        cb_ref.bind("<<ComboboxSelected>>", self.on_refresh_rate_changed)
        ToolTip(cb_ref, "Configure how often market prices automatically refresh.")

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
        self.tree_alch.column("speed", width=112, anchor="center")
        self.tree_alch.column("limit", width=95, anchor="center")
        self.tree_alch.column("batch_profit", width=110, anchor="e")
        self.tree_alch.column("max_afford", width=85, anchor="center")
        self.tree_alch.column("volume", width=85, anchor="e")

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
            "#8": "Fill Speed:\nEstimated wait time for buy offer to fill based on real-time 5-minute sales velocity.\n⚡ Fast (<15m) | ⏱️ Steady (<1h) | 🐢 Slow (>1h) | ⚠️ Stale (>45m)\nClick column header to sort.",
            "#9": "4h GE Buy Limit:\nOfficial Grand Exchange purchase limit every 4 hours.\n⚠️ Volume Capped: If 24h market volume is lower than GE limit, shows 'Volume / Limit ⚠️' to avoid illiquid paper profit traps.",
            "#10": "4h Batch Profit:\nRealistic profit achievable for a full 4-hour batch (Profit ea * Effective volume-capped limit).\nClick column header to sort.",
            "#11": "Max Afford:\nMaximum quantity your current cash stack can afford out of remaining available limit.\nClick column header to sort.",
            "#12": "24h Volume:\nTotal units traded on Grand Exchange over the last 24 hours.\nClick column header to sort."
        }
        HeadingToolTip(self.tree_alch, alch_col_tooltips)
        RowToolTip(self.tree_alch, self.get_alch_row_tooltip)

    def build_craft_tab(self):
        sub_top = tk.Frame(self.tab_craft, bg="#252528")
        sub_top.pack(fill="x", padx=6, pady=6)

        tk.Label(sub_top, text="Your Stats:", font=("Segoe UI", 9, "bold"), fg="#f39c12", bg="#252528").pack(side="left", padx=4)

        levels = self.state.config.get("player_levels", {})
        tk.Label(sub_top, text="Crafting:", fg="#cccccc", bg="#252528").pack(side="left")
        self.ent_craft_lvl = tk.Entry(sub_top, width=4, bg="#1e1e1e", fg="#ffffff", relief="flat")
        self.ent_craft_lvl.insert(0, str(levels.get("Crafting", 99)))
        self.ent_craft_lvl.pack(side="left", padx=(2, 6))
        self.ent_craft_lvl.bind("<FocusOut>", self.on_levels_changed)
        ToolTip(self.ent_craft_lvl, "Your in-game Crafting level. Recipes above this level are flagged or hidden.")

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
        ToolTip(cb_usable, "Filter out recipes that exceed your current Crafting, Fletching, or Magic levels.")

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

    def build_timers_tab(self):
        container = ttk.Frame(self.tab_timers)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        top_info = tk.Label(container, text="Active 4-Hour GE Buy Limit Watchlist. Alerts you when 4h expires!",
                            fg="#cccccc", bg="#1e1e1e", font=("Segoe UI", 9, "italic"))
        top_info.pack(anchor="w", pady=(0, 6))

        cols = ("item", "qty", "time_left", "status")
        self.tree_timers = ttk.Treeview(container, columns=cols, show="headings", height=12)

        self.tree_timers.heading("item", text="Item Name")
        self.tree_timers.heading("qty", text="Quantity Bought")
        self.tree_timers.heading("time_left", text="Time Remaining")
        self.tree_timers.heading("status", text="Status")

        self.tree_timers.column("item", width=260, anchor="w")
        self.tree_timers.column("qty", width=140, anchor="center")
        self.tree_timers.column("time_left", width=160, anchor="center")
        self.tree_timers.column("status", width=180, anchor="center")

        self.tree_timers.pack(fill="both", expand=True)

        timers_col_tooltips = {
            "#1": "Item Name:\nItem currently on 4-hour Grand Exchange buy limit cooldown.",
            "#2": "Quantity Bought:\nNumber of units purchased in this 4-hour limit window.",
            "#3": "Time Remaining:\nCount down until the 4-hour Grand Exchange limit completely resets.",
            "#4": "Status:\nShows whether cooldown is actively ticking or ready to purchase again."
        }
        HeadingToolTip(self.tree_timers, timers_col_tooltips)

        btn_bar = tk.Frame(container, bg="#1e1e1e")
        btn_bar.pack(fill="x", pady=6)

        btn_edit_timer = tk.Button(btn_bar, text="✏️ Edit Quantity Bought", command=self.edit_selected_timer,
                                   bg="#f39c12", fg="#000000", font=("Segoe UI", 8, "bold"), relief="flat", padx=8, pady=4, cursor="hand2")
        btn_edit_timer.pack(side="left")
        ToolTip(btn_edit_timer, "Edit Quantity Bought:\nAdjust the purchased amount for this 4h cooldown timer.")

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

        cols = ("time", "item", "qty", "buy_price", "nat_price", "alch_val", "profit")
        self.tree_session = ttk.Treeview(container, columns=cols, show="headings", height=10)
        self.tree_session.heading("time", text="Time")
        self.tree_session.heading("item", text="Item Name")
        self.tree_session.heading("qty", text="Quantity")
        self.tree_session.heading("buy_price", text="Bought At (ea)")
        self.tree_session.heading("nat_price", text="Nat Cost (ea)")
        self.tree_session.heading("alch_val", text="Alch Value (Fixed)")
        self.tree_session.heading("profit", text="Realized Profit")

        self.tree_session.column("time", width=80, anchor="center")
        self.tree_session.column("item", width=220, anchor="w")
        self.tree_session.column("qty", width=90, anchor="center")
        self.tree_session.column("buy_price", width=110, anchor="e")
        self.tree_session.column("nat_price", width=100, anchor="e")
        self.tree_session.column("alch_val", width=110, anchor="e")
        self.tree_session.column("profit", width=140, anchor="e")

        self.tree_session.pack(fill="both", expand=True)
        self.tree_session.bind("<Double-1>", lambda e: self.open_edit_session_dialog())

        session_col_tooltips = {
            "#1": "Time:\nTimestamp when this alch batch was recorded.",
            "#2": "Item Name:\nName of the alched item.",
            "#3": "Quantity:\nNumber of items alched in this batch.",
            "#4": "Bought At (ea):\nGold price paid per item on the Grand Exchange.",
            "#5": "Nat Cost (ea):\nPrice paid per Nature Rune.",
            "#6": "Alch Value (Fixed):\nFixed High Alchemy gold payout per item.",
            "#7": "Realized Profit:\nNet profit earned = (Alch Value - Buy Price - Nat Cost) * Quantity."
        }
        HeadingToolTip(self.tree_session, session_col_tooltips)

        btn_reset = tk.Button(container, text="Reset Session", command=self.reset_session,
                              bg="#7f8c8d", fg="#ffffff", relief="flat", padx=10, pady=4, cursor="hand2")
        btn_reset.pack(anchor="e", pady=8)
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

        self.after(0, self._on_fetch_complete)

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

        # Check for alerts ONLY on fresh fetch!
        self._check_alerts_on_sync()

        sync_str = time.strftime("%H:%M:%S")
        self.lbl_status_left.config(text=f"Live Nature Rune: {self.get_effective_nature_price()} gp | Items Monitored: {len(self.api.latest_prices):,} | Last Sync: {sync_str}")

    def _check_alerts_on_sync(self):
        """Runs strictly when new API data arrives to avoid alert spam on UI interactions."""
        threshold = self.state.config.get("alert_threshold_alch", 200)
        min_vol = self.state.config.get("min_volume", 5000)

        for row in self.alch_rows:
            iid = str(row["id"])
            profit = row["profit_ea"]
            vol = row["volume"]

            # Mute popup and sound alerts if item has reached its 4h GE buy limit!
            base_limit = row.get("base_limit", row.get("limit", 0))
            rem_limit, _, is_cd = self.state.get_remaining_limit(row["id"], base_limit)
            if is_cd and rem_limit <= 0:
                continue

            if profit >= threshold and vol >= min_vol:
                last_profit = self.state.last_alerted_profits.get(iid)
                # Only alert if brand new OR margin shifted by >= 2 gp
                if last_profit is None or abs(profit - last_profit) >= 2:
                    self.state.last_alerted_profits[iid] = profit
                    alert_msg = f"{row['name']} margin: +{profit:,} gp/ea ({row['profit_hr']/1000:.0f}k/hr)"
                    self.state.alert_history.insert(0, f"[{time.strftime('%H:%M:%S')}] 🚨 {alert_msg}")
                    self.state.alert_history = self.state.alert_history[:60]
                    self.update_alerts_display()
                    self.trigger_alert_notification(row['name'], f"+{profit:,} gp/ea (+{row['profit_hr']/1000:.0f}k/hr)", item_id=row["id"])

    # ------------------ GITHUB AUTO-UPDATER ------------------

    def _check_update_startup(self):
        try:
            has_up, remote_v, dl_url, notes = check_for_updates(APP_VERSION)
            if has_up:
                self.latest_update_info = (remote_v, dl_url, notes)
                self.after(0, self._render_update_available)
        except Exception as e:
            print(f"Startup update check: {e}")
        finally:
            # Automatically re-checks GitHub every 30 minutes while running
            self.after(30 * 60 * 1000, lambda: threading.Thread(target=self._check_update_startup, daemon=True).start())

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
                self.destroy()
                return
            else:
                return # Cancelled, stay in app
        self.destroy()

    def update_owned_nat_display(self):
        if hasattr(self, "ent_owned_nat"):
            self.ent_owned_nat.delete(0, tk.END)
            owned = self.state.config.get("owned_nature_runes", 0)
            if owned > 0:
                self.ent_owned_nat.insert(0, str(owned))

    def recalculate_all(self):
        self.recalculate_alch_table()
        self.recalculate_craft_table()
        self.update_cart_display()
        self.update_session_display()
        self.update_timers_display()
        self.update_owned_nat_display()

    def focus_search(self):
        self.notebook.select(self.tab_alch)
        self.ent_search.focus_set()
        self.ent_search.select_range(0, tk.END)
        return "break"

    def clear_search(self):
        self.ent_search.delete(0, tk.END)
        self.recalculate_alch_table()

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

        for item_id_str, mdata in self.api.mapping.items():
            high_alch = mdata.get("highalch", 0)
            if not high_alch or high_alch <= 10:
                continue

            if search_query and search_query not in mdata["name"].lower():
                continue

            is_mem = mdata.get("members", False)
            if is_mem and not mem_ok:
                continue
            if not is_mem and not f2p_ok and mem_ok:
                pass

            bid, ask = self.api.get_bid_ask(item_id_str)
            buy_price = self.api.get_price(item_id_str, strat)
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
                if rem_limit > 0:
                    limit_str = f"{effective_limit}/{base_limit} ⚠️" if is_vol_capped else f"{rem_limit}/{base_limit}"
                else:
                    hours = int(secs_left // 3600)
                    mins = int((secs_left % 3600) // 60)
                    limit_str = f"0 ({hours}h {mins:02d}m)"
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

        self.tree_alch.delete(*self.tree_alch.get_children())
        for row in self.alch_rows[:300]:
            cart_str = f"{row['cart']}x" if row['cart'] > 0 else ""
            vol_str = f"{row['volume']:,}" if row['volume'] < 100000 else f"{row['volume']/1000:.0f}k"
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
        headers = {
            "cart": "Cart",
            "name": "Item Name",
            "offer_bid": "Target Offer (Bid)",
            "instant_ask": "Instant Buy (Ask)",
            "alch_val": "Alch Value",
            "profit_ea": "Profit / Alch",
            "profit_hr": "Profit / Hr (1.2k)",
            "speed": "Fill Speed",
            "limit": "4h Limit",
            "batch_profit": "4h Batch Profit",
            "max_afford": "Max Afford",
            "volume": "24h Volume"
        }
        for c, title in headers.items():
            self.tree_alch.heading(c, text=title + (arrow if c == self.alch_sort_col else ""))

        self.recalculate_alch_table()

    def recalculate_craft_table(self):
        nat_cost = self.get_effective_nature_price()
        strat = self.var_strat.get().split()[0]
        levels = self.state.config.get("player_levels", {})
        only_usable = self.var_only_usable.get()

        self.tree_craft.delete(*self.tree_craft.get_children())
        rows = []

        for r in CRAFTING_RECIPES:
            req_skill = r["skill"]
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

        self.lbl_cart_status.config(
            text=f"🛒 Slots: {slots_used}/{max_slots}  |  Allocated: {format_gp(total_cost)}  |  {budget_str}  |  Profit: +{format_gp(total_exp_profit)}{time_part}{nat_part}",
            fg=slot_color
        )

    def update_session_display(self):
        sess = self.state.session
        self.card_alchs.config(text=f"{sess.get('total_alchs', 0):,}")
        self.card_profit.config(text=format_gp(sess.get('total_profit', 0)))
        self.card_xp.config(text=f"{sess.get('total_xp', 0):,.0f} XP")
        self.card_nats.config(text=f"{sess.get('total_alchs', 0):,}")

        self.tree_session.delete(*self.tree_session.get_children())
        for h in sess.get("history", []):
            self.tree_session.insert("", "end", iid=h.get("id"), values=(
                h.get("time"),
                h.get("item"),
                f"{h.get('qty', 0):,}",
                f"{h.get('buy_price', 0):,} gp",
                f"{h.get('nat_price', 0):,} gp",
                f"{h.get('alch_val', 0):,} gp",
                f"+{format_gp(h.get('profit', 0))}"
            ))

    def update_timers_display(self):
        self.tree_timers.delete(*self.tree_timers.get_children())
        now = time.time()
        for iid, tinfo in self.state.timers.items():
            elapsed = now - tinfo["bought_time"]
            left = max(0, 14400 - elapsed)
            hours = int(left // 3600)
            mins = int((left % 3600) // 60)
            secs = int(left % 60)
            time_left_str = f"{hours:02d}h {mins:02d}m {secs:02d}s"
            status = "Ready to buy! 🎉" if left == 0 else "Cooldown Active"

            self.tree_timers.insert("", "end", iid=iid, values=(
                tinfo["name"],
                f"{tinfo['qty']:,}",
                time_left_str,
                status
            ))

    def update_alerts_display(self):
        self.lst_alerts.delete(0, tk.END)
        for a in self.state.alert_history:
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
                ("24h Vol / 5m:", f"{row['volume']:,}  (5m: {metrics['vol_5m_total']:,})", "#f1f1f1"),
                ("4h Buy Limit:", limit_info, "#e67e22" if row.get("is_vol_capped") else "#f1f1f1"),
                ("4h Batch Profit:", f"{row['batch_profit']:+,} gp", "#2ecc71" if row["batch_profit"] >= 0 else "#e74c3c"),
                ("Quote Freshness:", metrics["age_str"], "#e67e22" if metrics["is_stale"] else "#95a5a6"),
            ]

            warnings = []
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

        for iid_str, qty in list(self.state.cart_items.items()):
            row = next((r for r in self.alch_rows if str(r["id"]) == iid_str), None)
            if row:
                self.state.log_alch_batch(
                    item_id=row["id"],
                    item_name=row["name"],
                    qty=qty,
                    buy_price=row["buy_at"],
                    nat_price=nat_cost,
                    alch_val=row["alch_val"]
                )
                self.state.add_timer(row["id"], row["name"], qty)

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

    def reset_session(self):
        if messagebox.askyesno("Reset Session", "Are you sure you want to reset all session statistics?"):
            self.state.reset_session()
            self.update_session_display()

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
            for item_name in expired:
                if self.state.config.get("sound_enabled") and HAS_WINSOUND:
                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                if self.state.config.get("desktop_alerts"):
                    FloatingToast(self, "⏰ GE 4-Hour Limit Reset!", f"You can now buy {item_name} on the GE again!")
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

    def on_filter_changed(self, event=None):
        self.state.config["members"] = self.var_members.get()
        self.state.config["f2p"] = self.var_f2p.get()
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
            f = int(self.ent_fletch_lvl.get())
            m = int(self.ent_mage_lvl.get())
            self.state.config["player_levels"] = {"Crafting": c, "Fletching": f, "Magic": m}
        except ValueError:
            pass
        self.state.config["only_usable_recipes"] = self.var_only_usable.get()
        self.save_preferences()
        self.recalculate_craft_table()

    def on_hide_maxed_changed(self):
        self.state.config["hide_maxed_cooldown"] = self.var_hide_maxed.get()
        self.save_preferences()
        self.recalculate_alch_table()

    def save_preferences(self):
        self.state.config["sound_enabled"] = self.var_sound.get()
        self.state.config["desktop_alerts"] = self.var_desktop.get()
        if hasattr(self, "var_hide_maxed"):
            self.state.config["hide_maxed_cooldown"] = self.var_hide_maxed.get()
        self.state.save_config()

if __name__ == "__main__":
    app = OSRSAlchDashboard()
    app.mainloop()
