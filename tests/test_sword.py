import unittest
from simple_rpg.sword import Sword

class TestSword(unittest.TestCase):

    def setUp(self):
        self.sword = Sword(level=1, material_level=1)

    def test_initialization(self):
        self.assertEqual(self.sword.get_level(), 1)
        self.assertEqual(self.sword.get_material_level(), 1)
        self.assertEqual(self.sword.get_name(), "Basic Wood Sword")
        self.assertEqual(self.sword.get_description(), "Swords are for stabbing or slashing a target")

    def test_invalid_initialization_level(self):
        with self.assertRaises(ValueError):
            Sword(level=0, material_level=1)
        with self.assertRaises(ValueError):
            Sword(level=11, material_level=1)

    def test_invalid_initialization_material_level(self):
        with self.assertRaises(ValueError):
            Sword(level=1, material_level=0)
        with self.assertRaises(ValueError):
            Sword(level=1, material_level=6)

    def test_upgrade_increases_level(self):
        self.sword._level = 1
        self.sword._material_level = 1
        self.sword.upgrade()
        self.assertEqual(self.sword.get_level(), 2)
        self.assertEqual(self.sword.get_material_level(), 1)

    def test_upgrade_resets_level_and_increases_material_level(self):
        # Set level to max
        self.sword._level = Sword.MAX_LEVEL
        self.sword._material_level = 1
        self.sword.upgrade()
        self.assertEqual(self.sword.get_level(), 1)
        self.assertEqual(self.sword.get_material_level(), 2)

    def test_upgrade_max_raises(self):
        self.sword._level = Sword.MAX_LEVEL
        self.sword._material_level = Sword.MAX_MATERIAL_LEVEL
        with self.assertRaises(ValueError):
            self.sword.upgrade()

    def test_damage_calculation(self):
        expected_damage = self.sword.calculate_damage(self.sword.get_level(), self.sword.get_material_level())
        self.assertEqual(self.sword.get_damage(), expected_damage)

    def test_value_calculation(self):
        expected_value = self.sword.calculate_value(self.sword.get_level(), self.sword.get_material_level())
        self.assertEqual(self.sword.get_value(), expected_value)

    def test_str_contains_expected_info(self):
        s = str(self.sword)
        self.assertIn("Basic", s)
        self.assertIn("Wood", s)
        self.assertIn("Sword", s)
        self.assertIn("Description", s)
        self.assertIn("Level: 1", s)
        self.assertIn("Material Level: 1", s)
        self.assertIn("Damage", s)
        self.assertIn("Value", s)

    def test_repr_contains_expected_info(self):
        r = repr(self.sword)
        self.assertIn("Sword(", r)
        self.assertIn("level=1", r)
        self.assertIn("material_level=1", r)
        self.assertIn("damage=", r)
        self.assertIn("value=", r)


if __name__ == "__main__":
    unittest.main()
