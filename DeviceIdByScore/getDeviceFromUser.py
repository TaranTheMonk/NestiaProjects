import json
import csv

userId = list()
with open('TargetUserId.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        userId.append(row[0])
f.close()

with open('TargetUserId.json', 'w', encoding='utf-8') as f:
    json.dump(userId, f)
f.close()