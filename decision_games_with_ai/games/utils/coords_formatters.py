"""Module providing ways of formatting the board coordinates"""
from enum import Enum
from string import ascii_lowercase


class CoordsFormatter:
    """Class providing methods for transforming given coordinates"""

    LETTERS = {letter: index for index, letter in enumerate(ascii_lowercase, start=1)}
    Letters = Enum('Letters', LETTERS)

    @staticmethod
    def translate_from_uci_to_xy(uci_str):
        """
        Methods that translates uci string to normal indexes
        :param uci_str: Board field coordinates in UCI format in string (ex'a1')
        :return: Boards indexes in int starting from 0 a1 - 0, 0
        """
        return CoordsFormatter.LETTERS[uci_str[0]] - 1, int(uci_str[1:]) - 1

    @staticmethod
    def translate_from_xy_to_uci(x_ind, y_ind):
        """
        Methods that translates normal indexes string to uci
        :param x_ind: X index in int starting from 0
        :param y_ind: Y index in int starting from 0
        :return:
        """
        return str(CoordsFormatter.Letters(x_ind + 1).name + str(y_ind + 1))


if __name__ == "__main__":
    print(" ".join(ascii_lowercase))
    print(CoordsFormatter.Letters.a.name)
