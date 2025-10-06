from simple_rpg.monsters.monster import Monster
from simple_rpg.item import Item
import random

class Plant(Monster):
    def __init__(self, level):
        super().__init__(
            name="Plant",
            level=level,
            base_attack=5,
            base_armor=2,
            base_max_health=20,
            base_max_stamina=10
        )

    def drop_item(self):
        # Base items always available
        base_drops = [
            (Item("Leaf", "Just a leaf", 10), 0.5),
            (Item("Poison Spores", "Watch out! They are poisonous", 25), 0.3),
        ]

        # Higher level unlocks
        if self._level >= 2:
            base_drops.append((Item("Sap", "Sticky and maybe useful", 15), 0.15))
        if self._level >= 3:
            base_drops.append((Item("Rare Seed", "A mysterious glowing seed", 100), 0.08))
        if self._level >= 4:
            base_drops.append((Item("Ancient Root", "Old and powerful root", 250), 0.05))
        if self._level >= 5:
            base_drops.append((Item("Golden Thorn", "Extremely rare and valuable", 500), 0.02))

        # Normalize probabilities (optional, for safety)
        total_prob = sum(prob for _, prob in base_drops)
        normalized_drops = [(item, prob / total_prob) for item, prob in base_drops]

        # Random selection
        roll = random.random()
        cumulative = 0.0
        for item, prob in normalized_drops:
            cumulative += prob
            if roll <= cumulative:
                return item

        # Fallback
        return Item("Nothing", "You found nothing...", 0)
