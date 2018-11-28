"""Module that provides methods for packing monte carlo tree builder class
into virtual enemy"""
from decision_games_with_ai.players.virtual_player.search_algorithms.search_algorithms_abc import \
    SearchAlgorithmsABC


class MonteCarloSearchAlghoritm(SearchAlgorithmsABC):
    """Class providing methods for packing monte carlo tree builder methods
    into virtual enemy"""

    def __init__(self):
        self.actual_search_method = self._get_montecarlo_move

    def search_tree(self, move):
        return self.actual_search_method(move)

    def _get_montecarlo_move(self, move):
        return move
