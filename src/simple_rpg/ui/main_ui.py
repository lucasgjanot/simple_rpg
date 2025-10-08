import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import json

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)


def get_save_path(name):
    return os.path.join(SAVE_DIR, f"{name}.json")


def character_exists(name):
    return os.path.exists(get_save_path(name))


def launch_game(name, new_game=False, filename=None):
    from simple_rpg.ui import game_ui
    game_ui.start_game_ui(name, new_game, filename)


def main():
    # ============================================================
    # UI Setup
    # ============================================================
    root = tk.Tk()
    root.title("Simple RPG - Menu")
    root.geometry("420x300")
    root.configure(bg="#1e1e2e")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#1e1e2e")
    style.configure("TLabel", background="#1e1e2e", foreground="#fafafa", font=("Consolas", 11))
    style.configure("Header.TLabel", font=("Consolas", 14, "bold"), foreground="#ffcc00")
    style.configure("TEntry", fieldbackground="#2b2b3b", foreground="#fafafa", insertcolor="#fafafa")
    style.configure("TButton", background="#29293d", foreground="#fafafa", font=("Consolas", 11, "bold"), padding=6)
    style.map("TButton", background=[("active", "#404060")])

    frame = ttk.Frame(root)
    frame.pack(expand=True)

    # ============================================================
    # Layout
    # ============================================================
    ttk.Label(frame, text="Welcome to Simple RPG", style="Header.TLabel").pack(pady=(10, 15))

    ttk.Label(frame, text="Type your name:").pack(pady=5)
    name_entry = ttk.Entry(frame, width=30, justify="center")
    name_entry.pack(pady=5)
    name_entry.focus()

    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=20)

    # ============================================================
    # Button callbacks (need access to name_entry and root)
    # ============================================================
    def start_new_game():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Type a name to start")
            return

        # Check if character already exists
        if character_exists(name):
            res = messagebox.askyesno(
                "Overwrite?",
                f"A character named '{name}' already exists. Overwrite?"
            )
            if not res:
                return

        root.destroy()
        launch_game(name, True)

    def load_game():
        saves = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
        if not saves:
            messagebox.showinfo("No Saves", "No saved characters found.")
            return

        load_window = tk.Toplevel(root)
        load_window.title("Load Game")
        load_window.geometry("350x300")
        load_window.configure(bg="#1e1e2e")

        ttk.Label(load_window, text="Select a saved character", style="Header.TLabel").pack(pady=10)

        listbox = tk.Listbox(load_window, bg="#2b2b3b", fg="#fafafa", selectbackground="#444466", width=40)
        listbox.pack(padx=10, pady=5, fill="both", expand=True)

        saves_data = []
        for save_file in saves:
            path = os.path.join(SAVE_DIR, save_file)
            with open(path, "r") as f:
                data = json.load(f)
            saves_data.append((save_file, data))
            listbox.insert(tk.END, f"{data['name']} (Lvl {data.get('level',1)})")

        def confirm_load():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Select", "Select a character to load")
                return
            idx = selection[0]
            save_file, data = saves_data[idx]
            filename = os.path.join(SAVE_DIR, save_file)
            root.destroy()
            launch_game(data['name'], new_game=False, filename=filename)

        ttk.Button(load_window, text="Load", command=confirm_load).pack(pady=5)
        ttk.Button(load_window, text="Cancel", command=load_window.destroy).pack(pady=5)

    # ============================================================
    # Buttons
    # ============================================================
    ttk.Button(button_frame, text="New Game", command=start_new_game).grid(row=0, column=0, padx=10)
    ttk.Button(button_frame, text="Load Game", command=load_game).grid(row=0, column=1, padx=10)

    # ============================================================
    # Start main loop
    # ============================================================
    root.mainloop()


if __name__ == "__main__":
    main()
