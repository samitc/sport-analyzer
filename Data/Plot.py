from Data.GeoPos import GeoPos


class Plot:
    def __init__(self, geo: GeoPos, time: str, alt: float, distance: float, bpm: int):
        self.pos = geo
        import dateutil.parser
        self.time = dateutil.parser.parse(time)
        self.alt = alt
        self.distance = distance
        self.bpm = bpm
