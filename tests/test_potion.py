import unittest
from simple_rpg.potions import Potion, PotionType, PotionLevel


class TestPotion(unittest.TestCase):

    def test_potion_initialization_health_level1(self):
        potion = Potion(PotionType.HEALTH, 1)

        self.assertEqual(potion.get_name(), "Small Health Potion")
        self.assertEqual(potion.get_potiontype(), PotionType.HEALTH)
        self.assertEqual(potion.get_potionlevel(), 1)
        self.assertEqual(potion.get_amount(), 20)
        self.assertEqual(potion.get_value(), 50)
        self.assertEqual(potion.get_description(), "Drink to find out what it does!")

    def test_potion_initialization_stamina_level3(self):
        potion = Potion(PotionType.STAMINA, 3)

        self.assertEqual(potion.get_name(), "Large Stamina Potion")
        self.assertEqual(potion.get_potiontype(), PotionType.STAMINA)
        self.assertEqual(potion.get_potionlevel(), 3)
        self.assertEqual(potion.get_amount(), 100)
        self.assertEqual(potion.get_value(), 200)

    def test_invalid_potion_level_description(self):
        with self.assertRaises(ValueError):
            PotionLevel.get_description(0)
        with self.assertRaises(ValueError):
            PotionLevel.get_description(4)

    def test_invalid_potion_level_size(self):
        with self.assertRaises(ValueError):
            PotionLevel.get_size(99)

    def test_invalid_potion_level_value(self):
        with self.assertRaises(ValueError):
            PotionLevel.get_value(-1)

    def test_str_representation(self):
        potion = Potion(PotionType.HEALTH, 2)
        expected_name = "Medium Health Potion"
        self.assertIn(expected_name, str(potion))
        self.assertIn("Type: Health", str(potion))
        self.assertIn("Value: 100", str(potion))
        self.assertIn("Description: Drink to find out what it does!", str(potion))

    def test_repr_representation(self):
        potion = Potion(PotionType.STAMINA, 1)
        representation = repr(potion)
        self.assertIn("Potion", representation)
        self.assertIn("Stamina", representation)
        self.assertIn("amount=20", representation)
        self.assertIn("value=50", representation)


if __name__ == '__main__':
    unittest.main()
