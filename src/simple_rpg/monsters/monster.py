from simple_rpg.entity import Entity
from abc import ABC, abstractmethod
from enum import Enum


class MonsterLevel(Enum):
    LEVEL_1 = ("Weak", 0.5)
    LEVEL_2 = ("Average", 1.0)
    LEVEL_3 = ("Strong", 1.5)
    LEVEL_4 = ("Elite", 2.0)
    LEVEL_5 = ("Boss", 3.0)

    def __init__(self, description, multiplier):
        self._description = description
        self._multiplier = multiplier

    @property
    def description(self):
        return self._description

    @property
    def multiplier(self):
        return self._multiplier

    @classmethod
    def from_level(cls, level: int):
        try:
            return cls[f"LEVEL_{level}"]
        except KeyError:
            raise ValueError("Monster level must be between 1 and 5")


class Monster(Entity, ABC):
    def __init__(self, name, level, base_attack, base_armor,
                 base_max_health, base_max_stamina):

        if not (1 <= level <= 5):
            raise TypeError("Monster level must be between 1 and 5")

        self._level = level
        self._strength_enum = MonsterLevel.from_level(level)

        full_name = f"{self._strength_enum.description} {name}"

        self._xp_gain = self._calculate_xp_gain()

        super().__init__(full_name, level, base_attack, base_armor,
                         base_max_health, base_max_stamina)

    def _calculate_xp_gain(self):
        base_xp = 50
        return int(base_xp * self._strength_enum.multiplier)

    def get_xp_gain(self):
        return self._xp_gain

    def get_strength(self):
        return self._strength_enum

    @abstractmethod
    def drop_item(self):
        pass

    def __str__(self):
        return (
            f"{self.get_name()} (Level {self.get_level()})\n"
            f"Health: {self.get_health()}/{self.get_max_health()} | "
            f"Stamina: {self.get_stamina()}/{self.get_max_stamina()}\n"
            f"Attack: {self.get_attack()} | Armor: {self.get_armor()}\n"
            f"XP on defeat: {self.get_xp_gain()}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.get_name()!r}, level={self.get_level()}, "
            f"health={self.get_health()}, stamina={self.get_stamina()}, "
            f"attack={self.get_attack()}, armor={self.get_armor()}, "
            f"xp_gain={self._xp_gain})"
        )
