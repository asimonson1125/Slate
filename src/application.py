import flask
import datetime
import calc
from dateutil import parser
import time
import icalendar
from flask_socketio import SocketIO
# https://github.com/liam-middlebrook/csh_ldap
# https://pypi.org/project/Flask-pyoidc/ 

app = flask.Flask(__name__)

socketio = SocketIO(app)

@socketio.on('example')
def loadExample():
    timezone = -5
    DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
    start = datetime.datetime(2022, 8, 10, 13, 0, 0).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    end = datetime.datetime(2022, 10, 15, 13, 0, 0).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    interval = datetime.timedelta(minutes=60)
    length = datetime.timedelta(minutes=60)
    files = ['person1.ics', 'person2.ics', 'CSH.ics']
    calendars = []
    names = ['Caitlyn', 'Andrew', 'CSH']
    scores = [2, 1, 3]
    status = [0]
    for name in names:
        status.append([name, 0, 0])
    socketio.emit('loader', status)

    getStart = time.time()
    for file in range(len(files)):
        with open('src/static/calendars/' + files[file], encoding="utf8") as chat:
            g = chat.read()
        cal = icalendar.Calendar.from_ical(g)
        calendars.append(calc.cleanCal(cal, start, end))
        status[file + 1][1] = 100
        socketio.emit('loader', status)

    getTime = time.time() - getStart
    days, max_score, processingTime = calc.getData(calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    socketio.emit('loaded', output)


@socketio.on('submit')
def runSlate(data):
    urls, names, scores, timezone, start, end, daylighSavingsTick, interval, length = data
    timezone = int(timezone)
    start = parser.parse(start).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    end = parser.parse(end).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone))
    if(daylighSavingsTick):
        DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
    interval = datetime.timedelta(minutes=int(interval))
    length = datetime.timedelta(minutes=int(length))

    if start > end:
        flask.abort(416, "Range end time cannot be after start time")
    
    status = [0]
    for name in names:
        status.append([name, 0, 0])
    socketio.emit('loader', status)

    getStart = time.time()
    calendars = []
    for url in range(len(urls)):
        calendar = calc.get_cal(urls[url], start, end)
        if type(calendar) == str:
            socketio.emit('loader', calendar)
            flask.abort(406)
        calendars.append(calendar)
        status[url + 1][1] = 100
        socketio.emit('loader', status)
    getTime = time.time() - getStart
    days, max_score, processingTime = calc.getData(calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    socketio.emit('loaded', output)


@app.route('/')
def get_in():
    return flask.render_template('input.html')

@app.route('/about')
def get_about():
    return flask.render_template('about.html')


@app.errorhandler(Exception)
def page404(e):
    try:
        eCode = e.code
        message = e.description
        try:
            message = e.length
        finally:
            return flask.render_template('error.html', error=eCode, message=message)
    except:
        return flask.render_template('unknownError.html', error=str(e))


if __name__ == '__main__':
    socketio.run(app)
