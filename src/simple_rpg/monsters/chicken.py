from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Chicken(Monster):
    def __init__(self, level):
        super().__init__(
            name="Chicken",
            level=level,
            base_attack=2,
            base_armor=1,
            base_max_health=10,
            base_max_stamina=15
        )
        self._drops = [
            Item("Feather", "A soft feather", 1),
            Item("Raw Chicken Meat", "Better cook it first!", 5),
            Item("Golden Feather", "Rare and shiny!", 50)
        ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.7),
            (self._drops[1], 0.3),
        ]

        # Higher levels slightly increase chance of meat
        if self._level >= 3:
            base_drops.append((self._drops[3], 0.05))

        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        return Item("Nothing", "You found nothing...", 0)
