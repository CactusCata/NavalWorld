import utils.mathsUtils as mathsUtils
import sys
from time import time

sys.setrecursionlimit(8000)

class PathFinding:

    def __init__(self, map, nonObstacleArray, startPoint, objectivePoint):
        self.startingTime = time()
        self.dimX = len(map)
        self.dimY = len(map[0])
        self.map = map
        self.nonObstacleArray = nonObstacleArray
        self.startPoint = [int(startPoint[0]), int(startPoint[1])]
        self.objectivePoint = [int(objectivePoint[0]), int(objectivePoint[1])]

        self.openPointsMatrixPresence = createMatrixOf(1160, 900, 0)
        self.evaluedPointsMatrixPresence = createMatrixOf(1160, 900, 0)
        self.lowerFCosts = []
        for i in range(100):
            self.lowerFCosts.append([])

    def printArray(self, arrayOfPoints):
        for point in arrayOfPoints:
            print(f"y: {point.getX()} x: {point.getY()} DStart: {point.getGCost()} DEnd: {point.getHCost()} DTotal: {point.getFCost()}")

    def reach(self):
        openPoints = []
        evaluedPoints = []
        startingPoint = PointStats(self.startPoint[0], self.startPoint[1], 0, mathsUtils.distance(self.startPoint, self.objectivePoint))
        openPoints.append(startingPoint)
        self.lowerFCosts[len(bin(int(startingPoint.getFCost()))) - 3].append(startingPoint)
        self.openPointsMatrixPresence[self.startPoint[0]][self.startPoint[1]] = 1

        iterationCount = 0
        while len(openPoints) != 0:
            iterationCount += 1
            bestPoint = self.getLowerFCost()
            openPoints.remove(bestPoint)
            self.lowerFCosts[len(bin(int(bestPoint.getFCost()))) - 3].remove(bestPoint)
            self.openPointsMatrixPresence[bestPoint.getX()][bestPoint.getY()] = 0
            evaluedPoints.append(bestPoint)
            self.evaluedPointsMatrixPresence[bestPoint.getX()][bestPoint.getY()] = 1

            if time() - self.startingTime > 10 or bestPoint.getX() == self.objectivePoint[0] and bestPoint.getY() == self.objectivePoint[1]:
                #print(iterationCount)
                #print(f"taille d'openPoints: {len(openPoints)}")
                #print(f"taille d'evaluedPoints: {len(evaluedPoints)}")
                return bestPoint.getAllGeneration()

            for neighbours in self.getNeighbourOf(bestPoint):
                if self.evaluedPointsMatrixPresence[neighbours.getX()][neighbours.getY()] == 0:
                    if neighbours.getGenerationSize() > bestPoint.getGenerationSize() or self.openPointsMatrixPresence[neighbours.getX()][neighbours.getY()] == 0:
                        neighbours.setParent(bestPoint)
                        if self.evaluedPointsMatrixPresence[neighbours.getX()][neighbours.getY()] == 0:
                            openPoints.append(neighbours)
                            self.lowerFCosts[len(bin(int(neighbours.getFCost()))) - 3].append(neighbours)
                            self.openPointsMatrixPresence[neighbours.getX()][neighbours.getY()] = 1

        return []

    def getLowerFCost(self):
        i = 0
        while len(self.lowerFCosts[i]) == 0:
            i += 1

        lowersFCost = self.lowerFCosts[i]
        betterPointsF = lowersFCost[0]
        lowerF = betterPointsF.getFCost()
        for i in range(1, len(lowersFCost)):
            if lowersFCost[i].getFCost() < lowerF:
                betterPointsF = lowersFCost[i]
                lowerF = betterPointsF.getFCost()

        return betterPointsF

    def getNeighbourOf(self, parent):
        parentX = parent.getX()
        parentY = parent.getY()
        neighbours = []
        for i in {-1, 0, 1}:
            x = parentX + i
            for j in {-1, 0, 1}:
                y = parentY + j
                if j != 0 or i != 0:
                    if (not self.isOutOfBound(x, y)) and self.isTraversable(x, y):
                        gCost = parent.getGCost() + 0.1
                        hCost = mathsUtils.distance([x, y], self.objectivePoint)
                        neighbours.append(PointStats(x, y, gCost, hCost))
        return neighbours

    def isOutOfBound(self, x, y):
        return x < 0 or x > self.dimX - 1 or y < 0 or y > self.dimY - 1

    def isTraversable(self, x, y):
        return self.map[x][y] in self.nonObstacleArray

class PointStats:

    def __init__(self, x, y, gCost, hCost):
        self.x = x
        self.y = y
        self.gCost = gCost
        self.hCost = int(hCost)
        self.fCost = self.gCost + self.hCost
        self.parent = None
        self.generationSize = 0

    def getX(self):
        return self.x

    def setX(self, x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y):
        self.y = y

    def getGCost(self):
        """
        Distance from the beggining
        """
        return self.gCost

    def setGCost(self, gCost):
        self.gCost = gCost
        self.fCost = self.getFCost() + self.getGCost()

    def getHCost(self):
        """
        Distance to the objective point
        """
        return self.hCost

    def setHCost(self, hCost):
        self.hCost = hCost
        self.fCost = self.getFCost() + self.getGCost()

    def getFCost(self):
        """
        Sum of G and H cost
        """
        return self.fCost

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent
        self.setGCost(parent.getGCost() + 0.1)
        self.generationSize = self.getParent().getGenerationSize() + 1

    def getGenerationSize(self):
        return self.generationSize

    def getAllGeneration(self):
        if self.getParent() == None:
            return [self]
        else:
            return self.getParent().getAllGeneration() + [self]

def generateRandomMap(size):
    from random import random
    map = []
    for i in range(10):
        line = []
        for j in range(10):
            if random() > 0.6:
                line.append([int(random() * 255), int(random() * 255), int(random() * 255)])
            else:
                line.append([255, 255, 255])
        map.append(line)

    map[0][0] = [255, 255, 255]
    map[7][7] = [255, 255, 255]
    """
    map = []
    map.append([[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]])
    map.append([[255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 255, 255], [255, 0, 255], [255, 0, 255], [255, 255, 255]])
    map.append([[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]])
    map.append([[255, 255, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 255, 255]])
    map.append([[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]])
    map.append([[255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 255, 255], [255, 255, 255]])
    map.append([[255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 0, 255], [255, 255, 255], [255, 255, 255]])
    """
    return map

def inArray(toFind, array):
    for e in array:
        if e.getX() == toFind[0] and e.getY() == toFind[1]:
            return True
    return False

def createMatrixOf(dimX, dimY, defaultValue):
    matrix = []
    for i in range(dimY):
        matrix.append([defaultValue] * dimX)
    return matrix



def presentMap(map, arrayOpen, arrayCalculated):
    print((2 * len(map) + 1) * "-")
    y = 0
    for line in map:
        x = 0
        lineString = "|"
        for point in line:
            if inArray([y, x], arrayOpen):
                lineString += "O"
            elif inArray([y, x], arrayCalculated):
                lineString += "+"
            elif point == [255, 255, 255]:
                lineString += " "
            else:
                lineString += "X"
            x += 1
            lineString += "|"
        print(lineString)
        y += 1
    print((2 * len(map) + 1) * "-")

if __name__ == "__main__":
    map = generateRandomMap(10)
    #presentMap(map)

    pathFinding = PathFinding(map, [255, 255, 255], [2, 7], [8, 4])
    #generation = pathFinding.getNeighbourOf(PointStats(0, 0, 0, 10))
    generation = pathFinding.reach()
    #presentMap(map, [], [])

    for guy in generation:
        print(guy.getX(), guy.getY())
