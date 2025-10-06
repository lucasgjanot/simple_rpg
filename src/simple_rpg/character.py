from simple_rpg.entity import Entity
from simple_rpg.item import Item
from simple_rpg.potions import Potion, PotionType, PotionLevel
from simple_rpg.weapon import Weapon, WeaponLevel, WeaponMaterial
from simple_rpg.armor import Armor, ArmorLevel, ArmorMaterial
from collections import defaultdict
from simple_rpg.load import item_from_dict


class Character(Entity):

    def __init__(self, name):
        self._inventory = []
        self._equipped = {}
        self._gold = 100
        self._xp = 0
        super().__init__(name, level=1, base_attack=10, base_armor=0, base_max_health=100, base_max_stamina=100)

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
        if self._equipped.get("armor"):
            return self._equipped["armor"]
        return None
    
    def get_equipped_weapon(self):
        if self._equipped.get("weapon"):
            return self._equipped["weapon"]
        return None

    def get_gold(self):
        return self._gold
    
    def spend_gold(self, amount):
        if self._gold < amount:
            raise ValueError("Not enough gold.")
        self._gold -= amount

    def upgrade_item(self, item):
        if item not in self._inventory and item not in self._equipped.values():
            raise ValueError("Item must be in inventory or equipped to upgrade.")

        if not isinstance(item, (Weapon, Armor)):
            raise ValueError("Only weapons and armors can be upgraded.")

        try:
            upgrade_cost = item.get_upgrade_cost()
        except ValueError as e:
            raise ValueError(f"Cannot upgrade item: {e}")

        if self._gold < upgrade_cost:
            raise ValueError(f"Not enough gold to upgrade. Required: {upgrade_cost}, you have: {self._gold}")

        self.spend_gold(upgrade_cost)
        item.upgrade()
        self._update_stats()

        print(f"{item.get_name()} upgraded! Gold remaining: {self._gold}")


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
            return super().get_attack_stamina_cost() + weapon.get_material_level()  # scales with material
        return super().get_attack_stamina_cost()

    def get_equipped(self):
        return self._equipped
    

    def to_dict(self):
        return {
            "name": self._name,
            "level": self._level,
            # other character attributes
            "inventory": [item.to_dict() for item in self._inventory],
            "equipped": {slot: (item.to_dict() if item else None) 
                        for slot, item in self._equipped.items()},
        }



    @classmethod
    def from_dict(cls, data):
        char = cls(data["name"], data["level"], ...)  # fill as appropriate

        # Load inventory
        char._inventory = [item_from_dict(item_data) for item_data in data.get("inventory", [])]

        # Load equipped items, if it's a dict of slot -> item(s)
        equipped_data = data.get("equipped", {})
        char._equipped = {}
        for slot, item_data in equipped_data.items():
            if isinstance(item_data, list):
                char._equipped[slot] = [item_from_dict(i) for i in item_data]
            elif item_data is None:
                char._equipped[slot] = None
            else:
                char._equipped[slot] = item_from_dict(item_data)

        # Load other character fields as needed

        return char


    def __str__(self):
        equipped_weapon = self._equipped.get("weapon")
        equipped_armor = self._equipped.get("armor")
        potions = self._equipped.get("potions", [])

        # Count potions by type and level label


        potion_counts = defaultdict(lambda: defaultdict(int))  # {PotionType: {level_label: count}}

        for potion in potions:
            potion_type = potion.get_potiontype()
            potion_level = potion.get_potionlevel()
            level_label = potion_level.value[0]  # e.g. "Small", "Medium"
            potion_counts[potion_type][level_label] += 1

        # Build potion display string
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
        return (
            f"{self.__class__.__name__}("
            f"name={self.get_name()!r}, level={self.get_level()}, xp={self.get_xp()}, "
            f"gold={self.get_gold()}, "
            f"inventory_size={len(self._inventory)}, "
            f"equipped={{{', '.join(f'{k}: {v.get_name() if isinstance(v, Item) else len(v)}' for k, v in self._equipped.items())}}}, "
            f"health={self.get_health()}, stamina={self.get_stamina()}"
            ")"
        )


