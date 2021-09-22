"""
This script uses the CSH calendar and my own and checks if they are available at the present time

For CSH in particular, it's important to note that optional, long-term events will be processed as 
times when CSH is unavailable.  For example, the RIT blood drive is from 10 am to 3 pm, but nobody
at CSH is going to be there for the whole thing if at all.
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


# Gets calendars from google in ICS file ------------------------------------------------------

myUrl = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(myUrl).read()
myCal = icalendar.Calendar.from_ical(ical_string)

ical_string = urllib.request.urlopen(staticCalendars.cshCal).read()
cshCal = icalendar.Calendar.from_ical(ical_string)

# --------------------------------------------------------------------------------------------

availabilities = availabilityHandler.availableFor([myCal, cshCal], datetime.datetime.now(), datetime.datetime.now())
for i in availabilities:
    print(i[0]['X-WR-CALNAME'] , i[1])
print("SCORE:", availabilityHandler.availabilityScore(availabilities, [1,2]))