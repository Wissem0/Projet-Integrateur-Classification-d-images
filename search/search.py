from flask import Flask
import random
app = Flask(__name__)
NB_FEATURES = 40
DB = [''.join(map(str, [random.randint(0, 1) for j in range(NB_FEATURES)])) for k in range(200000)] 

# Returns Hamming distance between two binary numbers
def hamming_distance(v1:str,v2:str) -> int :
     return sum([ int(bit) for bit in bin(int(v1,base=2)^int(v2,base=2))[2:]])

# K-Nearest Neighbors
@app.route("/knn/<user_vector>/<int:k>")
def KNN(user_vector:str,k:int):
    k_nearest = []
    for vector_id in range(len(DB)) :
        vector = DB[vector_id]
        d = hamming_distance(vector,user_vector)
        k_nearest.append((d,vector_id))
        k_nearest.sort(key=lambda tup: tup[0])
        if len(k_nearest) > k :
            k_nearest.pop(0)
    return k_nearest

@app.route("/show")
def show():
    return str(DB)


