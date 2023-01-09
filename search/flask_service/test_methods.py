#!/usr/bin/env python3
import pandas
import random
from model import Attribute, Example, Dataset
from methods import knn, SearchTree
from treelib import Tree, Node

def generate_example(nb_features: int) -> Example:
    return Example("Random Example",[random.randint(0, 1) for j in range(nb_features)])

def test_knn () :
    csvFile = pandas.read_csv('../../list_attr_celeba.csv')
    features = csvFile.axes[1][1:]
    names = [str(n) for n in csvFile.get('image_id')]
    print(features)
    examples = []
    for raw_example in csvFile.values.tolist() :
        attributes = ['0' if atr==-1 else '1' for atr in raw_example[1:]]
        example = Example(raw_example[0],attributes)
        examples.append(example)
    dataset = Dataset(features,examples)
    print(dataset)
    user_example = generate_example(len(dataset.features))
    print(str(user_example))
    knn_result = knn(10,dataset,user_example)
    print(knn_result)

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
    

if __name__ == "__main__":
    test_tree ()
