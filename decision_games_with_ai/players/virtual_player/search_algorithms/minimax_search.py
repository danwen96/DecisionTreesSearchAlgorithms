"""Module providing ways of searching through tree using minimax algorithms"""
import random
from enum import Enum

from decision_games_with_ai.players.virtual_player.search_algorithms.search_algorithms_abc import \
    SearchAlgorithmsABC


class MinimaxSearchAlgorithms(SearchAlgorithmsABC):
    """Class containing ways of searching trees using minimax like algorithms"""

    class Operator(Enum):
        MAX = 0
        MIN = 1

    def __init__(self, depth=5):
        self.actual_search_method = self._tic_tac_toe_search_algorithm
        # self.actual_search_method = self._tic_tac_toe_search_algorithm
        # self.depth = depth

    def search_tree(self, root_node):
        """
        Method that searches through tree
        :param root_node:
        :return:
        """
        return self.actual_search_method(root_node)

    def _random_search(self, root_node):
        """
        Random search for testing purpose
        :param root_node: Root node of the tree
        :return: Move which was drawn
        """
        moves = [node.move for node in root_node.children]
        print("Moves: {}".format(moves))
        return random.choice(moves)

    def _tic_tac_toe_search_algorithm(self, root_node):
        """
        Searches through tic tac toe game tree
        :param root_node: Main root of the game tree
        :return: Move in UCI format of the move that got the best score
        """
        children_values = [self._minimax_recursive_call(child_node, self.Operator.MIN) for
                           child_node in root_node.children]

        next_move_index = children_values.index(max(children_values))
        next_move_node = root_node.children[next_move_index]
        print(children_values)
        print([root_node.children])
        return next_move_node.move

    def _minimax_recursive_call(self, node, operator):
        """
        Each call searches for given max or min value in it`s node`s children
        and children of their children using recurrence
        :param node: Node that children are gonna be searched
        :param operator: Operation, on base of which which children will be
        returned - min or max
        :return: Value that matched operator
        """
        if operator == self.Operator.MAX:
            reverse_operator = self.Operator.MIN
        elif operator == self.Operator.MIN:
            reverse_operator = self.Operator.MAX
        else:
            raise TypeError("Wrong operator passed to minimax recursive call method")

        if node.name is None:
            if not node.children:
                raise TypeError("Node passed to minimax method was incorrect")
            children_values = [self._minimax_recursive_call(child_node, reverse_operator) for
                               child_node in node.children]
            if operator == self.Operator.MAX:
                value_after_operation = max(children_values)
            else:
                value_after_operation = min(children_values)

            return value_after_operation
        else:
            return node.name
