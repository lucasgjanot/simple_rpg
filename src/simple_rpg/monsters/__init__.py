from simple_rpg.monsters.monster import Monster
from simple_rpg.monsters.plant import Plant
from simple_rpg.monsters.goblin import Goblin
from simple_rpg.monsters.dragon import Dragon
import os

monsters = os.listdir("./src/simple_rpg/monsters")
monsters = list(filter(lambda x: ".py" in x, monsters))
monsters = list(filter(lambda x: '__init__.py' != x, monsters))
monsters = list(map(lambda x: x[:-3], monsters))
monsters = list(map(lambda x: x.capitalize(), monsters))

__all__ = [monsters]

