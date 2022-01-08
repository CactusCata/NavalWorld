from tkinter import Canvas
from PIL import Image
import utils.mathsUtils as mathsUtils
import utils.db.DDBUtils as DDBUtils
from frame.navalFrame import NavalFrame

class BoatViewRealTimeFrame(NavalFrame):

    def __init__(self, master, regionID):
        super().__init__(master, "Real time view ships", 1160, 900)
        self.regionID = regionID
        self.ovalAlive = []
        super().enableCanvas()
        super().setBackgroundImage("../../../res/img/world_map.jpg")

        self.updateShipsView()

        super().loop()


    def updateShipsView(self):
        shipsPosLongLat = DDBUtils.prepareRequest(f"""
            SELECT Batiment.latitude, Batiment.longitude
            FROM Batiment
            WHERE Batiment.region_id = {self.regionID};
        """, 1)

        for oval in self.ovalAlive:
            super().deleteForm(oval)
        self.ovalAlive = []

        shipsPosXY = []
        for shipPosLongLat in shipsPosLongLat:
            shipsPosXY.append((mathsUtils.GPSToCartesianCoordinates(shipPosLongLat[0], shipPosLongLat[1], 1160, 900)))

        for shipPosXY in shipsPosXY:
            self.ovalAlive.append(super().drawCircle(shipPosXY[0], shipPosXY[1], 2))
        super().scheduleTask(80, self.updateShipsView)
