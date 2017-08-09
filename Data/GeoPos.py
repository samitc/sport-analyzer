import math


class GeoPos:
    EARTH_RADIUS_IN_KM = 6371.0
    EARTH_RADIUS_IN_METERS = EARTH_RADIUS_IN_KM * 1000

    def __init__(self, lat: float, lon: float):
        self.lat = lat
        self.lon = lon
        self.latRad = math.radians(lat)
        self.lonRad = math.radians(lon)
        self.cosLat = math.cos(self.latRad)

    def distance(self, geoPos):
        sdLat = math.sin((geoPos.latRad - self.latRad) / 2)
        sdLon = math.sin((geoPos.lonRad - self.lonRad) / 2)
        a = sdLat * sdLat + sdLon * sdLon * self.cosLat * geoPos.cosLat
        return self.EARTH_RADIUS_IN_METERS * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
