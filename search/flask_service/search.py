#!/usr/bin/env python3
from flask import Flask, render_template
import random
import heapq
from treelib import Node, Tree

app = Flask(__name__)
NB_FEATURES = 40
NB_EXAMPLES = 200_000
SYMBOLS = ('0', '1')
DB = [''.join(map(str, [SYMBOLS[random.randint(0, 1)] for j in range(NB_FEATURES)])) for k in range(NB_EXAMPLES)]


# Returns Hamming distance between two binary numbers
def hamming_distance(v1: str, v2: str) -> int:
    if len(v1) != len(v2):
        raise ValueError("Binary vectors should have same length (len(v1)=" + str(len(v1)) + ",len(v2)=" + str(len(v2)))
    return sum([int(bit) for bit in bin(int(v1, base=2) ^ int(v2, base=2))[2:]])


# KNN-BASED METHODS
# K-Nearest Neighbors
@app.route("/knn/<user_vector>/<int:k>")
def search(user_vector: str, k: int, dataset: list[str] = DB):
    k_nearest = []
    for vector_id in range(len(DB)):
        vector = DB[vector_id]
        d = hamming_distance(vector, user_vector)
        k_nearest.append((d, vector_id))
        k_nearest.sort(key=lambda tup: tup[0])
        if len(k_nearest) > k:
            k_nearest.pop(0)
    return str(k_nearest)


# Improved version:
# - use a heap to store the k nearest neighbors
# - use a dictionary to store the distance between the user and the vectors
# - use a set to store the vectors that have been visited
@app.route("/knn_heap/<user_vector>/<int:k>")
def search_heap(user_vector: str, k: int) -> str:
    k_nearest = []
    distances = {}
    for vector_id in range(len(DB)):
        vector = DB[vector_id]
        d = hamming_distance(vector, user_vector)
        distances[vector_id] = d
        if len(k_nearest) < k:
            heapq.heappush(k_nearest, (d, vector_id))
        else:
            heapq.heappushpop(k_nearest, (d, vector_id))
    return str(k_nearest)


# TODO: use Kd-tree
@app.route("/knn_kdtree/<user_vector>/<int:k>")
def search_kdtree(user_vector: str, k: int) -> int:
    pass


# TODO: use LSH
@app.route("/knn_lsh/<user_vector>/<int:k>")
def search_lsh(user_vector: str, k: int) -> int:
    pass



# Search tree
search_tree = Tree()
# SEARCH TREE METHODS

# Utilities
@app.route("/show_tree")
def app_show_tree() :
    return str(search_tree)

@app.route("/search_tree/<user_vector>")
def app_search_tree(user_vector: str) -> str :
    def aux_search(vector:str, tree:Tree) -> Tree : 
        
    return search_tree(user_vector)

# Building the tree
@app.route("/tree_build")
def app_tree_build():
    search_tree = tree_build(DB)

def tree_build(db: list[str]) -> Tree:
    # TODO: make feature order relevant
    feature_order = [k for k in range(len(db[-1]))]

    def aux_build(feature_id: int, examples_ids: list[int]) -> Tree:
        aux_tree = Tree()
        root = Node(identifier="root")
        aux_tree.add_node(root)

        if not feature_order:
            node = Node(str(feature_id), data=examples_ids)
            aux_tree.add_node(node, "root")
            return aux_tree
        else:
            node = Node(str(feature_id))
            aux_tree.add_node(node, "root")

        next_feature_id = feature_order.pop()

        left_subtree_example_list, right_subtree_example_list = [], []
        for example_id in examples_ids:
            if db[example_id][feature_id] == '0':
                left_subtree_example_list.append(example_id)
            else:
                right_subtree_example_list.append(example_id)
        if left_subtree_example_list:
            aux_tree.merge(node.identifier, aux_build(next_feature_id, left_subtree_example_list))

        if right_subtree_example_list:
            aux_tree.merge(node.identifier, aux_build(next_feature_id, right_subtree_example_list))

        return aux_tree

    # print(str(DB))
    return aux_build(feature_order.pop(), [k for k in range(NB_EXAMPLES)])


# Other Utilities
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
    # build()
    # tree = build()
    # print(str(tree))
    # TODO: test unit examples in tree
    # for leaf in tree.leaves() :
    #    print(leaf)
    app.run(host='0.0.0.0', port=8080)
