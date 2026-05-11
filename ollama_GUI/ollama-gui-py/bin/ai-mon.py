#!/usr/bin/env python3
import tkinter as tk
import requests

PS_URL = "http://192.168.1.152:11434/api/ps"
PS_LOCAL = "http://localhost:11434/api/ps"

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
                        errors.append(f"{url} error: str(e)")
                        continue
        return{"Error": " | ".join(errors)}

def refresh():
        data = fetch()
        label.config(text=str(data))
        root.after(1000, refresh)

root = tk.Tk()
root.title("Local LLM API Monitor")

label = tk.Label(root, font=("monospace", 10), justify="left")
label.pack(fill="both", expand=True)

refresh()
root.mainloop()
