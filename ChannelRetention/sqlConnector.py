import mysql.connector
import json
from datetime import datetime

def getChannelInfo():
    channelDict = dict()
    conn = mysql.connector.connect(host='prod-mysql-nestia-food.cd29ypfepkmi.ap-southeast-1.rds.amazonaws.com',
                                   user='statistics', password='nGVHAY2Hgf6t', database='base_info')
    cursor = conn.cursor()
    cursor.execute('select content, user_agent from log where source = 1')
    queryResult = cursor.fetchall()
    for valuePair in queryResult:
        content = json.loads(valuePair[0].decode('utf-8'))
        user_agent = valuePair[1].decode('utf-8')
        deviceId = user_agent.split(';')[-1].strip(' )')
        if not deviceId in channelDict.keys():
            channelDict.update({deviceId: list()})
        channelDict[deviceId].append(content)
    return channelDict

def saveChannelInformation():
    channelInfo = dict()
    rawChannelInfo = getChannelInfo()
    for deviceId in rawChannelInfo.keys():
        for infoMap in rawChannelInfo[deviceId]:
            try:
                link = infoMap['~referring_link']
                timeStamp = infoMap['+click_timestamp']
                timeStamp = datetime.fromtimestamp(timeStamp).strftime('%Y-%m-%d')
                channelInfo.update({deviceId: {'link':link, 'time': timeStamp}})
            except:
                pass
    with open('channelInfo.json', 'w', encoding='utf-8') as wf:
        json.dump(channelInfo, wf)
    wf.close()


if __name__ == '__main__':
    saveChannelInformation()