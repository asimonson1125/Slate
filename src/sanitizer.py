"""
sanitizer.py
input sanitization, duh.
"""
import urllib.request
import icalendar


def isCalendar(url):
    try:
        url = url.replace("webcal://", "http://") # Apple links are type 'webcal', which urllib doesn't recognize
        ical_string = urllib.request.urlopen(url).read()
        calendar = icalendar.Calendar.from_ical(ical_string)
        return True
    except Exception as e:
        print(e)
        return False

# print(isCalendar("webcal://p35-caldav.icloud.com/published/2/NjI5OTM0OTU1NjI5OTM0OekOcxwBCOsPqSzPVdtLtqrHr4sccxUNMJ9heH0PZsZtHHAiU_gkmu0HuVybf6TIk7-4fG1ZwvXOrxtizeOuAas"))
# print(isCalendar("https://calendar.google.com/calendar/ical/abs1907%40g.rit.edu/public/basic.ics"))