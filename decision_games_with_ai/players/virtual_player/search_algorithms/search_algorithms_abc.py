"""Module providing interface for searching the trees"""
from abc import ABC, abstractmethod


class SearchAlgorithmsABC(ABC):
    """Class providing interface of search algorithms"""

    @abstractmethod
    def search_tree(self, root_node):
        """
        Method that should search the tree and return move with the best result
        :param root_node: Root node containing tree
        :return: Move with the best result
        """
        pass
