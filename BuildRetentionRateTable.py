import csv
import sys
import re
from datetime import datetime
import time
import os
import pandas as pd

class ModulePattern():
    def __init__(self, moduleName):
        self.moduleName = moduleName
        self.modulePattern = None

    def getModulePattern(self, moduleName):
        return

def defineModulePatterns():
    return



def getSystemArgs():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', sys.argv)
    startDate = sys.argv[1]
    stopDate = sys.argv[2]
    moduleName = sys.argv[3:]
    print('Start Date:', startDate)
    print('Stop Date:', stopDate)
    print('Module Name:', moduleName)
    return startDate, stopDate, moduleName

def oneMoreDay(previousDay):
    previousValue = time.mktime(time.strptime(previousDay, "%Y-%m-%d"))
    previousValue += 24*60*60
    Future = datetime.strftime(datetime.fromtimestamp(previousValue), "%Y-%m-%d")
    return Future

def main():
    validPattern = re.compile('[0-9A-Za-z/-]{36,36}|[0-9a-z]{12,16}')
    startDate, stopDate, moduleName = getSystemArgs()
    while startDate != stopDate:
        with open(os.path.expanduser('~/nestia_logs_with_parameters/data-' + startDate +'.csv'), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            try:
                for row in reader:
                    if validPattern.search(row[5]):
                        a = 1
            except:
                print()

if __name__ == '__main__':
    main()