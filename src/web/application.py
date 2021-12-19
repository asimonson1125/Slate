import flask
from time import sleep
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
      user = flask.request.form['Calendar 1']
      return flask.redirect(flask.url_for('success',name = user))

@app.route('/success/<name>')
def success(name):
   return name

if __name__ == '__main__':
   app.run()