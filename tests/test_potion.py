import unittest
from simple_rpg.items.potions import Potion, PotionType, PotionLevel

class TestPotion(unittest.TestCase):

    def test_potion_initialization_health(self):
        potion = Potion(PotionType.HEALTH, 1)
        self.assertEqual(potion.get_potionlevel(), 1)
        self.assertEqual(potion.get_potiontype(), PotionType.HEALTH)
        self.assertEqual(potion.get_amount(), 40)
        self.assertEqual(potion.get_value(), 50)
        self.assertIn("Small Health Potion", potion.get_name())

    def test_potion_initialization_stamina(self):
        potion = Potion(PotionType.STAMINA, 2)
        self.assertEqual(potion.get_potionlevel(), 2)
        self.assertEqual(potion.get_potiontype(), PotionType.STAMINA)
        self.assertEqual(potion.get_amount(), 80)
        self.assertEqual(potion.get_value(), 100)
        self.assertIn("Medium Stamina Potion", potion.get_name())

    def test_to_dict_and_from_dict(self):
        potion = Potion(PotionType.HEALTH, 3)
        potion_dict = potion.to_dict()

        expected_keys = {"name", "description", "value", "potiontype", "potionlevel", "amount"}
        self.assertTrue(expected_keys.issubset(potion_dict.keys()))
        self.assertEqual(potion_dict["potiontype"], "Health")
        self.assertEqual(potion_dict["potionlevel"], 3)
        self.assertEqual(potion_dict["amount"], 150)

        new_potion = Potion.from_dict(potion_dict)
        self.assertEqual(new_potion.get_potiontype(), PotionType.HEALTH)
        self.assertEqual(new_potion.get_potionlevel(), 3)
        self.assertEqual(new_potion.get_amount(), 150)

    def test_str_representation(self):
        potion = Potion(PotionType.STAMINA, 2)
        string = str(potion)
        self.assertIn("Level 2", string)
        self.assertIn("Stamina", string)
        self.assertIn("Value", string)

    def test_repr_representation(self):
        potion = Potion(PotionType.HEALTH, 1)
        rep = repr(potion)
        self.assertIn("Potion", rep)
        self.assertIn("Health", rep)
        self.assertIn("level=1", rep)


if __name__ == '__main__':
    unittest.main()
