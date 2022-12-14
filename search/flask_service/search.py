#!/usr/bin/env python3
from flask import Flask
import random
import heapq
app = Flask(__name__)
NB_FEATURES = 5
DB = [''.join(map(str, [random.randint(0, 1) for j in range(NB_FEATURES)])) for k in range(20000)]

# Returns Hamming distance between two binary numbers
def hamming_distance(v1:str,v2:str) -> int :
    if len(v1) != len(v2) :
        raise ValueError("Binary vectors should have same lenght (len(v1)="+str(len(v1))+",len(v2)="+str(len(v2)))
    return sum([ int(bit) for bit in bin(int(v1,base=2)^int(v2,base=2))[2:]])

# KNN-BASED METHODS
## K-Nearest Neighbors
@app.route("/knn/<user_vector>/<int:k>")
def search(user_vector:str,k:int,dataset:list[str]=DB):
    k_nearest = []
    for vector_id in range(len(DB)) :
        vector = DB[vector_id]
        d = hamming_distance(vector,user_vector)
        k_nearest.append((d,vector_id))
        k_nearest.sort(key=lambda tup: tup[0])
        if len(k_nearest) > k :
            k_nearest.pop(0)
    return str(k_nearest)
## Improved version:
## - use a heap to store the k nearest neighbors
## - use a dictionary to store the distance between the user and the vectors
## - use a set to store the vectors that have been visited
@app.route("/knn_heap/<user_vector>/<int:k>")
def search_heap(user_vector:str,k:int)->str:
    k_nearest = []
    visited = set()
    distances = {}
    for vector_id in range(len(DB)) :
        vector = DB[vector_id]
        d = hamming_distance(vector,user_vector)
        distances[vector_id] = d
        if len(k_nearest) < k :
            heapq.heappush(k_nearest,(d,vector_id))
        else :
            heapq.heappushpop(k_nearest,(d,vector_id))
    return str(k_nearest)

## TODO: use Kd-tree
@app.route("/knn_kdtree/<user_vector>/<int:k>")
def search_kdtree(user_vector:str,k:int)->int:
    pass

## TODO: use LSH
@app.route("/knn_lsh/<user_vector>/<int:k>")
def search_lsh(user_vector:str,k:int)->int:
    pass

# SEARCH TREE METHODS
#class SearchTree:
#    from tree import Tree
#
#    @app.route("/build")
#    def build(self,dataset:Dataset=DB)->Tree:
#        pass 
#    ## TODO: search tree
#    @app.route("/tree/<user_vector>")
#    def search_tree(self,user_vector:str)->list(int):
#        pass
#
#    ## TODO: search & prune
#    @app.route("/tree/<user_vector>") 
#    def KNN_search_tree(self,user_vector:str, accuracy:int)->list(int):
#        pass

@app.route("/show/<int:k>")
def show(k):
    return str(k)

@app.route("/nb_feature")
def get_nb_feature():
    return NB_FEATURES

@app.route("/generate_example")
def generate_example():
    return ''.join(map(str, [random.randint(0, 1) for j in range(NB_FEATURES)]))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
