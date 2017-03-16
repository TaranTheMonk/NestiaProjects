import sqlConnector
import csv
import time
from datetime import datetime
import os

def oneMoreDay(previousDay):
    currentValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
    currentValue += 24*60*60
    future = datetime.strftime(datetime.fromtimestamp(currentValue), "%Y-%m-%d")
    return future

def identifyNewsCriterion(rawRequest):

def calculatorMain():
    newsPaperHistory = sqlConnector.getNewsPaperHistory()
    dateSet = set(newsPaperHistory.keys())
    for date in dateSet:
        path = os.path.expanduser('/Users/Taran/Desktop/AmazonKeys/dataStore/data-' + date + '.csv')
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    if validPattern.search(row[5]):
                        row[1]

            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('file %s, line %d' % (date, reader.line_num))
    return