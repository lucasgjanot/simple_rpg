import unittest
from simple_rpg.armor import Armor, ArmorLevel, ArmorMaterial


class TestArmor(unittest.TestCase):

    def setUp(self):
        self.armor = Armor(level=1, material_level=1)

    def test_initialization(self):
        self.assertEqual(self.armor.get_level(), 1)
        self.assertEqual(self.armor.get_material_level(), 1)
        self.assertEqual(self.armor.get_armor(), 1 * 10 + 1 * 5)
        self.assertEqual(self.armor.get_value(), 50 + 20 * 1 + 30 * 1)
        self.assertIn("Armor", self.armor.get_name())

    def test_calculate_armor(self):
        self.assertEqual(Armor.calculate_armor(3, 2), 3 * 10 + 2 * 5)

    def test_calculate_value(self):
        expected_value = 50 + 20 * 4 + 30 * 3
        self.assertEqual(Armor.calculate_value(4, 3), expected_value)

    def test_upgrade_level_only(self):
        initial_armor = self.armor.get_armor()
        self.armor.upgrade()
        self.assertEqual(self.armor.get_level(), 2)
        self.assertEqual(self.armor.get_material_level(), 1)
        self.assertGreater(self.armor.get_armor(), initial_armor)

    def test_upgrade_material_level(self):
        armor = Armor(level=10, material_level=1)
        armor.upgrade()  # Should go to material_level 2 and reset level to 1
        self.assertEqual(armor.get_level(), 1)
        self.assertEqual(armor.get_material_level(), 2)

    def test_upgrade_cost_level(self):
        cost = self.armor.get_upgrade_cost()
        self.assertEqual(cost, ArmorLevel.from_level(1).upgrade_cost)

    def test_upgrade_cost_material(self):
        armor = Armor(level=10, material_level=1)
        armor.upgrade()  # Level becomes 1, material_level becomes 2
        cost = armor.get_upgrade_cost()
        self.assertEqual(cost, ArmorLevel.from_level(1).upgrade_cost)

    def test_upgrade_at_max(self):
        armor = Armor(level=10, material_level=5)
        with self.assertRaises(ValueError):
            armor.upgrade()

    def test_invalid_armor_level_from_enum(self):
        with self.assertRaises(ValueError):
            ArmorLevel.from_level(11)

    def test_invalid_armor_material_from_enum(self):
        with self.assertRaises(ValueError):
            ArmorMaterial.from_level(0)

    def test_str_output(self):
        output = str(self.armor)
        self.assertIn("Basic", output)
        self.assertIn("Leather", output)
        self.assertIn("Armor", output)
        self.assertIn("Description", output)
        self.assertIn("gold", output)

    def test_repr_output(self):
        output = repr(self.armor)
        self.assertIn("Armor", output)
        self.assertIn("level=1", output)
        self.assertIn("material_level=1", output)
        self.assertIn("armor=", output)
        self.assertIn("value=", output)


if __name__ == '__main__':
    unittest.main()
