"""Module containing exceptions thrown for different events that may occur in
game"""


class InvalidMoveException(ValueError):
    """Type of exception thrown when move that is going to be made is forbidden"""
    pass


class MoveCheckOutsideOfArray(IndexError):
    """Exception thrown when one of move checking function has moved outside of
    array"""
    pass
