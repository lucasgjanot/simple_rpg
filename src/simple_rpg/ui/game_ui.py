import tkinter as tk
from tkinter import messagebox
import os
import json

from simple_rpg.character import Character
from simple_rpg.monsters import Dragon, Plant
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
    else:
        char = load_game(filename, Character)

    root = tk.Tk()
    root.title(f"Simple RPG - {char.get_name()}")
    root.geometry("1000x400")

    # ============================================================
    # Function: Choose Monster
    # ============================================================
    def choose_monster():
        def confirm_choice():
            global current_monster

            monster_type = monster_var.get()
            level = int(level_var.get())

            # Create monster based on user choice
            if monster_type == "Dragão":
                current_monster = Dragon(level)
            elif monster_type == "Planta":
                current_monster = Plant(level)
            else:
                messagebox.showerror("Erro", "Tipo de monstro inválido.")
                return

            update_output(f"Novo monstro criado: {current_monster.get_name()} (Nível {level})")
            update_monster_status()
            monster_window.destroy()

        # Popup window
        monster_window = tk.Toplevel(root)
        monster_window.title("Escolher Monstro")
        monster_window.geometry("300x200")

        tk.Label(monster_window, text="Tipo de Monstro:").pack(pady=5)
        monster_var = tk.StringVar(monster_window)
        monster_var.set("Dragão")  # default
        tk.OptionMenu(monster_window, monster_var, "Dragão", "Planta").pack()

        tk.Label(monster_window, text="Nível do Monstro:").pack(pady=5)
        level_var = tk.StringVar(monster_window)
        level_var.set("1")  # default
        tk.OptionMenu(monster_window, level_var, *[str(i) for i in range(1, 11)]).pack()

        tk.Button(monster_window, text="Confirmar", command=confirm_choice).pack(pady=10)
        tk.Button(monster_window, text="Cancelar", command=monster_window.destroy).pack()

        monster_window.transient(root)
        monster_window.grab_set()

    # ============================================================
    # Function: Attack
    # ============================================================
    def attack():
        if not char.is_alive():
            update_output(f"{char.get_name()} está morto!")
            return

        if not current_monster:
            update_output("Nenhum monstro selecionado.")
            return

        if not current_monster.is_alive():
            update_output("Monstro já derrotado.")
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
            char.gain_xp(current_monster.get_xp_gain())
            item = current_monster.drop_item()
            char.add_to_inventory(item)
            update_output(f"Você derrotou {current_monster.get_name()}! Ganhou item: {item.get_name()}")

        update_player_status()
        update_monster_status()

    # ============================================================
    # Function: Use Potion
    # ============================================================
    def use_potion():
        if not char.is_alive():
            update_output(f"{char.get_name()} está morto!")
            return

        potions = char.get_equipped_potions()
        if not potions:
            update_output("Nenhuma poção equipada.")
            return

        potion_window = tk.Toplevel(root)
        potion_window.title("Escolha uma Poção")
        potion_window.geometry("300x200")
        tk.Label(potion_window, text="Selecione a poção que deseja usar:").pack(pady=5)

        listbox = tk.Listbox(potion_window, height=6, width=40)
        for i, potion in enumerate(potions):
            listbox.insert(tk.END, f"{i + 1}. {potion.get_name()} (Nv {potion.get_potionlevel()})")
        listbox.pack(pady=5)

        def confirm_potion():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione uma poção antes de confirmar.")
                return
            index = selection[0]
            potion = potions[index]
            try:
                msg = char.use_potion(potion)
                update_output(msg)
            except Exception as e:
                update_output(str(e))
            update_player_status()
            potion_window.destroy()

        tk.Button(potion_window, text="Usar", command=confirm_potion).pack(pady=5)
        tk.Button(potion_window, text="Cancelar", command=potion_window.destroy).pack()

        potion_window.transient(root)
        potion_window.grab_set()

    # ============================================================
    # Upgrade functions
    # ============================================================
    def upgrade_armor():
        if char.is_alive():
            try:
                char.upgrade_item(char.get_equipped_armor())
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} está morto!")

    def upgrade_weapon():
        if char.is_alive():
            try:
                char.upgrade_item(char.get_equipped_weapon())
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} está morto!")

    def open_sell_window(player):
        sell_window = tk.Toplevel()
        sell_window.title("Sell Items")

        tk.Label(sell_window, text="Select items to sell:").pack(pady=5)

        # Listbox com múltipla seleção
        listbox = tk.Listbox(sell_window, selectmode=tk.MULTIPLE, width=40, height=10)
        listbox.pack(padx=10, pady=5)

        inventory = player.get_inventory()

        # Preenche o inventário com nome + valor
        for i, item in enumerate(inventory):
            listbox.insert(i, f"{item.get_name()} (Value: {item.get_value()}g)")

        def sell_selected_items():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showinfo("Info", "No items selected.")
                return

            total_gold = 0
            sold_items = []

            for idx in reversed(selected_indices):  # reversed para evitar índice quebrado ao remover
                item = inventory[idx]
                try:
                    player.sell_item(item)
                    total_gold += item.get_value()
                    sold_items.append(item.get_name())
                    listbox.delete(idx)
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

            messagebox.showinfo(
                "Items Sold",
                f"Sold {len(sold_items)} item(s) for {total_gold} gold.\n"
                f"Current Gold: {player.get_gold()}"
            )

        sell_button = tk.Button(sell_window, text="Sell Selected", command=sell_selected_items)
        sell_button.pack(pady=10)

        close_button = tk.Button(sell_window, text="Close", command=sell_window.destroy)
        close_button.pack()

        sell_window.grab_set()






    # ============================================================
    # UI Helpers
    # ============================================================
    def update_output(msg):
        output_box.config(state="normal")
        output_box.insert(tk.END, msg + "\n")
        output_box.see(tk.END)
        output_box.config(state="disabled")

    def update_player_status():
        status_label.config(text=str(char))

    def update_monster_status():
        battle_label.config(text=str(current_monster) if current_monster else "Nenhum monstro")

    # ============================================================
    # UI Layout
    # ============================================================
    status_label = tk.Label(root, text="")
    status_label.pack(side="left")

    battle_label = tk.Label(root, text="Nenhum monstro")
    battle_label.pack()

    tk.Button(root, text="Atacar", command=attack).pack(fill="x")
    tk.Button(root, text="Usar Poção", command=use_potion).pack(fill="x")
    tk.Button(root, text="Melhorar Armadura", command=upgrade_armor).pack(fill="x")
    tk.Button(root, text="Melhorar Arma", command=upgrade_weapon).pack(fill="x")
    tk.Button(root, text="Novo Monstro", command=choose_monster).pack(fill="x")
    tk.Button(root, text="Salvar Jogo", command=save_game).pack(fill="x")
    tk.Button(root, text="Sell Items", command=lambda: open_sell_window(char)).pack(fill="x")

    output_box = tk.Text(root, height=100, width=500, state="disabled")
    output_box.pack(pady=5)

    update_player_status()
    update_monster_status()
    root.mainloop()
