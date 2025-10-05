import unittest
from enum import Enum
from simple_rpg.weapon import Weapon, WeaponLevel, WeaponMaterial



class ConcreteWeapon(Weapon):
    def _update_stats(self):
        level_desc = WeaponLevel.from_level(self._level).description
        material_name = WeaponMaterial.from_level(self._material_level).name
        self._name = f"{level_desc} {material_name} Sword"
        self._description = f"A {level_desc.lower()} sword made of {material_name.lower()}."
        self._damage = self.calculate_damage(self._level, self._material_level)
        self._value = self.calculate_value(self._level, self._material_level)



class TestWeaponClass(unittest.TestCase):

    def setUp(self):

        self.weapon = ConcreteWeapon(level=1, material_level=1)

    def test_initial_stats(self):
        self.assertEqual(self.weapon.get_level(), 1)
        self.assertEqual(self.weapon.get_material_level(), 1)
        self.assertEqual(self.weapon.get_damage(), 10 * 1 + 5 * 1)
        self.assertEqual(self.weapon._name, "Basic Wood Sword")
        self.assertIn("sword", self.weapon._description.lower())
    
    def test_upgrade_level(self):

        for lvl in range(1, Weapon.MAX_LEVEL):
            self.weapon.upgrade()
            self.assertEqual(self.weapon.get_level(), lvl + 1)
            self.assertEqual(self.weapon.get_material_level(), 1)

    def test_upgrade_material(self):

        self.weapon._level = Weapon.MAX_LEVEL
        self.weapon._material_level = 1
        self.weapon._update_stats()

        self.weapon.upgrade()
        self.assertEqual(self.weapon.get_level(), 1)  
        self.assertEqual(self.weapon.get_material_level(), 2)

    def test_upgrade_max(self):
        self.weapon._level = Weapon.MAX_LEVEL
        self.weapon._material_level = Weapon.MAX_MATERIAL_LEVEL
        self.weapon._update_stats()

        with self.assertRaises(ValueError) as context:
            self.weapon.upgrade()
        self.assertIn("already at max level", str(context.exception))

    def test_calculate_damage_and_value(self):
        damage = ConcreteWeapon.calculate_damage(3, 2)
        value = ConcreteWeapon.calculate_value(3, 2)
        self.assertEqual(damage, 3 * 10 + 2 * 5)
        self.assertEqual(value, 50 + 20 * 3 + 30 * 2)

    def test_get_upgrade_cost_level(self):
        self.weapon._level = 2
        self.weapon._material_level = 1
        self.weapon._update_stats()
        cost = self.weapon.get_upgrade_cost()
        self.assertEqual(cost, WeaponLevel.LEVEL_2.upgrade_cost)

    def test_get_upgrade_cost_material(self):
        self.weapon._level = Weapon.MAX_LEVEL
        self.weapon._material_level = 2
        self.weapon._update_stats()
        cost = self.weapon.get_upgrade_cost()
        self.assertEqual(cost, WeaponMaterial.LEVEL_2.upgrade_cost)

    def test_get_upgrade_cost_max_raises(self):
        self.weapon._level = Weapon.MAX_LEVEL
        self.weapon._material_level = Weapon.MAX_MATERIAL_LEVEL
        self.weapon._update_stats()
        with self.assertRaises(ValueError):
            self.weapon.get_upgrade_cost()

    def test_str_repr(self):
        s = str(self.weapon)
        r = repr(self.weapon)
        self.assertIn(self.weapon._name, s)
        self.assertIn("Damage", s)
        self.assertIn("Upgrade Cost", s)
        self.assertIn("ConcreteWeapon", r)
        self.assertIn("level=", r)
        self.assertIn("material_level=", r)


if __name__ == "__main__":
    unittest.main()
