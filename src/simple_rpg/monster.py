from simple_rpg.entity import Entity
from abc import ABC, abstractmethod



class Monster(Entity, ABC):
    
    def __init__(self, name, level, base_attack, base_armor, base_max_health, base_max_stamina, xp_gain):
        self._xp_gain = xp_gain
        super().__init__(name, level, base_attack, base_armor, base_max_health, base_max_stamina)

    def get_xp_gain(self):
        return self._xp_gain
    
    @abstractmethod
    def drop_item(self):
        """Each monster must implement its drop logic"""
        pass

    def __str__(self):
        return (
            f"{self.get_name()} (Level {self.get_level()})\n"
            f"Health: {self.get_health()}/{self.get_max_health()}\n"
            f"Stamina: {self.get_stamina()}/{self.get_max_stamina()}\n"
            f"Attack: {self.get_attack()} | Armor: {self.get_armor()}\n"
            f"XP on defeat: {self.get_xp_gain()}"
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.get_name()!r}, "
            f"level={self.get_level()}, "
            f"health={self.get_health()}, "
            f"stamina={self.get_stamina()}, "
            f"attack={self.get_attack()}, "
            f"armor={self.get_armor()}, "
            f"xp_gain={self._xp_gain}"
            ")"
        )
