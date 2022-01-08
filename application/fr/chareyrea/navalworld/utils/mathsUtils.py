from math import log, pi, tan, sqrt, pow, exp, atan

def GPSToCartesianCoordinates(latitude, longitude, mapWidth, mapHeight):
    x = (longitude + 180) * (mapWidth / 360)
    latitudeRad = latitude * pi / 180
    mercN = 0
    try:
        mercN = log(tan((pi / 4) + (latitudeRad / 2)))
    except ValueError:
        return GPSToCartesianCoordinates(-89.9, longitude, mapWidth, mapHeight)
    y = (mapHeight / 2) - (mapWidth * mercN / (2 * pi))
    return x, y

def cartesianCoordinatesToGPS(x, y, mapWidth, mapHeight):
    long = ((x * 360) / mapWidth) - 180
    mercN = ((-y + (mapHeight / 2)) * 2 * pi) / mapWidth
    latitudeRad = 2 * atan(exp(mercN)) - pi/2
    lat = latitudeRad * 180 / pi
    return lat, long

def calculLeftRightUpDownCorner(arrayOfPolygon):
    left = arrayOfPolygon[0][0][0]
    right = arrayOfPolygon[0][0][0]
    up = arrayOfPolygon[0][0][1]
    down = arrayOfPolygon[0][0][1]
    for poly in arrayOfPolygon:
        for point in poly:
            if point[0] < left:
                left = point[0]
            if point[0] > right:
                right = point[0]
            if point[1] < down:
                down = point[1]
            if point[1] > up:
                up = point[1]
    return left, right, up, down

def distance(point1, point2):
    return sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2))

if __name__ == "__main__":

    """
    x = 518
    y = 23
    longLat = cartesianCoordinatesToGPS(518, 23, 1160, 900)
    print(GPSToCartesianCoordinates(longLat[0], longLat[1], 1160, 900))
    """

    convertedCoordinates = cartesianCoordinatesToGPS(728, 530, 1160, 900)
    print(int(convertedCoordinates[0]), int(convertedCoordinates[1]))
