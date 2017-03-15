import csv
import pandas as pd
import re
import os
import sys
import time
from datetime import datetime

class UserProfile():
    def __init__(self, deviceId, totalDays):
        self.deviceId = deviceId
        self.countFlag = False
        self.countDays = 0
        self.tempCounter4News = 0
        self.newsRecord = [0] * totalDays
        self.output = None

    def resetTempCounter4News(self):
        self.tempCounter4News = 0

    def addCounter2Record(self, specificDay):
        self.newsRecord[specificDay] = self.tempCounter4News

    def setCountFlagTrue(self):
        self.countFlag = True

    def setCountFlagFalse(self):
        self.countFlag = False

class TimeFunctions():
    def oneMoreDay(previousDay):
        currentValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
        currentValue += 24*60*60
        future = datetime.strftime(datetime.fromtimestamp(currentValue), "%Y-%m-%d")
        return future

    def computeIntervalDays(startDate, stopDate):
        startValue = time.mktime(time.strptime(startDate, "%Y-%m-%d"))
        stopValue = time.mktime(time.strptime(stopDate, "%Y-%m-%d"))
        intervalDays = (stopValue - startValue)/(24*60*60)
        return intervalDays

def main(startDate, stopDate):
    newsPattern = re.compile('/news/\d+$')
    intervalDays = TimeFunctions.computeIntervalDays(startDate, stopDate)
    outputDict = dict()
    output = list()
    headers = []
    currentDate = startDate
    dayNum = 0
    while currentDate != stopDate:
        headers.append(currentDate)
        path = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + currentDate + '.csv')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(line.replace('\0','') for line in f)
            for row in reader:
                if not row[5] in outputDict.keys():
                    outputDict[row[5]] = UserProfile(row[5], intervalDays)
                if newsPattern.search(row[1]):
                    outputDict[row[5]].tempCounter4News += 1
                    outputDict[row[5]].setCountFlagTrue()
            f.close()
            for deviceId in outputDict.keys():
                tempTarget = outputDict[deviceId]
                if tempTarget.countFlag:
                    tempTarget.countDays += 1
                    tempTarget.addCounter2Record(dayNum)
                    tempTarget.resetTempCounter4News()
                    tempTarget.setCountFlagFalse()
                else:
                    continue
        print(currentDate)
        currentDate = TimeFunctions.oneMoreDay(currentDate)

    for deviceId in outputDict.keys():
        tempTarget = outputDict[deviceId]
        if tempTarget.countDays >= 10:
            output.append([deviceId] + tempTarget.newsRecord)

    output = pd.DataFrame(output)
    output.columns = headers
    output.to_csv('DeviceNewsMatrix.csv', index=False)

if __name__ == '__main__':
    main('2017-02-01', '2017-03-15')