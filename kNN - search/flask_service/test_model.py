#!/usr/bin/env python3
import pandas, os
from model import Attribute, Example, Dataset
PATH_TO_CSV = ['list_attr_celeba.csv','../list_attr_celeba.csv','../../list_attr_celeba.csv',]
if __name__ == "__main__":
    
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
