#!/usr/bin/env python3
# DEV: https://www.github.com/GR00T-User-706
# VERSION = "v1.3.0"
import tkinter as tk
from tkinter import ttk
import requests
import traceback
from pathlib import Path
from datetime import datetime,timezone
import humanfriendly

LOG_FILE = Path.home() /".ai-mon.log"

PS_URL = "http://192.168.1.152:11434/api/ps"
PS_LOCAL = "http://localhost:11434/api/ps"

def log_error(e):
        with open(LOG_FILE, "a") as f:
                f.write(traceback.format_exc())

def bytes_to_gb(bytes_val):
        return f"{bytes_val / (1024**3):.1f} GB"

def time_remaining(expires_at_str):
        try:
                expires = datetime.fromisoformat(expires_at_str.replace('Z', '+00:00'))
                now = datetime.now(timezone.utc) if expires.tzinfo else datetime.now()
                delta = expirers - now
                seconds = delta.total_seconds()
                if seconds <= 0:
                        return "expired"
                if seconds < 60:
                        return f"{int(seconds)} sec"
                if seconds < 3600:
                        return f"{int(seconds//60)} min"
                return f"{seconds/3600:.1f} hr"
        except:
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
        return{"Error": " | ".join(errors)}

def update_table(tree, data):
        for row in tree.get_children():
                tree.delete(row)

        if "error" in data:
                tree.insert("", tk.END, values=("Error", data["error"], "", ""))
                return

        models = data.get("models", [])
        for m in models:
                vram = m.get("size_vram", 0)
                vram_str= bytes_to_gb(vram) if vram else "?"
                expires = m.get("expires_at", "")
                remaining = time_remaining(expires) if expires else "?"
                details = m.get("details", {})
                tree.insert("", tk.END, values=(
                        m.get("name", "?"),
                        vram_str,
                        m.get("context_length", "?"),
                        remaining,
                        details.get("parameter_size", ""),
                        details.get("quantization_level", "?")
                ))

def refresh(tree, root):
        data = fetch()
        update_table(tree, data)
        root.after(1000, lambda:  refresh(tree, root))


def main():
        root = tk.Tk()
        root.title("Local LLM API Monitor")

        columns = ("Model", "VRAM", "Context", "Expires In", "Params", "Quant")
        tree = ttk.Treeview(root, columns=columns, show="headings")
        for col in columns:
                tree.heading(col, tex=col)
                tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        refresh(tree, root)
        root.mainloop()

if __name__=="__main__":
        try:
                main()
        except Exception as e:
                log_error(e)
                import tkinter.messagebox as mb
                mb.showerror("AI-Monitor Error", f"See {LOG_FILE}\n{e}")
