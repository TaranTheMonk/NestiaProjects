import csv
import pandas as pd
import re
import os
import sys
import time
from datetime import datetime
import json

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
        return int(intervalDays)

def main(startDate, stopDate):
    validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}')
    with open('OffNotificationList.json', 'r', encoding='utf-8') as f:
        validIdSet = set(json.load(f))
    f.close()
    newsPattern = re.compile('/news/\d+$')
    validIdPattern = re.compile('[0-9A-Za-z/-]{36,36}')
    intervalDays = TimeFunctions.computeIntervalDays(startDate, stopDate)
    outputDict = dict()
    output = list()
    headers = ['DeviceId', 'CountDays']
    currentDate = startDate
    dayNum = 0
    while currentDate != stopDate:
        headers.append(currentDate)
        path = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + currentDate + '.csv')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(line.replace('\0','') for line in f)
            for row in reader:
                if validIdPattern.match(row[5]):
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
        dayNum += 1
        currentDate = TimeFunctions.oneMoreDay(currentDate)

    for deviceId in outputDict.keys():
        tempTarget = outputDict[deviceId]
        output.append([deviceId] + [tempTarget.countDays] + tempTarget.newsRecord)
    output = list(filter(lambda row: row[0] in validIdSet, output))

    output = pd.DataFrame(output)
    output.columns = headers
    output.to_csv('DeviceNewsMatrix.csv', index=False)

if __name__ == '__main__':
    main('2017-02-01', '2017-03-15')