import flask
import datetime
from dateutil import parser
import time
from flask_socketio import SocketIO
from threading import Thread
from flask_login import login_required, current_user

from orgServices import app, ldap
import calc
import downloader
from help import *
from urlGetter import GLogin, GReciept

socketio = SocketIO(app)


@socketio.on('example')
def loadExample():
    """
    A sample run of Slate with predetermined parameters, designed for people who just want to see slate doing shit.
    """
    sid = flask.request.sid
    timezone = -5
    DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
    start = datetime.datetime(2022, 8, 10, 13, 0, 0).replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    end = datetime.datetime(2022, 10, 15, 13, 0, 0).replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    interval = datetime.timedelta(minutes=60)
    length = datetime.timedelta(minutes=60)
    files = ['person1.ics', 'person2.ics', 'person3.ics', 'CSH.ics']
    calendars = [-1] * len(files)
    names = ['Caitlyn', 'Andrew', 'Susan', 'CSH']
    scores = [2, 1, -1, 3]
    # Actually running below

    status = buildStatus(names)
    socketio.emit('loader', status, to=sid)  # build status display

    getStart = time.time()
    threads = []
    for file in range(len(files)):  # load locals cals
        threads.append(Thread(target=downloader.local, args=(
            start, end, files[file], calendars, file, socketio, sid)))
        threads[file].start()
    for i in range(len(threads)):
        threads[i].join()

    getTime = time.time() - getStart
    status[0][1] = "Calculating:"
    days, max_score, processingTime = calc.getData(
        calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status, sid)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[
                                   getTime, processingTime], names=names)
    socketio.emit('loaded', output, to=sid)


@socketio.on('submit')
def runSlate(data):
    """
    Main slate
    """
    sid = flask.request.sid
    urls, names, scores, cType, ignoreErrors, timezone, start, end, daylighSavingsTick, interval, length = data
    timezone = int(timezone)
    start = parser.parse(start).replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    end = parser.parse(end).replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
    DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone))
    if(daylighSavingsTick):
        DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
    interval = datetime.timedelta(minutes=int(interval))
    length = datetime.timedelta(minutes=int(length))

    if start > end:
        flask.abort(416, "Range end time cannot be after start time")

    status = buildStatus(names)
    socketio.emit('loader', status, to=sid)

    getStart = time.time()
    calendars = [-1] * len(names)
    threads = []
    problems = []
    remove = []
    for url in range(len(urls)):  # Download calendars
        error = False
        if not cType[url] == ('manual'):  # Manual calendars already have their urls
            if cType[url] == ('CSH'):  # Get urls from CSH_LDAP
                if current_user.is_authenticated:
                    try:
                        urls[url] = ldap.get_member(
                            urls[url], uid=True).icallink
                    except:
                        problems.append(
                            "Member " + names[url] + " does not have a calendar.")
                        remove.append(url)
                        error = True
                else:
                    socketio.emit(
                        'loader', "User not logged into a CSH account", to=sid)
                    return
            else:
                socketio.emit(
                    'loader', "Unknown member type: " + cType[url], to=sid)
                return
        if(not error):  # Assuming no error, we can try downloading this bitch
            threads.append(Thread(target=downloader.run, args=(
                start, end, urls[url], calendars, url, socketio, sid)))
            threads[len(threads)-1].start()
    for i in range(len(threads)):
        threads[i].join()
    for calendar in range(len(calendars)):
        if type(calendars[calendar]) == str:  # Broken cals are string types
            problems.append(calendars[calendar])
            remove.append(calendar)
            return
        elif type(calendars[calendar]) == bool:  # non-calendars are bool types
            problems.append("Invalid calendar for member " + names[calendar])
            remove.append(calendar)

    if(len(problems) == 0 or ignoreErrors):  # Only compute when no errors or we don't care about errors
        # sorting because errors are logged in different locations.  Would help if I just made a participant class.  But I won't.
        remove = sorted(remove)
        alreadyDeleted = 0
        for i in remove: # removing err'd participants
            names.pop(i - alreadyDeleted)
            scores.pop(i - alreadyDeleted)
            calendars.pop(i - alreadyDeleted)
            alreadyDeleted += 1
    else: # "Hey these calendars suck"
        string = ''
        for i in problems:
            string += i + '\n'
        socketio.emit('loader', string, to=sid)
        return

    getTime = time.time() - getStart
    status[0][1] = "Calculating:"
    days, max_score, processingTime = calc.getData(
        calendars, names, scores, start, end, DSTinfo, interval, length, socketio, status, sid)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[
                                   getTime, processingTime], names=names, errors=problems)
    socketio.emit('loaded', output, to=sid)


@socketio.on('getMembers')
def getMembers(group):
    """
    Sends client list of members from org DB
    """
    if current_user.is_authenticated: # CSH Logged in
        members = ldap.get_group(group).get_members()
        out = []
        for member in members:
            name = member.cn
            username = member.uid
            usergroups = []
            groups = member.groups()
            for group in groups:
                usergroups.append(group[3:group.index(',')])
            out.append({'name': name,
                        'uid': username,
                        'image': 'https://profiles.csh.rit.edu/image/' + username,
                        'groups': usergroups,
                        'type': 'CSH'})
    else: # Not logged in, send sample BS
        out = [{'name': 'Computer Science House',
                           'uid': 'exampleUser1',
                           'image': flask.url_for('static', filename='images/csh.png'),
                           'groups': ['RIT', 'Special Interest House', 'Based', 'Big Honkin Calendar'],
                           'icallink': 'https://www.google.com/calendar/ical/rti648k5hv7j3ae3a3rum8potk%40group.calendar.google.com/public/basic.ics',
                           'type': 'example'},
                          {'name': 'Engineering House',
                           'uid': 'exampleUser2',
                           'image': flask.url_for('static', filename='images/ehouse.png'),
                           'groups': ['RIT', 'Special Interest House'],
                           'icallink': 'https://calendar.google.com/calendar/ical/enghouseevents%40gmail.com/public/basic.ics',
                           'type': 'example'},
                          {'name': 'House of General Science',
                           'uid': 'exampleUser3',
                           'image': flask.url_for('static', filename='images/hogs.png'),
                           'groups': ['RIT', 'Special Interest House'],
                           'icallink': 'https://calendar.google.com/calendar/ical/ko4735rbci43emk20gq2msi3dc%40group.calendar.google.com/public/basic.ics',
                           'type': 'example'},
                          {'name': 'RIT',
                           'uid': 'exampleUser4',
                           'image': flask.url_for('static', filename="images/rit.png"),
                           'groups': ['RIT', 'Big Honkin Calendar'],
                           'icallink': 'https://campusgroups.rit.edu/ical/ical_rit.ics',
                           'type': 'example'},
                          {'name': "FIFA World Cup 2022",
                           'uid': 'exampleUser5',
                           'image': flask.url_for('static', filename='images/worldCup.jpeg'),
                           'groups': ['Sports'],
                           'icallink': 'webcal://calendar.google.com/calendar/ical/3hq899li0lh09cfs1h4bqdsdjs%40group.calendar.google.com/public/basic.ics',
                           'type': 'example'}]
    socketio.emit('memberList', out, to=flask.request.sid)


@socketio.on('checkURL')
def checkURL(url):
    message = downloader.check(url)
    if message == "":
        message = "urlCheck0A calendar was found at this link!"
    else:
        message = "urlCheck1" + message
    socketio.emit('stringtype', message, to=flask.request.sid)



@app.route('/')
def get_in():
    return flask.render_template('input.html')


@app.route('/about')
def get_about():
    return flask.render_template('about.html')


@app.route('/blank')
def get_blank():
    return flask.render_template('blank.html')


@app.route('/verifyURL')
def get_verifier():
    return flask.render_template("verifyURL.html")


@app.route('/tryConnect')
def tryConnector():
    url, state = GLogin(app)
    return flask.redirect(url)

@app.route('/GLogin')
def getSesh():
    GReciept(flask, app)
    return "<h3>haha</h3>"

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
