from enum import Enum
from abc import ABC, abstractmethod
from simple_rpg.item import Item

class PotionType(Enum):
    HEALTH = "Health"
    STAMINA = "Stamina"

class PotionLevel(Enum):
    LEVEL_1 = ("Small", 40, 50)
    LEVEL_2 = ("Medium", 80, 100)
    LEVEL_3 = ("Large", 150, 200)

    @classmethod
    def get_description(cls, level: int) -> str:
        try:
            return cls[f"LEVEL_{level}"].value
        except KeyError:
            raise ValueError("Level must be between 1 and 3")
        
    @classmethod
    def get_size(cls, level) -> str:
        try:
            return cls[f"LEVEL_{level}"].value[1]
        except KeyError:
            raise ValueError("Level must be between 1 and 3")
        
    @classmethod
    def get_value(cls, level) -> str:
        try:
            return cls[f"LEVEL_{level}"].value[2]
        except KeyError:
            raise ValueError("Level must be between 1 and 3")

class Potion(Item):

    def __init__(self, potiontype, potionlevel):
        self._name = f"{PotionLevel.get_description(potionlevel)[0]} {potiontype.value} Potion"
        self._value = PotionLevel.get_value(potionlevel)
        self._amount = PotionLevel.get_size(potionlevel)
        self._description = "Drink to find out what it does!"
        self._potionlevel = potionlevel 
        self._potiontype = potiontype
            
        super().__init__(self._name, self._description, self._value)

    def get_potionlevel(self):
        return self._potionlevel
    
    def get_potiontype(self):
        return self._potiontype
    
    def get_amount(self):
        return self._amount
    
    def to_dict(self):
        data = super().to_dict()
        # add Potion-specific info
        data.update({
            "potiontype": self._potiontype.value,
            "potionlevel": self._potionlevel,
            "amount": self._amount,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        # Convert potiontype string back to enum
        potion_type_enum = PotionType(data["potiontype"])
        potion_level = data["potionlevel"]
        return cls(potion_type_enum, potion_level)


    def __str__(self):
        return (f"{self._name} (Level {self.get_potionlevel()})\n"
                f"Type: {self.get_potiontype().value}\n"
                #f"Restores: {self.get_ammount()} points\n"
                f"Value: {self.get_value()} gold\n"
                f"Description: {self.get_description()}")

    def __repr__(self):
        return (f"Potion(name={self.get_name()!r}, type={self.get_potiontype().value!r}, "
                f"level={self.get_potionlevel()}, amount={self.get_amount()}, value={self.get_value()})")
