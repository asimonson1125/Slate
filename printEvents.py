# And the creator said: Here I will make a test, so that all may see that I am competent
# and Lo, the test was made and impressed nobody, though viability was proven.

import urllib.request
import recurring_ical_events
import datetime
import icalendar


def deltaConversion(td): # output: HH:MM
    minutes = (td.seconds % 3600 //60)
    if (minutes < 10):
        minutes = "0" + str(minutes)
    else:
        minutes = str(minutes)
    return str(td.seconds // 3600) + ":" + minutes

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(ical_string)
# --------------------------------------------------------------------------------------------

events = recurring_ical_events.of(calendar).between(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=12)) # Gets calendar timeline between now and now+2days as a list

for i in range(len(events)): # For each event in the next 2 days...
    eName = events[i]['SUMMARY'] # Event name in string
    eStart = events[i]['DTSTART'].dt # Event start time in Arrow
    eEnd = events[i]['DTEND'].dt # Event duration in timedelta
    print(eName, "\n\tStarts: ", eStart, "\n\tDuration: ", eEnd - eStart, '\n')
