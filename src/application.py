import flask
import datetime
import calc


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
      start = datetime.datetime.now() - datetime.timedelta(hours=9)
      end = datetime.datetime.now() - datetime.timedelta(hours=2)
      interval = datetime.timedelta(minutes=15)
      length = datetime.timedelta(hours=2)
      # for i in
      urls.append(flask.request.form['Calendar 1'])
      in_scores.append(5)
      output = calc.run(urls, in_scores, start, end, interval, length)
      return output

if __name__ == '__main__':
   app.run()