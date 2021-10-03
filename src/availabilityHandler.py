import recurring_ical_events
import datetime
import math


def availableFor(calendars, start, end):
    """
    takes an array of calendars and the start/end times of a hypothetical meeting
    Returns an array of tuples (calendar, availability boolean)
    """
    if start == end: # if start and end are the same, 'between' will return true regardless of if an event is ongoing.  We don't want that. 
        end += datetime.timedelta(seconds=1)
    availability = []
    for i in calendars:
        if len(recurring_ical_events.of(i).between(start, end)) == 0: # no conflicting events were found
            availability.append((i,True))
        else:
            availability.append((i,False))
    return availability


def availabilityScore(availabilities, calValues):
    """
    Could probably be called unavailability score, since it is rating the number
    of people who CAN'T make it.  

    availabilities should be an array of tuples a la availableFor(), ie [[ics,false]]
    calValues[i] should be an int representing the value of the availability
    of the calendar at availabilities[i][0]
    """
    score = 0
    for i in range(len(availabilities)): # for each calendar
        if not availabilities[i][1]: # if unavailable
            if calValues[i] == -1: # -1 represents a mandatory attendance
                return -1 # a required participant can't make this time
            score += calValues[i]
    return score

