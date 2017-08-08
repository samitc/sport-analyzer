from collections import defaultdict

from Xml import Xml


def tree(): return defaultdict(tree)


def getFindString(search):
    GARMIN_SEARCH = "{" + Tcx.GARMIN_NAMESPACE + "}"
    return GARMIN_SEARCH + search


class Tcx:
    GARMIN_NAMESPACE = "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2"

    def __init__(self, tcxFilePath: str):
        self.tcxFilePath = tcxFilePath
        self.tcxFile = Xml.Xml(tcxFilePath)
        self.tcxFile.regNamespace('', self.GARMIN_NAMESPACE)

    def getRoot(self):
        return self.tcxFile.getRoot()

    def readTcx(self):
        root = self.getRoot()
        self.data = tree()
        activities = root.findSon(getFindString("Activities"))
        activityies = activities.findSons(getFindString("Activity"))
        index = 0
        for activitis in activityies:
            treeIndex = "Activity" + str(index)
            self.data[treeIndex] = activitis
            Tcx.readActivity(self.data["s" + treeIndex], activitis)
            index = index + 1

    @staticmethod
    def readPosition(data, position):
        data["LatitudeDegrees"] = position.findSon(getFindString("LatitudeDegrees"))
        data["LongitudeDegrees"] = position.findSon(getFindString("LongitudeDegrees"))

    @staticmethod
    def readTrackPoint(data, trackPoint):
        position = trackPoint.findSon(getFindString("Position"))
        data["position"] = position
        Tcx.readPosition(data["s" + "position"], position)

    @staticmethod
    def readTrack(data, track):
        trackPoints = track.findSons(getFindString("Trackpoint"))
        index = 0
        for trackPoint in trackPoints:
            treeIndex = "Trackpoint" + str(index)
            data[treeIndex] = trackPoint
            Tcx.readTrackPoint(data["s" + treeIndex], trackPoint)
            index = index + 1

    @staticmethod
    def readLap(data, lap):
        track = lap.findSon(getFindString("Track"))
        data["Track"] = track
        Tcx.readTrack(data["s" + "Track"], track)

    @staticmethod
    def readActivity(data, activity):
        Id = activity.findSon(getFindString("Id"))
        data["Id"] = Id
        laps = activity.findSons(getFindString("Lap"))
        index = 0
        for lap in laps:
            treeIndex = "Lap" + str(index)
            data[treeIndex] = lap
            Tcx.readLap(data["s" + treeIndex], lap)
            index = index + 1
