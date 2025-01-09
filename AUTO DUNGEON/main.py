from math import *
from random import *
from vector import *
from hero import *
from events import *
from enemy import *
from dungeondata import DIALOGUE_DICTIONARY, ENEMY_DICTIONARY
from time import *

"""

GNA DUNGEON

by Will Kibel

TO-DO (in order):
    implement dexterity for both players and enemies
    skill check events
    pick up items w/ stat bonuses
    implement more stats
        ~something~ for critical hits (luck for random, something else for nonrandom)
        poise for counterattacks (might be pretty complicated)

"""

SLEEP_TIME = 1

player = hero()

for i in range(20):
    print()

pointsToAllot = 60
print("Welcome to GNA Dungeon.")
print("You are about to create your hero by allotting skill points into 3 unique skills.")
print("You can only allot " + str(pointsToAllot) + " points, so choose wisely.")
totalAllotted = 0

initVitality = int(input("How many points will you invest into Vitality? "))
while not totalAllotted + initVitality <= pointsToAllot:
    initVitality = int(input("Please enter a smaller number: "))
player.vitality += initVitality
totalAllotted += initVitality


initDefense = int(input("How many points will you invest into Defense? "))
while not totalAllotted + initDefense <= pointsToAllot:
    initDefense = int(input("Please enter a smaller number: "))
player.defense += initDefense
totalAllotted += initDefense


initStrength = int(input("How many points will you invest into Strength? "))
while not totalAllotted + initStrength <= pointsToAllot:
    initStrength = int(input("Please enter a smaller number: "))
player.strength += initStrength
totalAllotted += initStrength


# initDexterity = int(input("How many points will you invest into Dexterity? "))
# while not totalAllotted + initDexterity <= pointsToAllot:
#     initDexterity = int(input("Please enter a smaller number: "))
# player.dexterity += initDexterity
# totalAllotted += initDexterity


print()
print("Your hero's stats are:")
print("Vitality: " + str(player.vitality))
print("Defense: " + str(player.defense))
print("Strength: " + str(player.strength))
# print("Dexterity: " + str(player.dexterity))
print()

player.hp = 10 * player.vitality

input("Enter the dungeon?")

print("Generating dungeon...")



######################
# generate a dungeon #
######################

dungeon = []

NUM_FLOORS = 100

for i in range(NUM_FLOORS):
    eventTypeSeed = random()
    if eventTypeSeed>0.25: # encounter
        enemyTypeSeed = round(random()*(floor(i/100 * ENEMY_DICTIONARY.__len__()))) 
        # right now this seeds randomly and KIND OF accounts for depth. not ideal though
        # the main issue is that at deeper depths, lower level enemies are just as likely 
        # to show up as higher level ones. how to fix?? idk. maybe I don't. this sucks.
        enemyNumberSeed = round(random()*3)
        if enemyNumberSeed == 0:
            enemyNumberSeed = 1
        # right now this seeds purely randomly. i hate this.        
        dungeon.append(event("ENCOUNTER", enemyNumberSeed, str(ENEMY_DICTIONARY[enemyTypeSeed].name)))
    else: # dialogue (no other events for now)
        dialogueSeed = round(random()*(DIALOGUE_DICTIONARY.__len__()-1)) # dialogues are chosen purely at random
        dungeon.append(event("DIALOGUE", DIALOGUE_DICTIONARY[dialogueSeed]))


print()


# TELEMETRY - PRINT THE DUNGEON
# for i in dungeon:
#     print(str(i.type))
#     if i.type == "ENCOUNTER":
#         print(str(i.numberOfEnemies))
#         print(str(i.enemyType))
#     if i.type == "DIALOGUE":
#         print(str(i.dialogueText))



########################
# traverse the dungeon #
########################

for currentEvent in dungeon:
    if player.hp == 0:
        break
    sleep(SLEEP_TIME)
    if currentEvent.type == "ENCOUNTER":
        currentEncounter = []
        # INIT MESSAGE
        if currentEvent.numberOfEnemies == 1:
            print("A " + str(currentEvent.enemyType) + " blocks your way.")
        elif currentEvent.numberOfEnemies == 2:
            print("A pair of " + str(currentEvent.enemyType) + "s block your way.")
        else:
            print("A group of " + str(currentEvent.enemyType) + "s block your way.")
        sleep(SLEEP_TIME)
        print("...")
        # find list index of enemy in encounter
        for i in ENEMY_DICTIONARY:
            if i.name == currentEvent.enemyType:
                enemyIndex = ENEMY_DICTIONARY.index(i)
        # populate encounter with unique enemies of the right type
        for i in range(currentEvent.numberOfEnemies):
            currentEncounter.append(enemy(ENEMY_DICTIONARY[enemyIndex].name, ENEMY_DICTIONARY[enemyIndex].hp, ENEMY_DICTIONARY[enemyIndex].damage, ENEMY_DICTIONARY[enemyIndex].dex)) #CAUSING PROBLEMS RIGHT NOW
        # at this point, currentEncounter[] is an array containing every enemy in the encounter, along with their hp, damage, and dex
        ENCOUNTER_FLAG = True
        while ENCOUNTER_FLAG == True:
            sleep(SLEEP_TIME)
            activeEnemies = [] # array of all enemies with positive health and their location in the "encounter" array
            for i in currentEncounter:
                if i.hp > 0:
                    activeEnemies.append((i, currentEncounter.index(i)))
                # print(str(i.hp))
        # hero
            # target a random enemy with positive health
            targetedEnemyIndex = round(random()*activeEnemies.__len__())
            if targetedEnemyIndex == 0:
                    targetedEnemyIndex = 1
            targetedEnemy = activeEnemies[targetedEnemyIndex-1][1]
            # attack that enemy
            currentEncounter[targetedEnemy].hp -= int(player.strength)
            if currentEncounter[targetedEnemy].hp < 0:
                currentEncounter[targetedEnemy].hp = 0
            print("The hero dealt " + str(player.strength) + " damage to " + currentEvent.enemyType.capitalize() + " " + str(targetedEnemy+1) + ".")
            # announce enemy health
            enemiesDead = 0
            for i in range(currentEvent.numberOfEnemies):
                sleep(SLEEP_TIME)
                # print(currentEncounter[i].hp)
                if currentEncounter[i].hp > 0:
                    print(currentEvent.enemyType.capitalize() + " " + str(i+1) + " has " + str(currentEncounter[i].hp) + " HP remaining.")
                else:
                    print(currentEvent.enemyType.capitalize() + " " + str(i+1) + " is dead.")
                    enemiesDead += 1
        # check if all enemies dead
            if enemiesDead == currentEvent.numberOfEnemies:
                sleep(SLEEP_TIME)
                print("...")
                sleep(SLEEP_TIME)
                print("Encounter complete! The hero has " + str(player.hp) + " HP remaining.")
                sleep(SLEEP_TIME)
                print()
                break
        # update activeEnemies to account for deaths
            activeEnemies = [] # array of all enemies with positive health and their location in the "encounter" array
            for i in currentEncounter:
                if i.hp > 0:
                    activeEnemies.append((i, currentEncounter.index(i)))
            sleep(SLEEP_TIME)
            print("...")
        # enemies (for each)
            for i in activeEnemies:
                sleep(SLEEP_TIME)
                # attack (if enemy health is over 0)
                player.hp -= ((i[0].damage)-floor(float((player.defense/100)*i[0].damage))) #damage mitigation - the floor of defense% of damage is subtracted
                print(currentEvent.enemyType.capitalize() + " " + str(i[1]+1) + " dealt " + str((i[0].damage)-floor(float((player.defense/100)*i[0].damage))) + " damage to the hero.")
                # announce hero health
            if player.hp < 0:
                player.hp = 0
            sleep(SLEEP_TIME)
            print("The hero has " + str(player.hp) + " HP remaining.")
            sleep(SLEEP_TIME)
            print("...")
            # check if hero dead
            if player.hp <= 0:
                print("The hero has perished.")
                print()
                break
    if currentEvent.type == "DIALOGUE":
        print(str(currentEvent.dialogueText))
        sleep(SLEEP_TIME)
        print()
    if input("Continue? ") != "": # uncomment this for manual control of floor traversal
        player.hp = 0
        print()
if player.hp > 0:
    sleep(SLEEP_TIME)
    print("You have successfully cleared this dungeon. Congratulations, hero!")
if player.hp == 0:
    sleep(SLEEP_TIME)
    print("You have failed the dungeon. Condolences, hero.")
    print("You traversed " + str(dungeon.index(currentEvent)-1) + " rooms before dying.")