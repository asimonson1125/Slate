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

    eventCount = 0
    for calendar in calendars:
        eventCount += len(calendar)
    numDone = [0, eventCount]

    max_score = 0
    for score in scores:
        if(score > 0):
            max_score += score
    processStart = time.time()
    output, maxIntervals = run(calendars, names, scores, start, end,
                               interval, length, DSTinfo, socketio, status, sid, numDone)
    processingTime = time.time() - processStart
    days = splitDays(output, maxIntervals)
    return(days, max_score, processingTime)


def get_cal(url, start, end):
    try:
        calendar = isCalendar(url)
        if(calendar):
            assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", flask.abort(
                400, "Non-Gregorian Calendar Detected")
        else:
            return 'Calendar could not be found at "' + url + '".'
        calendar = cleanCal(calendar, start, end)
    except Exception as e:
        return e
    return calendar


def cleanCal(cal, start, end):
    timezone = getTZ(cal)
    events = recurring_ical_events.of(cal).between(start, end)
    for event in range(len(events)):
        if type(events[event]['DTSTART'].dt) == datetime.date:
            day = events[event]['DTSTART'].dt
            dtime = datetime.datetime.combine(day, datetime.time.min)
            events[event]['DTSTART'].dt = timezone.localize(dtime)
        if type(events[event]['DTEND'].dt) == datetime.date:
            day = events[event]['DTEND'].dt
            dtime = datetime.datetime.combine(day, datetime.time.min)
            events[event]['DTEND'].dt = timezone.localize(dtime)
        if events[event]['DTEND'].dt.tzinfo == "None":
            events[event]['DTEND'].dt = timezone.localize(
                events[event]['DTEND'].dt)
        if events[event]['DTSTART'].dt.tzinfo == "None":
            events[event]['DTSTART'].dt = timezone.localize(
                events[event]['DTSTART'].dt)
    return events


def getTZ(cal):
    for inverseSubcomponent in range(len(cal.subcomponents)):
        if(cal.subcomponents[len(cal.subcomponents) - 1 - inverseSubcomponent].name == "VTIMEZONE"):
            name = icalendar.cal.Timezone(cal.subcomponents[len(
                cal.subcomponents) - 1 - inverseSubcomponent])['TZID']
            timezone = pytz.timezone(name)
            return timezone


def max_score(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def run(calendars, names, scores, start, end, interval, length, DSTinfo, socketio, status, sid, numDone):
    times, maxIntervals = availabilityHandler.timesBetween(
        start, end, interval, DSTinfo)
    data = []
    availabilities = []
    for cal in range(len(calendars)):
        availabilities.append(availabilityHandler.availableFor(
            calendars[cal], times, length, socketio, status, sid, cal+1, numDone))
    for time in range(len(times)):
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
