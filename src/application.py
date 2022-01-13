import flask
import datetime
import calc
from dateutil import parser
import math

app = flask.Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello World"


@app.route("/test/")
def html_test():
    return flask.render_template('test.html')


@app.route('/run', methods=['POST', 'GET'])
def run():
    if flask.request.method == 'POST':
        start = parser.parse(flask.request.form['startTime'])
        end = parser.parse(flask.request.form['endTime'])
        if start > end:
            flask.abort(416, "Range end time cannot be after start time")
        interval = datetime.timedelta(
            minutes=int(flask.request.form['interval']))
        length = datetime.timedelta(
            minutes=int(flask.request.form['duration']))
        urls = flask.request.form['Calendar 1'].split('\n')
        str_scores = flask.request.form['Score 1'].split('\n')
        scores = []
        max_score = 0
        for i in str_scores:
            intVer = int(i)
            scores.append(intVer)
            if intVer > 0:
                max_score += intVer
        calendars = calc.get_cals(urls)
        if type(calendars[0]) == str:  # Problems in calendar loading
            flask.abort(406, calendars)
        output = calc.run(calendars, scores, start, end, interval, length)
        days = calc.splitDays(output, math.ceil(86400/interval.total_seconds()))
        return flask.render_template('dataOut.html', days=days, max_score=max_score)
    else:
        return "stop that."


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
