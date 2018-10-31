import hashlib

from flask import Flask, send_from_directory
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import uuid
import shutil

UPLOAD_FOLDER = 'dragon_data'
UPLOAD_FOLDER_TMP = 'dragon_data_tmp'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_TMP'] = UPLOAD_FOLDER_TMP


@app.route('/')
def hello():
    return "Welcome to file storage!"


@app.route('/download/<string:file_hash>', methods=['GET', 'POST'])
def dragon_download(file_hash):
    file_dir = app.config['UPLOAD_FOLDER'] + "/" + file_hash[:2]
    file_path = file_dir + "/" + file_hash
    if os.path.exists(file_path):
        return send_from_directory(directory=file_dir, filename=file_hash)
    else:
        return "file not found"


@app.route('/delete/<string:file_hash>')
def dragon_delete(file_hash):
    file_path = app.config['UPLOAD_FOLDER'] + "/" + file_hash[:2] + "/" + file_hash
    if os.path.exists(file_path):
        os.remove(file_path)
        return 'deleted ' + file_hash
    else:
        return 'file not found'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def dragon_upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "not file"

        file = request.files['file']
        if file.filename == '':
            return "no file"

        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # save to tmp dir
            uuid_file_path = app.config['UPLOAD_FOLDER_TMP'] + "/" + uuid.uuid1().__str__()
            file.save(uuid_file_path)
            file.close()

            file_hash = get_file_hash(uuid_file_path)
            file_dir = app.config['UPLOAD_FOLDER'] + "/" + file_hash[:2]
            os.makedirs(file_dir, exist_ok=True)
            file_path = file_dir + "/" + file_hash

            # move from tmp dir to storage
            if not os.path.exists(file_path):
                shutil.move(uuid_file_path, file_path)
                return file_hash
            else:
                return "file already exists " + file_hash


def get_file_hash(uuid_file_path):
    with open(uuid_file_path, 'rb') as uuid_file:
        file_hash = hashlib.md5(uuid_file.read()).hexdigest()
    return file_hash


def start():
    app.run()
    # gunicorn project:app --daemon


if __name__ == '__main__':
    start()
