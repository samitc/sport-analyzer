class Lap:
    def __init__(self, startPosition: int, endPosition: int, startTime: str, totalTime: float, totalDistance: float,
                 maxSpeedInMPH: float, cal: int, avgBMP: int, maxBMP: int):
        self.startPosition = startPosition
        self.endPosition = endPosition
        import dateutil.parser
        self.startTime = dateutil.parser.parse(startTime)
        self.totalTime = totalTime
        self.totalDistance = totalDistance
        self.maxSpeedInMPH = maxSpeedInMPH
        self.cal = cal
        self.avgBMP = avgBMP
        self.maxBMP = maxBMP
