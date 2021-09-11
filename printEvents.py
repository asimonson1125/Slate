# And the creator said: Here I will make a test, so that all may see that I am competent
# and Lo, the test was made and impressed nobody, though viability was proven.

from ics import Calendar
import requests
import arrow

def deltaConversion(td): # output: HH:MM
    minutes = (td.seconds % 3600 //60)
    if (minutes < 10):
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return str(td.seconds // 3600) + ":" + minutes

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
calendar = Calendar(requests.get(url).text)
# --------------------------------------------------------------------------------------------

events = list(calendar.timeline.included(arrow.now(), arrow.now().shift(days=+2))) # Gets calendar timeline between now and now+2days as a list

for i in range(len(events)): # For each event in the next 2 days...
    eName = events[i].name # Event name in string
    eStart = events[i].begin # Event start time in Arrow
    eDuration = events[i].duration # Event duration in timedelta
    print(eName, "\n\tStarts: ", eStart.humanize(),"\n\tDuration: ", deltaConversion(eDuration))