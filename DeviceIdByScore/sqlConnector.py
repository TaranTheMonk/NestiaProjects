import mysql.connector
import json
from datetime import datetime

def getExistId():
    with open('../DeviceIdByScore/exist_id.json', 'r', encoding='utf-8') as f:
        existId = set(json.load(f))
    f.close()
    return existId

def getAllFromSql():
    existId = getExistId()

    conn = mysql.connector.connect(host='nestia-new-prod-rds.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                               user='readonly', password='nestiareadonly', database='notification', port='6603')
    cursor = conn.cursor()
    cursor.execute('select distinct(device_id) from devices')
    queryResult = cursor.fetchall()
    cursor.close()
    conn.close()
    for row in queryResult:
        if row[0] != None:
            deviceId = row[0].decode('utf-8')
            if deviceId in existId:
                existId.discard(deviceId)
    print(len(existId))
    existId = list(existId)
    with open('OffNotificationList.json', 'w', encoding='utf-8') as f:
        json.dump(existId, f)
    f.close()
    print('Finished')


getAllFromSql()
