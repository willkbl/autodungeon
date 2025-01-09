from math import *
from random import *
from vector import *
from events import *

class hero:

#truthfully this class may not be necessary. we'll see

    def __init__(self):
        self.vitality = 10
        self.defense = 25
        self.strength = 10
        self.dexterity = 10
        self.hp = 10 * self.vitality