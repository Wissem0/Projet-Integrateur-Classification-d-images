import heapq

from model import Attribute, Example, Dataset
from treelib import Node, Tree


def knn(k:int, dataset:Dataset, user_vector:Example) -> list[Example]:
    """

    :param k: Number of neighbors
    :param dataset: Dataset
    :param user_vector: Example
    :return: list of neighbors
    """
    k_nearest = []
    distances = {}
    for vector_id in range(len(dataset)):
        vector = dataset.examples[vector_id]
        d = Example.hamming_distance(vector, user_vector)
        distances[vector_id] = d
        if len(k_nearest) < k:
            heapq.heappush(k_nearest, (d, vector_id))
        else:
            heapq.heappushpop(k_nearest, (d, vector_id))
    
    return [(nearest[0],dataset.examples[nearest[1]].name) for nearest in k_nearest]

class SearchTree:
    search_tree = Tree()

    def __str__(self) -> str:
        return str(self.search_tree)

    def __init__(self, dataset: Dataset):
        feature_order = [k for k in range(len(dataset.features))]

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
                if dataset.examples[example_id].attributes[feature_id] == '0':
                    left_subtree_example_list.append(example_id)
                else:
                    right_subtree_example_list.append(example_id)
            if left_subtree_example_list:
                aux_tree.merge(node.identifier, aux_build(next_feature_id, left_subtree_example_list))

            if right_subtree_example_list:
                aux_tree.merge(node.identifier, aux_build(next_feature_id, right_subtree_example_list))

            return aux_tree

        # print(str(DB))
        self.search_tree = aux_build(feature_order.pop(), [k for k in range(len(dataset.examples))])

    # def search(self, user_vector:Example) -> list[Example] :

"""         def search_aux(node:Node) -> Node

            search_aux(node)
            self.search_tree.children(node)
            if(node.)   """


