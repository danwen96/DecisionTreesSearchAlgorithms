from abc import ABC, abstractmethod


class ControlInterfaceABC(ABC):
    """Abstract class defining methods needed for this class to be compatible
    with game controller"""

    @abstractmethod
    def play(self, player1, player2):
        pass

