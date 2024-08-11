import os
import hashlib
from flask import Blueprint, request

files_bp = Blueprint('files', __name__)
BUFFER_SIZE = 65536 # 64KB
md5 = hashlib.md5()
sha256 = hashlib.sha256()

def hash_file_sha256(file):
  file.stream.seek(0)
  for chunk in iter(lambda: file.stream.read(BUFFER_SIZE), b''):
    sha256.update(chunk)
  return sha256.hexdigest()

@files_bp.route('/receipt', methods=['POST'])
def upload_receipt():
  print(request.files)
  file = request.files['receipt']
  if file:
    name = hash_file_sha256(file)
    ext = file.filename.split('.')[-1]
    # check if the file exists
    if os.path.exists(f'./data/receipts/{name}.{ext}'):
      return { 'message': 'Receipt already exists' }, 406
    # save the file
    file.stream.seek(0)
    file.save(f'./data/receipts/{name}.{ext}')
    return { 'message': 'Receipt uploaded successfully' }, 200
  return { 'message': 'No receipt found' }, 400