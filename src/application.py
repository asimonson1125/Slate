import flask
import datetime
from dateutil import parser
import time
import icalendar
from flask_socketio import SocketIO
from threading import Thread
# https://github.com/liam-middlebrook/csh_ldap
# https://pypi.org/project/Flask-pyoidc/ 

import calc
import downloader

app = flask.Flask(__name__)

socketio = SocketIO(app)

@socketio.on('example')
def loadExample():
    sid = flask.request.sid
    timezone = -5
    DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
    start = datetime.datetime(2022, 8, 10, 13, 0, 0).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    end = datetime.datetime(2022, 10, 15, 13, 0, 0).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    interval = datetime.timedelta(minutes=60)
    length = datetime.timedelta(minutes=60)
    files = ['person1.ics', 'person2.ics', 'CSH.ics']
    calendars = [-1] * len(files)
    names = ['Caitlyn', 'Andrew', 'CSH']
    scores = [2, 1, 3]
    status = [[0, "Downloading:"]]
    for name in names:
        status.append([name, 0])
    socketio.emit('loader', status, to=sid)

    getStart = time.time()
    threads = []
    for file in range(len(files)):
        threads.append(Thread(target=downloader.local, args=(start, end, files[file], calendars, file, socketio, sid)))
        threads[file].start()
    for i in range(len(threads)):
        threads[i].join()

    getTime = time.time() - getStart
    status[0][1] = "Calculating:"
    days, max_score, processingTime = calc.getData(calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status, sid)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    socketio.emit('loaded', output, to=sid)


@socketio.on('submit')
def runSlate(data):
    sid = flask.request.sid
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
    
    status = [[0, "Downloading:"]]
    for name in names:
        status.append([name, 0])
    socketio.emit('loader', status, to=sid)

    getStart = time.time()
    calendars = [-1] * len(names)
    threads = []
    for url in range(len(urls)):
        threads.append(Thread(target=downloader.run, args=(start, end, urls[url], calendars, url, socketio, sid)))
        threads[url].start()
    for i in range(len(threads)):
        threads[i].join()
    for calendar in calendars:
        if type(calendar) == str:
            socketio.emit('loader', calendar, to=sid)
            return
    
    getTime = time.time() - getStart
    status[0][1] = "Calculating:"
    days, max_score, processingTime = calc.getData(calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status, sid)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    socketio.emit('loaded', output, to=sid)


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
