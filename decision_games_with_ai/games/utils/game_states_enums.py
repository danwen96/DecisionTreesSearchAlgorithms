"""Module providing enums used in games implementation"""
from enum import Enum


class GameStates(Enum):
    """Class defining states in witch the game can be"""
    ONGOING = 0
    PLAYER1WIN = 1
    PLAYER2WIN = 2
    DRAW = 3
