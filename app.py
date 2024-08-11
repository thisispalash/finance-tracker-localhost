from flask import Flask, render_template, g
from blueprints import *

app = Flask(__name__)

app.register_blueprint(db_bp, url_prefix='/db')
app.register_blueprint(files_bp, url_prefix='/files')

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/data')
def data():
  return render_template('data.html')

@app.route('/upload-receipt')
def upload_receipt():
  return render_template('upload_receipt.html')


if __name__ == '__main__':
  app.run(debug=True)