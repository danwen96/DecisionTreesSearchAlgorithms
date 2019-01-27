"""Module defining the interface for the tree builder class"""
from abc import ABC, abstractmethod


class TreeBuilderABC(ABC):
    """Class defining interface for tree builders classes"""

    @abstractmethod
    def build_minimax_tree(self, depth):
        """
        This method will return tree that can searched through minimax alghortim
        :param depth: Max depth that will be checked
        :return: Tree structure ready to be searched through
        """
        raise NotImplementedError("To override")

    @abstractmethod
    def build_monte_carlo_tree(self, num_of_sim):
        """
        Should build tree that will be searched through using the Monte Carlo
        tree search method
        :param num_of_sim: Time limit after witch the tree will be returned
        :return: Tree structure ready to be searched through
        """
        raise NotImplementedError("To override")