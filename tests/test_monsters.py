from simple_rpg.monsters import Plant
import unittest

class TestPlantMonster(unittest.TestCase):

    def setUp(self):
        self.plant = Plant(3)

    def test_drop_item(self):
        drop = self.plant.drop_item()
        self.assertIn(drop, self.plant.get_drops())

if __name__ == '__main__':
    unittest.main()