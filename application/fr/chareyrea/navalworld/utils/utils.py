from os import listdir
from os.path import isfile, join

def getPictureOfShip(shipName):
    allPictures = [f for f in listdir("../../../res/img/Ships/") if isfile(join("../../../res/img/Ships/", f))]
    for picture in allPictures:
        if picture.split(".")[0] == shipName:
            return picture
    return None

def isInt(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
