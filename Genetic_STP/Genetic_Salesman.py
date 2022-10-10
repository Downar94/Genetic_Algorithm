import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import numpy as np
import imageio
import os

cityList = {}
cityNumber = 20
chromosomeNumber = 40
mutationRate = 0.6
iterationNumber = 50
distancePlot = {}
x_values = []
y_values = []
screenNumber = 0
files = []

for i in range(cityNumber):
    cityList[i] = {
        'x' : int(rd.random() * 100), 
        'y' : int(rd.random() * 100)
        }
    
cityList = pd.DataFrame(cityList).transpose()

def distance(cityList, startCity, endCity):
    distanceX = abs(cityList.loc[startCity]['x'] - cityList.loc[endCity]['x'])
    distanceY = abs(cityList.loc[startCity]['y'] - cityList.loc[endCity]['y'])
    distance = np.sqrt(distanceX ** 2 + distanceY ** 2)
    
    return distance

def generateChromosome(cityList):
    chromosome = cityList.sample(n = cityNumber).index.values.tolist()
    
    return chromosome

def generatePopulation(cityList, chromosomeNumber):
    population = []
    
    for i in range(chromosomeNumber):
        population.append(generateChromosome(cityList))
        
    return population
    
def fintessFunction(cityList, chromosome):
    rating = 0
    totalDistance = 0
    
    for i in range(len(chromosome) - 1):
        totalDistance += distance(cityList, chromosome[i], chromosome[i + 1])
    totalDistance += distance(cityList, chromosome[len(chromosome)-1], chromosome[0])
    rating = 1 / totalDistance
    
    return rating
        
def rankSelection(cityList, population):
    selectionRanking = {}
    rank = len(population)
    
    for i in range(len(population)):
        selectionRanking[i] = fintessFunction(cityList, population[i])
    selectionRanking = {k: v for k, v in sorted(selectionRanking.items(), key=lambda item: item[1], reverse = True)}
    for key in selectionRanking:
        selectionRanking[key] = rank
        rank -= 1
    
    return selectionRanking

def selectPotentialParents(cityList, population):
    parents = []
    parentsIds = []
    parentsRank = []
    selected = rankSelection(cityList, population)
    probabilityDivisor = 0
    parentNumber = int(0.8 * len(population))
    eliteSize = int(0.1 * parentNumber)
    
    for ids in selected:
        parentsIds.append(ids)
        parentsRank.append(selected[ids])
        probabilityDivisor += selected[ids]
        
    parents.extend(parentsIds[0:eliteSize])
    probabilityDivisor -= sum(parentsRank[0:eliteSize])
    del parentsRank[0:eliteSize]
    del parentsIds[0:eliteSize]
    parentsRank = [parentRank / probabilityDivisor for parentRank in parentsRank]

    parents.extend(np.random.choice(parentsIds, size = (parentNumber-eliteSize), replace = False, p = parentsRank))

    return parents

def createChildren(potentialParents, population, cityNumber):
    child = []
    children = []
    chosenParents = []
    childrenNumber = len(population) - len(potentialParents) 
    eliteSize = int(0.1 * len(potentialParents))

    chosenParents = rd.sample(potentialParents[eliteSize:], childrenNumber - eliteSize)
    chosenParents.extend(potentialParents[:eliteSize])
    crossoverPoint = int(cityNumber / 2)
    for i in range(len(chosenParents)):
        child = []
        child.extend(population[chosenParents[i]][:crossoverPoint])
        for element in population[chosenParents[len(chosenParents)-i-1]]:
            if element not in child:
                child.append(element)
        children.append(child)

    return children

def mutateChildren(children, mutationRate):
    firstMutatedGene = 0
    secondMutatedGene = 0
    
    for i in range(len(children)):
        if rd.random() < mutationRate:          
            firstMutatedGene = int(rd.random() * len(children[i]))
            secondMutatedGene = int(rd.random() * len(children[i]))
            while firstMutatedGene == secondMutatedGene:
                firstMutatedGene = int(rd.random() * len(children[i]))
                secondMutatedGene = int(rd.random() * len(children[i]))
                
            temp = children[i][firstMutatedGene]
            children[i][firstMutatedGene] = children[i][secondMutatedGene]
            children[i][secondMutatedGene] = temp
            
    return children
            
     
def createNextPopulation(children, potentialParents, population):
    nextPopulation = []   
    for i in range(len(potentialParents)):
        nextPopulation.append(population[potentialParents[i]])
    nextPopulation.extend(children)

    return nextPopulation
        
def geneticAlgorithm(cityList, childrenNumber, mutationRate, iterationNumber):
    population = generatePopulation(cityList, chromosomeNumber)
    firstRank = rankSelection(cityList, population)
    firstDistance = 1 / fintessFunction(cityList, population[list(firstRank.keys())[0]])
    distancePlot[0] = {
        'iteration' : 0, 
        'distance' : firstDistance
        }
    bestRoute = list(firstRank.keys())[0]
    print('shortest distance: ', firstDistance)

    for u in range(iterationNumber):
        print('iteration:' + str(u))
        selectedPotentialParents = selectPotentialParents(cityList, population)
        children = createChildren(selectedPotentialParents, population, cityNumber)
        mutatedChildren = mutateChildren(children, mutationRate)
        population = createNextPopulation(mutatedChildren, selectedPotentialParents, population)
        nextRank = rankSelection(cityList, population)
        nextDistance = 1 / fintessFunction(cityList, population[list(nextRank.keys())[0]])
        distancePlot[u+1] = {
            'iteration' : u+1, 
            'distance' : nextDistance
        }
        print('shortest distance: ', nextDistance)
        
    return population
    
finalPopulation = geneticAlgorithm(cityList, chromosomeNumber, mutationRate, iterationNumber)

finalRank = rankSelection(cityList, finalPopulation)
finalDistance = 1 / fintessFunction(cityList, finalPopulation[list(finalRank.keys())[0]])

distancePlot = pd.DataFrame(distancePlot).transpose()

bestRoute = list(finalRank.keys())[0]

plt.ion()
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)
xlim=(0,100)
ylim=(0,100)
plt.xlabel("x coordinate")
plt.ylabel("y coordinate")
scatter = ax.scatter(x = cityList['x'], y = cityList['y'], color = 'black')
plt.show()
plt.savefig('images/{}.png'.format(screenNumber))
screenNumber += 1 
plt.pause(0.2)

for city in finalPopulation[bestRoute]:
    print('visited city: \n x: ' + str(cityList.loc[city, 'x']) + '\n y: ' + str(cityList.loc[city, 'y']))
    x_values.append(cityList.loc[city, 'x'])
    y_values.append(cityList.loc[city, 'y'])
    ax.plot(x_values,y_values, color = 'b')
    fig.canvas.draw_idle()
    plt.savefig('images/{}.png'.format(screenNumber))
    screenNumber += 1 
    plt.pause(0.5)

x_values.append(cityList.loc[finalPopulation[bestRoute][0], 'x'])
y_values.append(cityList.loc[finalPopulation[bestRoute][0], 'y'])
ax.plot(x_values,y_values, color = 'b')
fig.canvas.draw_idle()
plt.savefig('images/{}.png'.format(screenNumber))
screenNumber += 1 
plt.pause(0.5)

for i in range(cityNumber + 2):    
    files.append('{}.png'.format(i))
image_path = [os.path.join('images',file) for file in files]
images = []

for img in image_path:
    images.append(imageio.imread(img))
    
imageio.mimwrite('result/result.gif', images, fps = 2)

plt.figure(figsize=(10,10))
ax = plt.gca()
distancePlot.plot(x = 'iteration' , y = 'distance', ax = ax)

print(distancePlot)
