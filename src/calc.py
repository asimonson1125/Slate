from sanitizer import isCalendar
import staticCalendars
import availabilityHandler

"""
the main, haha.
"""


def get_cals(urls):
    problems = []
    calendars = []
    out = []
    for i in range(len(urls)):
        try:
            calendar = isCalendar(urls[i])
            if(calendar):
                assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", problems.append(
                    "In calendar at " + urls[i] + ": non-gregorian calendar detected")
            else:
                problems.append(
                    'Calendar could not be found at "' + urls[i] + '".')
            # calendar = cleanCal(calendar)
            calendars.append(calendar)
        except Exception as e:
            problems.append(e)
    # prompt user with errors
    for i in problems:
        out.append(str(i))
    if out != []:
        return out
    return calendars

def cleanCal(cal):
    return cal



def max_score(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def run(calendars, names, scores, start, end, interval, length):
    times, maxIntervals = availabilityHandler.timesBetween(
        start, end, interval)
    data = []
    availabilities = []
    for cal in calendars:
        availabilities.append(availabilityHandler.availableFor(
            cal, times, length))
    for time in range(len(times)):
        score = availabilityHandler.availabilityScore(
            availabilities, time, scores)
        thisData = []
        thisData.append(times[time].strftime("%A, %d/%m/%Y - %I:%M %p") + " to " + (times[time] + length).strftime(
            "%I:%M %p"))
        thisData.append(score)
        unavailables = []
        for i in range(len(availabilities)):
            if availabilities[i][1] == False:
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
