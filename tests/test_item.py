import unittest
from simple_rpg.items.item import Item


class TestItem(unittest.TestCase):

    def test_initialization_and_getters(self):
        item = Item("Mystery Box", "Could be anything", 100)
        self.assertEqual(item.get_name(), "Mystery Box")
        self.assertEqual(item.get_description(), "Could be anything")
        self.assertEqual(item.get_value(), 100)

    def test_to_dict(self):
        item = Item("Health Elixir", "Restores full health", 250)
        expected = {
            "type": "Item",
            "name": "Health Elixir",
            "description": "Restores full health",
            "value": 250
        }
        self.assertEqual(item.to_dict(), expected)

    def test_from_dict(self):
        data = {
            "name": "Mana Potion",
            "description": "Refills your mana pool",
            "value": 180
        }
        item = Item.from_dict(data)
        self.assertIsInstance(item, Item)
        self.assertEqual(item.get_name(), "Mana Potion")
        self.assertEqual(item.get_description(), "Refills your mana pool")
        self.assertEqual(item.get_value(), 180)

    def test_str_representation(self):
        item = Item("Ancient Coin", "Very old and mysterious", 999)
        string = str(item)
        self.assertIn("Ancient Coin", string)
        self.assertIn("Description: Very old and mysterious", string)
        self.assertIn("Value: 999", string)

    def test_repr_representation(self):
        item = Item("Scroll", "A forgotten spell", 300)
        representation = repr(item)
        self.assertEqual(representation, "Item(name='Scroll', description='A forgotten spell', value=300)")


if __name__ == '__main__':
    unittest.main()
