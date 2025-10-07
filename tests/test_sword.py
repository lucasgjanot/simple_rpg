import unittest
from simple_rpg.items.sword import Sword
from simple_rpg.items.weapon import WeaponLevel, WeaponMaterial


class TestSword(unittest.TestCase):

    def test_valid_initialization(self):
        sword = Sword(2, 3)
        self.assertEqual(sword.get_level(), 2)
        self.assertEqual(sword.get_material_level(), 3)
        self.assertEqual(sword.get_damage(), 2 * 10 + 3 * 5)
        self.assertIn("Superior", sword.get_name())
        self.assertIn("Iron", sword.get_name())
        self.assertEqual(sword.get_description(), "Swords are for stabbing or slashing a target")

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            Sword(0, 3)
        with self.assertRaises(ValueError):
            Sword(11, 3)

    def test_invalid_material_level(self):
        with self.assertRaises(ValueError):
            Sword(3, 0)
        with self.assertRaises(ValueError):
            Sword(3, 6)

    def test_str_representation(self):
        sword = Sword(4, 2)
        s = str(sword)
        self.assertIn("Elite", s)
        self.assertIn("Bronze", s)
        self.assertIn("Damage", s)
        self.assertIn("Value", s)

    def test_repr_representation(self):
        sword = Sword(1, 1)
        r = repr(sword)
        self.assertIn("Sword(name=", r)
        self.assertIn("level=1", r)
        self.assertIn("material_level=1", r)

    def test_upgrade_level(self):
        sword = Sword(1, 1)
        sword.upgrade()
        self.assertEqual(sword.get_level(), 2)
        self.assertEqual(sword.get_material_level(), 1)

    def test_upgrade_material(self):
        sword = Sword(10, 2)
        sword.upgrade()
        self.assertEqual(sword.get_level(), 1)
        self.assertEqual(sword.get_material_level(), 3)

    def test_upgrade_at_max(self):
        sword = Sword(10, 5)
        with self.assertRaises(ValueError):
            sword.upgrade()

    def test_get_upgrade_cost_level(self):
        sword = Sword(4, 1)
        self.assertEqual(sword.get_upgrade_cost(), WeaponLevel.from_level(4).upgrade_cost)

    def test_get_upgrade_cost_material(self):
        sword = Sword(10, 2)
        self.assertEqual(sword.get_upgrade_cost(), WeaponMaterial.from_level(2).upgrade_cost)

    def test_get_upgrade_cost_at_max(self):
        sword = Sword(10, 5)
        with self.assertRaises(ValueError):
            sword.get_upgrade_cost()

    def test_to_dict(self):
        sword = Sword(3, 2)
        data = sword.to_dict()
        self.assertEqual(data["_level"], 3)
        self.assertEqual(data["_material_level"], 2)
        self.assertEqual(data["_damage"], sword.get_damage())

    def test_from_dict(self):
        original = Sword(5, 4)
        data = original.to_dict()
        new_sword = Sword.from_dict(data)
        self.assertEqual(new_sword.get_level(), 5)
        self.assertEqual(new_sword.get_material_level(), 4)
        self.assertEqual(new_sword.get_damage(), original.get_damage())
        self.assertEqual(new_sword.get_value(), original.get_value())
        self.assertEqual(new_sword.get_name(), original.get_name())


if __name__ == "__main__":
    unittest.main()
