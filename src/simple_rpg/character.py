from simple_rpg.entity import Entity
from simple_rpg.items.item import Item
from simple_rpg.items.potions import Potion, PotionType
from simple_rpg.items.weapon import Weapon
from simple_rpg.items.armor import Armor
from collections import defaultdict
from simple_rpg.load import item_from_dict


class Character(Entity):

    def __init__(self, name, level=1, base_attack=10, base_armor=0, base_max_health=100, base_max_stamina=100):
        self._inventory = []
        self._equipped = {}
        self._gold = 0
        self._xp = 0
        super().__init__(name, level, base_attack, base_armor, base_max_health, base_max_stamina)
        self._update_stats()

    def _update_stats(self):
        super()._update_stats()
        self._xp_next_level = int(75 * (1.15 ** (self._level - 1)))
        weapon = self._equipped.get("weapon")
        if weapon:
            self._attack += weapon.get_damage()
        armor = self._equipped.get("armor")
        if armor:
            self._armor += armor.get_armor()

    def add_to_inventory(self, item):
        if not isinstance(item, Item):
            raise ValueError("You can only add Item instances to the inventory.")
        self._inventory.append(item)

    def get_xp(self):
        return self._xp

    def equip_item(self, item):
        if not isinstance(item, Item):
            raise ValueError("You can only equip items")
        if item not in self._inventory:
            raise ValueError("Item must be in inventory to equip.")

        if isinstance(item, Potion):
            self._inventory.remove(item)
            self._equipped.setdefault('potions', []).append(item)
        elif isinstance(item, Weapon):
            self._inventory.remove(item)
            current = self._equipped.get('weapon')
            if current:
                self._inventory.append(current)
            self._equipped['weapon'] = item
        elif isinstance(item, Armor):
            self._inventory.remove(item)
            current = self._equipped.get('armor')
            if current:
                self._inventory.append(current)
            self._equipped['armor'] = item
        else:
            raise ValueError("This item type cannot be equipped.")
        self._update_stats()

    def unequip_item(self,item):
        if not isinstance(item, Item):
            raise ValueError("You can only unequip items")
        if isinstance(item, Weapon):
            if self._equipped.get("weapon"):
                if item == self._equipped["weapon"]:
                    self._equipped.setdefault('weapon', item)
                    self._inventory.append(item)
                else:
                    return ValueError("Item is not equipped")
        if isinstance(item, Armor):
            if self._equipped.get("armor"):
                if item == self._equipped["armor"]:
                    self._equipped.setdefault('armor', item)
                    self._inventory.append(item)
                else:
                    return ValueError("Item is not equipped") 
        if isinstance(item, Potion):
            if self._equipped.get("potions"):
                if item in self._equipped["potions"]:
                    index = self._equipped["potions"].find(item)
                    del self._equipped["potions"][index]
                    self._inventory.append(item)
                else:
                    return ValueError("Item is not equipped")
        return ValueError("Item is not equipped") 
    

    def sell_item(self,item):
        if not isinstance(item, Item):
            raise ValueError("You can only sell items")
        if not item in self._inventory:
            raise ValueError("You can't sell items you don't have or are equipped")
        index = self._inventory.find(item)
        del self._inventory[index]
        self.earn_gold(item.get_value())



    def use_potion(self, potion):
        if not isinstance(potion, Potion):
            raise ValueError("Item must be a Potion.")

        equipped_potions = self._equipped.get('potions')
        if not equipped_potions:
            raise ValueError("No potions equipped.")

        if potion not in equipped_potions:
            raise ValueError("Potion must be equipped to use.")

        if potion.get_potiontype() == PotionType.HEALTH:
            self.restore_health(potion.get_amount())
        elif potion.get_potiontype() == PotionType.STAMINA:
            self.restore_stamina(potion.get_amount())

        equipped_potions.remove(potion)

    def get_equipped_armor(self):
        return self._equipped.get("armor", None)

    def get_equipped_weapon(self):
        return self._equipped.get("weapon", None)
    
    def get_equipped_potions(self):
        return self._equipped.get("potions", None)
    
    def get_inventory(self):
        return self._inventory

    def get_gold(self):
        return self._gold
    
    def earn_gold(self,amount):
        if amount < 0:
            raise ValueError("Amount to earn cannot be negative.")
        self._gold += amount


    def spend_gold(self, amount):
        if amount < 0:
            raise ValueError("Amount to spend cannot be negative.")
        if self._gold < amount:
            raise ValueError("Not enough gold.")
        self._gold -= amount

    def upgrade_item(self, item):
        if not isinstance(item, (Weapon, Armor)):
            raise ValueError("Only weapons and armors can be upgraded.")
        if isinstance(item, Armor):
            if self._equipped.get("armor"):
                if item != self._equipped["armor"]:
                    raise ValueError("Item must be in  equipped to upgrade.")
        if isinstance(item, Weapon):
            if self._equipped.get("weapon"):
                if item != self._equipped["weapon"]:
                    raise ValueError("Item must be in equipped to upgrade.")

        try:
            upgrade_cost = item.get_upgrade_cost()
        except ValueError as e:
            raise ValueError(f"Cannot upgrade item: {e}")

        if self._gold < upgrade_cost:
            raise ValueError(f"Not enough gold to upgrade. Required: {upgrade_cost}, you have: {self._gold}")

        self.spend_gold(upgrade_cost)
        item.upgrade()
        self._update_stats()

        return f"{item.get_name()} upgraded! Gold remaining: {self._gold}"

    def gain_xp(self, amount):
        self._xp += amount
        while self._xp >= self._xp_next_level:
            self._xp -= self._xp_next_level
            self.level_up()

    def level_up(self):
        self._level += 1
        print(f"{self.get_name()} leveled up to {self.get_level()}!")
        self._update_stats()
        self._health = self._max_health
        self._stamina = self._max_stamina

    def get_attack_stamina_cost(self):
        weapon = self.get_equipped_weapon()
        if weapon:
            return super().get_attack_stamina_cost() + weapon.get_material_level()
        return super().get_attack_stamina_cost()

    def get_equipped(self):
        return self._equipped

    def to_dict(self):
        return {
            "name": self._name,
            "level": self._level,
            "xp": self._xp,
            "gold": self._gold,
            "inventory": [item.to_dict() for item in self._inventory],
            "equipped": {
                slot: ([item.to_dict() for item in items] if isinstance(items, list) else (items.to_dict() if items else None))
                for slot, items in self._equipped.items()
            },
        }

    @classmethod
    def from_dict(cls, data):
        # Create character with minimal required args
        char = cls(
            name=data["name"],
            level=data.get("level", 1),
            base_attack=10,      # Or pull from data if you save it
            base_armor=0,
            base_max_health=100,
            base_max_stamina=100,
        )

        char._xp = data.get("xp", 0)
        char._gold = data.get("gold", 100)

        # Load inventory
        char._inventory = [item_from_dict(item_data) for item_data in data.get("inventory", [])]

        # Load equipped items
        equipped_data = data.get("equipped", {})
        char._equipped = {}
        for slot, item_data in equipped_data.items():
            if isinstance(item_data, list):
                char._equipped[slot] = [item_from_dict(i) for i in item_data]
            elif item_data is None:
                char._equipped[slot] = None
            else:
                char._equipped[slot] = item_from_dict(item_data)

        # Update stats after loading everything
        char._update_stats()

        # You might want to restore health and stamina to max or from saved data if saved

        return char

    def __str__(self):
        equipped_weapon = self._equipped.get("weapon")
        equipped_armor = self._equipped.get("armor")
        potions = self._equipped.get("potions", [])

        potion_counts = defaultdict(lambda: defaultdict(int))

        for potion in potions:
            potion_type = potion.get_potiontype()
            potion_level = potion.get_potionlevel_description()
            level_label = potion_level  # e.g. "Small", "Medium"
            potion_counts[potion_type][level_label] += 1

        if not potion_counts:
            potion_display = "  None"
        else:
            potion_display = ""
            for ptype in PotionType:
                if ptype in potion_counts:
                    potion_display += f"  {ptype.value}:\n"
                    for level_label, count in potion_counts[ptype].items():
                        potion_display += f"    - {level_label} x{count}\n"

        lines = [
            super().__str__(),
            f"Gold: {self.get_gold()}",
            f"XP: {self._xp}/{self._xp_next_level}",
            f"Equipped Weapon: {equipped_weapon.get_name() if equipped_weapon else 'None'}",
            f"Equipped Armor: {equipped_armor.get_name() if equipped_armor else 'None'}",
            f"Potions Equipped:\n{potion_display.rstrip()}",
            f"Inventory: {len(self._inventory)} item(s)",
        ]
        return "\n".join(lines)

    def __repr__(self):
        equipped_repr = []
        for k, v in self._equipped.items():
            if isinstance(v, list):
                equipped_repr.append(f"{k}: {len(v)} items")
            elif isinstance(v, Item):
                equipped_repr.append(f"{k}: {v.get_name()}")
            else:
                equipped_repr.append(f"{k}: None")

        return (
            f"{self.__class__.__name__}("
            f"name={self.get_name()!r}, level={self.get_level()}, xp={self.get_xp()}, "
            f"gold={self.get_gold()}, "
            f"inventory_size={len(self._inventory)}, "
            f"equipped={{{', '.join(equipped_repr)}}}, "
            f"health={self.get_health()}, stamina={self.get_stamina()}"
            ")"
        )

