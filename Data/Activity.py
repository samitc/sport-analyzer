from Tcx.TcxFile import Tcx


class Activity:
    def __init__(self, tcxFile: Tcx):
        positions, laps = tcxFile.getPointsAndLaps()
        self.positions = positions
        self.laps = laps
