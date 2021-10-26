"""
The idea here is to testrun the availability processor with a 
hardcoded sample of calendars and scores
"""

import urllib.request
import datetime
import icalendar
import os
import sys

#for local imports
# -----------------------------------
os.chdir('./src')
sys.path.append(os.getcwd())
# -----------------------------------
import staticCalendars
import availabilityHandler
import mathHelper

# Gets calendars from google in ICS file ------------------------------------------------------

myUrl = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(myUrl).read()
myCal = icalendar.Calendar.from_ical(ical_string)

ical_string = urllib.request.urlopen(staticCalendars.cshCal).read()
cshCal = icalendar.Calendar.from_ical(ical_string)

# --------------------------------------------------------------------------------------------

calendars = [myCal, cshCal]
calValues = [1, 2]
start = datetime.datetime.now()
end = datetime.datetime.now() + datetime.timedelta(hours=5)
interval = datetime.timedelta(minutes=30)
eventLength = datetime.timedelta(seconds=1)

timesChecked = mathHelper.timesBetween(start, end, interval)

for i in timesChecked: # for all time on intervals between start/end conditions
    availabilities = availabilityHandler.availableFor(calendars, i, i+eventLength)
    score = availabilityHandler.availabilityScore(availabilities, calValues)
    print(i.strftime("%d/%m/%Y - %I:%M:%S") + " to " + (i+eventLength).strftime("%I:%M:%S"), score)