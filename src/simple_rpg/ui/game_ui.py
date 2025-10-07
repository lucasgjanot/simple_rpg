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
current_monster = Dragon(1)
char = None

def start_game_ui(player_name, new_game=False, filename=None):
    global char, current_monster

    if new_game:
        char = Character(player_name)
        initial_items = [
            Potion(PotionType.HEALTH, 1),
            Potion(PotionType.STAMINA, 1),
            Sword(1,1),
            Armor(1,1)
        ]
        
        for item in initial_items:
            char.add_to_inventory(item)
            char.equip_item(item)
    else:
        char = load_game(filename,Character)

    root = tk.Tk()
    root.title(f"Simple RPG - {char.get_name()}")

    def choose_monster():
        if current_monster:
            battle_label.config(text=str(current_monster))
        else:
            battle_label.config(text="Nenhum monstro selecionado.")

    def attack():
        if char.is_alive():
            if not current_monster:
                update_output("Nenhum monstro selecionado.")
                return
            if not current_monster.is_alive():
                update_output("Monstro já derrotado")
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
        else: 
            update_output(f"{char.get_name()} is dead!")
        update_player_status()

    def use_potion():
        if char.is_alive():
            potions = char.get_equipped_potions()
            if not potions:
                update_output("Nenhuma poção equipada.")
                return
            try:
                update_output(char.use_potion(potions[0]))
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} is dead!")
        
    def upgrade_armor():
        if char.is_alive():
            try:
                char.upgrade_item(char.get_equipped_armor())
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} is dead!")

    def upgrade_weapon():
        if char.is_alive():
            try:
                char.upgrade_item(char.get_equipped_weapon())
            except Exception as e:
                update_output(str(e))
            update_player_status()
        else:
            update_output(f"{char.get_name()} is dead!")

    def update_output(msg):
        output_box.config(state="normal")
        output_box.insert(tk.END, msg + "\n")
        output_box.see(tk.END)
        output_box.config(state="disabled")
    
    def update_player_status():
        status_label.config(text=str(char))

    # Widgets
    status_label = tk.Label(root, text="")
    status_label.pack(side="left")
    root.geometry("1000x400")
    battle_label = tk.Label(root, text="Nenhum monstro")
    battle_label.pack()

    tk.Button(root, text="Atacar", command=attack).pack(fill='x')
    tk.Button(root, text="Usar Poção", command=use_potion).pack(fill='x')
    tk.Button(root, text="Melhorar Armadura", command=upgrade_armor).pack(fill='x')
    tk.Button(root, text="Melhorar Arma", command=upgrade_weapon).pack(fill='x')
    tk.Button(root, text="Novo Monstro", command=choose_monster).pack(fill='x')
    tk.Button(root, text="Salvar Jogo", command=save_game).pack(fill='x')

    output_box = tk.Text(root, height=100, width=500, state="disabled")
    output_box.pack(pady=5)

    choose_monster()
    update_player_status()
    root.mainloop()
