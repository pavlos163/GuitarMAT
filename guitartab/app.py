import os
import mir
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/')
PLOT_FOLDER = os.path.join(APP_ROOT, 'static/plots/')
ALLOWED_EXTENSIONS = set(['.wav', '.mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    if 'file' not in request.files:
      flash('No file part')
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      handle_file(file)
    return render_template('index.html', request="POST")

def handle_file(file):
  filename = secure_filename(file.filename)
  filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  file.save(filepath)
  mir.save_plot(filepath)
  os.remove(filepath)

if __name__ == "__main__":
  app.run()