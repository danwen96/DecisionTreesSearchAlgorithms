"""Module for defining Interface for controlling the game"""
from abc import ABC, abstractmethod


class PlayerABC(ABC):
    """Class defining methods used in games for getting user moves intention"""

    @abstractmethod
    def get_player_move(self):
        pass
