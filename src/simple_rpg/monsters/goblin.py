from simple_rpg.monsters.monster import Monster
from simple_rpg.items.item import Item
import random

class Goblin(Monster):
    def __init__(self, level):
        super().__init__(
            name="Goblin",
            level=level,
            base_attack=7,         # a bit stronger attack than Plant (5)
            base_armor=3,          # slightly better armor than Plant (2)
            base_max_health=15,    # a little less health than Plant (20)
            base_max_stamina=15    # more stamina than Plant (10) for agility
        )
        self._drops = [
        Item("Goblin Ear", "Proof you defeated a goblin", 8),
        Item("Rusty Dagger", "A worn but usable weapon", 20),
        Item("Goblin Tooth", "Sharp and jagged", 12),
        Item("Tattered Cloak", "Worn clothing of a goblin", 40),
        Item("Goblin Ring", "A strange ring with magical aura", 150),
        Item("Goblin King's Crown", "Rare and powerful headpiece", 400),
    ]

    def drop_item(self):
        base_drops = [
            (self._drops[0], 0.5),
            (self._drops[1], 0.3),
        ]

        if self._level >= 2:
            base_drops.append((self._drops[2], 0.15))
        if self._level >= 3:
            base_drops.append((self._drops[3], 0.08))
        if self._level >= 4:
            base_drops.append((self._drops[4], 0.05))
        if self._level >= 5:
            base_drops.append((self._drops[5], 0.02))

        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        return Item("Nothing", "You found nothing...", 0)
