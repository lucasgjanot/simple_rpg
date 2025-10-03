
class Entity:

    def __init__(self, name, level, base_attack, base_armor, base_max_health=100, base_max_stamina=100):
        self._name = name
        self._level = level
        self.base_max_health = base_max_health
        self.base_max_stamina = base_max_stamina
        self._base_attack = base_attack
        self._base_armor = base_armor
        self._xp = 0
        self._update_stats()
        self._health = self._max_health
        self._stamina = self._max_stamina
    
    def __str__(self):
        return (f"{self.get_name()} (Level {self.get_level()})\n"
                f"XP: {self.get_xp()}/{self.get_xp_next_level()}\n"
                f"Health: {self.get_health()}/{self.get_max_health()}\n"
                f"Stamina: {self.get_stamina()}/{self.get_max_stamina()}\n"
                f"Attack: {self.get_attack()}\n"
                f"Armor: {self.get_armor()}")
    
    def __repr__(self):
        return (f"Entity(name={self.get_name()!r}, level={self.get_level()}, "
                f"max_health={self.get_max_health()}, max_stamina={self.get_max_stamina()}, "
                f"attack={self.get_attack()}, armor={self.get_armor()}, "
                f"xp={self.get_xp()}, xp_next_level={self.get_xp_next_level()})")
    
    def get_stats(self):
        return {
            "Name": self.get_name(),
            "Level": self.get_level(),
            "XP": f"{self.get_xp()}/{self.get_xp_next_level()}",
            "Health": f"{self.get_health()}/{self.get_max_health()}",
            "Stamina": f"{self.get_stamina()}/{self.get_max_stamina()}",
            "Attack": self.get_attack(),
            "Armor": self.get_armor(),
        }
    
    
    def _update_stats(self):
        self._max_health = self.base_max_health + (self._level - 1) * 10
        self._max_stamina = self.base_max_stamina + (self._level - 1) * 5
        self._xp_next_level = 100 + (self._level - 1) * 50
        self._attack = self._base_attack + (self._level - 1) * 3
        self._armor = self._base_armor + (self._level - 1) * 2

    def get_name(self):
        return self._name
    
    def get_level(self):
        return self._level

    def get_max_health(self):
        return self._max_health
    
    def get_health(self):
        return self._health
    
    def get_max_stamina(self):
        return self._max_stamina
    
    def get_stamina(self):
        return self._stamina
    
    def get_attack(self):
        return self._attack
    
    def get_armor(self):
        return self._armor

    def get_xp(self):
        return self._xp
    
    def get_xp_next_level(self):
        return self._xp_next_level
    
    def level_up(self):
        self._level +=1
        self._update_stats()
        self._health = self._max_health
        self._stamina = self._max_stamina

    def gain_xp(self,amount):
        self._xp += amount
        if self._xp >= self._xp_next_level:
            self._xp -= self._xp_next_level 
            self.level_up()

    def is_alive(self):
        return self._health > 0

    def take_damage(self, amount):
        damage_taken = max(0, amount - self.get_armor())
        self._health -= damage_taken
        if not self.is_alive():
            return f"{self.get_name()} has died."
        else:
            return f"{self.get_name()} took {damage_taken} damage. Current health: {self._health}/{self._max_health}"
        
    def restore_health(self,amount):
        if amount < 0:
            raise ValueError("Amount to restore cannot be negative.")
        if self._health == self._max_health:
            raise ValueError(f"{self.get_name()} is already at full health.")
        self._health = min(self._health + amount, self.base_max_health)

    def use_stamina(self,amount):
        if amount < 0:
            raise ValueError("Amount to restore cannot be negative.")
        if self._stamina < amount:
            raise ValueError(f"{self.get_name()} does not have enough stamina!")
        self._stamina -= amount

    def restore_stamina(self,amount):
        if amount < 0:
            raise ValueError("Amount to restore cannot be negative.")
        if self._stamina == self._max_stamina:
            raise ValueError(f"{self.get_name()} is already at full stamina.")
        self._stamina = min(self._stamina + amount, self._max_stamina)
    
    
    def attack_target(self, target):
        if not isinstance(target, Entity):
            raise ValueError("Target must be an Entity.")
        return target.take_damage(self.get_attack())
            
