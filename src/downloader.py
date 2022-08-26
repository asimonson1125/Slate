import icalendar
import calc

from sanitizer import isCalendar


def local(start, end, path, calendars, i, socketio, sid):
    """
    loads calendars from file
    """
    with open('static/calendars/' + path, encoding="utf8") as chat:
        g = chat.read()
    cal = icalendar.Calendar.from_ical(g)
    calendars[i] = calc.cleanCal(cal, start, end)
    socketio.emit('loadUpdate', i, to=sid)


def run(start, end, path, calendars, i, socketio, sid):
    """
    Downloads calendars by URL
    """
    calendar = calc.get_cal(path, start, end)
    calendars[i] = calendar
    socketio.emit('loadUpdate', i, to=sid)

def check(url):
    """
    Checks validity of a url
    """
    message = ""
    try:
        calendar = isCalendar(url) # downloads cal
        if(calendar):
            if calendar.get("CALSCALE", "GREGORIAN") != "GREGORIAN":
                message = "Only gregorian calendars can be loaded!"
        else:
            message = "Calendar not found!"
    except:
        message = "Error on load!"
    return message