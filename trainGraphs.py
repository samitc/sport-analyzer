import csv

from Tcx.TcxFile import Tcx

inputFile = "test.tcx"
outPutFile = "tst"
tcxFile = Tcx(inputFile)
tcxFile.readTcx()
activities = tcxFile.getActivities()
activityIndex = 0
for activity in activities:
    with open(outPutFile + str(activityIndex) + "BPM.csv", 'w', newline='') as csvFileBpm:
        with open(outPutFile + str(activityIndex) + "SPEED.csv", 'w', newline='') as csvFileSpeed:
            writerBpm = csv.writer(csvFileBpm, delimiter=',')
            writerSpeed = csv.writer(csvFileSpeed, delimiter=',')
            # writerBpm.writerow(["date", "time", "lat", "lon", "alt", "distance", "bpm"])
            writerBpm.writerow(["time", "bpm"])
            writerSpeed.writerow(["time", "speed"])
            preDistance = 0
            preTime = 0
            lapIndex = 0
            for lap in activity.laps:
                lapIndex = lapIndex + 1
                pointIndex = 0
                for point in activity.positions[lap.startPosition: lap.endPosition]:
                    pointIndex = pointIndex + 1
                    if point.pos is not None:
                        writerBpm.writerow([point.time.timestamp(), point.bpm])
                        curSpeed = 0
                        if point.time.timestamp() > preTime:
                            if preTime != 0:
                                curSpeed = (point.distance - preDistance) / (point.time.timestamp() - preTime)
                            writerSpeed.writerow([point.time.timestamp(), curSpeed])
                        preDistance = point.distance
                        preTime = point.time.timestamp()
    activityIndex = activityIndex + 1
