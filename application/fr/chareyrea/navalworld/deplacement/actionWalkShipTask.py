from PIL import Image
from time import time
import numpy as np
import utils.db.DDBUtils as DDBUtils
import utils.mathsUtils as mathsUtils
import deplacement.pathFindingA as pathFindingA
import random

INSTANCE = None

class WalkerShip:

    def __init__(self, canvas):
        self.canvas = canvas
        global INSTANCE
        INSTANCE = self

        img = Image.open("../../../res/img/world_map.jpg")
        self.map = np.array(img).tolist()
        self.nonObstacleArray = [[5, 3, 50]]

        actionsBatiment = DDBUtils.prepareRequest(f"""
            SELECT Action_Batiment.*
            FROM Action_Batiment;
        """, DDBUtils.ALL)

        self.deplacements = {}
        for actionBatiment in actionsBatiment:
            commandID = actionBatiment[0]
            batimentID = actionBatiment[1]
            latObjective = actionBatiment[2]
            longObjective = actionBatiment[3]
            latLonObjective = [latObjective, longObjective]
            latLonObjective = self.getSeaAccessible(latObjective, longObjective)
            self.addDeplacement(commandID, batimentID, latLonObjective[0], latLonObjective[1])

        self.startDeplacements()

    def getSeaAccessible(self, latObjective, longObjective):
        shipXY = mathsUtils.GPSToCartesianCoordinates(latObjective, longObjective, 1160, 900)
        shipXY = (int(shipXY[0]) + random.randint(-10, 10), int(shipXY[1]) + random.randint(-10, 10))
        while self.map[shipXY[1]][shipXY[0]] not in self.nonObstacleArray:
            shipLonLat = (latObjective + random.randint(-10, 10), longObjective + random.randint(-10, 10))
            shipXY = mathsUtils.GPSToCartesianCoordinates(shipLonLat[0], shipLonLat[1], 1160, 900)
            shipXY = (int(shipXY[0]), int(shipXY[1]))
        return mathsUtils.cartesianCoordinatesToGPS(shipXY[0], shipXY[1], 1160, 900)

    def addDeplacement(self, commandID, batimentID, latObjective, longObjective):
        xyObjective = mathsUtils.GPSToCartesianCoordinates(latObjective, longObjective, 1160, 900)
        latLongActual = DDBUtils.prepareRequest(f"""
            SELECT Batiment.latitude, Batiment.longitude
            FROM Batiment
            WHERE Batiment.batiment_id = {batimentID};
        """, DDBUtils.ONE)

        latLongActual = self.getSeaAccessible(latLongActual[0], latLongActual[1])

        xyActual = mathsUtils.GPSToCartesianCoordinates(latLongActual[0], latLongActual[1], 1160, 900)

        start = time()
        pathFinding = pathFindingA.PathFinding(self.map, self.nonObstacleArray, [xyActual[1], xyActual[0]], [xyObjective[1], xyObjective[0]])
        cases = pathFinding.reach()
        print(f"Time needed: {time() - start}s")
        self.deplacements[commandID] = {"currentCase": 0, "batimentID": batimentID, "cases": cases}


    def startDeplacements(self):

        toRemoveList = []

        for commandID, infos in self.deplacements.items():
            currentCase = infos["currentCase"]
            batimentID = infos["batimentID"]
            cases = infos["cases"]

            currentXY = cases[currentCase]
            currentLatLong = mathsUtils.cartesianCoordinatesToGPS(currentXY.getY(), currentXY.getX(), 1160, 900)
            DDBUtils.updateRequest(f"""
                UPDATE Batiment
                SET latitude = {currentLatLong[0]},
                    longitude = {currentLatLong[1]}
                WHERE Batiment.batiment_id = {batimentID};
            """)

            if currentCase >= len(cases) - 1:
                toRemoveList.append(commandID)
            elif currentCase + 2 >= len(cases):
                infos["currentCase"] = len(cases) - 1
            else:
                infos["currentCase"] += 2

        for commandID in toRemoveList:
            self.deplacements.pop(commandID)
            DDBUtils.prepareDelete(f"""
                DELETE FROM Command
                WHERE Command.command_id = {commandID};
            """)

        self.canvas.after(80, self.startDeplacements)
