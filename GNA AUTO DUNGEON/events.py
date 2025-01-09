from math import *
from random import *
from vector import *
from hero import *

"""

EVENT SYSTEM (would matter more if I had other things happening)

initiate  an enemy encounter:
    event(ENCOUNTER, /number of enemies/, /enemy type/)
can reference:
    event.type
    event.numberOfEnemies
    event.enemyType


initiate dialogue:
    event(DIALOGUE, text)
can reference:
    event.type
    event.dialogueText

"""

class event:

    def __init__(self, type, *args):
        self.type = type
        if self.type == "ENCOUNTER":
            self.numberOfEnemies = int(args[0])
            self.enemyType = str(args[1])
        if self.type == "DIALOGUE":
            self.dialogueText = str(args[0])