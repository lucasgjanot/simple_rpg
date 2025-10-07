import unittest
from simple_rpg.entity import Entity


# Minimal concrete subclass for testing
class MockEntity(Entity):
    def __init__(self, name="Test", level=1, base_attack=10, base_armor=5):
        super().__init__(name, level, base_attack, base_armor)


class TestEntity(unittest.TestCase):

    def setUp(self):
        self.entity = MockEntity(name="Hero", level=3, base_attack=10, base_armor=5)
        self.enemy = MockEntity(name="Goblin", level=2, base_attack=8, base_armor=3)

    def test_initial_stats(self):
        self.assertEqual(self.entity.get_name(), "Hero")
        self.assertEqual(self.entity.get_level(), 3)
        self.assertGreater(self.entity.get_max_health(), 100)
        self.assertGreater(self.entity.get_max_stamina(), 100)
        self.assertGreater(self.entity.get_attack(), 10)
        self.assertGreater(self.entity.get_armor(), 5)
        self.assertEqual(self.entity.get_health(), self.entity.get_max_health())
        self.assertEqual(self.entity.get_stamina(), self.entity.get_max_stamina())

    def test_is_alive(self):
        self.assertTrue(self.entity.is_alive())
        self.entity._health = 0
        self.assertFalse(self.entity.is_alive())

    def test_take_damage_reduces_health(self):
        result = self.entity.take_damage(20)  # armor will reduce this
        self.assertIn("took", result)
        self.assertLess(self.entity.get_health(), self.entity.get_max_health())

    def test_take_lethal_damage(self):
        self.entity._armor = 0
        result = self.entity.take_damage(999)
        self.assertIn("has died", result)
        self.assertEqual(self.entity.get_health(), self.entity._health)

    def test_restore_health(self):
        self.entity._health -= 20
        self.entity.restore_health(10)
        self.assertEqual(self.entity.get_health(), self.entity.get_max_health() - 10)

    def test_restore_health_to_full(self):
        self.entity._health -= 10
        self.entity.restore_health(1000)  # more than max
        self.assertEqual(self.entity.get_health(), self.entity.get_max_health())

    def test_restore_health_invalid(self):
        with self.assertRaises(ValueError):
            self.entity.restore_health(-5)
        with self.assertRaises(ValueError):
            self.entity.restore_health(1)  # already full health

    def test_use_stamina_valid(self):
        old_stamina = self.entity.get_stamina()
        self.entity.use_stamina(20)
        self.assertEqual(self.entity.get_stamina(), old_stamina - 20)

    def test_use_stamina_invalid(self):
        with self.assertRaises(ValueError):
            self.entity.use_stamina(-10)
        self.entity._stamina = 5
        with self.assertRaises(ValueError):
            self.entity.use_stamina(15)

    def test_restore_stamina_valid(self):
        self.entity._stamina -= 30
        self.entity.restore_stamina(20)
        self.assertEqual(self.entity.get_stamina(), self.entity.get_max_stamina() - 10)

    def test_restore_stamina_invalid(self):
        with self.assertRaises(ValueError):
            self.entity.restore_stamina(-1)
        with self.assertRaises(ValueError):
            self.entity.restore_stamina(1)  # already at full

    def test_attack_target(self):
        enemy_starting_health = self.enemy.get_health()
        result = self.entity.attack_target(self.enemy)
        self.assertIn("took", result)
        self.assertLess(self.enemy.get_health(), enemy_starting_health)
        self.assertEqual(self.entity.get_stamina(), self.entity.get_max_stamina() - self.entity.get_attack_stamina_cost())

    def test_attack_target_invalid(self):
        with self.assertRaises(ValueError):
            self.entity.attack_target("not an entity")

    def test_get_stats(self):
        stats = self.entity.get_stats()
        self.assertIn("Name", stats)
        self.assertIn("Health", stats)
        self.assertTrue(stats["Health"].endswith(f"/{self.entity.get_max_health()}"))

    def test_str(self):
        string = str(self.entity)
        self.assertIn("Hero", string)
        self.assertIn("Health:", string)
        self.assertIn("Stamina:", string)

    def test_repr(self):
        rep = repr(self.entity)
        self.assertIn("MockEntity(name='Hero'", rep)
        self.assertIn("health=", rep)
        self.assertIn("stamina=", rep)


if __name__ == '__main__':
    unittest.main()
