from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Spider(Monster):
    def __init__(self, level):
        super().__init__(
            name="Spider",
            level=level,
            base_attack=7,
            base_armor=1,
            base_max_health=15,
            base_max_stamina=20
        )
        self._drops = [
            Item("Spider Silk", "Strong and flexible", 30),
            Item("Venom Gland", "Could be used for poison", 40),
            Item("Rare Spider Fang", "Sharp and deadly", 80),
            Item("Spider Queen's Eye", "Legendary item", 200)
        ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.5),
            (self._drops[1], 0.25),
        ]
        if self._level >= 3:
            base_drops.append((self._drops[2], 0.1))
        if self._level >= 5:
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
