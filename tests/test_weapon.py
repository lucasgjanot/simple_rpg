import unittest
from simple_rpg.items.weapon import Weapon, WeaponLevel, WeaponMaterial



class ConcreteWeapon(Weapon):
    def _update_stats(self):
        level_desc = WeaponLevel.from_level(self._level).description
        material_name = WeaponMaterial.from_level(self._material_level).name
        self._name = f"{level_desc} {material_name} Sword"
        self._description = f"A {level_desc.lower()} sword made of {material_name.lower()}."
        self._damage = self.calculate_damage(self._level, self._material_level)
        self._value = self.calculate_value(self._level, self._material_level)


class TestWeaponCore(unittest.TestCase):

    def test_initialization(self):
        weapon = ConcreteWeapon(1, 1)
        self.assertEqual(weapon.get_level(), 1)
        self.assertEqual(weapon.get_material_level(), 1)
        self.assertEqual(weapon.get_damage(), 1 * 10 + 1 * 5)
        self.assertEqual(weapon.get_value(), 50 + 20 + 30)

    def test_upgrade_level(self):
        weapon = ConcreteWeapon(1, 1)
        weapon.upgrade()
        self.assertEqual(weapon.get_level(), 2)
        self.assertEqual(weapon.get_material_level(), 1)

    def test_upgrade_material(self):
        weapon = ConcreteWeapon(10, 1)
        weapon.upgrade()
        self.assertEqual(weapon.get_level(), 1)
        self.assertEqual(weapon.get_material_level(), 2)

    def test_upgrade_at_max(self):
        weapon = ConcreteWeapon(10, 5)
        with self.assertRaises(ValueError):
            weapon.upgrade()

    def test_upgrade_cost_level(self):
        weapon = ConcreteWeapon(3, 1)
        cost = weapon.get_upgrade_cost()
        self.assertEqual(cost, WeaponLevel.from_level(3).upgrade_cost)

    def test_upgrade_cost_material(self):
        weapon = ConcreteWeapon(10, 2)
        cost = weapon.get_upgrade_cost()
        self.assertEqual(cost, WeaponMaterial.from_level(2).upgrade_cost)

    def test_upgrade_cost_at_max(self):
        weapon = ConcreteWeapon(10, 5)
        with self.assertRaises(ValueError):
            weapon.get_upgrade_cost()

    def test_to_dict(self):
        weapon = ConcreteWeapon(4, 2)
        data = weapon.to_dict()
        self.assertIn("_level", data)
        self.assertIn("_material_level", data)
        self.assertIn("_damage", data)
        self.assertEqual(data["_level"], 4)
        self.assertEqual(data["_material_level"], 2)

    def test_from_dict_raises(self):
        data = {
            "_level": 3,
            "_material_level": 1,
            "_damage": 35
        }
        with self.assertRaises(NotImplementedError):
            Weapon.from_dict(data)

    def test_str_representation(self):
        weapon = ConcreteWeapon(3, 2)
        string = str(weapon)
        self.assertIn("Level 3", string)
        self.assertIn("Damage", string)
        self.assertIn("Upgrade Cost", string)

    def test_repr_representation(self):
        weapon = ConcreteWeapon(2, 1)
        rep = repr(weapon)
        self.assertIn("ConcreteWeapon", rep)
        self.assertIn("level=2", rep)
        self.assertIn("material_level=1", rep)


if __name__ == '__main__':
    unittest.main()