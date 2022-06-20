import flask
import datetime
import calc
from dateutil import parser
import time

app = flask.Flask(__name__)


@app.route('/')
def get_in():
    return flask.render_template('input.html')


@app.route('/run', methods=['POST', 'GET'])
def run():
    if flask.request.method == 'POST':
        timezone = int(flask.request.form['utc-offset'])
        start = parser.parse(flask.request.form['startTime']).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
        end = parser.parse(flask.request.form['endTime']).replace(tzinfo=datetime.timezone(datetime.timedelta(hours=timezone)))
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
                    names.append(flask.request.form["Name " + str(id)])
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
        output, maxIntervals = calc.run(calendars, names, scores, start, end, interval, length)
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
    app.run()
