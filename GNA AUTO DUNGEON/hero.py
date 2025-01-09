from math import *
from random import *
from vector import *
from events import *

class hero:

    # def __init__(self): #initialize without inputs
    #     self.vitality = 10
    #     self.defense = 25
    #     self.strength = 10
    #     self.hp = 0
    #     self.count = 0

    def __init__(self, vitality, defense, strength): #initialize with skill point inputs
        self.vitality = vitality + 10
        self.defense = defense + 25
        self.strength = strength + 10
        self.hp = 10 * vitality
        self.count = 0