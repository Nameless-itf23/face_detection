import time
import datetime
import zoneinfo
date = int(time.time())
d = datetime.datetime.fromtimestamp(date, datetime.timezone.utc).astimezone(zoneinfo.ZoneInfo("Asia/Tokyo"))
print(str(d)[:10])