import recurring_ical_events
import datetime
import math


def availableFor(calendar, times, length):
    """
    takes an array of calendars and the start/end times of a hypothetical meeting
    Returns an array of tuples (calendar, availability boolean)
    """
    if length < datetime.timedelta(seconds=0): # if start and end are the same, 'between' will return true regardless of if an event is ongoing.  We don't want that. 
        end += datetime.timedelta(seconds=2)
    availability = []
    recurrer = recurring_ical_events.of(calendar)
    for time in times:
        if len(recurrer.between(time + datetime.timedelta(seconds=1), time + length)) == 0: # no conflicting events were found
            availability.append(True)
        else:
            availability.append(False)
    return availability


def availabilityScore(availabilities, index, calValues):
    """
    Could probably be called unavailability score, since it is rating the number
    of people who CAN'T make it.  

    availabilities should be an array of tuples a la availableFor(), ie [[ics,false]]
    calValues[i] should be an int representing the value of the availability
    of the calendar at availabilities[i][0]
    """
    score = 0
    for i in range(len(availabilities)): # for each calendar
        if not availabilities[i][index]: # if unavailable
            if calValues[i] == -1: # -1 represents a mandatory attendance
                return -1 # a required participant can't make this time
            score += calValues[i]
    return score


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
    max_intervals_per_day = 0
    intervals_on_day = 0
    while(newTime < checkEnd):
        intervals_on_day += 1
        if(max_intervals_per_day < intervals_on_day):
            max_intervals_per_day = intervals_on_day
        times.append(newTime)
        newTime = newTime + interval
        if(newTime.date() != day):
            day = newTime.date()
            newTime = datetime.datetime.combine(newTime.date(), displace)
            intervals_on_day = 0
    return times, max_intervals_per_day