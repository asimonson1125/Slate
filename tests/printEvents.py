# And the creator said: Here I will make a test, so that all may see that I am competent
# and Lo, the test was made and impressed nobody, though viability was proven.

# NO HOMEMADE DEPENDENCIES REQUIRED

import urllib.request
import recurring_ical_events
import datetime
import icalendar
import arrow

def printEvents(events):
    for i in range(len(events)): # For each event in the next 2 days...
        eName = events[i]['SUMMARY'] # Event name in string
        eStart = events[i]['DTSTART'].dt # Event start time in dt
        eEnd = events[i]['DTEND'].dt # Event end time in dt
        print(eName, "\n\tStarts: ", eStart, "\n\tDuration: ", eEnd - eStart, '\n')

def checkEvents(calendar, time, length):
    print("Event is on " + time.strftime("%m/%d %H:%M") + " to " + (time + length).strftime("%m/%d %H:%M"))
    if len(calendar) > 0:  # make sure there are events
        for event in calendar:
            start = event['DTSTART'].dt 
            end = event['DTEND'].dt
            if(type(start) == datetime.date):
                start = datetime.datetime.combine(start, datetime.time.min)
                start = start.replace(tzinfo=event['DTSTAMP'].dt.tzinfo)
            if(type(end) == datetime.date):
                end = datetime.datetime.combine(end, datetime.time.min)
                end = end.replace(tzinfo=event['DTSTAMP'].dt.tzinfo)
            print(event['SUMMARY'] + " is on " + start.strftime("%m/%d %H:%M") + " to " + end.strftime("%m/%d %H:%M"))
            print(start < time+length)
            if (start < time + length and end > time):
                return False
    return True

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://www.google.com/calendar/ical/rti648k5hv7j3ae3a3rum8potk%40group.calendar.google.com/public/basic.ics"
ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(ical_string)

# --------------------------------------------------------------------------------------------

start = datetime.datetime(2022, 3, 15)
end = datetime.datetime(2022, 3, 16)


events = recurring_ical_events.of(calendar).between(start, end) 
# Gets calendar timeline between now and now+2days as an array

# printEvents(events)

eventStart = datetime.datetime(2022, 3, 15, hour=13, tzinfo=datetime.timezone.utc)
print(checkEvents(events, eventStart, datetime.timedelta(hours=3)))

