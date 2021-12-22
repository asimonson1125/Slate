# And the creator said: Here I will make a test, so that all may see that I am competent
# and Lo, the test was made and impressed nobody, though viability was proven.

# NO HOMEMADE DEPENDENCIES REQUIRED

import urllib.request
import recurring_ical_events
import datetime
import icalendar
import arrow

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/c_r5ot90fojbjvd4a8uu5ia5h9v8%40group.calendar.google.com/public/basic.ics"
# ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(open("egg.ics").read())

# --------------------------------------------------------------------------------------------

events = recurring_ical_events.of(calendar).between(datetime.datetime.today() - datetime.timedelta(hours=5), datetime.datetime.today() + datetime.timedelta(days=2)) 
# Gets calendar timeline between now and now+2days as an array

for i in range(len(events)): # For each event in the next 2 days...
    eName = events[i]['SUMMARY'] # Event name in string
    eStart = events[i]['DTSTART'].dt # Event start time in dt
    eEnd = events[i]['DTEND'].dt # Event end time in dt
    print(eName, "\n\tStarts: ", eStart, "\n\tDuration: ", eEnd - eStart, '\n')
