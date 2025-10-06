from enum import Enum
from simple_rpg.item import Item


class ArmorLevel(Enum):
    LEVEL_1 = ("Basic", 100)
    LEVEL_2 = ("Polished", 200)
    LEVEL_3 = ("Reinforced", 300)
    LEVEL_4 = ("Superior", 400)
    LEVEL_5 = ("Majestic", 500)
    LEVEL_6 = ("Mythic", 600)
    LEVEL_7 = ("Divine", 700)
    LEVEL_8 = ("Ancient", 800)
    LEVEL_9 = ("Ethereal", 900)
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
            raise ValueError("Armor level must be between 1 and 10.")

class ArmorMaterial(Enum):
    LEVEL_1 = ("Cloth", 300)
    LEVEL_2 = ("Leather", 500)
    LEVEL_3 = ("Chainmail", 800)
    LEVEL_4 = ("Plate", 1100)
    LEVEL_5 = ("Dragonhide", 0)


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
        


class Armor(Item):

    MAX_LEVEL = 10
    MAX_MATERIAL_LEVEL = 5

    def __init__(self, level, material_level):
        self._level = level
        self._material_level = material_level
        self._update_stats()
        super().__init__(self._name, self._description, self._value)
        

    
    def _update_stats(self):
        level_desc = ArmorLevel.from_level(self._level).description
        material_name = ArmorMaterial.from_level(self._material_level).name

        self._armor = self.calculate_armor(self._level, self._material_level)
        self._value = self.calculate_value(self._level, self._material_level)

        self._name = f"{level_desc} {material_name} Armor"
        self._description = "This is supposed to protect you"

        # Atualiza os atributos da superclasse Item
        super().__init__(self._name, self._description, self._value)

    def upgrade(self):
        if self._level < self.MAX_LEVEL:
            self._level += 1
        elif self._material_level < self.MAX_MATERIAL_LEVEL:
            self._material_level += 1
            self._level = 1  # reset após upgrade de material
        else:
            raise ValueError("Armor is already at max level")

        self._update_stats()

    @staticmethod
    def calculate_armor(level, material_level):
        return level * 10 + material_level * 10


    @staticmethod
    def calculate_value(level, material_level):
        base_value = 50
        level_multiplier = 20
        material_multiplier = 30
        return base_value + (level_multiplier * level) + (material_multiplier * material_level)

    def get_armor(self):
        return self._armor

    def get_level(self):
        return self._level

    def get_material_level(self):
        return self._material_level
    
    def get_upgrade_cost(self) -> int:
        if self._level < self.MAX_LEVEL:
            return ArmorLevel.from_level(self._level).upgrade_cost
        elif self._material_level < self.MAX_MATERIAL_LEVEL:
            return ArmorMaterial.from_level(self._material_level).upgrade_cost
        else:
            raise ValueError("Weapon is already at max level and material.")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "_level": self._level,
            "_material_level": self._material_level,
            "_armor": self._armor,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        level = data["_level"]
        material_level = data["_material_level"]
        armor = cls(level, material_level)
        # _armor is recalculated in __init__, but if you want to set it directly:
        # armor._armor = data["_armor"]
        return armor


    def __str__(self):
        level = ArmorLevel.from_level(self._level).description
        material = ArmorMaterial.from_level(self._material_level).name
        return (
            f"{level} {material} Armor\n"
            f"Description: {self.get_description()}\n"
            f"Level: {self._level}, Material Level: {self._material_level}\n"
            f"Armor Value: {self.get_armor()}\n"
            f"Item Value: {self.get_value()} gold"
        )


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"level={self._level}, material_level={self._material_level}, "
            f"armor={self.get_armor()}, value={self.get_value()}, "
            f"name={self.get_name()!r})"
        )
