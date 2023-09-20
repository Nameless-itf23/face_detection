import json
import time

def write(user_id: str, date: int):
    with open('db.json') as f:
        db = json.load(f)
    if user_id not in db.keys():
        db[user_id] = []
    db[user_id].append(date)
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=2)

def trim(hour):  # 直近hour時間のデータのみにtrim
    with open('db.json') as f:
        db = json.load(f)
    now = time.time()
    for key, value in db.items():
        ans = []
        for i in value:
            if now - i < hour * 3600:
                ans.append(i)
        db[key] = ans
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=2)
