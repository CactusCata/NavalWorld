import utils.db.DDBConnectionLoader as DDBConnectionLoader
import utils.db.DDBUtils as DDBUtils
import utils.mathsUtils as mathsUtils
import random
import tkinter
import numpy as np
from PIL import Image, ImageTk


if __name__ == "__main__":
    DDBConnectionLoader.createConnection()

    img = Image.open("../../../res/img/world_map.jpg")
    map = np.array(img).tolist()

    nonObstacleArray = [[5, 3, 50]]
    """
    for x in range(414, 510):
        for y in range(260, 340):
            if map[x][y] not in nonObstacleArray:
                nonObstacleArray.append(map[x][y])
    """

    ships = DDBUtils.prepareRequest(f"""
        SELECT Batiment.*
        FROM Batiment;
    """, 1)

    countShips = 1
    for ship in ships:
        print(f"Resolving ship number {countShips}: {ship}")
        countShips += 1
        shipXY = mathsUtils.GPSToCartesianCoordinates(ship[4] + random.randint(-5, 5), ship[5] + random.randint(-5, 5), 1160, 900)
        shipXY = (int(shipXY[0]), int(shipXY[1]))
        print(f"Starting: {shipXY}")
        while map[shipXY[1]][shipXY[0]] not in nonObstacleArray:
            shipLonLat = (ship[4] + random.randint(-5, 5), ship[5] + random.randint(-5, 5))
            shipXY = mathsUtils.GPSToCartesianCoordinates(shipLonLat[0], shipLonLat[1], 1160, 900)
            shipXY = (int(shipXY[0]), int(shipXY[1]))
            print(f"While : {shipXY}")
        shipLatLong = mathsUtils.cartesianCoordinatesToGPS(shipXY[0], shipXY[1], 1160, 900)
        print(f"final: {shipLatLong}")
        DDBUtils.updateRequest(f"""
            UPDATE Batiment
            SET latitude = {shipLatLong[0]},
                longitude = {shipLatLong[1]}
            WHERE Batiment.batiment_id = {ship[0]};
        """)

    DDBConnectionLoader.closeConnection()
