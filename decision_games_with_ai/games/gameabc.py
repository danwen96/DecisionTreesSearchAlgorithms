from abc import ABC, abstractmethod


class GameABC(ABC):
    """Class defining methods that must be available in Game classes for games to be compatible
    with the rest of the project"""

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def make_move(self, move_coords):
        pass

    @abstractmethod
    def get_board(self):
        pass

    @abstractmethod
    def tell_whose_turn_it_is(self):
        pass

