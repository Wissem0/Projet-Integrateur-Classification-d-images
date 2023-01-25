#!/usr/bin/env python3
from flask import Flask
from methods import knn
from model import Attribute, Example, Dataset
import pandas
import os

app = Flask(__name__)
dataset = None
PATH_TO_CSV = ['list_attr_celeba.csv',
               '../list_attr_celeba.csv', '../../list_attr_celeba.csv',]

# WEIGHTS = [0,0,0,1,0,1,2,2,4,4,0,4,1,1,1,4,0,4,3,2,6,1,1,1,1,1,0,1,0,0,0,2,1,1,1,0,3,0,0,3]
WEIGHTS = [1 for _ in range(40)]
S_WEIGHTS = 100/sum(WEIGHTS)
@app.route("/search/<user_vector>", methods=['POST', 'GET'])
def search(user_vector: str):
    # v = [Attribute(k) for k in user_vector]
    v = []
    for k in range(len(user_vector)) :
        v.append(Attribute(user_vector[k]))
    s = knn(5, dataset, Example("user", v))
    s = [ (str(n[0]*S_WEIGHTS),n[1]) for n in s ]
    return {"res": s}

@app.route("/")
def help():
    return "<b>Welcome to my brand new webpage.</b><div>Services available:</div><div>- /search/< binary vector (size = "+str(len(dataset.features))+")><div/>"


if __name__ == "__main__":

    path = None
    for trypath in PATH_TO_CSV:
        if os.path.isfile(trypath):
            path = trypath
            break
    if not path:
        raise FileExistsError(
            "No file found in any of the following location: \n"+str(PATH_TO_CSV))

    print("Loading "+path+" ...")
    csvFile = pandas.read_csv(path)
    print("Listing features ...")
    features = list(csvFile.axes[1][1:])

    print("Found "+str(len(features))+" features. \nLoading image names . . .")
    names = [str(n) for n in csvFile.get('image_id')]
    print("Found "+str(len(names))+" image names.")
    example_list = []
    print("Loading examples ...")
    for raw_example in csvFile.iloc:
        attributes = [Attribute('0') if raw_example[1:][atr] == -1 else Attribute('1')
                      for atr in range(len(raw_example[1:]))]

        example = Example(raw_example[0], attributes)
        example_list.append(example)
        if (len(example.attributes) > len(features)):
            raise ValueError('Example <'+example.name+'> has ' + str(len(example.attributes)) +
                             ' attribute(s): ' + str(len(features)) + ' required. (len(attributes) = '+str(len(attributes))+')')
    print("Loaded "+str(len(example_list))+" examples. \nBuilding dataset ...")
    dataset = Dataset(features, example_list, WEIGHTS)
    print("Dataset build.")
    print(str(dataset))
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
