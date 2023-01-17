# Imports
from flask import Flask, request
import os
from PIL import Image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import joblib
import matplotlib.pylab as plt
import matplotlib.pyplot as plt
from PIL import Image
import sys
from tensorflow.keras.models import model_from_json
import tensorflow_hub as hub
import pandas as pd
from PIL import Image
import base64

# Functions


def image_prediction(prediction_score):
    s = ""
    for i, label in enumerate(features_str):
        pred = prediction_score[i][0][0]
        s += f"{label}: predicted {1 if pred > 0.5 else 0} ({format(pred, '.4f')})"
        s += "\n"
    return s


def open_images(inference_folder: str) -> np.ndarray:
    images = []
    for img in os.listdir(inference_folder):
        img_location = os.path.join(inference_folder, img)
        with Image.open(img_location) as img:
            img = np.array(img)
            img = img[:, :, :3]
            img = np.expand_dims(img, axis=0)
        images.append(img)
    images_array = np.vstack(images)
    return images_array


def resize(dirs, path, resized_path):
    for item in dirs:
        print(item)
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            im = im.convert('RGB')
            f, e = os.path.splitext(path+item)
            imResize = im.resize((220, 220), Image.ANTIALIAS)
            imResize.save(resized_path + item +
                          '_resized.jpg', 'JPEG', quality=90)

# Main microservice


app = Flask(__name__)


@app.route("/receive", methods=['POST', 'GET'])
def vector_prediction():
    # Decoding image
    encodedImage = request.data
    decoded_data = base64.b64decode((encodedImage))

    # Saving decoded data as image
    img_file = open('./saved_image/decoded_image.jpg', 'wb')
    img_file.write(decoded_data)
    img_file.close()

    # Features
    features_str = ['Mouth_Slightly_Open', 'Smiling', 'Wearing_Lipstick', 'High_Cheekbones', 'Male', 'Heavy_Makeup', 'Wavy_Hair', 'Oval_Face', 'Pointy_Nose', 'Arched_Eyebrows',
                    'Big_Lips', 'Black_Hair''Big_Nose', 'Young', 'Straight_Hair', 'Brown_Hair', 'Bags_Under_Eyes', 'Wearing_Earrings', 'No_Beard', 'Bangs', 'Blond_Hair', 'Chubby', 'Bald']

    # Resizing image & saving resized image
    path = './saved_image/'
    dirs = os.listdir(path)
    resized_path = './saved_resized_image/'
    resize(dirs, path, resized_path)

    # Opening trained model
    with open('model.json', 'r') as f:
        json = f.read()
        model = model_from_json(json, custom_objects={
                                'KerasLayer': hub.KerasLayer})

    # Prediction
    images = open_images(resized_path)
    prediction_vector = []
    for image in images:
        img_batch = np.expand_dims(image, axis=0)
        normalizedData = (img_batch-np.min(img_batch)) / \
            (np.max(img_batch)-np.min(img_batch))
        prediction_score = model.predict(normalizedData)

    # Creating output vector
    for i, label in enumerate(features_str):
        pred = 1 if prediction_score[i][0][0] > 0.5 else 0
        prediction_vector.append((label, pred))

    return str(prediction_vector)
    # return str(prediction_vector)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8083)
