#!/usr/bin/env python3
# DEV: https://www.github.com/GR00T-User-706
# VERSION = "v1.3.0"
import tkinter as tk
from tkinter import ttk
import requests
import traceback
from pathlib import Path
from datetime import datetime, timezone

LOG_FILE = Path.home() / ".ai-mon.log"

PS_URL = "http://192.168.1.152:11434/api/ps"
PS_LOCAL = "http://localhost:11434/api/ps"
REFRESH_INTERVAL_MS = 1000


def log_error(e):
    with open(LOG_FILE, "a") as f:
        f.write(traceback.format_exc())


def bytes_to_gb(bytes_val):
    return f"{bytes_val / (1024**3):.1f} GB"


def time_remaining(expires_at_str):
    try:
        expires = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc) if expires.tzinfo else datetime.now()
        delta = expires - now
        seconds = delta.total_seconds()
        if seconds <= 0:
            return "expired"
        if seconds < 60:
            return f"{int(seconds)} sec"
        if seconds < 3600:
            return f"{int(seconds//60)} min"
        return f"{seconds/3600:.1f} hr"
    except Exception:
        return "?"


def fetch():
    urls = [PS_LOCAL, PS_URL]
    errors = []
    for url in urls:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code != 200:
                errors.append(f"{url} returned status {resp.status_code}")
                continue
            return resp.json()
        except Exception as e:
            errors.append(f"{url}: Error: {str(e)}")
            continue
    return {"error": " | ".join(errors)}


def update_table(tree, data):
    for row in tree.get_children():
        tree.delete(row)

    if "error" in data:
        tree.insert("", tk.END, values=("Error", data["error"], "", "", "", ""))
        return

    models = data.get("models", [])
    for m in models:
        vram = m.get("size_vram", 0)
        vram_str = bytes_to_gb(vram) if vram else "?"
        expires = m.get("expires_at", "")
        remaining = time_remaining(expires) if expires else "?"
        details = m.get("details", {})
        tree.insert(
            "",
            tk.END,
            values=(
                m.get("name", "?"),
                vram_str,
                m.get("context_length", "?"),
                remaining,
                details.get("parameter_size", ""),
                details.get("quantization_level", "?"),
            ),
        )


def refresh(tree, window):
    if not tree.winfo_exists() or not window.winfo_exists():
        return

    data = fetch()
    update_table(tree, data)
    window.after(REFRESH_INTERVAL_MS, lambda: refresh(tree, window))


def create_monitor_window(parent=None):
    """Create the LLM process monitor as a Tk root or child popup window."""
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Local LLM API Monitor")
    window.geometry("950x320")

    frame = ttk.Frame(window, padding=8)
    frame.pack(fill=tk.BOTH, expand=True)

    columns = ("Model", "VRAM", "Context", "Expires In", "Params", "Quant")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="w")

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    refresh(tree, window)
    return window


def main():
    root = create_monitor_window()
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_error(e)
        import tkinter.messagebox as mb

        mb.showerror("AI-Monitor Error", f"See {LOG_FILE}\n{e}")
