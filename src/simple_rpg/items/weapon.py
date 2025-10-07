from enum import Enum
from abc import ABC, abstractmethod
from simple_rpg.items.item import Item

class WeaponLevel(Enum):
    LEVEL_1 = ("Basic", 100)
    LEVEL_2 = ("Superior", 200)
    LEVEL_3 = ("Majestic", 300)
    LEVEL_4 = ("Elite", 400)
    LEVEL_5 = ("Legendary", 550)
    LEVEL_6 = ("Mythic", 700)
    LEVEL_7 = ("Divine", 900)
    LEVEL_8 = ("Ancient", 1100)
    LEVEL_9 = ("Ethereal", 1350)
    LEVEL_10 = ("Transcendent", 0)

    def __init__(self, description, upgrade_cost):
        self._description = description
        self._upgrade_cost = upgrade_cost

    @property
    def description(self):
        return self._description

    @property
    def upgrade_cost(self):
        return self._upgrade_cost

    @classmethod
    def from_level(cls, level: int):
        try:
            return cls[f"LEVEL_{level}"]
        except KeyError:
            raise ValueError("Weapon level must be between 1 and 10.")


class WeaponMaterial(Enum):
    LEVEL_1 = ("Wood", 300)
    LEVEL_2 = ("Bronze", 500)
    LEVEL_3 = ("Iron", 800)
    LEVEL_4 = ("Mithril", 1100)
    LEVEL_5 = ("Steel", 0)

    def __init__(self, name, upgrade_cost):
        self._name = name
        self._upgrade_cost = upgrade_cost

    @property
    def name(self):
        return self._name

    @property
    def upgrade_cost(self):
        return self._upgrade_cost

    @classmethod
    def from_level(cls, level: int):
        try:
            return cls[f"LEVEL_{level}"]
        except KeyError:
            raise ValueError("Material level must be between 1 and 5.")

        


class Weapon(Item, ABC):
    MAX_LEVEL = 10
    MAX_MATERIAL_LEVEL = 5

    def __init__(self, level, material_level):
        self._level = level
        self._material_level = material_level
        self._damage = self.calculate_damage(level, material_level)
        self._name = ""
        self._description = ""
        self._value = self.calculate_value(self._level, self._material_level)

        super().__init__(self._name, self._description, self._value)
        self._update_stats()

    @abstractmethod
    def _update_stats(self):
        pass

    def upgrade(self):
        if self._level < self.MAX_LEVEL:
            self._level += 1
        elif self._material_level < self.MAX_MATERIAL_LEVEL:
            self._material_level += 1
            self._level = 1  # reset após upgrade de material
        else:
            raise ValueError("Weapon is already at max level")

        self._update_stats()

    @staticmethod
    def calculate_damage(level, material_level):
        return level * 10 + material_level * 5

    @staticmethod
    def calculate_value(level, material_level):
        base_value = 50
        level_multiplier = 20
        material_multiplier = 30
        return base_value + (level_multiplier * level) + (material_multiplier * material_level)

    def get_damage(self):
        return self._damage

    def get_level(self):
        return self._level

    def get_material_level(self):
        return self._material_level

    def get_upgrade_cost(self) -> int:
        if self._level < self.MAX_LEVEL:
            return WeaponLevel.from_level(self._level).upgrade_cost
        elif self._material_level < self.MAX_MATERIAL_LEVEL:
            return WeaponMaterial.from_level(self._material_level).upgrade_cost
        else:
            raise ValueError("Weapon is already at max level and material.")
        
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "_level": self._level,
            "_material_level": self._material_level,
            "_damage": self._damage,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        # This will rarely be called directly but good to have
        level = data["_level"]
        material_level = data["_material_level"]
        # Weapon is abstract, so raise error or return None
        raise NotImplementedError("Use subclass from_dict")

    def __str__(self):
        return (
            f"{self._name} (Level {self._level} - {WeaponLevel.from_level(self._level).description}, "
            f"Material: {WeaponMaterial.from_level(self._material_level).name})\n"
            f"Damage: {self._damage}\n"
            f"Value: {self._value} gold\n"
            f"Upgrade Cost: {self.get_upgrade_cost()} gold"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"level={self._level}, "
            f"material_level={self._material_level}, "
            f"name={self._name!r}, "
            f"description={self._description!r}, "
            f"damage={self._damage}, "
            f"value={self._value})"
        )
    






