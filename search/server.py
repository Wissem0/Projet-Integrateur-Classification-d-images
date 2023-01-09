#!/usr/bin/env python3
from flask import Flask,request
import base64
 
app = Flask(__name__)

@app.route("/receive",methods = ['POST','GET'])

def receive():
    encoded = request.data
    decoded_data=base64.b64decode((encoded))
    #write the decoded data back to original format in  file
    img_file = open('image_decoded.jpg', 'wb')
    img_file.write(decoded_data)
    img_file.close()
    return encoded
                        
if __name__ == "__main__":
    #decode base64 string data
    app.run(host='localhost', port=8080)