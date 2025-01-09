from math import *
from random import *
from vector import *
from hero import *
from events import *
from enemy import *
from dungeondata import DIALOGUE_DICTIONARY, ENEMY_DICTIONARY
from time import *

OFFSPRING_DISTRIBUTION = [20, 15, 15, 10, 10, 10, 5, 5, 5, 5]
SLEEP_TIME = 1

"""

GNA DUNGEON

by Will Kibel


This program is a rudimentary genetic algorithm (GNA) that optimizes the skill tree of the hero
based on how far they can traverse through the (randomly generated) dungeon.

Each generation contains a certain number of heroes, and only the top heroes (the ones that make it the furthest)
are able to reproduce and randomly seed the next generation. After several generations, the GNA
should converge on a single hero design that is most effective - for current balancing, that
generally lands around a 40-0-20 point distribution among the three stats.

The actual dungeon-crawling part is very similar to that of the non-GNA auto dungeon, just much more simplified.

    
"""

# MISC FUNCTIONS THAT I USE

# returns a random number between a min and a max
def getRandom(min, max):
    return min + (random() * (max - min))

# returns the first element of an array (needed for sort key)
def takeFirst(array):
    return array[0]

# return the index of the largest value in an array
def getIndexOfGreatest(array):
    greatestValue = array[0]
    greatestIndex = 0
    for i in range(array.__len__()):
        if array[i] > greatestValue:
            greatestIndex = i
            greatestValue = array[i]
    return greatestIndex

# return the index of the smallest value in an array
def getIndexOfLeast(array):
    leastValue = array[0]
    leastIndex = 0
    for i in range(array.__len__()):
        if array[i] < leastValue:
            leastIndex = i
            leastValue = array[i]
    return leastIndex

# returns an array of X random integers that sum up to N
def randomSumTo(x, n):
    temp = []
    for i in range(x):
        temp.append(n*(random())) #generate X random numbers from 0 to N
    tempSum = sum(temp)
    final = []
    for i in temp:
        final.append(round(n*(i/tempSum))) #populate final array with scaled versions of temp array numbers
    # exceptions - if array adds up to one more or one less than intended N
    if sum(final) > n:
        final[getIndexOfGreatest(final)] -= 1
    if sum(final) < n:
        final[getIndexOfLeast(final)] += 1
    return final


######################
# generate a dungeon #
######################

print("Generating dungeon...")

dungeon = []

enemyTally = []
for i in ENEMY_DICTIONARY:
    enemyTally.append(0)

NUM_FLOORS = 100

for i in range(NUM_FLOORS):
    eventTypeSeed = random()
    if eventTypeSeed>0.25: # encounter
        enemyTypeSeed = round(random()*(floor(i/NUM_FLOORS * ENEMY_DICTIONARY.__len__()))) 
        # right now this seeds randomly and KIND OF accounts for depth. not ideal though
        # the main issue is that at deeper depths, lower level enemies are just as likely 
        # to show up as higher level ones. how to fix?? idk. maybe I don't. this sucks.
        enemyNumberSeed = round(random()*3)
        if enemyNumberSeed == 0:
            enemyNumberSeed = 1
        # right now this seeds purely randomly. i hate this.        
        dungeon.append(event("ENCOUNTER", enemyNumberSeed, str(ENEMY_DICTIONARY[enemyTypeSeed].name)))
        enemyTally[enemyTypeSeed] += 1
    else: # dialogue (no other events for now)
        # the dialogue system doesn't (notably) affect the GNA, it's just left over from the standalone version
        dialogueSeed = round(random()*(DIALOGUE_DICTIONARY.__len__()-1)) # dialogues are chosen purely at random
        dungeon.append(event("DIALOGUE", DIALOGUE_DICTIONARY[dialogueSeed]))

# for i in range(20):
#     print()

sleep(SLEEP_TIME)

print("The dungeon has " + str(NUM_FLOORS) + " randomly seeded floors.")
print("It contains " + str(enemyTally[0]) + " slimes, " + str(enemyTally[1]) + " gremlins, " + str(enemyTally[2]) + " gnomes, " + str(enemyTally[3]) + " goblins, " + str(enemyTally[4]) + " bandits, " + str(enemyTally[5]) + " orcs, " + str(enemyTally[6]) + " scramblers, " + str(enemyTally[7]) + " trolls, " + str(enemyTally[8]) + " drakes, and " + str(enemyTally[9]) + " balrogs.")

input("Begin? ")

#############
# gna stuff #
#############

NUM_HEROES = 100
heroes = [] # array containing all heroes at the end of their journey
currentHeroes = [] # array containing all heroes + copies DURING their journey
bestHeroes = [] # array containing all the best heroes from each generation

pointsToAllot = 60

generation = 0

print("Generating " + str(NUM_HEROES) + " heroes.")
print("...")
sleep(SLEEP_TIME)

for i in range(NUM_HEROES): #CREATE ALL HEROES (first gen)

    currentRandomHero = randomSumTo(3, pointsToAllot) #array that contains randomized point distribution for hero

    player = hero(currentRandomHero[0], currentRandomHero[1], currentRandomHero[2])

    playerCopy = hero(player.vitality-10, player.defense-25, player.strength-10) # creates a pre-run, unchanging version of this hero

    # input("Enter the dungeon?")

    currentHeroes.append([player, playerCopy])

    # for i in currentHeroes:
    #     print("(" + str(i[0].vitality-10) + ", " + str(i[0].defense-25) + ", " + str(i[0].strength-10) + ")")

GNA_STOP_FLAG = False

while not GNA_STOP_FLAG:

    generation += 1

    ########################
    # traverse the dungeon #
    ########################

    # MOST OF THE LINES OF CODE THAT ARE COMMENTED OUT HERE ARE REMNANTS FROM THE STANDALONE (NON-GNA) VERSION

    heroes = []
    for i in currentHeroes:
        player = i[0]
        playerCopy = i[1]
        for currentEvent in dungeon:
            if player.hp == 0:
                break
            # sleep(SLEEP_TIME)
            hpLeftAsDecimal = player.hp/(10*player.vitality) # needs to change w/ hp balancing
            if currentEvent.type == "ENCOUNTER":
                currentEncounter = []
                # INIT MESSAGE
                # if currentEvent.numberOfEnemies == 1:
                #     print("A " + str(currentEvent.enemyType) + " blocks your way.")
                # elif currentEvent.numberOfEnemies == 2:
                #     print("A pair of " + str(currentEvent.enemyType) + "s block your way.")
                # else:
                #     print("A group of " + str(currentEvent.enemyType) + "s block your way.")
                # sleep(SLEEP_TIME)
                # print("...")
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
                    # sleep(SLEEP_TIME)
                    activeEnemies = [] # array of all enemies with positive health and their location in the "encounter" array
                    for i in currentEncounter:
                        if i.hp > 0:
                            activeEnemies.append((i, currentEncounter.index(i)))
                        # print(str(i.hp))
                # hero
                    # target a random enemy with positive health
                    targetedEnemyIndex = round(random()*activeEnemies.__len__()) # maybe this should not be random
                    if targetedEnemyIndex == 0:
                            targetedEnemyIndex = 1
                    targetedEnemy = activeEnemies[targetedEnemyIndex-1][1]
                    # attack that enemy
                    currentEncounter[targetedEnemy].hp -= int(player.strength)
                    if currentEncounter[targetedEnemy].hp < 0:
                        currentEncounter[targetedEnemy].hp = 0
                    # print("The hero dealt " + str(player.strength) + " damage to " + currentEvent.enemyType.capitalize() + " " + str(targetedEnemy+1) + ".")
                    # announce enemy health
                    enemiesDead = 0
                    for i in range(currentEvent.numberOfEnemies):
                        # sleep(SLEEP_TIME)
                        # print(currentEncounter[i].hp)
                        if not currentEncounter[i].hp > 0:
                            # print(currentEvent.enemyType.capitalize() + " " + str(i+1) + " has " + str(currentEncounter[i].hp) + " HP remaining.")
                        # else:
                            # print(currentEvent.enemyType.capitalize() + " " + str(i+1) + " is dead.")
                            enemiesDead += 1
                # check if all enemies dead
                    if enemiesDead == currentEvent.numberOfEnemies:
                        # sleep(SLEEP_TIME)
                        # print("...")
                        # sleep(SLEEP_TIME)
                        # print("Encounter complete! The hero has " + str(player.hp) + " HP remaining.")
                        # sleep(SLEEP_TIME)
                        # print()
                        break
                # update activeEnemies to account for deaths
                    activeEnemies = [] # array of all enemies with positive health and their location in the "encounter" array
                    for i in currentEncounter:
                        if i.hp > 0:
                            activeEnemies.append((i, currentEncounter.index(i)))
                    # sleep(SLEEP_TIME)
                    # print("...")
                # enemies (for each)
                    for i in activeEnemies:
                        # sleep(SLEEP_TIME)
                        # attack (if enemy health is over 0)
                        player.hp -= ((i[0].damage)-floor(float((player.defense/100)*i[0].damage))) #damage mitigation - the floor of defense% of damage is subtracted
                        # print(currentEvent.enemyType.capitalize() + " " + str(i[1]+1) + " dealt " + str((i[0].damage)-floor(float((player.defense/100)*i[0].damage))) + " damage to the hero.")
                        # announce hero health
                    if player.hp < 0:
                        player.hp = 0
                    # sleep(SLEEP_TIME)
                    # print("The hero has " + str(player.hp) + " HP remaining.")
                    # sleep(SLEEP_TIME)
                    # print("...")
                    # check if hero dead
                    if player.hp <= 0:
                        # print("The hero has perished.")
                        # print()
                        break
            # if currentEvent.type == "DIALOGUE":
            #     print(str(currentEvent.dialogueText))
            #     # sleep(SLEEP_TIME)
            #     print()
            # if input("Continue? ") != "": # uncomment this for manual control of floor traversal
            #     player.hp = 0
            #     print()
            #     sleep(SLEEP_TIME)
        # if player.hp > 0:
        #     sleep(SLEEP_TIME)
        #     # print("You have successfully cleared this dungeon. Congratulations, hero!")
        # if player.hp == 0:
        #     sleep(SLEEP_TIME)
            # print("You have failed the dungeon. Condolences, hero.")
            # print("You traversed " + str(dungeon.index(currentEvent)+1) + " rooms before dying.")
        playerCopy.count = dungeon.index(currentEvent)+1+hpLeftAsDecimal # count becomes current room number + amount of HP left prior to current encounter
        heroes.append(playerCopy) # for HP purposes

    heroSort = [] #make new array for sorting with all appropriate values
    for i in heroes:
        heroSort.append([i.count, i.vitality-10, i.defense-25, i.strength-10]) # need to remember to change this if balancing changes
    heroSort.sort(key=takeFirst, reverse=True) # could write my own sort function instead of doing this

    best = heroSort[0]
    print("The best hero in Generation " + str(generation) + " traversed " + str(floor(best[0])) + " floors before dying.")
    print("This hero had " + str(best[1]) + " points in Vitality, " + str(best[2]) + " points in Defense, and " + str(best[3]) + " points in Strength.")
    bestHeroes.append(best)

    # at this point, heroSort contains all the heroes in the generation, ranked from best to worst

    if generation > 5: # run GNA at least 5 times before checking to end it
        if bestHeroes[generation-1][1] == bestHeroes[generation-2][1] == bestHeroes[generation-3][1] == bestHeroes[generation-4][1] == bestHeroes[generation-5][1] and bestHeroes[generation-1][2] == bestHeroes[generation-2][2] == bestHeroes[generation-3][2] == bestHeroes[generation-4][2] == bestHeroes[generation-5][2] and bestHeroes[generation-1][3] == bestHeroes[generation-2][3] == bestHeroes[generation-3][3] == bestHeroes[generation-4][3] == bestHeroes[generation-5][3]:
        # check if the last 5 "best finishers" have the same point distribution
        # if they do, stop the program
            GNA_STOP_FLAG = True
            print("...")
            print("The optimal hero for this dungeon traverses " + str(floor(best[0])) + " floors and has a point distribution of (" + str(best[1]) + ", " + str(best[2]) + ", " + str(best[3]) + ").")
            print("The GNA took " + str(generation) + " generations to arrive at this solution.")
            print("Stopping GNA...")
            break

    ####################
    # create offspring #
    ####################

    variation = 1 # no real need for a shrinking variation at this time
    newGeneration = []

    for i in range(10): # top 10 finishers only
        for j in range(OFFSPRING_DISTRIBUTION[i] * int((NUM_HEROES/100))): # reproduce a certain number of times according to OFFSPRING_DISTRIBUTION
            newDist = []
            for k in range(3): # for each stat
                currentVar = heroSort[i][k+1] # get stat from finisher
                lowerBound = currentVar-variation
                if lowerBound < 0:
                    lowerBound = 0 # no negative stats in offspring
                newVar = getRandom(lowerBound, currentVar + variation) # get new random stat within a certain range of original stat
                newDist.append(newVar)
            tempSum = sum(newDist)
            for k in range(newDist.__len__()):
                newDist[k] = round((newDist[k]/tempSum) * pointsToAllot)
            # check if one too many points, take away from highest stat
            if sum(newDist) > pointsToAllot:
                newDist[getIndexOfGreatest(newDist)] -= 1
            # check if one too few points, take away from lowest stat
            if sum(newDist) < pointsToAllot:
                newDist[getIndexOfLeast(newDist)] += 1
            newGeneration.append([hero(newDist[0], newDist[1], newDist[2]), hero(newDist[0], newDist[1], newDist[2])]) # usable player and player copy

    currentHeroes = newGeneration

    sleep(SLEEP_TIME)