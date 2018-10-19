"""Module providing methods, that board classes in game can inherit"""
from abc import ABC, abstractmethod


class GameBoardABC(ABC):
    """Class providing methods, that board classes in game can inherit"""

    def __init__(self):
        self.board_size = None
        self.board_arrays = None

    @abstractmethod
    def _initialize_board(self):
        pass

    def get_board_view(self):
        """
        Returns the view of board
        :return: Lists with the board values
        """
        return [list(act_list) for act_list in reversed(self.board_arrays)]

    def get_board_copy(self, board_to_copy):
        """
        Creates copy of the given board
        :param board_to_copy: Two dimensional board to copy
        :return: Two dimensional board copy as tuples
        """
        list_of_tuples = [list(row) for row in board_to_copy]
        return list(list_of_tuples)

    # @abstractmethod
    # def check_game_state(self):
    #     pass

    @abstractmethod
    def make_move(self, player_id, move_coords):
        pass
