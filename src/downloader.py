import icalendar
import calc


def local(start, end, path, calendars, i, socketio, sid):
    with open('src/static/calendars/' + path, encoding="utf8") as chat:
        g = chat.read()
    cal = icalendar.Calendar.from_ical(g)
    calendars[i] = calc.cleanCal(cal, start, end)
    socketio.emit('loadUpdate', i, to=sid)


def run(start, end, path, calendars, i, socketio, sid):
    calendar = calc.get_cal(path, start, end)
    calendars[i] = calendar
    socketio.emit('loadUpdate', i, to=sid)
