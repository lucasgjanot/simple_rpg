from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Slime(Monster):
    def __init__(self, level):
        super().__init__(
            name="Slime",
            level=level,
            base_attack=4,
            base_armor=0,
            base_max_health=12,
            base_max_stamina=15
        )
        self._drops = [
            Item("Slime Gel", "Sticky and useful", 25),
            Item("Small Slime Core", "Pulsating energy", 40),
            Item("Slime King Crown", "Rare artifact", 150)
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
