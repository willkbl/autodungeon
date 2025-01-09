from math import *
from random import *
from vector import *
from events import *

class enemy:

    def __init__(self, name, hp, damage, dex):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.dex = dex