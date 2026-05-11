"""
gui_integration.py
------------------
A drop-in example showing how to wire OllamaToolEngine into your
existing Tkinter GUI. This is NOT a standalone app — it shows the
patterns to copy into your own code.

Key additions to your existing GUI:
  1. Import OllamaToolEngine instead of calling ollama directly.
  2. Add a "Tools" menu to your menubar.
  3. Replace your send-button callback with engine.chat().

Look for the  <-- ADD THIS  comments to find the new lines.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading

# <-- ADD THIS: import the engine
from ollama_tools import OllamaToolEngine, TOOL_REGISTRY


class OllamaGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ollama Chat")
        self.geometry("900x650")

        # <-- ADD THIS: create the engine (do this once at startup)
        self.engine = OllamaToolEngine(model="mistral", verbose=True)

        self._build_menu()
        self._build_widgets()

    # ------------------------------------------------------------------
    # Menu bar
    # ------------------------------------------------------------------

    def _build_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu (you probably already have this)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Clear Chat",    command=self._clear_chat)
        file_menu.add_command(label="New Session",   command=self._new_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit",          command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # <-- ADD THIS: Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        self._build_tools_menu(tools_menu)
        menubar.add_cascade(label="Tools", menu=tools_menu)

    def _build_tools_menu(self, tools_menu: tk.Menu):
        """
        Populate the Tools dropdown from TOOL_REGISTRY.
        Each tool gets:
          - A checkbutton to enable/disable it at runtime
          - An "Info..." item that shows what the tool can do
        """
        self._tool_vars: dict[str, tk.BooleanVar] = {}

        for tool_name, entry in TOOL_REGISTRY.items():
            var = tk.BooleanVar(value=entry["enabled"])
            self._tool_vars[tool_name] = var

            # Checkbutton — toggles the tool on/off
            tools_menu.add_checkbutton(
                label=f"  {entry['label']}",
                variable=var,
                command=lambda n=tool_name, v=var: self._toggle_tool(n, v),
            )

        tools_menu.add_separator()

        # Info submenu — shows details for each tool
        info_menu = tk.Menu(tools_menu, tearoff=0)
        for tool_name, entry in TOOL_REGISTRY.items():
            info_menu.add_command(
                label=entry["label"],
                command=lambda n=tool_name: self._show_tool_info(n),
            )
        tools_menu.add_cascade(label="Tool Info...", menu=info_menu)

        tools_menu.add_separator()

        # Memory shortcuts
        tools_menu.add_command(label="Show All Memories",  command=self._show_memories)
        tools_menu.add_command(label="Open Sandbox Folder", command=self._open_sandbox)

    def _toggle_tool(self, tool_name: str, var: tk.BooleanVar):
        enabled = var.get()
        self.engine.toggle_tool(tool_name, enabled)
        label = TOOL_REGISTRY[tool_name]["label"]
        state = "enabled" if enabled else "disabled"
        self._append_system(f"[Tools] '{label}' {state}.")

    def _show_tool_info(self, tool_name: str):
        entry = TOOL_REGISTRY[tool_name]
        details = entry["details"]
        lines = [
            f"Tool: {entry['label']}",
            f"Description: {entry['description']}",
            "",
        ]
        t = details.get("type")
        if t == "system_command":
            lines.append("Allowed commands:")
            for cmd in details["commands"]:
                lines.append(f"  • {cmd}")
        elif t == "memory":
            lines.append("Operations: " + ", ".join(details["operations"]))
            lines.append("")
            lines.append("Memory is stored in:")
            lines.append(f"  ~/.ollama_tools/memory.json")
        elif t == "sandbox_file":
            lines.append("Operations: " + ", ".join(details["operations"]))
            lines.append("")
            lines.append("Sandbox directory:")
            lines.append(f"  ~/.ollama_tools/sandbox/")

        messagebox.showinfo(entry["label"], "\n".join(lines))

    def _show_memories(self):
        result = self.engine.memory_store.recall()
        messagebox.showinfo("Stored Memories", result)

    def _open_sandbox(self):
        import subprocess, shutil
        path = str(self.engine.sandbox_store.sandbox)
        # Try common file managers
        for fm in ["thunar", "nautilus", "dolphin", "nemo", "pcmanfm", "xdg-open"]:
            if shutil.which(fm):
                subprocess.Popen([fm, path])
                return
        messagebox.showinfo("Sandbox Directory", path)

    # ------------------------------------------------------------------
    # Main chat widgets
    # ------------------------------------------------------------------

    def _build_widgets(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self, wrap=tk.WORD, state=tk.DISABLED, font=("Monospace", 11)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=8, pady=(8, 0))

        # Tag styles
        self.chat_display.tag_config("user",   foreground="#00bfff", font=("Monospace", 11, "bold"))
        self.chat_display.tag_config("llm",    foreground="#e0e0e0")
        self.chat_display.tag_config("system", foreground="#888888", font=("Monospace", 10, "italic"))
        self.chat_display.tag_config("tool",   foreground="#ffa500")

        # Model selector
        model_frame = tk.Frame(self)
        model_frame.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(model_frame, text="Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value="mistral")
        model_entry = ttk.Combobox(
            model_frame, textvariable=self.model_var,
            values=["mistral", "llama3.1", "llama3.2", "qwen2.5", "phi3"],
            width=20,
        )
        model_entry.pack(side=tk.LEFT, padx=4)
        model_entry.bind("<<ComboboxSelected>>", self._on_model_change)

        # Input area
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, padx=8, pady=8)
        self.input_box = tk.Text(input_frame, height=3, font=("Monospace", 11), wrap=tk.WORD)
        self.input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_box.bind("<Return>",       self._on_enter)
        self.input_box.bind("<Shift-Return>", lambda e: None)  # allow newlines

        send_btn = ttk.Button(input_frame, text="Send", command=self._send)
        send_btn.pack(side=tk.LEFT, padx=(4, 0))

    def _on_model_change(self, event=None):
        self.engine.model = self.model_var.get()
        self._append_system(f"[Model] Switched to {self.engine.model}")

    def _on_enter(self, event):
        # Enter sends, Shift+Enter is a newline
        if not event.state & 0x1:  # Shift not held
            self._send()
            return "break"

    # ------------------------------------------------------------------
    # Chat logic
    # ------------------------------------------------------------------

    def _send(self):
        prompt = self.input_box.get("1.0", tk.END).strip()
        if not prompt:
            return
        self.input_box.delete("1.0", tk.END)
        self._append_chat("You", prompt, tag="user")
        # Run in a thread so the GUI doesn't freeze
        threading.Thread(target=self._run_chat, args=(prompt,), daemon=True).start()

    def _run_chat(self, prompt: str):
        self._append_system("[Thinking...]")
        # <-- ADD THIS: use engine.chat() instead of calling ollama directly
        answer = self.engine.chat(prompt)
        self._remove_last_system()
        self._append_chat("Assistant", answer, tag="llm")

    def _append_chat(self, speaker: str, text: str, tag: str = "llm"):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{speaker}:\n", tag)
        self.chat_display.insert(tk.END, text + "\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _append_system(self, text: str):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, text + "\n", "system")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _remove_last_system(self):
        # Remove the "[Thinking...]" line
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.config(state=tk.DISABLED)

    def _clear_chat(self):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def _new_session(self):
        self.engine.clear_history()
        self._clear_chat()
        self._append_system("[New session started — conversation history cleared]")


if __name__ == "__main__":
    app = OllamaGUI()
    app.mainloop()
