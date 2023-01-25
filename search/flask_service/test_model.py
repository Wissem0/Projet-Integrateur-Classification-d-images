#!/usr/bin/env python3
from model import Attribute, Example, Dataset
import random

def generate_example(nb_features: int) -> Example:
    return Example("Random Example",[Attribute(str(random.randint(0, 1))) for j in range(nb_features)])

# Testing various properties for the Hamming distance
class TestHamming:

    # e1 = e2 <=> d(e1,e2) = 0
    def test_separation(self):
        for k in range(5,200,10):
            e1 = generate_example(k)
            e2 = generate_example(k)
            d = Dataset([str(f) for f in range(k)], [e1,e2], [random.randint(0,10) for _ in range(k)])
            # Vectors are either different or their distance is 0
            assert (d.hamming_distance(e1,e2) == 0) != (e1.attributes != e2.attributes)

    # d(e1,e2) = d(e2,e1)
    def test_symmetry(self):
        for k in range(5, 200, 10):
            e1 = generate_example(k)
            e2 = generate_example(k)
            d = Dataset([str(f) for f in range(k)], [e1, e2], [random.randint(0,10) for _ in range(k)])
            # Vectors can be mirrored in the function
            assert d.hamming_distance(e1,e2) == d.hamming_distance(e2,e1)

    # d(e1, e3) <= d(e1,e2) + d(e2,e3)
    def test_triangle_inequality(self):
        for k in range(5, 200, 10):
            e1 = generate_example(k)
            e2 = generate_example(k)
            e3 = generate_example(k)
            d = Dataset([str(f) for f in range(k)], [e1, e2, e3], [random.randint(0,10) for _ in range(k)])
            # Distance respects triangle inequality
            assert d.hamming_distance(e1,e3) <= d.hamming_distance(e1,e2) + d.hamming_distance(e2,e3)