import os
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import librosa
import numpy as np

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['wav', 'mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "GET":
    return render_template('index.html', request="GET")
  else:
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('index.html', request="POST")

if __name__ == "__main__":
  app.run()