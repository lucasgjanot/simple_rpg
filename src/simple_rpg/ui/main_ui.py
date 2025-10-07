import tkinter as tk
from tkinter import messagebox
import os
import json

SAVE_DIR = "saves"

# Garante que a pasta de saves exista
os.makedirs(SAVE_DIR, exist_ok=True)

def start_new_game():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Type a name to start")
        return
    
    save_path = os.path.join(SAVE_DIR, f"{name}.json")
    if os.path.exists(save_path):
        if not messagebox.askyesno("Overwrite", "A character with this name already exists. Do you want to overwrite it?"):
            return
    root.destroy()
    launch_game(name, new_game=True)

def load_game():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Type a saved character name")
        return
    save_path = os.path.join(SAVE_DIR,f"{name}.json")
    if not os.path.exists(save_path):
        messagebox.showerror("Error", "No character with this name has been found")
        return
    root.destroy()
    launch_game(name, new_game=False)

def launch_game(name, new_game=False):
    import game_ui
    game_ui.start_game_ui(name,new_game)

root = tk.Tk()
root.title("Simple RPG - Menu")
root.geometry("400x150")

tk.Label(root, text="Type your name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Button(root, text="New Game", command=start_new_game).pack(pady=5)
tk.Button(root, text="Carregar Jogo", command=load_game).pack(pady=5)

root.mainloop()