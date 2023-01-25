import os
from flask import Flask, flash, request, redirect, send_from_directory, url_for, render_template
from markupsafe import escape
from ast import literal_eval
from werkzeug.utils import secure_filename
import flask_monitoringdashboard as dashboard
import numpy as np
import requests
import base64
import time
import sys
# allow files of every image type
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'tif'}

# Define the upload folder constant
UPLOAD_FOLDER = './faces'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024    # 50 Mb limit
dashboard.bind(app)

encoded_string = ""
# global var


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
            with open("./faces/"+filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            # time.sleep(60)
            print("Success!: ")
            print('Hello world!', file=sys.stderr)
            response = requests.post(
                f'http://orchestrateur:8080/transfert_cnn', encoded_string)

            print(response.text, file=sys.stderr)
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('result', name=filename, response=response.text))
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():

    a = request.args.get('response')
    a = "".join(a)
    a = literal_eval(a)
    print(a, sys.stderr)
    # a = requests.args.get('response')

    b = []
    # print(a, sys.stderr)

    print("a get printeddd---------------", sys.stderr)

    # a = [["100.0", '202483.jpg'], [100.0, "202493.jpg"], [
    #     100.0, "202523.jpg"], [100.0, "202532.jpg"], [100.0, "202511.jpg"]]
    ratioList = []
    # a = [["99.89", "132108.jpg"], ["99", '143864.jpg'], ['99', '143369.jpg'],
    #      ["98", '191011.jpg'], ["98", '157682.jpg']]
    # a = [["123456.jpg", 86],
    #      ["123457.jpg", 80],
    #      ["123458.jpg", 50],
    #      ["123459.jpg", 45],
    #      ["123460.jpg", 40]]

    for row in a:
        b.append(row)
    print(b, file=sys.stderr)
    print("--------------------- final B", file=sys.stderr)
    for image in b:
        print(image[1])

    imageList = os.listdir('static/data')
    imageList = ['data/' + image[1] for image in b]
    print(imageList)
    for image in b:
        print(image[1])
    # for image in a:
    #     print(image[1])
    #     ratioList.append(image[1])
    # print(ratioList)
    return render_template('result.html', imageList=imageList, ratioList=b)


@app.route('/faces/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/<url>:<port>/show/<int:k>')
def make_request(url, port, k):
    response = requests.get(f'http://{url}:{port}/show/{k}')
    return response.text


@app.route("/send", methods=['GET'])
def send():
    response = requests.post(f'http://localhost:8083/receive', encoded_string)
    return "Success!: " + response.text


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3141)
