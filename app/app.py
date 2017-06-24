import os
from transcription import transcribe
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(APP_ROOT, 'static/')
ALLOWED_EXTENSIONS = set(['.wav', '.mp3', '.aif'])

app = Flask(__name__, static_url_path=STATIC_FOLDER)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = STATIC_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5
app.debug = True
app.secret_key = 'notverysecret'

def allowed_file(filename):
  return (
    '.' in filename 
    and os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS
  )

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == "GET":
    return render_template('index.html', request="GET")
  else:
    print "lol"
    if 'file' not in request.files:
      print "no file"
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    print file
    if file.filename == '':
      print "no filename"
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      print "yay"
      pitches = handle_file(file)
    else:
      print "wrong file extension"
      flash('Wrong file extension.')
      return redirect(request.url)
    return render_template('index.html', request="POST", pitches=pitches)

@app.route('/mxl')
def mxl():
  return send_from_directory(STATIC_FOLDER, 'piece.mxl')

def handle_file(file):
  filename = secure_filename(file.filename)
  filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(filepath)
  pitches = transcribe(filepath, STATIC_FOLDER)
  os.remove(filepath)
  return pitches

if __name__ == "__main__":
  app.run()