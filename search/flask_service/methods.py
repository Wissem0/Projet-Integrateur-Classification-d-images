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

            # Leaf
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

        self.search_tree = aux_build()

    def search(self, user_vector:Example) -> list[Example] :

        mismatch_features = []
        def search_aux(nid:int,current_feature:int=0) -> int :

            node = self.search_tree.get_node(nid)
            search_aux(node)
            self.search_tree.children(node)
            if(node.is_leaf(self.search_tree)) : 
                return node
            for childid in node.successors(self.search_tree) :
                if self.search_tree.get_node(childid).tag == user_vector[current_feature] :
                    return search_aux(childid,current_feature+1)
            mismatch_features.append(current_feature)
            return search_aux(childid,current_feature+1)
        nid = search_aux(self.search_tree.ROOT)
        siblings = self.search_tree.siblings(nid)
        siblings.append(nid)
        return siblings
        # TODO: get example for each sibling


