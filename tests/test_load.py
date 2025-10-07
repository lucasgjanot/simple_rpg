import unittest
import tempfile
import os
import json

from simple_rpg.items.potions import Potion, PotionLevel, PotionType
from simple_rpg.items.sword import Sword
from simple_rpg.items.armor import Armor
from simple_rpg.character import Character
from simple_rpg.load import item_from_dict, save_game, load_game

class TestLoadModule(unittest.TestCase):

    def test_item_from_dict_known_types(self):
        potion_data = {
        "type": "Potion",
        "name": "Small Health Potion",
        "description": "Restores 20 HP",
        "value": 30,
        "potiontype": "Health",
        "potionlevel": "1"
    }


        potion = item_from_dict(potion_data)
        self.assertIsInstance(potion, Potion)
        self.assertEqual(potion.get_potiontype().type, "Health")
        self.assertEqual(potion.get_potionlevel(), "1")

    def test_item_from_dict_unknown_type_raises(self):
        bad_data = {
            "type": "NonExistentType",
            "name": "Fake",
            "description": "None",
            "value": 0
        }
        with self.assertRaises(ValueError):
            item_from_dict(bad_data)

    def test_item_from_dict_missing_type_raises(self):
        bad_data = {
            "name": "MissingType",
            "description": "No type key",
            "value": 0
        }
        with self.assertRaises(ValueError):
            item_from_dict(bad_data)

    def test_save_and_load_game(self):
        char = Character("TestHero")
        char.add_to_inventory(Sword(1, 1))
        char.add_to_inventory(Potion(PotionType.HEALTH, 1))
        char.add_to_inventory(Armor(1, 1))
        char.equip_item(char._inventory[0])  # Equip sword

        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix=".json") as tmp:
            tmp_name = tmp.name
            save_game(char, tmp_name)
            tmp.seek(0)
            saved_data = json.load(tmp)
            self.assertIn("name", saved_data)
            self.assertIn("inventory", saved_data)
        
        # Load it back
        loaded_char = load_game(tmp_name, Character)
        self.assertIsInstance(loaded_char, Character)
        self.assertEqual(loaded_char.get_name(), "TestHero")
        self.assertEqual(len(loaded_char._inventory), 2)  # one was equipped
        self.assertEqual(loaded_char.get_equipped_weapon().get_level(), 1)

        os.remove(tmp_name)


if __name__ == "__main__":
    unittest.main()
