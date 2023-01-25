#!/usr/bin/env python3
from model import Attribute, Example, Dataset
from methods import knn
from hypothesis import given, strategies as st

# test method knn : image 1 : 0110000000010000001101001001000110101001
#                             0110000000010000001101001001110110101001
#                           x 0001012244041114043261111101000211103003'

#                            '0000000000040000003201001001000210103003'

import pandas
import random
import os

PATH_TO_CSV = ['list_attr_celeba.csv','../list_attr_celeba.csv','../../list_attr_celeba.csv',]
weights = [0,0,0,1,0,1,2,2,4,4,0,4,1,1,1,4,0,4,3,2,6,1,1,1,1,1,0,1,0,0,0,2,1,1,1,0,3,0,0,3]
# weights = [1 for _ in range(40)]
S_WEIGHTS = sum(weights)
def generate_example(nb_features: int) -> Example:
    return Example("Random Example",[Attribute(str(random.randint(0, 1)),weights[j]) for j in range(nb_features)])
def init_test() :
    path = None
    for trypath in PATH_TO_CSV : 
        if os.path.isfile(trypath) :
            path = trypath
            break
    if not path : 
        raise FileExistsError("No file found in any of the following location: \n"+str(PATH_TO_CSV))
    
    print("Loading "+path+" ...")
    csvFile = pandas.read_csv(path)
    print("Listing features ...")
    features = list(csvFile.axes[1][1:])
    print("Found "+str(len(features))+" features. \nLoading image names . . .")
    names = [str(n) for n in csvFile.get('image_id')]
    print("Found "+str(len(names))+" image names.")
    example_list = []
    # weights = [random.randint(1,10) for _ in range(len(features))]
    print("Loading examples with weight "+ str (weights)+"...")
    for raw_example in csvFile.iloc:
        attributes = [Attribute('0') if raw_example[1:][atr]==-1 else Attribute('1') for atr in range(len(raw_example[1:]))]
        # print([str(k) for k in attributes])
        example = Example(raw_example[0],attributes)
        example_list.append(example)
        if(len(example.attributes)>40) : 
            raise ValueError('Example <'+example.name+'> has ' + str(len(example.attributes)) + ' attribute(s): ' + str(len(features)) + ' required. (len(attributes) = '+str(len(attributes))+')')
    print("Loaded "+str(len(example_list))+" examples. \nBuilding dataset ...")
    dataset = Dataset(features,example_list,weights)
    print("Dataset build.")
    print(str(dataset))
    print("Generating random user example ...")
    user_example = generate_example(len(dataset.features))
    print("Random user example :")
    print(str(user_example))
    return(dataset,user_example)

def essai_knn(k) :
    dataset,user_example = init_test()
    print("Running KNN with K="+str(k)+" ...")
    knn_result = knn(k,dataset,user_example)
    print(knn_result)
# Testing various properties for the Hamming distance
class TestKNN :
    def setup(self) :
        self.dataset,_ = init_test()

    def distance_from_self(self, e_id:int):
        # Image 00001.jpg
        # user_example = Example("user",[Attribute(k) for k in "0110000000010000001101001001000110101001"])
        user_example = self.dataset.examples[e_id]
        print( str(user_example.attributes) )
        # print("Running KNN with K="+str(1)+" ...")
        knn_result = knn(1,self.dataset,user_example)
        # print(knn_result)
        # print(knn_result[0])
        knn_result = [(n[0] * 100 / S_WEIGHTS, n[1]) for n in knn_result]
        assert knn_result[0][0] == 100.0

    def test_distance_from_self(self) :
        self.setup()
        for _ in range(10):
            print(str(_))
            self.distance_from_self(random.randint( 0, len(self.dataset.examples)))
