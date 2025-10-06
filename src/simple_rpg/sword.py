from simple_rpg.weapon import Weapon, WeaponMaterial, WeaponLevel

class Sword(Weapon):
    
    def __init__(self, level, material_level):
        if not (1 <= level <= Sword.MAX_LEVEL):
            raise ValueError("Weapon level must be between 1 and 10.")
        if not (1 <= material_level <= Sword.MAX_MATERIAL_LEVEL):
            raise ValueError("Material level must be between 1 and 5.")
        super().__init__(level, material_level)

    def _update_stats(self):
        level_desc = WeaponLevel.from_level(self._level).description
        material_name = WeaponMaterial.from_level(self._material_level).name

        self._damage = self.calculate_damage(self._level, self._material_level)
        self._value = self.calculate_value(self._level, self._material_level)

        self._name = f"{level_desc} {material_name} Sword"
        self._description = "Swords are for stabbing or slashing a target"

    def to_dict(self):
        data = super().to_dict()
        # Add any Sword-specific data if needed (level/material_level handled in Weapon)
        return data

    @classmethod
    def from_dict(cls, data):
        # reconstruct from saved level/material_level in base class data
        level = data.get("_level", 1)
        material_level = data.get("_material_level", 1)
        return cls(level, material_level)

    def __str__(self):
        material = WeaponMaterial[f"LEVEL_{self.get_material_level()}"].name
        level_info = WeaponLevel.from_level(self.get_level()).description
        return (
            f"{self.get_name()} ({level_info}, {material})\n"
            f"Description: {self.get_description()}\n"
            f"Level: {self.get_level()} | Material Level: {self.get_material_level()}\n"
            f"Damage: {self.get_damage()} | Value: {self.get_value()} gold"
        )

    def __repr__(self):
        return (
            f"Sword(name={self.get_name()!r}, "
            f"level={self.get_level()}, "
            f"material_level={self.get_material_level()}, "
            f"damage={self.get_damage()}, "
            f"value={self.get_value()})"
        )