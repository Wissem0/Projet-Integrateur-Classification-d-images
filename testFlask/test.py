import os
from flask import Flask, flash, request, redirect, url_for, render_template
from markupsafe import escape
from werkzeug.utils import secure_filename
import flask_monitoringdashboard as dashboard

UPLOAD_FOLDER = './faces'
# allow files of every image type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3141)