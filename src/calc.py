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


def max_score(scores):
    sum = 0
    for score in scores:
        sum += score
    return sum


def run(calendars, scores, start, end, interval, length):
    times = availabilityHandler.timesBetween(start, end, interval)
    data = []
    for time in times:
        availabilities = availabilityHandler.availableFor(
            calendars, time, time + length)
        score = availabilityHandler.availabilityScore(
            availabilities, scores)
        thisData = []
        thisData.append(time.strftime("%d/%m/%Y - %I:%M:%S") + " to " + (time + length).strftime(
            "%I:%M:%S"))
        thisData.append(score)
        unavailables = []
        for i in range(len(availabilities)):
            if availabilities[i][1] == False:
                unavailables.append(
                    [availabilities[i][0]['X-WR-CALNAME'], str(scores[i])])
            thisData.append(unavailables)
        data.append(thisData)
    
    return data
