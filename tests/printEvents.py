# And the creator said: Here I will make a test, so that all may see that I am competent
# and Lo, the test was made and impressed nobody, though viability was proven.

# NO HOMEMADE DEPENDENCIES REQUIRED

import urllib.request
import recurring_ical_events
import datetime
import icalendar
import arrow

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(ical_string)

# --------------------------------------------------------------------------------------------

events = recurring_ical_events.of(calendar).between(datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=12)) 
# Gets calendar timeline between now and now+2days as an array

for i in range(len(events)): # For each event in the next 2 days...
    eName = events[i]['SUMMARY'] # Event name in string
    eStart = events[i]['DTSTART'].dt # Event start time in dt
    eEnd = events[i]['DTEND'].dt # Event end time in dt
    print(eName, "\n\tStarts: ", eStart, "\n\tDuration: ", eEnd - eStart, '\n')
