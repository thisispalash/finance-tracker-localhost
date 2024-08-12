import os
import base64
import hashlib
import pytesseract
from PIL import Image
from io import BytesIO
from pprint import pprint
from flask import Blueprint, request, flash
from flask import redirect, url_for, render_template, jsonify

from blueprints.db import add_receipt, add_receipt_item

files_bp = Blueprint('files', __name__)
BUFFER_SIZE = 65536 # 64KB
md5 = hashlib.md5()
sha256 = hashlib.sha256()

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def hash_file_sha256(file):
  file.stream.seek(0)
  for chunk in iter(lambda: file.stream.read(BUFFER_SIZE), b''):
    sha256.update(chunk)
  return sha256.hexdigest()

@files_bp.route('/receipt', methods=['PUT'])
def upload_receipt():
  print(request.files)
  file = request.files['receipt']
  if file:
    name = hash_file_sha256(file)
    print(name)
    ext = file.filename.split('.')[-1]
    # check if the file exists
    if os.path.exists(f'./data/receipts/{name}'):
      return { 'message': 'Receipt already exists' }, 406
    # save the file
    os.mkdir(f'./data/receipts/{name}')
    file.stream.seek(0)
    file.save(f'./data/receipts/{name}/receipt.{ext}')
    return redirect(url_for('files.process_receipt', receipt_name=name, extension=ext), code=303)
  return { 'message': 'No receipt found' }, 400

@files_bp.route('/receipt', methods=['GET'])
def process_receipt():
  print(request.args)
  receipt_name = request.args.get('receipt_name')
  extension = request.args.get('extension')
  return render_template('process-receipt.html', receipt_name=receipt_name, extension=extension)

@files_bp.route('/receipt', methods=['POST'])
def process_boxes():
  data = request.json
  receipt_name = data['receipt_name']
  boxes = data['boxes']
  
  items, prices = [], []
  
  for i, box in enumerate(boxes):
    b64 = box['b64Image'].split(',')[1]
    img_data = base64.b64decode(b64)
    cropped = Image.open(BytesIO(img_data))
  
    cropped_path = f'./data/receipts/{receipt_name}/{box["boxType"]}_{i}.png'
    cropped.save(cropped_path)
    
    text = pytesseract.image_to_string(cropped)
    print(box['boxType'], text, )
    if box['boxType'] == 'items':
      items += text.splitlines()
    elif box['boxType'] == 'prices':
      prices += text.splitlines()
      
  results = { 'items': items, 'prices': prices, 'count': max(len(items), len(prices)) }
  return jsonify(results), 200

@files_bp.route('/receipt', methods=['PATCH'])
def save_to_db():
  data = request.form
  pprint(data, indent=2)

  hash = data['receipt_name']
  store = data['store']
  date = data['date']
  time = data['time']
  count = int(data['count'])
  total = data['total']
  
  receipt_id = add_receipt(hash, store, date, time, count, total)
  
  for key in data.keys():
    if key.startswith('item_'):
      idx = key.split('_')[-1]
      item = data[f'item_{idx}']
      price = data[f'price_{idx}']
      
      if item and price:
        add_receipt_item(receipt_id, item, price)
  
  flash('Saved to DB!')
  
  return { 'message': 'Saved to DB' }, 200