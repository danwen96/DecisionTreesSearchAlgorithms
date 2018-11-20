"""Moudule providing virtual enemy behaviour for game of tic tac toe"""
import random

from decision_games_with_ai.players.player_abc import PlayerABC


class VirtualEnemy(PlayerABC):
    """Class providing methods for behaviour of virtual enemy"""

    def __init__(self, name, tree_builder, search_algorithm, search_depth=5,
                 time_limit=500):
        """
        Initializes virtual enemy class with necessary parameters
        :param name: Name of the virtual enemy
        :param tree_builder: Tree builder object instance responsible for
        building the game tree
        :param search_algorithm: Algorithm object instance responsible for
        searching through the decision tree and choosing the next move
        :param search_depth: Depth of the tree that is going to get build for
        minimax method
        :param time_limit: Time limit for the search of the tree for monte carlo
        tree search method
        """
        self.name = name
        self.tree_builder = tree_builder
        self.search_algorithm = search_algorithm
        self.search_depth = search_depth
        self.time_limit = time_limit

    def get_player_move(self):
        """
        Gets virtual enemy move
        :return:
        """
        # root_node = self._get_tree()
        # return self.search_algorithm.search_tree(root_node)
        return self._get_monte_carlo_move()

    def _get_tree(self):
        """
        Returns actual game tree
        :return: Root node of the game tree
        """
        return self.tree_builder.build_minimax_tree(self.search_depth)

    def _get_monte_carlo_move(self):
        # TODO
        """
        temporary method
        :return:
        """
        return self.tree_builder.build_monte_carlo_tree(self.time_limit)
