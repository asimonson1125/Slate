import urllib.request
import datetime
import icalendar
import os
import sys

myUrl = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
ical_string = urllib.request.urlopen(myUrl).read()
myCal = icalendar.Calendar.from_ical(ical_string)

ea = myCal.to_ical()
print(2)