# load.py

import json
from simple_rpg.items.item import Item
from simple_rpg.items.potions import Potion
from simple_rpg.items.sword import Sword
from simple_rpg.items.armor import Armor
# import your other item classes here

# Map item "type" string to class for loading
ITEM_CLASSES = {
    "Item": Item,
    "Potion": Potion,
    "Sword": Sword,
    "Armor": Armor,
    # add more item classes as you create them
}

def item_from_dict(data):
    """
    Factory function to load an item from a dictionary.
    Uses the 'type' field to decide which class to instantiate.
    """
    item_type = data.get("type")
    if not item_type:
        raise ValueError("Missing 'type' in item data")

    cls = ITEM_CLASSES.get(item_type)
    if cls is None:
        raise ValueError(f"Unknown item type: {item_type}")

    return cls.from_dict(data)


def save_game(character, filename):
    """
    Save character data (including inventory, equipment) to a JSON file.
    The character must have a to_dict() method.
    """
    with open(filename, "w") as f:
        json.dump(character.to_dict(), f, indent=4)
    print(f"Game saved to {filename}")


def load_game(filename, character_class):
    """
    Load character data from a JSON file and return a Character instance.
    The character_class argument is the Character class to instantiate.
    The Character.from_dict() method should call item_from_dict for items.
    """
    with open(filename, "r") as f:
        data = json.load(f)
    print
    character = character_class.from_dict(data)
    return character


# -- Example usage --

if __name__ == "__main__":
    from simple_rpg.character import Character  # your character class

    # Load saved game
    try:
        hero = load_game("savefile.json", Character)
        print("Character loaded:", hero)
    except Exception as e:
        print("Failed to load game:", e)
