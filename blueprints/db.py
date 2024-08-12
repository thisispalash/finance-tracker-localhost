import sqlite3
from flask import g, Blueprint, current_app

db_bp = Blueprint('db', __name__)

DATABASE = 'finances.db'

def setup(app=None):
  app = app or current_app
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  return db

def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()
    
  
## Receipts ##

def add_receipt(hash, store, date, time, count, total):
  db = get_db()
  cursor = db.cursor()
  try:
    cursor.execute(
      'INSERT INTO receipts (img_hash, store, date, time, count, total) VALUES (?, ?, ?, ?, ?, ?)', 
      [hash, store, date, time, count, total]
    )
    db.commit()
    receipt_id = cursor.lastrowid
  except sqlite3.IntegrityError as e:
    print('Error:', e)
    receipt_id = None
  finally:
    cursor.close()
  return receipt_id

def add_receipt_item(receipt_id, item, price):
  db = get_db()
  cursor = db.cursor()
  cursor.execute(
    'INSERT INTO items (receipt_id, item, price) VALUES (?, ?, ?)', 
    [receipt_id, item, price]
  )
  db.commit()
  cursor.close()