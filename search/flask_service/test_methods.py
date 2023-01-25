#!/usr/bin/env python3
from model import Attribute, Example, Dataset
from methods import knn
import random

def generate_example(nb_features: int) -> Example:
    return Example("Random Example",[Attribute(str(random.randint(0, 1))) for j in range(nb_features)])
def init_test() :
    N_FEATURES = 40
    N_EXAMPLES = 1000
    e = []
    for _ in range(N_EXAMPLES):
        e.append(generate_example(N_FEATURES))
    d = Dataset([str(f) for f in range(N_FEATURES)], e, [random.randint(0, 10) for _ in range(N_FEATURES)])
    return d

def essai_knn(k) :
    dataset,user_example = init_test()
    print("Running KNN with K="+str(k)+" ...")
    knn_result = knn(k,dataset,user_example)
    print(knn_result)
class TestKNN :
    def setup(self) :
        self.dataset = init_test()

    def distance_from_self(self, e_id:int):
        user_example = self.dataset.examples[e_id]
        print( str(user_example.attributes) )
        knn_result = knn(1,self.dataset,user_example)
        knn_result = [(n[0] * 100 / self.dataset.sum_weights, n[1]) for n in knn_result]
        assert knn_result[0][0] == 100.0

    def test_distance_from_self(self) :
        self.setup()
        for _ in range(10):
            print(str(_))
            self.distance_from_self(random.randint( 0, len(self.dataset.examples)))
