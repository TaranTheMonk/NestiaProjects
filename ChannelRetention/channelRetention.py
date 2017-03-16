import json
import pandas as pd

def readChannelInfo():
    with open('channelInfo.json', 'r', encoding='utf-8') as f:
        channelInfo = json.load(f)
    f.close()
    return channelInfo

def cleanUpChannelInfo():
    channelDF = list()
    channelInfo = readChannelInfo()
    for deviceId in channelInfo.keys():
        channelDF.append([deviceId, channelInfo[deviceId]['link'], channelInfo[deviceId]['time']])
    counterDate = dict()
    counterChannel = dict()
    for item in channelDF:
        if not item[1] in counterChannel.keys():
            counterChannel.update({item[1]: 0})
        if not item[2] in counterDate.keys():
            counterDate.update({item[2]: 0})
        counterChannel[item[1]] += 1
        counterDate[item[2]] += 1
    pd.DataFrame(counterChannel, index=['Count']).T.to_csv('counterByLink.csv')
    pd.DataFrame(counterDate, index=['Count']).T.to_csv('counterByDate.csv')
    pd.DataFrame(channelDF).to_csv('channelDataFrame.csv', header=False, index=False)

if __name__ == '__main__':
    cleanUpChannelInfo()