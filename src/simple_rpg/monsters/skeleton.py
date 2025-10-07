from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Skeleton(Monster):
    def __init__(self, level):
        super().__init__(
            name="Skeleton",
            level=level,
            base_attack=10,
            base_armor=5,
            base_max_health=25,
            base_max_stamina=15
        )
        self._drops = [
            Item("Bone", "Might be useful", 20),
            Item("Rusty Sword", "Old but still sharp", 35),
            Item("Ancient Bone Fragment", "Mystical and rare", 120)
        ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.7),
            (self._drops[1], 0.2),
        ]
        if self._level >= 5:
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
