import unittest
from simple_rpg.entity import Entity


class ConcreteEntity(Entity):
    """Concrete subclass of Entity for testing purposes."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TestEntityMethods(unittest.TestCase):

    def setUp(self):
        self.entity = ConcreteEntity("TestHero", level=1, base_attack=10, base_armor=5)

    def test_initial_values(self):
        self.assertEqual(self.entity.get_name(), "TestHero")
        self.assertEqual(self.entity.get_level(), 1)
        self.assertEqual(self.entity.get_health(), self.entity.get_max_health())
        self.assertEqual(self.entity.get_stamina(), self.entity.get_max_stamina())

    def test_take_damage(self):
        initial_health = self.entity.get_health()
        result = self.entity.take_damage(20)  # 20 - armor (5) = 15
        self.assertIn("took 15 damage", result)
        self.assertEqual(self.entity.get_health(), initial_health - 15)

    def test_take_lethal_damage(self):
        self.entity._health = 10
        result = self.entity.take_damage(1000)
        self.assertIn("has died", result)
        self.assertFalse(self.entity.is_alive())

    def test_restore_health(self):
        self.entity._health = 50
        self.entity.restore_health(30)
        self.assertEqual(self.entity.get_health(), 80)

    def test_restore_health_to_max(self):
        self.entity._health = 95
        self.entity.restore_health(30)
        self.assertEqual(self.entity.get_health(), self.entity.get_max_health())

    def test_restore_health_error_if_full(self):
        with self.assertRaises(ValueError):
            self.entity.restore_health(10)

    def test_restore_health_negative_amount(self):
        self.entity._health = 50
        with self.assertRaises(ValueError):
            self.entity.restore_health(-10)

    def test_use_stamina(self):
        initial_stamina = self.entity.get_stamina()
        self.entity.use_stamina(20)
        self.assertEqual(self.entity.get_stamina(), initial_stamina - 20)

    def test_use_stamina_insufficient(self):
        self.entity._stamina = 10
        with self.assertRaises(ValueError):
            self.entity.use_stamina(20)

    def test_restore_stamina(self):
        self.entity._stamina = 50
        self.entity.restore_stamina(30)
        self.assertEqual(self.entity.get_stamina(), 80)

    def test_restore_stamina_to_max(self):
        self.entity._stamina = 95
        self.entity.restore_stamina(30)
        self.assertEqual(self.entity.get_stamina(), self.entity.get_max_stamina())

    def test_restore_stamina_error_if_full(self):
        with self.assertRaises(ValueError):
            self.entity.restore_stamina(10)

    def test_attack_target(self):
        enemy = ConcreteEntity("Enemy", 1, base_attack=5, base_armor=2)
        self.entity._stamina = 100
        enemy._health = 100

        result = self.entity.attack_target(enemy)
        self.assertIn("damage", result)
        self.assertLess(enemy.get_health(), 100)
        self.assertLess(self.entity.get_stamina(), 100)

    def test_attack_invalid_target(self):
        with self.assertRaises(ValueError):
            self.entity.attack_target("not an entity")

    def test_repr_and_str(self):
        string_repr = repr(self.entity)
        self.assertIn("ConcreteEntity", string_repr)
        self.assertIn("health=", string_repr)

        string_str = str(self.entity)
        self.assertIn("Health:", string_str)
        self.assertIn("Attack:", string_str)


if __name__ == '__main__':
    unittest.main()
