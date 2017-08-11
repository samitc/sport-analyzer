from collections import defaultdict

from Data.GeoPos import GeoPos
from Data.Lap import Lap
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
        lapsD = []
        activities = Tcx.searchTree(self.data, "sActivity")
        if len(activities) > 1:
            return None
        for activity in activities:
            laps = Tcx.searchTree(activity, "sLap")
            index = 0
            for lap in laps:
                startLapPos = len(points)
                track = lap["sTrack"]
                trackPoints = Tcx.searchTree(track, "sTrackpoint")
                for trackPoint in trackPoints:
                    if trackPoint["position"] is None:
                        pos = None
                    else:
                        position = trackPoint["s" + "position"]
                        pos = GeoPos(float(position["LatitudeDegrees"].text()),
                                     float(position["LongitudeDegrees"].text()))
                    if trackPoint["BPM"] is None:
                        bpm = None
                    else:
                        bpmVal = trackPoint["sBPM"]
                        bpm = int(bpmVal["value"].text())
                    if trackPoint["AltitudeMeters"] is None:
                        alt = None
                    else:
                        alt = float(trackPoint["AltitudeMeters"].text())
                    if trackPoint["DistanceMeters"] is None:
                        dis = None
                    else:
                        dis = float(trackPoint["DistanceMeters"].text())
                    if bpm is not None or dis is not None or pos is not None or alt is not None:
                        points.append(Plot(pos, trackPoint["time"].text(), alt, dis, bpm))
                endLapPos = len(points)
                avgBpm = lap["savgBPM"]
                maxBpm = lap["smaxBPM"]
                lapsD.append(Lap(startLapPos, endLapPos, activity["Lap" + str(index)].attrib("StartTime"),
                                 float(lap["TotalTimeSeconds"].text()), float(lap["DistanceMeters"].text()),
                                 float(lap["MaximumSpeed"].text()), int(lap["Calories"].text()),
                                 int(avgBpm["value"].text()), int(maxBpm["value"].text())))
        return points, lapsD

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
        if position is not None:
            Tcx.readPosition(data["s" + "position"], position)
        heartRate = trackPoint.findSon(getFindString("HeartRateBpm"))
        data["BPM"] = heartRate
        if heartRate is not None:
            Tcx.readBPM(data["sBPM"], heartRate)

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
        data["TotalTimeSeconds"] = lap.findSon(getFindString("TotalTimeSeconds"))
        data["DistanceMeters"] = lap.findSon(getFindString("DistanceMeters"))
        data["MaximumSpeed"] = lap.findSon(getFindString("MaximumSpeed"))
        data["Calories"] = lap.findSon(getFindString("Calories"))
        avgHeartRate = lap.findSon(getFindString("AverageHeartRateBpm"))
        data["avgBPM"] = avgHeartRate
        Tcx.readBPM(data["savgBPM"], avgHeartRate)
        maxHeartRate = lap.findSon(getFindString("MaximumHeartRateBpm"))
        data["avgBPM"] = maxHeartRate
        Tcx.readBPM(data["smaxBPM"], maxHeartRate)
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
