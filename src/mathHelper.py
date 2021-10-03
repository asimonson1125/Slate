import math

def timesBetween(checkStart, checkEnd, interval):
    """
    Gets times between checkStart and checkEnd on interval interval and returns them as an array of datetimes

    Should probably be noted that the final item of the array will be either equal to or past checkEnd, ie if
    checkEnd-checkStart = 20 minutes and interval = 15 minutes, the returned array will be [checkStart, checkstart + 20]
    If this is not desired, remove the +1 from the range, lmao.
    """
    times = []
    for i in range(math.ceil((checkEnd-checkStart)/interval) + 1):
        times.append(checkStart + interval*i)
    return(times)