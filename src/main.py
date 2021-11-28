import sys, os
os.chdir('./src')
sys.path.append(os.getcwd())
from sanitizer import isCalendar
import staticCalendars
import availabilityHandler

"""
the main, haha.
"""

def run(urls, in_scores, start, end, interval, length):
    calendars = []
    scores = []
    problems = []
    for i in range(len(urls)):
        calendar = isCalendar(urls[i])
        if(calendar):
            calendars.append(calendar)
            scores.append(in_scores[i])
        else:
            problems.append('Calendar could not be found in "' + urls[i] + '".')
    # prompt user with errors
    for i in problems:
        print(i)
    if(len(problems) == 0): # All calendars functional
        times = availabilityHandler.timesBetween(start, end, interval)
        for time in times:
            availabilities = availabilityHandler.availableFor(calendars, time, time + length)
            score = availabilityHandler.availabilityScore(availabilities, scores)
            print(time.strftime("%d/%m/%Y - %I:%M:%S") + " to " + (time + length).strftime("%I:%M:%S"), score)

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
