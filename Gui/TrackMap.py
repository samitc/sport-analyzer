import math

from Data.GeoPos import GeoPos
from Gui.pygmaps import pygmaps


class TrackMap:
    def __init__(self):
        self.points = []
        self.colors = []

    @staticmethod
    def roundToCloser(num, roundTo):
        temp = num % roundTo
        if temp > roundTo / 2:
            return num - temp + roundTo
        else:
            return num - temp

    @staticmethod
    def floatDot2(num):
        temp = int(num * 100)
        afterDot = TrackMap.roundToCloser(temp % 100, 25)
        return int(temp / 100) + afterDot / 100

    def addPoints(self, points, color):
        self.points.append(points)
        self.colors.append(color)

    def calcMapPos(self):
        minPos = GeoPos(90, 90)
        maxPos = GeoPos(0, 0)
        widthInPixels = 1024
        for poses in self.points:
            for pos in poses:
                if pos is not None:
                    if minPos.lat > pos.lat:
                        minPos.lat = pos.lat
                    elif maxPos.lat < pos.lat:
                        maxPos.lat = pos.lat
                    if minPos.lon > pos.lon:
                        minPos.lon = pos.lon
                    elif maxPos.lon < pos.lon:
                        maxPos.lon = pos.lon
        dis = minPos.distance(maxPos) / widthInPixels
        cLat = (maxPos.lat + minPos.lat) / 2
        cLon = (maxPos.lon + minPos.lon) / 2
        tempZoom = (156543.03392 * math.cos(cLat * math.pi / 180)) / dis
        return cLat, cLon, TrackMap.floatDot2(math.log(tempZoom, 2))

    def draw(self, fileName):
        cLat, cLon, zoom = self.calcMapPos()
        mymap = pygmaps(cLat, cLon, zoom)
        for index in range(len(self.points)):
            mymap.addpath(
                list(map(
                    lambda pos:
                    (pos.lat, pos.lon),
                    self.points[index])), self.colors[index])
        mymap.draw(fileName)
