from simple_rpg.character import Character
from simple_rpg.monsters import Plant, Monster
from simple_rpg.items.potions import Potion, PotionType


def battle(char: Character, monster: Monster):
    print(f"\nA wild {monster.get_name()} appears!\n")

    while char.is_alive() and monster.is_alive():
        print(f"\n{char.get_name()} HP: {char.get_health()} | {monster.get_name()} HP: {monster.get_health()}")
        action = input("What do you want to do? (a: attack, p: use potion): ").strip().lower()

        if action == 'a':
            try:
                result = char.attack_target(monster)
                print(result)
            except Exception as e:
                print(f"Error during attack: {e}")
                continue

        elif action == 'p':
            potions = char.get_equipped_potions()
            if not potions:
                print("No potions equipped!")
                continue

            print("Available Potions:")
            for i, potion in enumerate(potions, start=1):
                print(f"{i}. {potion.get_name()}")

            try:
                choice = int(input("Which potion do you want to use? (number): "))
                if 1 <= choice <= len(potions):
                    print(char.use_potion(potions[choice - 1]))
                else:
                    print("Invalid choice.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid number.")
                continue

        else:
            print("Invalid action. Choose 'a' to attack or 'p' to use a potion.")
            continue

        if monster.is_alive():
            try:
                print(monster.attack_target(char))
            except Exception as e:
                print(f"Error during monster attack: {e}")
                continue

    # Battle result
    if char.is_alive():
        item = monster.drop_item()
        xp = monster.get_xp_gain()
        char.add_to_inventory(item)
        char.gain_xp(xp)

        print(f"\nYou defeated {monster.get_name()}!")
        print(f"XP received: {xp}")
        print("Item received:")
        print(item)
    else:
        print("\nYou died.")


# --------------------------
# Setup
# --------------------------
char = Character("Lucas")
char.add_to_inventory(Potion(PotionType.HEALTH, 1))
char.add_to_inventory(Potion(PotionType.HEALTH, 1))

# Equip a potion
char.equip_item(Potion(PotionType.HEALTH, 1))

# Create a monster
monster = Plant(level=2)

# Start battle
battle(char, monster)

# Final character state
print("\nFinal Character State:")
print(char)
