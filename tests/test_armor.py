import unittest
from simple_rpg.items.armor import Armor, ArmorLevel, ArmorMaterial

class TestArmor(unittest.TestCase):

    def test_initialization(self):
        armor = Armor(1, 1)
        self.assertEqual(armor.get_level(), 1)
        self.assertEqual(armor.get_material_level(), 1)
        self.assertEqual(armor.get_armor(), 20)  # 1*10 + 1*10
        self.assertEqual(armor.get_value(), 50 + 20 + 30)

    def test_upgrade_level(self):
        armor = Armor(1, 1)
        armor.upgrade()
        self.assertEqual(armor.get_level(), 2)
        self.assertEqual(armor.get_material_level(), 1)

    def test_upgrade_material(self):
        armor = Armor(10, 1)
        armor.upgrade()
        self.assertEqual(armor.get_level(), 1)
        self.assertEqual(armor.get_material_level(), 2)

    def test_upgrade_max_level_and_material(self):
        armor = Armor(10, 5)
        with self.assertRaises(ValueError):
            armor.upgrade()

    def test_get_upgrade_cost_level(self):
        armor = Armor(1, 1)
        expected = ArmorLevel.LEVEL_1.upgrade_cost
        self.assertEqual(armor.get_upgrade_cost(), expected)

    def test_get_upgrade_cost_material(self):
        armor = Armor(10, 1)
        expected = ArmorMaterial.LEVEL_1.upgrade_cost
        self.assertEqual(armor.get_upgrade_cost(), expected)

    def test_get_upgrade_cost_error(self):
        armor = Armor(10, 5)
        with self.assertRaises(ValueError):
            armor.get_upgrade_cost()

    def test_to_dict_and_from_dict(self):
        armor = Armor(3, 2)
        armor_dict = armor.to_dict()
        loaded_armor = Armor.from_dict(armor_dict)
        self.assertEqual(loaded_armor.get_level(), armor.get_level())
        self.assertEqual(loaded_armor.get_material_level(), armor.get_material_level())
        self.assertEqual(loaded_armor.get_armor(), armor.get_armor())
        self.assertEqual(loaded_armor.get_value(), armor.get_value())

    def test_str_representation(self):
        armor = Armor(1, 1)
        output = str(armor)
        self.assertIn("Basic", output)
        self.assertIn("Cloth", output)
        self.assertIn("Armor Value", output)

    def test_repr_representation(self):
        armor = Armor(1, 1)
        output = repr(armor)
        self.assertIn("Armor", output)
        self.assertIn("level=1", output)
        self.assertIn("material_level=1", output)


if __name__ == '__main__':
    unittest.main()
