from flask import Flask, render_template, g, send_from_directory
from blueprints import *

app = Flask(__name__)

app.register_blueprint(db_bp, url_prefix='/db')
app.register_blueprint(files_bp, url_prefix='/files')

app.secret_key = 'my-very-important-secret'

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/data/<path:path>')
def data(path):
  return send_from_directory('data', path)


if __name__ == '__main__':
  app.run(debug=True)