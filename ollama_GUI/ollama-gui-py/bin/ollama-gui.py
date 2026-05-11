#!/usr/bin/env python
# VERSION: v1.3.11
# KEY_SIG_ID: GR00T-User-706
# CREATOR: Zenrich Shadoestep
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import threading
import subprocess
import os
import time
import json

LLAMA_URL = "http://localhost:11434/api"
API_URL = f"{LLAMA_URL}/chat"
SHOW_URL = f"{LLAMA_URL}/show"
TAGS_URL = f"{LLAMA_URL}/tags"
PULL_URL = f"{LLAMA_URL}/pull"
RM_URL = f"{LLAMA_URL}/rm"


class OllamaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Local LLM")
        # Instance variables
        self.ollama_proc = None
        self.current_mode = "offline"
        self.response_active = False
        # Create menu bar first
        self.create_menu()
        # Setup the rest of the GUI
        self.setup_gui()
        # Protocol for closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Check if server is running; start it if needed
        self.check_and_start_server()
    # ---------------- Mode toggle ----------------

    def toggle_mode(self):
        """Toggle between online/offline mode and restart server if needed"""
        self.current_mode = "online" if self.mode_var_menu.get() else "offline"
        self.update_output(f"[Switched to {self.current_mode.upper()} mode]\n")
        self.status_label.config(text=(
            f"🟢 {self.current_mode.capitalize()
        }"
        if self.current_mode == "online" else "🟡 Offline"
        ),
        fg="green" if self.current_mode == "online" else "orange",)
        # Stop current Ollama process if running
        self.stop_ollama()
        # Start server in new mode
        self.ollama_proc = self.start_ollama(self.current_mode)
        # Threaded wait for server to respond and refresh GUI

        def wait_and_refresh():
            if self.wait_for_server():
                models = self.load_models()
                self.root.after(0, lambda: self.refresh_model_menu(models))
                self.root.after(0, lambda: self.update_output("[Server running]\n"))
                self.root.after(0, lambda: self.set_chat_enabled(True))

                if models:
                    self.root.after(0, lambda: self.update_output(f"[Models: {', '.join(models)}]\n"))
            else:
                self.root.after(0, lambda: self.update_output("[ERROR: Server failed to start]\n"))
                self.root.after(0, lambda: self.set_chat_enabled(False))
                self.root.after(0, lambda: self.status_label.config(text="🔴 Failed", fg="red"))

        threading.Thread(target=wait_and_refresh, daemon=True).start()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load System Prompt...", command=self.load_system_prompt)
        file_menu.add_separator()
        file_menu.add_command(label="Restart Server", command=self.restart_server_dialog)
        file_menu.add_command(label="Quit", command=self.on_closing)
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Chat", command=self.clear_chat)
        edit_menu.add_command(label="Interrupt", command=self.interrupt_response)
        # Models menu
        models_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Models", menu=models_menu)
        models_menu.add_command(label="Show Available Models", command=self.show_models)
        models_menu.add_command(label="Pull Model...", command=self.pull_model)
        models_menu.add_command(label="Remove Model...", command=self.remove_model)
        models_menu.add_command(label="Show Model Info", command=self.show_model_info)
        models_menu.add_separator()
        # Parameters submenu
        params_menu = tk.Menu(models_menu, tearoff=0)
        models_menu.add_cascade(label="Set Parameters", menu=params_menu)
        params_menu.add_command(label="Temperature...", command=lambda: self.set_param("temperature"))
        params_menu.add_command(label="Top P...", command=lambda: self.set_param("top_p"))
        params_menu.add_command(label="Context Length...", command=lambda: self.set_param("num_ctx"))
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        # Mode toggle (checkbutton)
        self.mode_var_menu = tk.BooleanVar(value=False)  # False = offline, True = online
        settings_menu.add_checkbutton(label="Online Mode", variable=self.mode_var_menu, command=self.toggle_mode)
        settings_menu.add_separator()
        settings_menu.add_command(label="Server Options...", command=self.server_options)
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)

    def setup_gui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(padx=10, pady=5, fill="x")
        tk.Label(top_frame, text="Model:").pack(side="left", pady=5, padx=5)
        self.model_var = tk.StringVar()
        self.menu = tk.OptionMenu(top_frame, self.model_var, "")
        self.menu.pack(side="left", padx=5)
        self.status_label = tk.Label(top_frame, text="⚫ Server stopped", fg="gray")
        self.status_label.pack(side="right", padx=5)
        tk.Label(self.root, text="System Prompt (optional)").pack(anchor="w", padx=10)
        self.sys_prompt = tk.Text(self.root, height=4, width=100)
        self.sys_prompt.pack(padx=10, pady=5)
        tk.Label(self.root, text="User Prompt").pack(anchor="w", padx=10)
        self.entry = tk.Text(self.root, height=8, width=100)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.pack(padx=10, pady=5)
        self.btn = tk.Button(self.root, text="Run", command=self.run)
        self.btn.pack(pady=5)
        self.output = tk.Text(self.root, height=25, width=100)
        self.output.pack(padx=10, pady=5)

    def set_chat_enabled(self, enabled):
        state = "normal" if enabled else "disabled"
        self.menu.config(state=state)
        self.sys_prompt.config(state=state)
        self.entry.config(state=state)
        self.btn.config(state=state if enabled else "disabled")
# ---------------- Ollama server management ----------------

    def start_ollama(self, mode):
        env = os.environ.copy()
        if mode == "offline":
            env["OLLAMA_HOME"] = "/home/lykthornyx/.ollama/models"
            env["OLLAMA_MODELS"] = "/home/lykthornyx/.ollama/models"
        env["OLLAMA_HOST"] = "127.0.0.1:11434"
        return subprocess.Popen(["ollama", "serve"], env=env)

    def stop_ollama(self):
        if self.ollama_proc:
            self.ollama_proc.terminate()
            self.ollama_proc.wait()
            self.ollama_proc = None

    def wait_for_server(self):
        for _ in range(20):
            try:
                requests.get(TAGS_URL)
                return True
            except:
                time.sleep(0.5)
        return False

    def is_server_running(self):
        try:
            requests.get(TAGS_URL, timeout=1)
            return True
        except:
            return False

    def check_and_start_server(self):
        def do_start():
            if not self.is_server_running():
                subprocess.run(["systemctl", "reload-or-restart", "ollama"], check=False)
            if self.wait_for_server():
                models = self.load_models()
                self.refresh_model_menu(models)
                self.root.after(0, lambda: self.update_output("[Server running]\n"))
                self.root.after(0, lambda: self.status_label.config(text="🟢 Running", fg="green"))
                self.root.after(0, lambda: self.set_chat_enabled(True))
                if models:
                    self.root.after(0, lambda: self.update_output(f"[Models: {', '.join(models)}]\n"),)
            else:
                self.root.after(0, lambda: self.update_output("[ERROR: Server failed to start]\n"))
                self.root.after(0, lambda: self.status_label.config(text="🔴 Failed", fg="red"))
                self.root.after(0, lambda: self.set_chat_enabled(False))
        threading.Thread(target=do_start, daemon=True).start()

    def restart_server_dialog(self):
        if messagebox.askyesno("Restart Server", f"Restart server in {self.current_mode} mode?"):
            self.toggle_mode()  # reuse toggle_mode for restart

    # ---------------- Chat & API ----------------
    def generate(self, prompt, model, system_prompt):
        try:
            r = requests.post(API_URL,json={"model": model,"messages": [{"role": "system", "content": system_prompt},{"role": "user", "content": prompt},],"stream": False,},)
            return r.json()["message"]["content"]
        except Exception as e:
            return (f"[ERROR] {e}")

    def update_output(self, result):
        self.output.insert(tk.END, f"{result}\n")
        self.output.see(tk.END)

    def run(self):
        if self.response_active:
            return
        prompt = self.entry.get("1.0", tk.END).strip()
        if not prompt:
            return
        model = self.model_var.get()
        system_text = self.sys_prompt.get("1.0", tk.END).strip()
        self.output.insert(tk.END, f"\n\n> {prompt}\nThinking....\n")
        self.output.see(tk.END)
        self.response_active = True
        self.btn.config(text="Interrupt", command=self.interrupt_response)

        def task():
            result = self.generate(prompt, model, system_text)

            if not self.response_active:
                result = "\n[INTERRUPTED]\n"

            self.root.after(0, lambda: self.update_output(result))
            self.root.after(0, self.reset_run_button)

        threading.Thread(target=task, daemon=True).start()

    def interrupt_response(self):
        self.response_active = False
        self.update_output("\n[INTERRUPTING...]\n")
        self.reset_run_button()

    def reset_run_button(self):
        self.response_active = False
        self.btn.config(text="Run", command=self.run)

    def on_enter(self, event):
        if event.state & 0x0001:
            return
        self.run()
        return "break"

    # ---------------- Model management ----------------
    def load_models(self):
        try:
            r = requests.get(TAGS_URL)
            return [m["name"] for m in r.json().get("models", [])]
        except:
            return []

    def load_model_params(self, model):
        config_path = (f"/home/lykthornyx/.ollama/models/manifests/registry.ollama.ai/library/{model}/config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                cfg = json.load(f)
            self.temperature = cfg.get("temperature", 0.7)
            self.top_p = cfg.get("top_p", 0.9)
            self.num_ctx = cfg.get("num_ctx", 8192)
        else:
            self.temperature = 0.7
            self.top_p = 0.9
            self.num_ctx = 8192 # 16384

    def refresh_model_menu(self, models):
        if models:
            self.model_var.set(models[0])
            self.load_model_params(models[0])
            self.menu["menu"].delete(0, "end")
        for m in models:
            self.menu["menu"].add_command(
                label=m, command=lambda v=m: self.model_var.set(v)
            )

    # ---------------- Menu commands ----------------
    def load_system_prompt(self):
        filename = filedialog.askopenfilename(
            title="Load System Prompt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            with open(filename, "r") as f:
                content = f.read()
            self.sys_prompt.delete("1.0", tk.END)
            self.sys_prompt.insert("1.0", content)
            self.update_output(f"[Loaded system prompt from {filename}]\n")

    def clear_chat(self):
        self.output.delete("1.0", tk.END)

    def show_models(self):
        try:
            r = requests.get(TAGS_URL)
            models = r.json().get("models", [])
            self.update_output("\n--- Available Models ---\n")
            for m in models:
                self.update_output(f"  {m['name']}\n")
        except Exception as e:
            self.update_output(f"[Error: {e}]\n")

    def pull_model(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Pull Model")
        dialog.geometry("300x100")
        tk.Label(dialog, text="Model name:").pack(pady=5)
        entry = tk.Entry(dialog)
        entry.pack(pady=5)

        def do_pull():
            model = entry.get().strip()
            if model:
                dialog.destroy()
                self.update_output(f"[Pulling {model}...]\n")

                def pull_thread():
                    process = subprocess.run(
                        ["ollama", "pull", model], capture_output=True, text=True
                    )
                    if process.returncode == 0:
                        self.root.after(
                            0, lambda: self.update_output(f"[Pulled {model}]\n")
                        )
                        self.root.after(0, self.refresh_models)
                    else:
                        self.root.after(
                            0,
                            lambda: self.update_output(f"[Error: {process.stderr}]\n"),
                        )

            threading.Thread(target=pull_thread, daemon=True).start()

        tk.Button(dialog, text="Pull", command=do_pull).pack(pady=5)

    def remove_model(self):
        model = self.model_var.get()
        if not model:
            messagebox.showwarning("No Model", "Select a model first")
            return
        if messagebox.askyesno("Remove Model", f"Remove {model}?"):
            self.update_output(f"[Removing {model}...]\n")

        def remove_thread():
            process = subprocess.run(["ollama", "rm", model], capture_output=True, text=True)
            if process.returncode == 0:
                self.root.after(0, lambda: self.update_output(f"[Removed {model}]\n"))
                self.root.after(0, self.refresh_models)
            else:
                self.root.after(0, lambda: self.update_output(f"[Error: {process.stderr}]\n"))

        threading.Thread(target=remove_thread, daemon=True).start()

    def refresh_models(self):
        models = self.load_models()
        self.refresh_model_menu(models)

    def show_model_info(self):
        model = self.model_var.get()
        if not model:
            messagebox.showwarning("No Model", "Select a model first")
            return

        self.update_output(f"\n--- {model} Info ---\n")

        def get_info():
            try:
                r = requests.post(SHOW_URL, json={"model": model})
                data = r.json()
                if "modelfile" in data:
                    lines = data["modelfile"].split("\n")[:15]
                    self.root.after(0, lambda: self.update_output("\n".join(lines) + "\n"))
                if "details" in data:
                    details = data["details"]
                    self.root.after(0, lambda: self.update_output(f"\nFormat: {details.get('format', 'N/A')}\n"))
                    self.root.after(0, lambda: self.update_output(f"Family: {details.get('family', 'N/A')}\n"))
                    self.root.after(0, lambda: self.update_output(f"Parameter size: {details.get('parameter_size', 'N/A')}\n"))
            except Exception as e:
                self.root.after(0, lambda: self.update_output(f"Error: {e}\n"))

        threading.Thread(target=get_info, daemon=True).start()

    def set_param(self, param):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Set {param}")
        dialog.geometry("300x100")
        tk.Label(dialog, text=f"{param} value:").pack(pady=5)
        default = ("0.7" if param == "temperature" else "0.9" if param == "top_p" else "8192")
        entry = tk.Entry(dialog)
        entry.insert(0, default)
        entry.pack(pady=5)

        def apply():
            value = entry.get()
            dialog.destroy()
            model = self.model_var.get()
            if not model:
                self.update_output("[No model selected]\n")
                return
            config_path = (f"/home/lykthornyx/.ollama/models/manifests/registry.ollama.ai/library/{model}/config.json")
            cfg = {}
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    cfg = json.load(f)
                    cfg[param] = value
            with open(config_path, "w") as f:
                json.dump(cfg, f, indent=2)
                self.update_output(f"[{param}={value} saved for {model}]\n")

        tk.Button(dialog, text="Apply", command=apply).pack(pady=5)

    def server_options(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Server Options")
        dialog.geometry("400x250")
        tk.Label(dialog, text="Server Configuration", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(dialog, text=f"OLLAMA_HOST: 127.0.0.1:11434").pack(anchor="w", padx=10, pady=2)
        tk.Label(dialog, text=f"Current mode: {self.current_mode}").pack(anchor="w", padx=10, pady=2)
        path = ("/home/lykthornyx/.ollama/models" if self.current_mode == "offline" else "~/.ollama/models")
        tk.Label(dialog, text=f"Models path: {path}").pack(anchor="w", padx=10, pady=2)
        status = "Running" if self.ollama_proc else "Stopped"
        tk.Label(dialog, text=f"Server status: {status}").pack(anchor="w", padx=10, pady=10)

    def about(self):
        messagebox.showinfo("About","Local LLM Interface\n\nOllama frontend\nRuns completely offline\nModels stored locally",)

    def on_closing(self):
        self.stop_ollama()
        self.root.destroy()


# ---------------- Run the app ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaApp(root)
    root.mainloop()
