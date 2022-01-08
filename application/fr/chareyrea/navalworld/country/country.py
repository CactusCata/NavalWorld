from shapely.geometry.polygon import Polygon
import utils.mathsUtils as mathsUtils

class Country:

    def __init__(self, name, downRightPoint, upLeftPoint, arrayOfPolygon):
        self.name = name
        self.arrayOfPolygon = arrayOfPolygon
        self.downRightPoint = downRightPoint
        self.upLeftPoint = upLeftPoint

    def getName(self):
        return self.name

    def getArrayOfPolygon(self):
        return self.arrayOfPolygon

    def getDownRightPoint(self):
        return self.downRightPoint

    def getUpLeftPoint(self):
        return self.upLeftPoint

    def toJsonObject(self):
        return {'name': self.getName(), 'downRightPoint': self.getDownRightPoint(), 'upLeftPoint': self.getUpLeftPoint(), 'poly': self.getArrayOfPolygon()}

def loadFromRaw(name, arrayOfPolygon):
    print(name)
    if type(arrayOfPolygon[0][0][0]) == float: # Sometimes, there is only one polygon
        arrayOfPolygon = [arrayOfPolygon]
    startingPoint = mathsUtils.GPSToCartesianCoordinates(arrayOfPolygon[0][0][0][1], arrayOfPolygon[0][0][0][0], 1160, 900)
    minLeft = int(startingPoint[0])
    maxRight = int(startingPoint[0])
    maxUp = int(startingPoint[1])
    minDown = int(startingPoint[1])
    polygons = []
    for polyAndAntiPoly in arrayOfPolygon:
        polyCorrected = []
        for pointGPS in polyAndAntiPoly[0]:
            point = mathsUtils.GPSToCartesianCoordinates(pointGPS[1], pointGPS[0], 1160, 900)
            point = int(point[0]), int(point[1])
            if point not in polyCorrected:
                polyCorrected.append(tuple(point))
        polygons.append(polyCorrected)
    print(len(polygons))
    polygons = bernoulliFilter(polygons, 1160)
    print(len(polygons))
    leftRightUpDownCorner = mathsUtils.calculLeftRightUpDownCorner(polygons)
    downRightPoint = (leftRightUpDownCorner[1], leftRightUpDownCorner[3])
    upLeftPoint = (leftRightUpDownCorner[0], leftRightUpDownCorner[2])
    return Country(name, downRightPoint, upLeftPoint, polygons)

def loadFromRefined(countryProperties):
    polygons = []
    for poly in countryProperties["poly"]:
        if len(poly) > 2:
            polygons.append(Polygon(poly))
    return Country(countryProperties["name"],
                countryProperties["downRightPoint"],
                countryProperties["upLeftPoint"],
                polygons)

def bernoulliFilter(arrayOfPolygon, imageWidth):

    countPart = [0] * 10
    for poly in arrayOfPolygon:
        for point in poly:
            countPart[int((point[0] - 1) * 10 / imageWidth)] += 1
    print(countPart)

    if countPart[0] == 0 or countPart[9] == 0:
        return arrayOfPolygon

    print("--------------------------> Create poly remplacement")

    countLeft = countPart[0]
    countRight = 0

    i = 0
    while countPart[i] != 0:
        countLeft += countPart[i]
        i += 1


    middleZero = int((i + 1) * (imageWidth / 10))
    print(middleZero)
    while countPart[i] == 0:
        i += 1

    while i < 10:
        countRight += countPart[i]
        i += 1

    bernoulliFilterPolygons = []
    if countLeft > countRight:
        for poly in arrayOfPolygon:
            bernoulliFilterPoly = []
            for point in poly:
                if point[0] < middleZero:
                    bernoulliFilterPoly.append(point)
            bernoulliFilterPolygons.append(bernoulliFilterPoly)
    else:
        for poly in arrayOfPolygon:
            bernoulliFilterPoly = []
            for point in poly:
                if point[0] > middleZero:
                    bernoulliFilterPoly.append(point)
            bernoulliFilterPolygons.append(bernoulliFilterPoly)

    return bernoulliFilterPolygons
