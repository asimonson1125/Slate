"""
sanitizer.py
input sanitization, duh.
"""
import urllib.request
import icalendar


def isCalendar(url):
    """
    takes a url and determines if it leads to an ics file that we can process. 
    If valid url, returns the calendar object.  If not, returns false.
    """
    try:
        # public Apple calendar links are type 'webcal', which urllib doesn't recognize
        url = url.replace("webcal://", "http://")
        ical_string = urllib.request.urlopen(url).read()
        calendar = icalendar.Calendar.from_ical(ical_string)
        return calendar
    except Exception as e:
        print("for url " + url + " error recieved: " + str(e))
        return False
