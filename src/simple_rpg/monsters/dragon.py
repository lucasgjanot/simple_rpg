from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Dragon(Monster):
    def __init__(self, level):
        super().__init__(
            name="Dragon",
            level=level,
            base_attack=40,
            base_armor=15,
            base_max_health=200,
            base_max_stamina=150
        )
        self._drops = [
            Item("Dragon Scale", "Tough and magical", 500),
            Item("Dragon Claw", "Sharp and deadly", 450),
            Item("Dragon Heart", "Powerful core of the beast", 1000),
            Item("Ancient Dragon Horn", "Rare and valuable", 1500),
            Item("Dragon's Crown", "Symbol of dominance", 3000)
        ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.4),
            (self._drops[1], 0.3),
            (self._drops[2], 0.1),
        ]

        if self._level >= 4:
            base_drops.append((self._drops[3], 0.15))
        if self._level >= 5:
            base_drops.append((self._drops[4], 0.05))

        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        return Item("Nothing", "You found nothing...", 0)
