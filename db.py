import json
import time
import datetime
import zoneinfo
import os

db_path = './db/'

def write(user_id: str, date: int):
    d = datetime.datetime.fromtimestamp(date, datetime.timezone.utc).astimezone(datetime.timezone(datetime.timedelta(hours=9)))
    file_name = db_path+f'{str(d)[:10]}.json'
    if not os.path.isfile(file_name):
        with open(file_name, mode='w') as f:
            f.write(r'{}')
    with open(file_name) as f:
        db = json.load(f)
    if user_id not in db.keys():
        db[user_id] = []
    db[user_id].append(date)
    with open(file_name, 'w') as f:
        json.dump(db, f, indent=2)
