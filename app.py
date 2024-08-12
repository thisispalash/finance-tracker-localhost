from flask import Flask, render_template, g, send_from_directory
from blueprints import *
from blueprints.db import setup, close_connection

app = Flask(__name__)

app.register_blueprint(db_bp, url_prefix='/db')
app.register_blueprint(files_bp, url_prefix='/files')

app.secret_key = 'my-very-important-secret'

# initialize the database
setup(app)

@app.teardown_appcontext
def shutdown_db(exception):
  close_connection(exception)

@app.route('/')
def home():
  setup()
  return render_template('home.html')

@app.route('/data/<path:path>')
def data(path):
  return send_from_directory('data', path)


if __name__ == '__main__':
  app.run(debug=True)