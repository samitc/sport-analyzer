import csv


class Csv:
    def __init__(self, activities):
        self.activities = activities

    def writeActivities(self, outPutFile):
        with open(outPutFile, 'w', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=',')
            writer.writerow(["activityIndex", "lapIndex", "date", "time", "lat", "lon", "alt", "distance", "bpm"])
            activityIndex = 0
            for activity in self.activities:
                lapIndex = 0
                for lap in activity.laps:
                    for point in activity.positions[lap.startPosition: lap.endPosition]:
                        if point.pos is not None:
                            writer.writerow(
                                [activityIndex, lapIndex, point.time.date(), point.time.time(), point.pos.lat,
                                 point.pos.lon, point.alt, point.distance, point.bpm])
                    lapIndex = lapIndex + 1
                activityIndex = activityIndex + 1
