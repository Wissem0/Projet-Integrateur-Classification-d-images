#!/usr/bin/env python3
from flask import Flask
import base64
import requests

app = Flask(__name__)
encoded_string = ""

@app.route("/send",methods = ['GET'])
def send():
    return str(requests.post(f'http://localhost:8080/receive', encoded_string))    

@app.route("/favicon.ico",methods = ['GET'])
def cache_misere():
    return "Success!"

if __name__ == "__main__":
    with open("image.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    app.run(host='localhost', port=8081)