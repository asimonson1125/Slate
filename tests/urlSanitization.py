import sys, os
os.chdir('./src')
sys.path.append(os.getcwd())
from sanitizer import isCalendar


url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
test = isCalendar(url)
if(test):
    print("success")
else:
    print("error")

url = "google.com"
test = isCalendar(url)
if(test):
    print("success")
else:
    print("error")