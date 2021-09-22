from ics import Calendar
import requests
import arrow

# Gets calendar from google in ICS file ------------------------------------------------------
url = "https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"
calendar = Calendar(requests.get(url).text)
# --------------------------------------------------------------------------------------------

events = list(calendar.timeline.included(arrow.now(), arrow.now().shift(days=+2))) # Gets calendar timeline between now and now+2days as a list