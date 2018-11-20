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

    def get_board_copy(self, board_to_copy=None, copy_format='list'):
        """
        Creates copy of the given board
        :param board_to_copy: Two dimensional board to copy
        :return: Two dimensional board copy as tuples
        """
        if copy_format == 'list':
            if board_to_copy is None:
                board_to_copy = self.board_arrays
            list_of_tuples = [list(row) for row in board_to_copy]
            return list(list_of_tuples)
        elif copy_format == 'tuple':
            if board_to_copy is None:
                board_to_copy = self.board_arrays
            list_of_tuples = [tuple(row) for row in board_to_copy]
            return tuple(list_of_tuples)
        else:
            raise TypeError("Wrong copy_format specified")

    # @abstractmethod
    # def check_game_state(self):
    #     pass

    @abstractmethod
    def make_move(self, player_id, move_coords):
        pass
