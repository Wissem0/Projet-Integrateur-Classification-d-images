import os
from flask import Flask, flash, request, redirect, url_for, render_template
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
    return '''
    <!DOCTYPE html>
    <html style = 'overflow-y:hidden'>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Upload new File</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
            <style>
                html, body {
                    height: 100%;
                }

                .footer {
                    position: absolute;
                    bottom: 0;
                    width: 100%;
                    height: 60px; /* Set the height of the footer */
                }
            </style>
        </head>
        <body>
        <section class="section">
            <div class="container has-text-centered">
                <h1 class="title is-1">
                    Upload new File
                </h1>
                <form method="post" enctype="multipart/form-data">
                    <div class="field">
                        <div class="file has-name is-fullwidth">
                            <label class="file-label">
                                <input class="file-input" type="file" name="file" onchange="displayFileName(this)">
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span class="file-label">
                                        Choose a file…
                                    </span>
                                </span>
                                <span class="file-name has-text-left">
                                    No file chosen
                                </span>
                            </label>
                        </div>
                    </div>
                    <div class="field is-grouped is-grouped-right">
                        <div class="control">
                            <input type="submit" value="Upload" class="button is-primary">
                        </div>
                    </div>
                </form>
            </div>
        </section>
        <footer class="footer">
            <div class="content has-text-centered">
                <p>
                <strong>Classimage</strong>. The source code is licensed
                <a href="http://opensource.org/licenses/mit-license.php">MIT</a>. The website content
                is licensed <a href="http://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.
                </p>
            </div>
        </footer>
        <script>
            // Get the input element
            var input = document.querySelector('input[type="file"]');

            // Listen for changes to the input element
            input.addEventListener('change', displayFileName);

            function displayFileName() {
                // Get the file name from the input element
                var fileName = input.value;

                // Split the path by the '\\' character to get the file name
                var fileName = fileName.replace(/^.*[\\\/]/, '');

                // Get the file name display element
                var fileNameDisplay = document.querySelector('.file-name');

                // Set the file name display text to the selected file name
                fileNameDisplay.innerHTML = fileName;
            }
        </script>
        </body>
    </html>
    '''

@app.route('/<url>:<port>/show/<int:k>')
def make_request(url, port, k):
    response = requests.get(f'http://{url}:{port}/show/{k}')
    return response.text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3141)