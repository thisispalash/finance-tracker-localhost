import os
import base64
import hashlib
import pytesseract
from io import BytesIO
from PIL import Image
from flask import Blueprint, request
from flask import redirect, url_for, render_template, jsonify

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
    ext = file.filename.split('.')[-1]
    # check if the file exists
    if os.path.exists(f'./data/receipts/{name}'):
      return { 'message': 'Receipt already exists' }, 406
    # save the file
    os.mkdir(f'./data/receipts/{name}')
    file.stream.seek(0)
    file.save(f'./data/receipts/{name}/receipt.{ext}')
    return redirect(url_for('files.process_receipt', receipt_name=name, extension=ext))
  return { 'message': 'No receipt found' }, 400

@files_bp.route('/receipt', methods=['GET'])
def process_receipt():
  receipt_name = request.args.get('receipt_name')
  extension = request.args.get('extension')
  return render_template('process-receipt.html', receipt_name=receipt_name, extension=extension)

@files_bp.route('/receipt', methods=['POST'])
def process_boxes():
  data = request.json
  receipt_name = data['receipt_name']
  boxes = data['boxes']
  
  results = []
  
  for i, box in enumerate(boxes):
    b64 = box['b64Image'].split(',')[1]
    img_data = base64.b64decode(b64)
    cropped = Image.open(BytesIO(img_data))
  
    cropped_path = f'./data/receipts/{receipt_name}/{box["boxType"]}_{i}.png'
    cropped.save(cropped_path)
    
    text = pytesseract.image_to_string(cropped)
    
    results.append({
      'boxType': box['boxType'],
      'text': text,
      'path': cropped_path
    })
  
  return jsonify(results), 200