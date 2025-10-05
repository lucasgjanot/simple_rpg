import unittest
from simple_rpg.monster import Monster
from simple_rpg.entity import Entity
from simple_rpg.item import Item
from unittest.mock import MagicMock
import random


class ConcreteMonster(Monster):
    def drop_item(self):
        # Simulate item drop logic
        return MagicMock(spec=Item, name="FakeItem")


class MonsterTests(unittest.TestCase):

    def setUp(self):
        self.monster = ConcreteMonster(
            name="Test Goblin",
            level=3,
            base_attack=15,
            base_armor=5,
            base_max_health=80,
            base_max_stamina=50,
            xp_gain=150
        )

    def test_monster_initialization(self):
        self.assertEqual(self.monster.get_name(), "Test Goblin")
        self.assertEqual(self.monster.get_level(), 3)
        self.assertEqual(self.monster.get_attack(), 15 + (3 - 1) * 3)
        self.assertEqual(self.monster.get_armor(), 5 + (3 - 1) * 2)
        self.assertEqual(self.monster.get_health(), self.monster.get_max_health())
        self.assertEqual(self.monster.get_stamina(), self.monster.get_max_stamina())
        self.assertEqual(self.monster.get_xp_gain(), 150)

    def test_drop_item_returns_item(self):
        item = self.monster.drop_item()
        self.assertIsInstance(item, Item)

    def test_str_output(self):
        string_output = str(self.monster)
        self.assertIn("Test Goblin", string_output)
        self.assertIn("XP on defeat", string_output)

    def test_repr_output(self):
        repr_output = repr(self.monster)
        self.assertIn("ConcreteMonster", repr_output)
        self.assertIn("name='Test Goblin'", repr_output)
        self.assertIn("xp_gain=150", repr_output)

    def test_monster_is_alive(self):
        self.assertTrue(self.monster.is_alive())
        self.monster.take_damage(1000)  # Overkill
        self.assertFalse(self.monster.is_alive())

    def test_monster_take_damage_reduces_health(self):
        health_before = self.monster.get_health()
        self.monster.take_damage(10)
        self.assertLess(self.monster.get_health(), health_before)

    def test_monster_restore_health_and_stamina(self):
        self.monster.take_damage(30)
        self.monster.use_stamina(20)

        current_health = self.monster.get_health()
        current_stamina = self.monster.get_stamina()

        self.monster.restore_health(10)
        self.monster.restore_stamina(10)

        self.assertEqual(self.monster.get_health(), min(current_health + 10, self.monster.get_max_health()))
        self.assertEqual(self.monster.get_stamina(), min(current_stamina + 10, self.monster.get_max_stamina()))


if __name__ == '__main__':
    unittest.main()
