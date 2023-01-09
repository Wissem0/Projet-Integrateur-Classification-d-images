#!/usr/bin/env python3
from flask import Flask
from methods import knn
from model import Attribute, Example, Dataset 
import pandas

app = Flask(__name__)
dataset = None 

@app.route("/search/<user_vector>", methods=['POST','GET'])
def search(user_vector:str):
    v = [k for k in user_vector]
    s = knn(50,dataset,Example("osef",v))
    print(str(v))
    return str(s)

if __name__ == "__main__":
    csvFile = pandas.read_csv('../../list_attr_celeba.csv')
    features = csvFile.axes[1][1:]
    names = [str(n) for n in csvFile.get('image_id')]
    # print(features)
    examples = []
    for raw_example in csvFile.values.tolist() :
        attributes = ['0' if atr==-1 else '1' for atr in raw_example[1:]]
        example = Example(raw_example[0],attributes)
        examples.append(example)
    dataset = Dataset(features,examples)
    app.run(host='localhost', port=8084)