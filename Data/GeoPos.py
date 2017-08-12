import math


class GeoPos:
    EARTH_RADIUS_IN_KM = 6371.0
    EARTH_RADIUS_IN_METERS = EARTH_RADIUS_IN_KM * 1000

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.updateCache()

    def updateCache(self):
        self.latRad = math.radians(self.lat)
        self.lonRad = math.radians(self.lon)
        self.cosLat = math.cos(self.latRad)

    def distance(self, geoPos):
        self.updateCache()
        geoPos.updateCache()
        return self.fastDistance(geoPos)

    def fastDistance(self, geoPos):
        sdLat = math.sin((geoPos.latRad - self.latRad) / 2)
        sdLon = math.sin((geoPos.lonRad - self.lonRad) / 2)
        a = sdLat * sdLat + sdLon * sdLon * self.cosLat * geoPos.cosLat
        return self.EARTH_RADIUS_IN_METERS * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def __str__(self):
        return str(self.lat) + "," + str(self.lon)
