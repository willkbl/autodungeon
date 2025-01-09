from math import *
from random import *
from vector import *
from hero import *
from events import *
from enemy import *

# enemy(name, hp, damage, dex)
ENEMY_DICTIONARY = [
    enemy("slime", 5, 1, 0),
    enemy("gremlin", 10, 3, 0),
    enemy("gnome", 15, 5, 0),
    enemy("goblin", 20, 5, 1),
    enemy("bandit", 30, 5, 3),
    enemy("orc", 50, 10, 0),
    enemy("scrambler", 80, 15, 6),
    enemy("troll", 100, 20, 0),
    enemy("drake", 200, 30, 0),
    enemy("balrog", 500, 50, 0),
]

DIALOGUE_DICTIONARY = [ # this truly serves no purpose in the GNA version - I was just messing around
    "Pressing onward, you see a pile of bones on your path. They aren’t identifiable as any creature you know of.",
    "The cold interior of the dungeon grows even colder - a grim omen of things to come.",
    "A lone flower grows out of the dungeon wall. How could it have survived down here?",
    "You hear a guttural noise echo from behind you. But when you turn, there’s nothing there.",
    "Your own footsteps echo all around, keeping the silence from entombing you.",
    "A low hum fills your ears, then quickly passes.",
    "A high pitched ringing fills your ears, then quickly passes.",
    "A chill goes down your spine as you move forward.",
    "The ceiling is low ahead, so you crawl through to the next area. ",
    "An indiscernible light briefly flickers at the end of the passage ahead of you, before going out completely.",
    "There’s writing on the walls in some ancient language. You can’t decipher it.",
    "Your hands grow clammy as you anticipate what horrors might lie ahead.",
    "When you think about it, you can’t remember anything from before the dungeon. Strange…",
    "Your hands start to shake as you think about what might lie on the path ahead of you.",
    "Your vision goes blurry for a second. What a splitting headache…",
    "Staring at your hands, you don’t recognize them. Whose body have you inhabited?",
    "You feel like an intruder in this world. Who is saying those words?",
    "A roar echoes throughout the cavern, some beast yet unseen. You draw your blade once more.",
    "There is an unidentifiable odor in the air. Perhaps the stench of corpses…",
    "You smell metal in the air. Bringing your hand up to your nose, you realize you’re bleeding.",
    "The sounds of a faraway harp reverberate throughout the hall. As you try to locate the source, it fades away into nothing.",
    "The wall turns into rows and rows of words in a language you can’t decipher. For a second, you see behind the curtain. Soon, you will forget again.",
    "Your sleeve is torn now, the result of a fierce battle - or perhaps a battle yet to come.",
    "Time does not work the same in here. There's something unreal about this place."
]