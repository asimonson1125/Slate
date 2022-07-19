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
    socketio.emit('loader', ["Calendar 1", "Calendar 2"])
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
    getStart = time.time()
    for file in files:
        with open('src/static/calendars/' + file, encoding="utf8") as chat:
            g = chat.read()
        cal = icalendar.Calendar.from_ical(g)
        calendars.append(calc.cleanCal(cal, start, end))
    getTime = time.time() - getStart
    days, max_score, processingTime = calc.getData(calendars, names, scores, start, end, DSTinfo, interval, length)
    output = flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    socketio.emit('loaded', output)


@app.route('/')
def get_in():
    return flask.render_template('input.html')


@app.route('/results', methods=['POST', 'GET'])
def renderResults():
    if flask.request.method == 'POST':
        pass
    else:
        return "It's hard to display results if you didn't submit anything!"


@app.route('/run', methods=['POST', 'GET'])
def run():
    if flask.request.method == 'POST':
        timezone = int(flask.request.form['utc-offset'])
        start = parser.parse(flask.request.form['startTime']).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
        end = parser.parse(flask.request.form['endTime']).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
        DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone))
        try:
            flask.request.form['daylightSavingsTick']
            DSTinfo = datetime.timezone(datetime.timedelta(hours=timezone+1))
        except:
            pass

        if start > end:
            flask.abort(416, "Range end time cannot be after start time")
        interval = datetime.timedelta(
            minutes=int(flask.request.form['interval']))
        length = datetime.timedelta(
            minutes=int(flask.request.form['duration']))
        valueAdded = True
        id = 1
        urls = []
        names = []
        scores = []
        max_score = 0
        while(valueAdded):
            try:
                cal = flask.request.form["Calendar " + str(id)]
                if(len(cal) > 0):
                    urls.append(cal)
                    name = flask.request.form["Name " + str(id)]
                    if len(name) < 1:
                        name = "Calendar " + str(id)
                    names.append(name)
                    score = int(flask.request.form["Score " + str(id)])
                    if(score > 0):
                        max_score += score
                    scores.append(score)
                    id += 1
                else:
                    valueAdded = False
            except Exception:
                valueAdded = False
        getStart = time.time()
        calendars = calc.get_cals(urls, start, end)
        if type(calendars[0]) == str:  # Problems in calendar loading
            flask.abort(406, calendars)
        getTime = time.time() - getStart
        processStart = time.time()
        output, maxIntervals = calc.run(calendars, names, scores, start, end, interval, length, DSTinfo)
        processingTime = time.time() - processStart
        days = calc.splitDays(output, maxIntervals)
        return flask.render_template('dataOut.html', days=days, max_score=max_score, timer=[getTime, processingTime], names=names)
    else:
        return "It's hard to display results if you didn't submit anything!"

@app.route('/about')
def get_about():
    return flask.render_template('about.html')

@app.route('/example')
def get_example():
    return flask.render_template('example.html')


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
