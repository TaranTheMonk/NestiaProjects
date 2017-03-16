import csv
import pandas as pd
from datetime import datetime
import time
import os
import re

def oneMoreDay(previousDay):
    currentValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
    currentValue += 24*60*60
    future = datetime.strftime(datetime.fromtimestamp(currentValue), "%Y-%m-%d")
    return future

def timeStr2Num(strTime):
    numTime = time.mktime(time.strptime(strTime, "%Y-%m-%d"))
    return numTime

def calculator(startDate, stopDate):
    #Build variables
    channelDF = pd.read_csv('channelDataFrame.csv')
    channelDF = channelDF.values.tolist()
    userDict = dict()
    outputSaver = dict()
    dateChannelPairSet = set()

    for record in channelDF:
        ##[id, channel, date]
        dateChannelPairSet.add((record[2], record[1]))
        ##dict structure:{date: {channel: ..}
        if not record[2] in userDict.keys():
            userDict.update({record[2]: dict()})
            outputSaver.update({record[2]: dict()})
        if not record[1] in userDict[record[2]].keys():
            userDict[record[2]].update({record[1]: set()})
            outputSaver[record[2]].update({record[1]: [0]})
        userDict[record[2]][record[1]].add(record[0])
        outputSaver[record[2]][record[1]][0] = len(userDict[record[2]][record[1]])

    currentDate = startDate
    while currentDate != stopDate:
        bufferSet = set()
        path = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + currentDate + '.csv')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    bufferSet.add(row[5])
            except:
                    pass
        f.close()
        for dateChannelPair in dateChannelPairSet:
            if timeStr2Num(currentDate) >= timeStr2Num(dateChannelPair[0]):
                dateLabel = dateChannelPair[0]
                channelLabel = dateChannelPair[1]
                try:
                    outputSaver[dateLabel][channelLabel].append(
                        round(len(userDict[dateLabel][channelLabel] & bufferSet) / outputSaver[dateLabel][channelLabel][0], 3))
                except:
                    pass
        print(currentDate)
        currentDate = oneMoreDay(currentDate)
    return outputSaver

if __name__ == '__main__':
    output = calculator('2017-03-01', '2017-03-15')
    pd.DataFrame(output).to_csv('retention4channel.csv')