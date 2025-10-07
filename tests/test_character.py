import unittest
from simple_rpg.character import Character
from simple_rpg.items.potions import Potion, PotionType
from simple_rpg.items.sword import Sword
from simple_rpg.items.armor import Armor
from simple_rpg.items.item import Item


class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.char = Character("Hero")

    def test_initial_values(self):
        self.assertEqual(self.char.get_name(), "Hero")
        self.assertEqual(self.char.get_level(), 1)
        self.assertEqual(self.char.get_health(), 100)
        self.assertEqual(self.char.get_stamina(), 100)
        self.assertEqual(self.char.get_gold(), 100)

    def test_equip_weapon(self):
        sword = Sword(1, 1)
        self.char._inventory.append(sword)
        self.char.equip_item(sword)
        self.assertEqual(self.char.get_equipped_weapon(), sword)

    def test_equip_armor(self):
        armor = Armor(1, 1)
        self.char._inventory.append(armor)
        self.char.equip_item(armor)
        self.assertEqual(self.char.get_equipped_armor(), armor)

    def test_equip_potion(self):
        potion = Potion(PotionType.HEALTH, 1)
        self.char._inventory.append(potion)
        self.char.equip_item(potion)
        self.assertIn(potion, self.char._equipped.get('potions'))

    def test_equip_invalid_item(self):
        class FakeItem:
            pass
        with self.assertRaises(ValueError):
            self.char.equip_item(FakeItem())

    def test_equip_not_in_inventory(self):
        sword = Sword(1, 1)
        with self.assertRaises(ValueError):
            self.char.equip_item(sword)

    def test_use_potion_health(self):
        potion = Potion(PotionType.HEALTH, 1)
        self.char._equipped.setdefault('potions', []).append(potion)
        self.char.take_damage(50)
        self.char.use_potion(potion)
        self.assertGreater(self.char.get_health(), 50)
        self.assertNotIn(potion, self.char._equipped['potions'])

    def test_use_potion_not_equipped(self):
        potion = Potion(PotionType.HEALTH, 1)
        with self.assertRaises(ValueError):
            self.char.use_potion(potion)

    def test_upgrade_item_in_inventory(self):
        sword = Sword(1, 1)
        self.char._inventory.append(sword)
        self.char.upgrade_item(sword)
        self.assertEqual(sword.get_level(), 2)

    def test_upgrade_item_equipped(self):
        sword = Sword(1, 1)
        self.char._inventory.append(sword)
        self.char.equip_item(sword)
        self.char.upgrade_item(sword)
        self.assertEqual(sword.get_level(), 2)

    def test_upgrade_item_insufficient_gold(self):
        sword = Sword(1, 1)
        sword._level = 9
        self.char._inventory.append(sword)
        self.char._gold = 0
        with self.assertRaises(ValueError):
            self.char.upgrade_item(sword)

    def test_upgrade_item_not_upgradable(self):
        class Dummy(Item):
            def __init__(self):
                super().__init__("Dummy", "Not upgradable", 0)

        dummy = Dummy()
        self.char._inventory.append(dummy)
        with self.assertRaises(ValueError):
            self.char.upgrade_item(dummy)

    def test_spend_gold(self):
        self.char.spend_gold(50)
        self.assertEqual(self.char.get_gold(), 50)

    def test_spend_too_much_gold(self):
        with self.assertRaises(ValueError):
            self.char.spend_gold(999)

    def test_gain_xp_and_level_up(self):
        self.char.gain_xp(150)  # Should be enough to level up at least once
        self.assertGreaterEqual(self.char.get_level(), 2)

    def test_get_attack_stamina_cost_without_weapon(self):
        cost = self.char.get_attack_stamina_cost()
        self.assertEqual(cost, 15)

    def test_get_attack_stamina_cost_with_weapon(self):
        sword = Sword(2, 1)
        self.char._inventory.append(sword)
        self.char.equip_item(sword)
        cost = self.char.get_attack_stamina_cost()
        self.assertGreater(cost, 10)

    def test_str_contains_all_info(self):
        s = str(self.char)
        self.assertIn("Gold", s)
        self.assertIn("XP", s)
        self.assertIn("Inventory", s)
        self.assertIn("Equipped Weapon", s)
        self.assertIn("Equipped Armor", s)

    def test_repr_format(self):
        r = repr(self.char)
        self.assertIn("Character(name=", r)
        self.assertIn("level=", r)
        self.assertIn("health=", r)
        self.assertIn("stamina=", r)


if __name__ == '__main__':
    unittest.main()
