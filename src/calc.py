from sanitizer import isCalendar
import availabilityHandler
import recurring_ical_events
import datetime
import icalendar
import pytz
import time
import flask

"""
the main, haha.
"""


def getData(calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status, sid):
    """
    Well named.  This function gets output data from the input data affter parsing.
    """
    eventCount = 0
    for calendar in calendars: # Calculating total event count for % completion
        eventCount += len(calendar)
    numDone = [0, eventCount]

    max_score = getMaxScore(scores)
    
    processStart = time.time()
    output, maxIntervals = process(calendars, names, scores, start, end,
                               interval, length, DSTinfo, socketio, status, sid, numDone)
    processingTime = time.time() - processStart
    days = splitDays(output, maxIntervals)
    return(days, max_score, processingTime)


def get_cal(url, start, end):
    """
    Leads calendar download process once a url is acquired 
    """
    try:
        calendar = isCalendar(url) # downloads cal
        if(calendar):
            assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", flask.abort(
                400, "Non-Gregorian Calendar Detected")
        else:
            return False
        calendar = cleanCal(calendar, start, end) # Turn cal into an array of events in the timeframe
    except:
        return False
    return calendar


def cleanCal(cal, start, end):
    """
    takes icalendar objects and turns it into an event list
    ignores events that are not in the selected time frame
    """
    timezone = getTZ(cal)
    events = recurring_ical_events.of(cal).between(start, end)
    for event in range(len(events)):
        # If an all-day event, turn it into a datetime with the assigned timezone
        if type(events[event]['DTSTART'].dt) == datetime.date:
            day = events[event]['DTSTART'].dt
            dtime = datetime.datetime.combine(day, datetime.time.min)
            events[event]['DTSTART'].dt = timezone.localize(dtime)
        if type(events[event]['DTEND'].dt) == datetime.date:
            day = events[event]['DTEND'].dt
            dtime = datetime.datetime.combine(day, datetime.time.min)
            events[event]['DTEND'].dt = timezone.localize(dtime)

        # If event has no timezone, assign the calendar's timezone
        if events[event]['DTEND'].dt.tzinfo == "None":
            events[event]['DTEND'].dt = timezone.localize(
                events[event]['DTEND'].dt)
        if events[event]['DTSTART'].dt.tzinfo == "None":
            events[event]['DTSTART'].dt = timezone.localize(
                events[event]['DTSTART'].dt)
    return events


def getTZ(cal):
    """
    Gets the calendar's timezone in case of naive tz events
    """
    for inverseSubcomponent in range(len(cal.subcomponents)):
        if(cal.subcomponents[len(cal.subcomponents) - 1 - inverseSubcomponent].name == "VTIMEZONE"):
            name = icalendar.cal.Timezone(cal.subcomponents[len(
                cal.subcomponents) - 1 - inverseSubcomponent])['TZID']
            timezone = pytz.timezone(name)
            return timezone
    return pytz.utc


def getMaxScore(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def process(calendars, names, scores, start, end, interval, length, DSTinfo, socketio, status, sid, numDone):
    """
    Actually processes calendar event lists, turns it into the time intervals with lists of absentees
    """
    times, maxIntervals = availabilityHandler.timesBetween(
        start, end, interval, DSTinfo) # gets time intervals
    data = []
    availabilities = []
    for cal in range(len(calendars)): # for each calendar add it to time intervals where they'd be unavailable
        availabilities.append(availabilityHandler.availableFor(
            calendars[cal], times, length, socketio, status, sid, cal+1, numDone))
    for time in range(len(times)): # creates datapoints for timeslots
        score = availabilityHandler.availabilityScore(
            availabilities, time, scores)
        thisData = []
        thisData.append(times[time].strftime("%A, %B %d, %Y - %I:%M %p") + " to " + (times[time] + length).strftime(
            "%I:%M %p"))
        thisData.append(score)
        unavailables = []
        for i in range(len(availabilities)):
            if availabilities[i][time] == False:
                unavailables.append(
                    [names[i], str(scores[i])])
        thisData.append(unavailables)
        thisData.append(times[time])
        data.append(thisData)

    return data, maxIntervals


def splitDays(data, intervalsPerDay):
    """
    Breaks timeslots into day groups
    """
    Days = [[]]
    day = 0
    Days[0].append(data[0])
    for time in range(len(data) - 1):
        if data[time + 1][3].date() != data[time][3].date():
            day += 1
            Days.append([])
        Days[day].append(data[time + 1])
    placeholder = []
    for i in range(intervalsPerDay - len(Days[0])):
        placeholder.append([])
    Days[0] = placeholder + Days[0]
    return Days
