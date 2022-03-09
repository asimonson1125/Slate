import datetime
import math

def timesBetween(checkStart, checkEnd, interval):
    """
    Gets times between 'checkStart' and 'checkEnd' on interval 'interval' and returns them as an array of datetimes
    To ensure table consistency between days, each new day may have a gap to match intervals of the previous days
    """
    times = []
    firstDay = checkStart.date()
    midnight = datetime.datetime.combine(firstDay, datetime.time.min)
    displaceDelta = (checkStart - midnight) % interval
    displace = datetime.time(hour=displaceDelta.seconds//3600, minute=(displaceDelta.seconds//60)%60)
    newTime = checkStart
    day = firstDay
    while(newTime < checkEnd):
        times.append(newTime)
        newTime = newTime + interval
        if(newTime.date() != day):
            day = newTime.date()
            newTime = datetime.datetime.combine(newTime.date(), displace)
            iPerDay = 0


    
    # for i in range(math.ceil((checkEnd-checkStart)/interval)):
    #     newTime = checkStart + interval*i
    #     if(newTime.date() != firstDay):
    #         iter = i
    #         break
    #     times.append(newTime)
    return(times)


times = timesBetween(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=2), datetime.timedelta(minutes=239))
for i in times:
    print(i)