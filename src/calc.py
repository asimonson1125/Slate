from sanitizer import isCalendar
import availabilityHandler
import recurring_ical_events
import datetime
import icalendar
import pytz

"""
the main, haha.
"""


def get_cals(urls, start, end):
    problems = []
    calendars = []
    out = []
    for i in range(len(urls)):
        try:
            calendar = isCalendar(urls[i])
            if(calendar):
                assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", problems.append(
                    "In calendar at " + urls[i] + ": non-gregorian calendar detected")
                calendar = cleanCal(calendar, start, end)
                calendars.append(calendar)
            else:
                problems.append(
                    'Calendar could not be found at "' + urls[i] + '".')
        except Exception as e:
            problems.append(e)
    # prompt user with errors
    for i in problems:
        out.append(str(i))
    if out != []:
        return out
    return calendars

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
            events[event]['DTEND'].dt = timezone.localize(events[event]['DTEND'].dt)
        if events[event]['DTSTART'].dt.tzinfo == "None":
            events[event]['DTSTART'].dt = timezone.localize(events[event]['DTSTART'].dt)
    return events

def getTZ(cal):
    for inverseSubcomponent in range(len(cal.subcomponents)):
                if(cal.subcomponents[len(cal.subcomponents) - 1 - inverseSubcomponent].name == "VTIMEZONE"):
                    name = icalendar.cal.Timezone(cal.subcomponents[len(cal.subcomponents) - 1 - inverseSubcomponent])['TZID']
                    timezone = pytz.timezone(name)
                    return timezone

def max_score(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def run(calendars, names, scores, start, end, interval, length, DSTinfo):
    times, maxIntervals = availabilityHandler.timesBetween(
        start, end, interval, DSTinfo)
    data = []
    availabilities = []
    for cal in calendars:
        availabilities.append(availabilityHandler.availableFor(
            cal, times, length))
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
                name = names[i]
                if(len(name) < 1):
                    name = "Calendar #" + str(i + 1)
                unavailables.append(
                    [name, str(scores[i])])
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
