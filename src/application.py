import flask
import datetime
from dateutil import parser
import time
from flask_socketio import SocketIO
from threading import Thread
from flask_login import login_required

from orgServices import app, ldap
import calc
import downloader


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
    files = ['person1.ics', 'person2.ics', 'person3.ics', 'CSH.ics']
    calendars = [-1] * len(files)
    names = ['Caitlyn', 'Andrew', 'Susan', 'CSH']
    scores = [2, 1, -1, 3]
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

@socketio.on('getMembers')
def getMembers(group):
    members = ldap.get_group(group).get_members()
    out = []
    for member in members:
        name = member.cn
        username = member.uid
        usergroups = []
        groups = member.groups()
        link = members.get('icallink')
        for group in groups:
            usergroups.append(group[3:group.index(',')])
        out.append({'name':name,
                    'uid':username,
                    'groups':usergroups,
                    'icallink': link})
    socketio.emit('memberList', out, to=flask.request.sid)


@app.route('/in')
@login_required
def get_in():
    return flask.render_template('input.html')

@app.route('/about')
@login_required
def get_about():
    return flask.render_template('about.html')

@app.route('/blank')
def get_blank():
    return flask.render_template('blank.html')


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
