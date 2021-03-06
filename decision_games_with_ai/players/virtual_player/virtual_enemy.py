"""Moudule providing virtual enemy behaviour for game of tic tac toe"""
import random

from decision_games_with_ai.games.utils.global_enums import SearchMethods
from decision_games_with_ai.players.player_abc import PlayerABC


class VirtualEnemy(PlayerABC):
    """Class providing methods for behaviour of virtual enemy"""

    def __init__(self, name, tree_builder, search_algorithm, search_method_enum,
                 search_depth=5, num_of_sim=100):
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
        self.num_of_sim = num_of_sim
        self.get_builder_output = {
            SearchMethods.MINIMAX: self._get_minimax_move,
            SearchMethods.MONTECARLO: self._get_monte_carlo_move,
            SearchMethods.ALPHABETA: self._get_alpha_beta_move
        }[search_method_enum]

    def get_player_move(self):
        """
        Gets virtual enemy move
        :return: Move in uct format
        """
        return self.get_builder_output()
        # return self._get_monte_carlo_move()

    def _get_minimax_move(self):
        """
        Gets minimax enemy move
        :return: Move in uct format
        """
        root_node = self._get_tree()
        return self.search_algorithm.search_tree(root_node)

    def _get_tree(self):
        """
        Returns actual game tree
        :return: Root node of the game tree
        """
        return self.tree_builder.build_minimax_tree(self.search_depth)

    def _get_monte_carlo_move(self):
        """
        Direct getting of the move for montecarlo
        :return: Move in uct format
        """
        return self.tree_builder.build_monte_carlo_tree(self.num_of_sim)

    def _get_alpha_beta_move(self):
        """
        Direct getting of the move for alpha beta algorithm
        :return: Move in uct format
        """
        root_node = self.tree_builder.build_alphabeta_tree(self.search_depth)
        # return self.tree_builder.build_alphabeta_tree(self.search_depth)
        return self.search_algorithm.search_tree(root_node)
