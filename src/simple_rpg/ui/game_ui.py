import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

from simple_rpg.character import Character
from simple_rpg.monsters.chicken import Chicken
from simple_rpg.monsters.slime import Slime
from simple_rpg.monsters.goblin import Goblin
from simple_rpg.monsters.skeleton import Skeleton
from simple_rpg.monsters.spider import Spider
from simple_rpg.monsters.plant import Plant
from simple_rpg.monsters.wolf import Wolf
from simple_rpg.monsters.dragon import Dragon
from simple_rpg.items.armor import Armor
from simple_rpg.items.sword import Sword
from simple_rpg.items.potions import Potion, PotionType
from simple_rpg.load import save_game, load_game

SAVE_DIR = "saves"
current_monster = None
char = None

def start_game_ui(player_name, new_game=False, filename=None):
    global char, current_monster

    if new_game:
        char = Character(player_name)
        initial_items = [
            Potion(PotionType.HEALTH, 1),
            Potion(PotionType.STAMINA, 1),
            Sword(1, 1),
            Armor(1, 1)
        ]
        for item in initial_items:
            char.add_to_inventory(item)
            char.equip_item(item)

        save_game(char, os.path.join(SAVE_DIR, f"{char.get_name()}.json"))
    else:
        char = load_game(filename, Character)

    # Root setup
    root = tk.Tk()
    root.title(f"⚔️ Simple RPG - {char.get_name()}")
    root.geometry("1200x600")
    root.configure(bg="#1c1c28")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#1c1c28")
    style.configure("TLabel", background="#1c1c28", foreground="#fafafa", font=("Consolas", 11))
    style.configure("Header.TLabel", font=("Consolas", 14, "bold"), foreground="#ffcc00")
    style.configure("TButton", background="#29293d", foreground="#fafafa", font=("Consolas", 10, "bold"), padding=6)
    style.map("TButton", background=[("active", "#404060")])
    style.configure("TLabelframe", background="#1c1c28")
    style.configure("TLabelframe.Label", background="#1c1c28", foreground="#ffcc00", font=("Consolas", 11, "bold"))

    # Utility functions
    def update_output(msg):
        output_box.config(state="normal")
        output_box.insert(tk.END, msg + "\n")
        output_box.see(tk.END)
        output_box.config(state="disabled")

    def update_player_status():
        player_status.config(state="normal")
        player_status.delete("1.0", tk.END)
        player_status.insert(tk.END, str(char))
        player_status.config(state="disabled")

    def update_monster_status():
        monster_status.config(state="normal")
        monster_status.delete("1.0", tk.END)
        monster_status.insert(tk.END, str(current_monster) if current_monster else "No monster")
        monster_status.config(state="disabled")

    # Actions
    def choose_monster():
        def confirm_choice():
            output_box.config(state="normal")
            output_box.delete("1.0", tk.END)
            output_box.config(state="disabled")
            nonlocal monster_window
            global current_monster
            monster_type = monster_var.get()
            level = int(level_var.get())

            # Map selection to monster classes
            monster_classes = {
                "Chicken": Chicken,
                "Slime": Slime,
                "Goblin": Goblin,
                "Skeleton": Skeleton,
                "Spider": Spider,
                "Plant": Plant,
                "Wolf": Wolf,
                "Dragon": Dragon
            }

            if monster_type in monster_classes:
                current_monster = monster_classes[monster_type](level)
            else:
                messagebox.showerror("Error", "Invalid monster type.")
                return

            update_output(f"You found a {current_monster.get_name()} (Level {level})")
            update_monster_status()
            monster_window.destroy()

        monster_window = tk.Toplevel(root)
        monster_window.title("Choose Monster")
        monster_window.geometry("300x300")
        monster_window.configure(bg="#1c1c28")

        ttk.Label(monster_window, text="Monster Type:", font=("Consolas", 11)).pack(pady=5)

        monster_var = tk.StringVar(value="Chicken")
        monster_names = ["Plant","Chicken", "Slime","Wolf", "Goblin", "Skeleton", "Spider", "Dragon"]
        ttk.OptionMenu(monster_window, monster_var, *monster_names).pack(pady=5)

        ttk.Label(monster_window, text="Monster Level:", font=("Consolas", 11)).pack(pady=5)
        level_var = tk.StringVar(value="1")
        ttk.OptionMenu(monster_window, level_var, *[str(i) for i in range(1, 6)]).pack(pady=5)

        ttk.Button(monster_window, text="Confirm", command=confirm_choice).pack(pady=10)
        ttk.Button(monster_window, text="Cancel", command=monster_window.destroy).pack()
        monster_window.transient(root)
        monster_window.grab_set()

    def attack():
        if not char.is_alive():
            update_output(f"{char.get_name()} is dead!")
            return
        if not current_monster:
            update_output("No monster selected.")
            return
        if not current_monster.is_alive():
            update_output("Monster already defeated.")
            return

        try:
            update_output(char.attack_target(current_monster))
        except Exception as e:
            update_output(str(e))

        if current_monster.is_alive():
            try:
                update_output(current_monster.attack_target(char))
            except Exception as e:
                update_output(str(e))
        else:
            level_up_msgs = char.gain_xp(current_monster.get_xp_gain())
            item = current_monster.drop_item()
            char.add_to_inventory(item)
            update_output(f"You defeated {current_monster.get_name()}! Received item: {item.get_name()}")
            for msg in level_up_msgs:
                update_output(msg)

        update_player_status()
        update_monster_status()

    def use_potion():
        if not char.is_alive():
            update_output(f"{char.get_name()} is dead!")
            return

        potions = char.get_equipped_potions()
        if not potions:
            update_output("No potions equipped.")
            return

        potion_window = tk.Toplevel(root)
        potion_window.title("Choose a Potion")
        potion_window.geometry("300x200")
        potion_window.configure(bg="#1c1c28")

        ttk.Label(potion_window, text="Select a potion:", font=("Consolas", 11)).pack(pady=5)
        listbox = tk.Listbox(potion_window, height=6, width=40, bg="#2b2b3b", fg="#fafafa", selectbackground="#444466")
        for i, potion in enumerate(potions):
            listbox.insert(tk.END, f"{i + 1}. {potion.get_name()} (Lv {potion.get_potionlevel()})")
        listbox.pack(pady=5)

        def confirm_potion():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a potion before confirming.")
                return
            potion = potions[selection[0]]
            try:
                msg = char.use_potion(potion)
                update_output(msg)
            except Exception as e:
                update_output(str(e))
            update_player_status()
            potion_window.destroy()

        ttk.Button(potion_window, text="Use", command=confirm_potion).pack(pady=5)
        ttk.Button(potion_window, text="Cancel", command=potion_window.destroy).pack()
        potion_window.transient(root)
        potion_window.grab_set()

    def upgrade_armor():
        if char.is_alive():
            try:
                msg = char.upgrade_item(char.get_equipped_armor())
                update_output(msg)
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} is dead!")

    def upgrade_weapon():
        if char.is_alive():
            try:
                msg = char.upgrade_item(char.get_equipped_weapon())
                update_output(msg)
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} is dead!")

    def open_sell_window(player):
        sell_window = tk.Toplevel(root)
        sell_window.title("Sell Items")
        sell_window.geometry("300x400")
        sell_window.configure(bg="#1c1c28")

        ttk.Label(sell_window, text="Select items to sell:", style="Header.TLabel").pack(pady=10)
        listbox = tk.Listbox(sell_window, selectmode=tk.MULTIPLE, width=50, height=12,
                             bg="#2b2b3b", fg="#fafafa", selectbackground="#444466")
        listbox.pack(padx=10, pady=5)

        inventory = player.get_inventory()
        for i, item in enumerate(inventory):
            listbox.insert(i, f"{item.get_name()} (Value: {item.get_value()}g)")

        def sell_selected_items():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showinfo("Info", "No items selected.")
                return
            total_gold = 0
            sold_items = []
            for idx in reversed(selected_indices):
                item = inventory[idx]
                try:
                    player.sell_item(item)
                    total_gold += item.get_value()
                    sold_items.append(item.get_name())
                    listbox.delete(idx)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
            update_player_status()
            messagebox.showinfo(
                "Items Sold",
                f"Sold {len(sold_items)} item(s) for {total_gold} gold.\nCurrent Gold: {player.get_gold()}"
            )

        ttk.Button(sell_window, text="Sell Selected", command=sell_selected_items).pack(pady=10)
        ttk.Button(sell_window, text="Close", command=sell_window.destroy).pack()
        sell_window.grab_set()

    def open_buy_potion_window(player):
        buy_window = tk.Toplevel(root)
        buy_window.title("Buy Potion")
        buy_window.geometry("300x300")
        buy_window.configure(bg="#1c1c28")

        ttk.Label(buy_window, text="Choose a potion to buy:", style="Header.TLabel").pack(pady=10)

        potions_available = [
            Potion(PotionType.HEALTH, 1),
            Potion(PotionType.HEALTH, 2),
            Potion(PotionType.HEALTH, 3),
            Potion(PotionType.STAMINA, 1),
            Potion(PotionType.STAMINA, 2),
            Potion(PotionType.STAMINA, 3)
        ]

        listbox = tk.Listbox(buy_window, height=6, width=40, bg="#2b2b3b", fg="#fafafa", selectbackground="#444466")
        for i, potion in enumerate(potions_available):
            listbox.insert(tk.END, f"{potion.get_name()} (Lv {potion.get_potionlevel()}) - {potion.get_value()}g")
        listbox.pack(pady=5)

        def buy_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Select a potion before buying.")
                return
            potion = potions_available[selection[0]]
            if player.get_gold() < potion.get_value():
                messagebox.showerror("Error", "Not enough gold!")
                return
            player.add_to_inventory(potion)
            player.equip_item(potion)
            player.spend_gold(potion.get_value())
            update_player_status()
            messagebox.showinfo("Purchase", f"You bought {potion.get_name()}!")

        ttk.Button(buy_window, text="Buy", command=buy_selected).pack(pady=5)
        ttk.Button(buy_window, text="Cancel", command=buy_window.destroy).pack()
        buy_window.transient(root)
        buy_window.grab_set()

    # Layout frames
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=0)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=0)

    # Player status - Left
    left_frame = ttk.Frame(root, padding=10, width=280, height=450)
    left_frame.grid(row=0, column=0, sticky="nsew")
    left_frame.grid_propagate(False)
    ttk.Label(left_frame, text="Player", style="Header.TLabel").pack(anchor="w", pady=5)
    player_status = tk.Text(left_frame, height=24, width=34, bg="#2b2b3b", fg="#fafafa", font=("Consolas", 11))
    player_status.pack(fill="both", expand=True)

    # Monster status - Right
    right_frame = ttk.Frame(root, padding=10, width=280, height=450)
    right_frame.grid(row=0, column=2, sticky="nsew")
    right_frame.grid_propagate(False)
    ttk.Label(right_frame, text="Monster", style="Header.TLabel").pack(anchor="w", pady=5)
    monster_status = tk.Text(right_frame, height=24, width=32, bg="#2b2b3b", fg="#fafafa", font=("Consolas", 11))
    monster_status.pack(fill="both", expand=True)

    # Battle log - Center
    center_frame = ttk.Frame(root, padding=10)
    center_frame.grid(row=0, column=1, sticky="nsew")
    center_frame.grid_propagate(False)
    ttk.Label(center_frame, text="Battle Log", style="Header.TLabel").pack(anchor="w", pady=5)
    output_box = tk.Text(center_frame, height=24, width=72, bg="#2b2b3b", fg="#fafafa", font=("Consolas", 11))
    output_box.pack(fill="both", expand=True)

    # Action buttons - Bottom
    actions_frame = ttk.Frame(root, padding=10, style="TFrame")
    actions_frame.grid(row=1, column=0, columnspan=4, sticky="ew")

    # Make three columns expand equally
    for i in range(3):
        actions_frame.columnconfigure(i, weight=1)

    def add_button_group(frame, buttons):
        for label, cmd in buttons:
            ttk.Button(frame, text=label, command=cmd).pack(padx=3, pady=3, fill="x")

    # Combat buttons
    combat_frame = ttk.Frame(actions_frame, style="TFrame")
    combat_frame.grid(row=0, column=0, sticky="nsew", padx=5)
    add_button_group(combat_frame, [
        ("Attack", attack),
        ("Use Potion", use_potion),
        ("New Monster", choose_monster)
    ])

    # Equipment buttons
    equipment_frame = ttk.Frame(actions_frame, style="TFrame")
    equipment_frame.grid(row=0, column=1, sticky="nsew", padx=5)
    add_button_group(equipment_frame, [
        ("Upgrade Armor", upgrade_armor),
        ("Upgrade Weapon", upgrade_weapon),
        ("Sell Items", lambda: open_sell_window(char)),
        ("Buy Potion", lambda: open_buy_potion_window(char))
    ])

    # Economy buttons
    economy_frame = ttk.Frame(actions_frame, style="TFrame")
    economy_frame.grid(row=0, column=2, sticky="nsew", padx=5)
    add_button_group(economy_frame, [
        ("Save Game", lambda: save_game(char, os.path.join(SAVE_DIR, f"{char.get_name()}.json"))),
    ])

    # Ensure frames expand vertically too
    for frame in (combat_frame, equipment_frame, economy_frame):
        frame.rowconfigure(0, weight=1)

    # Initial update
    update_player_status()
    update_monster_status()

    root.mainloop()
