from simple_rpg.monsters.monster import Monster
from simple_rpg.item import Item
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

    def drop_item(self):
        base_drops = [
            (Item("Bone", "Might be useful", 20), 0.7),
            (Item("Rusty Sword", "Old but still sharp", 35), 0.2),
        ]
        if self._level >= 5:
            base_drops.append((Item("Ancient Bone Fragment", "Mystical and rare", 120), 0.1))

        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        return Item("Nothing", "You found nothing...", 0)
