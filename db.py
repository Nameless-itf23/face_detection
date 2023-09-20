import json
import time

def write(user_id, date):
    with open('db.json') as f:
        db = json.load(f)
    db.append({'user_id':user_id, 'date':date})
    with open('db.json', 'w') as f:
        json.dump(db, f, indent=2)

def trim(hour):  # 直近hour時間のデータのみにtrim
    with open('db.json') as f:
        db = json.load(f)
    now = time.time()
    new_db = []
    for i in range(len(db)):
        if now - db[i]['date'] < hour * 3600:
            new_db.append(db[i])
    with open('db.json', 'w') as f:
        json.dump(new_db, f, indent=2)
