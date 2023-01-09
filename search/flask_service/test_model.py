#!/usr/bin/env python3
import pandas
from model import Attribute, Example, Dataset
if __name__ == "__main__":
    csvFile = pandas.read_csv('/home/work/Desktop/list_attr_celeba.csv')
    features = [str(f) for f in csvFile]
    names = [str(n) for n in csvFile.get('image_id')]
    examples = []
    for raw_example in csvFile.values.tolist() :
        attributes = ['0' if atr==-1 else '1' for atr in raw_example[1:]]
        example = Example(raw_example[0],attributes)
        examples.append(example)
    dataset = Dataset(features,examples)
    print(dataset)