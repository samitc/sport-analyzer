from datetime import datetime

from Data.GeoPos import GeoPos


class Plot:
    def __init__(self, geo: GeoPos, time: str, alt: float, distance: float, bpm: int):
        self.pos = geo
        self.time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ", tzinfo=None)
        self.alt = alt
        self.distance = distance
        self.bpm = bpm
