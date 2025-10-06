import unittest
from simple_rpg.monsters.monster import Monster, MonsterLevel

class ConcreteMonster(Monster):
    def drop_item(self):
        return "Test Loot"


class TestMonster(unittest.TestCase):

    def setUp(self):
        self.monster = ConcreteMonster(
            name="Goblin",
            level=3,
            base_attack=10,
            base_armor=5,
            base_max_health=30,
            base_max_stamina=20
        )

    def test_name_formatting(self):
        self.assertEqual(self.monster.get_name(), "Strong Goblin")

    def test_level_and_strength(self):
        self.assertEqual(self.monster.get_level(), 3)
        self.assertEqual(self.monster.get_strength(), MonsterLevel.LEVEL_3)
        self.assertEqual(self.monster.get_strength().description, "Strong")
        self.assertEqual(self.monster.get_strength().multiplier, 1.5)

    def test_xp_gain_calculation(self):
        expected_xp = int(50 * 1.5) 
        self.assertEqual(self.monster.get_xp_gain(), expected_xp)

    def test_drop_item(self):
        self.assertEqual(self.monster.drop_item(), "Test Loot")

    def test_invalid_level_too_high(self):
        with self.assertRaises(TypeError):
            ConcreteMonster("Orc", 6, 12, 4, 40, 25)

    def test_invalid_level_too_low(self):
        with self.assertRaises(TypeError):
            ConcreteMonster("Orc", 0, 12, 4, 40, 25)

    def test_str_contains_key_info(self):
        result = str(self.monster)
        self.assertIn("Strong Goblin", result)
        self.assertIn("Level 3", result)
        self.assertIn("XP on defeat", result)

    def test_repr_contains_all_info(self):
        result = repr(self.monster)
        self.assertIn("ConcreteMonster", result)
        self.assertIn("level=3", result)
        self.assertIn("xp_gain=75", result)


if __name__ == '__main__':
    unittest.main()
