#!/usr/bin/env python3
from model import Attribute, Example, Dataset
from methods import knn, SearchTree
from treelib import Tree, Node

"""
import pandas
import random
import os

PATH_TO_CSV = ['list_attr_celeba.csv','../list_attr_celeba.csv','../../list_attr_celeba.csv',]

def generate_example(nb_features: int) -> Example:
    return Example("Random Example",[Attribute(str(random.randint(0, 1))) for j in range(nb_features)])

def test_tree () :
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
    # print(dataset)
    tree = SearchTree(dataset)
    print(tree)
    #user_example = generate_example(len(dataset.features))
    #print(str(user_example))
 """
"""
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
    print("Loading examples ...")
    for raw_example in csvFile.iloc:
        attributes = [Attribute('0') if atr==-1 else Attribute('1') for atr in raw_example[1:]]
        example = Example(raw_example[0],attributes)
        example_list.append(example)
        if(len(example.attributes)>40) : 
            raise ValueError('Example <'+example.name+'> has ' + str(len(example.attributes)) + ' attribute(s): ' + str(len(features)) + ' required. (len(attributes) = '+str(len(attributes))+')')
    print("Loaded "+str(len(example_list))+" examples. \nBuilding dataset ...")
    dataset = Dataset(features,example_list)
    print("Dataset build.")
    print(str(dataset))
    print("Generating random user example ...")
    user_example = generate_example(len(dataset.features))
    print("Random user example :")
    print(str(user_example))
    return(dataset,user_example)

def test_knn(k) :
    dataset,user_example = init_test()
    print("Running KNN with K="+str(k)+" ...")
    knn_result = knn(k,dataset,user_example)
    print(knn_result)

def test_tree() :
    dataset,user_example = init_test()
    print("Generating search tree ...")
    tree = SearchTree(dataset)
    print("Search tree:")
    print(tree)
"""
class TestSearchTree:
    def generic_build(d:Dataset,expected:Tree) :
        assert SearchTree(d) == expected        

    def test_5x5():
        raw = [[0,0,1,1,0],
               [0,1,0,1,0],
               [0,0,0,1,0],
               [0,1,0,1,0],
               [1,1,0,1,0]]
        baked = []       
        for i in range(len(raw)) :
            baked.append([])
            for j in range(len(raw[0])) :
                baked[i].append(Attribute(str(raw[i][j])))
            baked[-1] = Example(str(i),baked[-1])
        d = ("5x5", baked)
        print(str(d))
if __name__ == "__main__":
    TestSearchTree.test_5x5()
