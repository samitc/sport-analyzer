from collections import defaultdict

from Data.GeoPos import GeoPos
from Data.Plot import Plot
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
    def searchTree(treeData, search):
        retVal = []
        for k, v in treeData.items():
            if str(k).startswith(search):
                retVal.append(v)
        return retVal

    def getPointsAndLaps(self):
        points = []
        startLaps = []
        activities = Tcx.searchTree(self.data, "sActivity")
        if len(activities) > 1:
            return None
        for activity in activities:
            laps = Tcx.searchTree(activity, "sLap")
            for lap in laps:
                startLaps.append(len(points))
                track = lap["s" + "Track"]
                trackPoints = Tcx.searchTree(track, "sTrackpoint")
                for trackPoint in trackPoints:
                    position = trackPoint["s" + "position"]
                    bpm = trackPoint["sBPM"]
                    points.append(Plot(
                        GeoPos(float(position["LatitudeDegrees"].text()), float(position["LongitudeDegrees"].text())),
                        trackPoint["time"].text()
                        , float(trackPoint["AltitudeMeters"].text()), float(trackPoint["DistanceMeters"].text()),
                        int(bpm["value"].text())))
        return points, startLaps

    @staticmethod
    def readPosition(data, position):
        data["LatitudeDegrees"] = position.findSon(getFindString("LatitudeDegrees"))
        data["LongitudeDegrees"] = position.findSon(getFindString("LongitudeDegrees"))

    @staticmethod
    def readTrackPoint(data, trackPoint):
        data["time"] = trackPoint.findSon(getFindString("Time"))
        data["AltitudeMeters"] = trackPoint.findSon(getFindString("AltitudeMeters"))
        data["DistanceMeters"] = trackPoint.findSon(getFindString("DistanceMeters"))
        position = trackPoint.findSon(getFindString("Position"))
        data["position"] = position
        Tcx.readPosition(data["s" + "position"], position)
        heartRate = trackPoint.findSon(getFindString("HeartRateBpm"))
        data["BPM"] = heartRate
        Tcx.readBPM(data["sBPM"], heartRate);

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

    @staticmethod
    def readBPM(data, heartRate):
        data["value"] = heartRate.findSon(getFindString("Value"))
