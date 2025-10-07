import unittest
from simple_rpg.monsters.monster import Monster, MonsterLevel
from simple_rpg.entity import Entity

# --- Concrete Test Monster subclass ---
class ConcreteMonster(Monster):
    def drop_item(self):
        return "test_item"
    def get_drops(self):
        return ["test_item"]

# --- Unit Tests ---
class TestMonsterClass(unittest.TestCase):

    def setUp(self):
        self.monster = ConcreteMonster(
            name="Goblin",
            level=3,
            base_attack=12,
            base_armor=4,
            base_max_health=100,
            base_max_stamina=80
        )

    def test_initialization(self):
        self.assertEqual(self.monster.get_name(), "Strong Goblin")
        self.assertEqual(self.monster.get_level(), 3)
        self.assertEqual(self.monster.get_attack(), 12 + (3 - 1) * 3)
        self.assertEqual(self.monster.get_armor(), 4 + (3 - 1) * 2)
        self.assertEqual(self.monster.get_max_health(), 100 + int((3 - 1) ** 1.5 * 5))
        self.assertEqual(self.monster.get_max_stamina(), 80 + (3 - 1) * 5)

    def test_invalid_level_raises(self):
        with self.assertRaises(TypeError):
            ConcreteMonster(
                name="InvalidGoblin",
                level=0,  # invalid level
                base_attack=10,
                base_armor=3,
                base_max_health=100,
                base_max_stamina=80
            )

        with self.assertRaises(TypeError):
            ConcreteMonster(
                name="InvalidGoblin",
                level=6,  # too high
                base_attack=10,
                base_armor=3,
                base_max_health=100,
                base_max_stamina=80
            )

    def test_xp_gain(self):
        expected_xp = int(50 * MonsterLevel.LEVEL_3.multiplier)  # 50 * 1.5 = 75
        self.assertEqual(self.monster.get_xp_gain(), expected_xp)

    def test_get_strength(self):
        self.assertEqual(self.monster.get_strength(), MonsterLevel.LEVEL_3)

    def test_str_representation(self):
        s = str(self.monster)
        self.assertIn("Strong Goblin", s)
        self.assertIn("XP on defeat", s)
        self.assertIn("Health", s)
        self.assertIn("Stamina", s)
        self.assertIn("Attack", s)
        self.assertIn("Armor", s)

    def test_repr_representation(self):
        r = repr(self.monster)
        self.assertIn("ConcreteMonster(name='Strong Goblin'", r)
        self.assertIn("level=3", r)
        self.assertIn("xp_gain=", r)

    def test_drop_item(self):
        self.assertEqual(self.monster.drop_item(), "test_item")


if __name__ == "__main__":
    unittest.main()
