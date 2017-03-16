import csv
import pandas as pd
import mysql.connector
import json

def getNewsPaperHistory():
    outputDict = dict()
    conn = mysql.connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                                   user='readonly', password='nestiareadonly', database='news')
    cursor = conn.cursor()
    cursor.execute('select device_id, news_ids, created_at from newspapers')
    queryResult = cursor.fetchall()
    cursor.close()
    conn.close()
    print('Query from database successfully')
    for record in queryResult:
        deviceId = record[0].decode('utf-8')
        newsList = set(json.loads(record[1].decode('utf-8')))
        date = record[2].strftime('%Y-%m-%d')
        if date not in outputDict.keys():
            outputDict.update({date: dict()})
        if deviceId not in outputDict[date].keys():
            outputDict[date].update({deviceId: set()})
        outputDict[date][deviceId] |= newsList
    print('Clean up output successfully')
    return outputDict