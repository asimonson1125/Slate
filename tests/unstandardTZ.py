import urllib.request
import recurring_ical_events
import datetime
import icalendar
import arrow


# Gets calendar from ICS file ------------------------------------------------------
#f = open("broken.ics", 'r')
#calendario = icalendar.Calendar.from_ical(f.read())
#f.close()
myUrl = "https://calendar.google.com/calendar/ical/c_grbi06ec0hl1s9gi46c3ooqvsc%40group.calendar.google.com/public/basic.ics"
ical_string = urllib.request.urlopen(myUrl).read()
calendario = icalendar.Calendar.from_ical(ical_string)


# --------------------------------------------------------------------------------------------


events = recurring_ical_events.of(calendario).between(datetime.datetime(2021, 12, 22), datetime.datetime(2021, 12, 23) + datetime.timedelta(days=2)) 

for i in range(len(events)): # For each event in the next 2 days...
    eName = events[i]['SUMMARY'] # Event name in string
    eStart = events[i]['DTSTART'].dt # Event start time in dt
    eEnd = events[i]['DTEND'].dt # Event end time in dt
    print(eName, "\n\tStarts: ", eStart, "\n\tDuration: ", eEnd - eStart, '\n')