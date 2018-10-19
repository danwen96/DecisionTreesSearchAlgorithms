"""Module providing methods for interacting with user using console interface"""
import re

from decision_games_with_ai.players.player_abc import PlayerABC


class ConsoleInterfacePlayer(PlayerABC):
    """Class providing methods for interacting with user by the console
    interface"""

    def __init__(self, name):
        self.name = name

    def get_player_move(self):
        """
        Gets player move using console interface and python input function
        :return: String with user move in UCI format
        """
        while True:
            user_input = self._get_string_from_user()
            if self._validate_uci_format(user_input):
                return user_input
            else:
                print("Invalid move format, try again")

    def _get_string_from_user(self):
        """
        Asks user for move using input function, and returns the passed string
        :return: String with user input
        """
        return input("{0} move in UCI format: ".format(self.name))

    @staticmethod
    def _validate_uci_format(move_in_uci_str):
        """
        Method that validates if entered move is correct and in UCI format
        :return: True if move format is valid, false otherwise
        """
        uci_pattern = re.compile('[a-z][0-9]+')
        match_list = uci_pattern.findall(move_in_uci_str)
        return ''.join(match_list) == move_in_uci_str if match_list else False


if __name__ == "__main__":
    ci_player = ConsoleInterfacePlayer()
    print(ci_player.get_player_move())
