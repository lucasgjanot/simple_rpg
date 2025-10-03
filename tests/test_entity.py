import unittest
from simple_rpg.entity import Entity

class TestEntity(unittest.TestCase):

    def test_str(self):
        entity = Entity("Lucas", 3, 10, 5)
        expected = (f"Lucas (Level 3)\n"
                f"XP: 0/200\n"
                f"Health: 120/120\n"
                f"Stamina: 110/110\n"
                f"Attack: 16\n"
                f"Armor: 9")
        self.assertEqual(str(entity), expected)

    def test_repr(self):
        entity = Entity("Goblin", 5, 10, 5)
        expected = (
            f"Entity(name='Goblin', level=5, "
            f"max_health=140, max_stamina=120, "
            f"attack=22, armor=13, "
            f"xp=0, xp_next_level=300)")
        self.assertEqual(repr(entity), expected)

    def test_get_stats(self):
        entity = Entity("Bat", 2, 1, 4)
        expected = {
            "Name": "Bat",
            "Level": 2,
            "XP": "0/150",
            "Health": "110/110",
            "Stamina": "105/105",
            "Attack": 4,
            "Armor": 6,
        }
        self.assertEqual(entity.get_stats(), expected)

    def test_level_up(self):
        entity = Entity("Lucas", 3, 10, 5)
        entity.level_up()
        expected = {
            "Name": "Lucas",
            "Level": 4,
            "XP": "0/250",
            "Health": "130/130",
            "Stamina": "115/115",
            "Attack": 19,
            "Armor": 11,
        }
        self.assertEqual(entity.get_stats(), expected)

    def test_gain_xp(self):
        entity = Entity("Lucas", 1, 2, 3)
        entity.gain_xp(10)
        self.assertEqual(entity.get_level(), 1)
        self.assertEqual(entity.get_xp(), 10)
        entity.gain_xp(90)
        self.assertEqual(entity.get_level(), 2)
        self.assertEqual(entity.get_xp(), 0)
        self.assertEqual(entity.get_xp_next_level(), 150)

    def test_is_alive(self):
        entity = Entity("Lucas", 1, 2, 3)
        self.assertEqual(entity.is_alive(), True)
        entity = Entity("Lucas", 1, 2, 3, 0)
        self.assertEqual(entity.is_alive(), False)

    def test_take_damage(self):
        entity = Entity("Lucas", 1, 2, 3)
        response = entity.take_damage(103)
        self.assertEqual(response, "Lucas has died.")
        self.assertEqual(entity.get_health(),0)
        self.assertEqual(entity.is_alive(), False)
        entity = Entity("Lucas", 1, 2, 3)
        response = entity.take_damage(50)
        self.assertEqual(response, 'Lucas took 47 damage. Current health: 53/100')
        self.assertEqual(entity.get_health(),53)
        self.assertEqual(entity.is_alive(), True)

    def test_restore_health(self):
        entity = Entity("Lucas", 1, 2, 3)
        with self.assertRaises(ValueError) as e:
            entity.restore_health(-10)
        self.assertEqual(str(e.exception), "Amount to restore cannot be negative.")
        
        with self.assertRaises(ValueError) as e:
            entity.restore_health(10)

        self.assertEqual(str(e.exception), "Lucas is already at full health.")
        entity.take_damage(20)
        entity.restore_health(10000)
        self.assertEqual(entity.get_health(), 100)
        entity.take_damage(20)
        entity.restore_health(10)
        self.assertEqual(entity.get_health(), 93)

    def test_use_stamina(self):
        entity = Entity("Lucas", 1, 2, 3)
        with self.assertRaises(ValueError) as e:
            entity.use_stamina(100000)
            self.assertEqual(str(e.exception), "Lucas does not have enough stamina!")

        with self.assertRaises(ValueError) as e:
            entity.use_stamina(-10)
            self.assertEqual(str(e.exception), "Amount to restore cannot be negative.")

        entity.use_stamina(10)
        self.assertEqual(entity.get_stamina(), 90)

    def test_restore_stamina(self):
        entity = Entity("Lucas", 1, 2, 3)
        with self.assertRaises(ValueError) as e:
            entity.restore_stamina(-10)
            self.assertEqual(str(e.exception), "Amount to restore cannot be negative.")

        with self.assertRaises(ValueError) as e:
            entity.restore_stamina(1000000)
            self.assertEqual(str(e.exception), "Lucas is already at full stamina.")

        entity.use_stamina(20)
        entity.restore_stamina(10000)
        self.assertEqual(entity.get_stamina(), 100)
        entity.use_stamina(20)
        entity.restore_stamina(10)
        self.assertEqual(entity.get_stamina(), 90)
    
    def test_attack_target(self):
        entity1 = Entity("Lucas", 1, 20000, 3)
        print(entity1)
        entity2 = Entity("Raul", 1, 20, 3)
        print(entity2)
        entity2.attack_target(entity1)
        self.assertEqual(entity1.get_health(), 83)
        entity1.attack_target(entity2)
        self.assertEqual(entity2.is_alive(), False)

        





        
        
