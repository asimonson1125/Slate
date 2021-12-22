from sanitizer import isCalendar
import staticCalendars
import availabilityHandler

"""
the main, haha.
"""


def get_cals(urls):
    problems = []
    calendars = []
    out = ""
    for i in range(len(urls)):
        try:
            calendar = isCalendar(urls[i])
            if(calendar):
                assert calendar.get("CALSCALE", "GREGORIAN") == "GREGORIAN", problems.append("In calendar at " + urls[i] + ": non-gregorian calendar detected")
                calendars.append(calendar)
            else:
                problems.append(
                    'Calendar could not be found at "' + urls[i] + '".')
        except Exception as e:
            problems.append(e)
    # prompt user with errors
    for i in problems:
        out += "<p>" + str(i) + "</p>"
    if out != "":
        return out
    return calendars


def run(calendars, scores, start, end, interval, length):
    out = ""
    times = availabilityHandler.timesBetween(start, end, interval)
    for time in times:
        availabilities = availabilityHandler.availableFor(
            calendars, time, time + length)
        score = availabilityHandler.availabilityScore(
            availabilities, scores)
        tester = time.strftime("%d/%m/%Y - %I:%M:%S")
        test = "<p>" + \
            (tester + " to " + (time + length).strftime("%I:%M:%S") +
               " => " + str(score)) + "</p>"
        out += test
    return out


"""
import datetime
cals = ["https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics", staticCalendars.cshCal]
calValues = [1, 2]
start = datetime.datetime.now()
end = datetime.datetime.now() + datetime.timedelta(hours=5)
interval = datetime.timedelta(minutes=30)
eventLength = datetime.timedelta(seconds=1)
run(cals, calValues, start, end, interval, eventLength)
"""
