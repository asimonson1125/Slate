import recurring_ical_events
import datetime
import math


def availableFor(calendar, times, length):
    """
    takes an array of events in a calendar and the start/end times of a hypothetical meeting
    Returns an array of boolean availabilities
    """
    availability = []
    for time in times: # generates time array, defaults to available (true)
        availability.append(True)
    for event in calendar:
        if event['DTEND'].dt - event['DTSTART'].dt <= datetime.timedelta(seconds=0):  # if start and end are the same, 'between' will return true regardless of if an event is ongoing.  We don't want that.
            event['DTEND'].dt += datetime.timedelta(seconds=2)
        startUnavailable = 0
         # I think this logic works??  Need to test.
        for i in range(len(times)): # get first conflicting time
            if(event['DTSTART'].dt < times[i] + length and event['DTEND'].dt > times[i]):
                #if the event has already started by timeslot end and event has not ended by the start of timeslot
                startUnavailable = i
                break
        while startUnavailable < len(times) and event['DTEND'].dt > times[startUnavailable]: # Make all timeslots false until the end of the event
            availability[startUnavailable] = False
            startUnavailable += 1
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
    for i in range(len(availabilities)):  # for each calendar
        if not availabilities[i][index]:  # if unavailable
            if calValues[i] == -1:  # -1 represents a mandatory attendance
                return -1  # a required participant can't make this time
            score += calValues[i]
    return score


def timesBetween(checkStart, checkEnd, interval):
    """
    Gets times between 'checkStart' and 'checkEnd' on interval 'interval' and returns them as an array of datetimes
    To ensure table consistency between days, each new day may have a gap to match intervals of the previous days
    """
    times = []
    firstDay = checkStart.date()
    midnight = datetime.datetime.combine(firstDay, datetime.time.min).replace(tzinfo=checkStart.tzinfo)
    displaceDelta = (checkStart - midnight) % interval
    displace = datetime.time(hour=displaceDelta.seconds //
                             3600, minute=(displaceDelta.seconds//60) % 60)
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
            newTime = datetime.datetime.combine(newTime.date(), displace).replace(tzinfo=checkStart.tzinfo)
            intervals_on_day = 0
    return times, max_intervals_per_day
