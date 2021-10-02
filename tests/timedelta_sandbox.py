import datetime
import math

time = datetime.timedelta(minutes=5)

print(int((time).total_seconds() / 60))
for i in range(int((time).total_seconds() / 60)):
    print(datetime.timedelta(minutes=i))