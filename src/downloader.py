import icalendar
import calc


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
