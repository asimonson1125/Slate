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
      urls = []
      in_scores = []
      start = parser.parse(flask.request.form['startTime'])
      end = parser.parse(flask.request.form['endTime'])
      interval = datetime.timedelta(minutes=int(flask.request.form['interval']))
      length = datetime.timedelta(minutes=int(flask.request.form['duration']))
      # for i in
      urls.append(flask.request.form['Calendar 1'])
      in_scores.append(int(flask.request.form['Score 1']))
      output = calc.run(urls, in_scores, start, end, interval, length)
      return output

if __name__ == '__main__':
   app.run()