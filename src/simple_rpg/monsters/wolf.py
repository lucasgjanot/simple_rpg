from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Wolf(Monster):
    def __init__(self, level):
        super().__init__(
            name="Wolf",
            level=level,
            base_attack=12,
            base_armor=3,
            base_max_health=30,
            base_max_stamina=40
        )
        self._drops = [
            Item("Wolf Pelt", "Warm and valuable", 60),
            Item("Wolf Fang", "Sharp and strong", 45),
            Item("Alpha Wolf Claw", "Rare and powerful", 150)
        ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.6),
            (self._drops[1], 0.3),
        ]
        if self._level >= 4:
            base_drops.append((self._drops[2], 0.1))

        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        return Item("Nothing", "You found nothing...", 0)
