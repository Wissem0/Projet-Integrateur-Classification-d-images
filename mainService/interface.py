import os
from flask import Flask, flash, request, redirect, send_from_directory, url_for, render_template
from markupsafe import escape
from werkzeug.utils import secure_filename
import flask_monitoringdashboard as dashboard
import requests

# allow files of every image type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

# Define the upload folder constant
UPLOAD_FOLDER = './faces'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit
dashboard.bind(app)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', name=filename))
    return render_template('index.html')

@app.route('/faces/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/<url>:<port>/show/<int:k>')
def make_request(url, port, k):
    response = requests.get(f'http://{url}:{port}/show/{k}')
    return response.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3141)