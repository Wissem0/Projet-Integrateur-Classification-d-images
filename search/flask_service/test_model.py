#!/usr/bin/env python3
import pandas
from model import Attribute, Example, Dataset
if __name__ == "__main__":
    csvFile = pandas.read_csv('list_attr_celeba.csv')
    features = list(csvFile.axes[1][1:])
    print(features)
    names = [str(n) for n in csvFile.get('image_id')]
    # print(features)
    examples = []
    print(str(len(csvFile.values.tolist()[0])))
    print(str(len(csvFile.iloc[0][1:]))+" "+str(list(csvFile.iloc[0][1:])))
    for raw_example in csvFile.iloc:
        attributes = [Attribute('0') if atr==-1 else Attribute('1') for atr in raw_example[1:]]
        example = Example(raw_example[0],attributes)
        examples.append(example)
        if(len(example.attributes)>40) : 
            raise ValueError('Example <'+example.name+'> has ' + str(len(example.attributes)) + ' attribute(s): ' + str(len(features)) + ' required.')
    dataset = Dataset(features,examples)
    print(dataset)