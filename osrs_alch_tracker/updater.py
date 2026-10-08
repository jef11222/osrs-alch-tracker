import os
import sys
import json
import time
import subprocess
import tempfile
import threading
import webbrowser
import urllib.request
import urllib.error
import urllib.parse
import tkinter as tk
from tkinter import ttk, messagebox

APP_VERSION = "1.3.21"
GITHUB_REPO = "jef11222/osrs-alch-tracker"
RELEASES_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def is_safe_https_url(url, allowed_domains=("github.com", "objects.githubusercontent.com", "api.github.com")):
    """Validates that a URL strictly uses HTTPS and originates from trusted GitHub domains."""
    try:
        parsed = urllib.parse.urlparse(str(url))
        if parsed.scheme.lower() != "https":
            return False
        hostname = (parsed.hostname or "").lower()
        return any(hostname == d or hostname.endswith("." + d) for d in allowed_domains)
    except Exception:
        return False

def parse_version_tuple(v_str):
    """Converts 'v1.3.0' or '1.3' into a comparable tuple of integers (1, 3, 0)."""
    cleaned = str(v_str).strip().lstrip("v").lstrip("V")
    parts = []
    for p in cleaned.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            break
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])

def check_for_updates(current_version=APP_VERSION):
    """
    Queries GitHub Releases API for the latest release.
    Returns: (has_update: bool, remote_version: str, download_url: str, release_notes: str)
    """
    req = urllib.request.Request(
        RELEASES_API_URL,
        headers={"User-Agent": "OSRS-Alch-Tracker-App"}
    )
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                tag_name = data.get("tag_name", "")
                remote_tuple = parse_version_tuple(tag_name)
                curr_tuple = parse_version_tuple(current_version)

                if remote_tuple > curr_tuple:
                    # Look for Windows executable asset (.exe) matching the running edition
                    curr_name = os.path.basename(sys.executable).lower() if getattr(sys, "frozen", False) else "osrs_alch_tracker.exe"
                    download_url = None
                    exact_match_url = None
                    fallback_exe_url = None
                    setup_url = None

                    for asset in data.get("assets", []):
                        name = asset.get("name", "").lower()
                        cand_url = asset.get("browser_download_url")
                        if not is_safe_https_url(cand_url):
                            continue
                        if name == curr_name:
                            exact_match_url = cand_url
                            break
                        elif name in ("osrs_alch_tracker.exe", "osrs_alch_tracker_portable.exe"):
                            fallback_exe_url = cand_url
                        elif name.endswith("_setup.exe") or name.endswith("_installer.exe"):
                            setup_url = cand_url
                        elif name.endswith(".exe") and not fallback_exe_url:
                            fallback_exe_url = cand_url

                    download_url = exact_match_url or fallback_exe_url
                    if not download_url:
                        html_url = data.get("html_url")
                        download_url = setup_url or (html_url if is_safe_https_url(html_url) else None)

                    if download_url:
                        return True, tag_name, download_url, data.get("body", "")
    except Exception as e:
        print(f"Update check failed: {e}")

    return False, current_version, None, ""

def download_file_with_progress(url, dest_path, progress_callback=None):
    """
    Downloads file from URL in chunks, calling progress_callback(percent_int, downloaded_bytes, total_bytes).
    """
    if not is_safe_https_url(url):
        raise ValueError(f"Untrusted download URL: {url}")

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "OSRS-Alch-Tracker-App"}
    )
    with urllib.request.urlopen(req, timeout=45) as resp, open(dest_path, "wb") as f:
        total_size = int(resp.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 64 * 1024 # 64 KB chunks

        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            downloaded += len(chunk)
            if progress_callback:
                pct = int((downloaded / total_size) * 100) if total_size > 0 else 0
                progress_callback(pct, downloaded, total_size)

def apply_update_and_restart(new_exe_path):
    """
    Replaces the current executable with the new one and relaunches.
    Cleans PyInstaller environment variables (_MEIPASS2) to prevent DLL load errors.
    """
    is_frozen = getattr(sys, "frozen", False)
    if not is_frozen:
        return False, "Application is running from Python source code, not a compiled .exe."

    current_exe = sys.executable
    app_dir = os.path.dirname(os.path.abspath(current_exe))

    # Sanitize path strings against injection/syntax breakage
    clean_new = os.path.abspath(new_exe_path).replace('"', '').replace('%', '%%')
    clean_curr = os.path.abspath(current_exe).replace('"', '').replace('%', '%%')
    clean_dir = os.path.abspath(app_dir).replace('"', '').replace('%', '%%')

    # Write small batch script to swap the exe after exit
    temp_dir = tempfile.gettempdir()
    bat_path = os.path.join(temp_dir, f"osrs_update_{int(time.time())}.bat")

    # Clear all PyInstaller environment variables and relaunch via Windows Shell (explorer.exe)
    bat_content = f"""@echo off
set _PYI_APPLICATION_HOME_DIR=
set _PYI_ARCHIVE_FILE=
set _PYI_PARENT_PROCESS_LEVEL=
set _MEIPASS2=
set _MEIPASS=
set PYINSTALLER_RESET_ENVIRONMENT=1

timeout /t 2 /nobreak >nul
:retry
move /y "{clean_new}" "{clean_curr}" >nul 2>&1
if exist "{clean_new}" (
    timeout /t 1 /nobreak >nul
    goto retry
)
cd /d "{clean_dir}"
explorer.exe "{clean_curr}"
del "%~f0"
"""
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)

    # Launch batch file detached with cleaned PyInstaller environment
    flags = 0
    if os.name == "nt":
        DETACHED_PROCESS = 0x00000008
        CREATE_NO_WINDOW = 0x08000000
        flags = DETACHED_PROCESS | CREATE_NO_WINDOW

    clean_env = os.environ.copy()
    for k in list(clean_env.keys()):
        if k.startswith("_PYI_") or k.startswith("_MEI") or k == "PYINSTALLER_STRICT_UNLOAD_MODE":
            clean_env.pop(k, None)
    clean_env["PYINSTALLER_RESET_ENVIRONMENT"] = "1"
    if hasattr(sys, "_MEIPASS"):
        meipass = os.path.abspath(sys._MEIPASS).lower()
        paths = [p for p in clean_env.get("PATH", "").split(os.pathsep) if os.path.abspath(p).lower() != meipass]
        clean_env["PATH"] = os.pathsep.join(paths)

    subprocess.Popen(["cmd.exe", "/c", bat_path], env=clean_env, creationflags=flags, close_fds=True)
    return True, "Restarting application..."

class UpdateDialog(tk.Toplevel):
    def __init__(self, parent, remote_version, download_url, release_notes):
        super().__init__(parent)
        self.parent = parent
        self.remote_version = remote_version
        self.download_url = download_url
        self.release_notes = release_notes
        self.is_downloading = False

        self.title(f"Update Available - {remote_version}")
        self.geometry("480x320")
        self.configure(bg="#252528")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Center dialog
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 240
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 160
        self.geometry(f"+{x}+{y}")

        # Header
        top_f = tk.Frame(self, bg="#252528")
        top_f.pack(fill="x", padx=15, pady=(15, 6))
        tk.Label(top_f, text="🚀 New Update Available!", font=("Segoe UI", 12, "bold"), fg="#2ecc71", bg="#252528").pack(anchor="w")
        tk.Label(top_f, text=f"Version {remote_version} is now available (Current: v{APP_VERSION})", font=("Segoe UI", 9), fg="#cccccc", bg="#252528").pack(anchor="w")

        # Bottom Progress / Button frame (DOCK TO BOTTOM FIRST so it is NEVER cut off!)
        self.bottom_frame = tk.Frame(self, bg="#252528")
        self.bottom_frame.pack(side="bottom", fill="x", padx=15, pady=12)

        self.btn_box = tk.Frame(self.bottom_frame, bg="#252528")
        self.btn_box.pack(fill="x")

        self.btn_later = tk.Button(self.btn_box, text="Later", command=self.destroy, bg="#3e3e42", fg="#ffffff", relief="flat", padx=10, pady=3, cursor="hand2")
        self.btn_later.pack(side="right", padx=(6, 0))

        self.btn_install = tk.Button(self.btn_box, text="⚡ Update Now", command=self.start_update, bg="#27ae60", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=12, pady=3, cursor="hand2")
        self.btn_install.pack(side="right")

        # Release notes text (fills remaining middle space)
        notes_f = tk.Frame(self, bg="#1e1e1e", relief="solid", borderwidth=1)
        notes_f.pack(side="top", fill="both", expand=True, padx=15, pady=6)
        self.txt_notes = tk.Text(notes_f, bg="#1e1e1e", fg="#f1f1f1", font=("Segoe UI", 9), relief="flat", wrap="word", padx=6, pady=6, height=5)
        self.txt_notes.pack(fill="both", expand=True)
        display_notes = release_notes.strip() if release_notes else "Performance improvements, bug fixes, and feature updates."
        self.txt_notes.insert("1.0", display_notes)
        self.txt_notes.config(state="disabled")

        self.bind("<Return>", lambda e: self.start_update())
        self.bind("<Escape>", lambda e: self.destroy())

    def start_update(self):
        if self.is_downloading:
            return

        is_frozen = getattr(sys, "frozen", False)
        if not is_frozen or not self.download_url or not self.download_url.lower().endswith(".exe"):
            # If running in python source code or no direct exe url, open trusted web page
            target_url = self.download_url if (self.download_url and is_safe_https_url(self.download_url)) else f"https://github.com/{GITHUB_REPO}/releases/latest"
            webbrowser.open(target_url)
            self.destroy()
            return

        self.is_downloading = True
        self.btn_box.pack_forget()

        # Progress UI
        self.prog_bar = ttk.Progressbar(self.bottom_frame, orient="horizontal", mode="determinate")
        self.prog_bar.pack(fill="x", pady=(2, 4))
        self.lbl_prog = tk.Label(self.bottom_frame, text="Connecting to GitHub...", font=("Segoe UI", 8), fg="#888888", bg="#252528")
        self.lbl_prog.pack(anchor="w")

        threading.Thread(target=self._download_worker, daemon=True).start()

    def _download_worker(self):
        temp_dir = tempfile.gettempdir()
        temp_exe = os.path.join(temp_dir, f"osrs_update_{int(time.time())}.exe")

        def progress(pct, dl, total):
            mb_dl = dl / (1024 * 1024)
            mb_tot = total / (1024 * 1024) if total > 0 else 0
            self.after(0, lambda: self._update_progress_ui(pct, f"Downloading: {mb_dl:.1f} MB / {mb_tot:.1f} MB ({pct}%)"))

        try:
            download_file_with_progress(self.download_url, temp_exe, progress)
            self.after(0, lambda: self._finish_and_restart(temp_exe))
        except Exception as e:
            self.after(0, lambda: self._on_download_error(str(e)))

    def _update_progress_ui(self, pct, text):
        self.prog_bar["value"] = pct
        self.lbl_prog.config(text=text)

    def _on_download_error(self, err_msg):
        messagebox.showerror("Update Error", f"Failed to download update:\n{err_msg}\n\nOpening release page in browser.")
        webbrowser.open(f"https://github.com/{GITHUB_REPO}/releases/latest")
        self.destroy()

    def _finish_and_restart(self, temp_exe):
        self.lbl_prog.config(text="Applying update & restarting...", fg="#2ecc71")
        success, msg = apply_update_and_restart(temp_exe)
        if success:
            self.after(300, lambda: os._exit(0))
        else:
            messagebox.showinfo("Update Complete", msg)
            self.destroy()

class WhatsNewDialog(tk.Toplevel):
    def __init__(self, parent, version_str):
        super().__init__(parent)
        self.title(f"What's New in v{version_str} 🎉")
        self.geometry("520x400")
        self.configure(bg="#252528")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Center dialog
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 260
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 200
        self.geometry(f"+{x}+{y}")

        top_f = tk.Frame(self, bg="#252528")
        top_f.pack(fill="x", padx=16, pady=(15, 8))
        tk.Label(top_f, text=f"🎉 Successfully Updated to v{version_str}!", font=("Segoe UI", 12, "bold"), fg="#2ecc71", bg="#252528").pack(anchor="w")
        tk.Label(top_f, text="Here is a summary of the latest features and improvements:", font=("Segoe UI", 9), fg="#cccccc", bg="#252528").pack(anchor="w")

        # Highlights box
        box_f = tk.Frame(self, bg="#1e1e1e", relief="solid", borderwidth=1)
        box_f.pack(side="top", fill="both", expand=True, padx=16, pady=6)

        txt = tk.Text(box_f, bg="#1e1e1e", fg="#f1f1f1", font=("Segoe UI", 9), relief="flat", wrap="word", padx=8, pady=8)
        txt.pack(fill="both", expand=True)

        features = (
            "✨ WHAT'S NEW IN v1.3.7 (Update Test Success! 🎉):\n\n"
            "• 🚀 In-App Self-Update Verified:\n"
            "  The app cleanly updated from v1.3.6 to v1.3.7 in-place without any DLL or environment errors!\n\n"
            "• 🛡️ Complete PyInstaller Process Isolation Active:\n"
            "  _PYI_APPLICATION_HOME_DIR and parent environment variables are cleanly scrubbed on restart.\n\n"
            "• 🌟 Two-Tier Responsive Top Control Bar:\n"
            "  Filters and search are cleanly separated from utility toggles. Sound Alerts, Popups, Ring (0 Nat), and Auto-Sync will never get cut off!\n\n"
            "• ↔️ Dark-Themed Horizontal Table Scrollbars:\n"
            "  Smooth horizontal scrolling across both Pure High Alch and Craft & Alch tables.\n\n"
            "• ⚡ Fill Speed & Transaction Velocity Tracking:\n"
            "  Real-time 5m OSRS Wiki velocity tracking with Fast (<15m), Steady (<1h), and Slow (>1h) badges and Speed filters.\n"
        )
        txt.insert("1.0", features)
        txt.config(state="disabled")

        btn_box = tk.Frame(self, bg="#252528")
        btn_box.pack(side="bottom", fill="x", padx=16, pady=12)
        tk.Button(btn_box, text="Awesome, Let's Go! 🚀", command=self.destroy,
                  bg="#27ae60", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=16, pady=5, cursor="hand2").pack(side="right")

        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())
