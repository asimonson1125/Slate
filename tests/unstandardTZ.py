import urllib.request
import recurring_ical_events
import datetime
import icalendar
import arrow
import os, sys

#for local imports
# -----------------------------------
os.chdir('./src')
sys.path.append(os.getcwd())
# -----------------------------------
import staticCalendars
import availabilityHandler

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(ical_string)


ical_string = urllib.request.urlopen("https://www.google.com/calendar/ical/rti648k5hv7j3ae3a3rum8potk%40group.calendar.google.com/public/basic.ics").read()
cshCal = icalendar.Calendar.from_ical(ical_string)
calendar = cshCal

# --------------------------------------------------------------------------------------------

time = datetime.datetime.now() + datetime.timedelta(hours=4)
print(availabilityHandler.availableFor([cshCal], time,datetime.datetime.now() + datetime.timedelta(hours=4.1))[0][1])
print(time)
print(recurring_ical_events.of(cshCal).at(time))