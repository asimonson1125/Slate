import flask
import datetime
import calc
from dateutil import parser

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
   return "Hello World"

@app.route("/test/")
def html_test():
   return flask.render_template('test.html')

@app.route('/run', methods = ['POST'])
def run():
   if flask.request.method == 'POST':
      start = parser.parse(flask.request.form['startTime'])
      end = parser.parse(flask.request.form['endTime'])
      interval = datetime.timedelta(minutes=int(flask.request.form['interval']))
      length = datetime.timedelta(minutes=int(flask.request.form['duration']))
      urls = flask.request.form['Calendar 1'].split('\n')
      str_scores = flask.request.form['Score 1'].split('\n')
      scores = []
      for i in str_scores:
         scores.append(int(i))
      calendars = calc.get_cals(urls)
      if type(calendars) == str: # Problems in calendar loading
         return calendars
      output = calc.run(calendars, scores, start, end, interval, length)
      return output

if __name__ == '__main__':
   app.run()