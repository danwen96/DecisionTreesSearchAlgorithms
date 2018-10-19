from decision_games_with_ai.games.checkers.game_implementation.game_board import GameBoard
from decision_games_with_ai.games.utils.events_exceptions import InvalidMoveException
from decision_games_with_ai.games.utils.game_states_enums import GameStates
from decision_games_with_ai.games.utils.view_modificators import create_string_board_from_output
from decision_games_with_ai.user_interfaces.control_interface_abc import ControlInterfaceABC


class CheckersConsoleInterface(ControlInterfaceABC):
    """Class providing console interface for playing the game of checkers"""

    def __init__(self, game):
        self.player1 = None
        self.player2 = None
        self.game = game

    def play(self, player1, player2):
        """
        Method that starts the game and interaction with the user
        :return:
        """
        self.player1 = player1
        self.player2 = player2
        self._control_flow_of_the_game()

    def _control_flow_of_the_game(self):
        """
        Controls flow of the game
        :return:
        """
        self._start_game()

        self._show_board()
        while self._check_if_the_game_is_ongoing():
            try:
                self._make_move()
                self._show_board()
            except InvalidMoveException as e_info:
                print(e_info)
                print("Chosen move is forbidden. Chose different move ")
            except IndexError:
                print("The field you chosen is not existent, chose another one: ")

    def _show_board(self):
        """
        Shows board on which the game is played
        :return:
        """
        get_board_str = create_string_board_from_output(
            should_add_indexes=True)(self.game.get_board)
        print(get_board_str())

    def _start_game(self):
        """
        Method that initializes the variables and lets the interactions between
        players begin
        :return:
        """
        self.game.start_game()

    def _make_move(self):
        """
        Provides console interface for the user to make a move
        :return:
        """
        enum_object_player_mapping = {
            GameBoard.Players.PLAYER1: self.player1,
            GameBoard.Players.PLAYER2: self.player2
        }

        players_move_str = enum_object_player_mapping[
            self.game.tell_whose_turn_it_is()].get_player_move()
        self.game.make_move(players_move_str)

    def _check_if_the_game_is_ongoing(self):
        """
        Checks if the game has over
        :return: True if the game is ongoing, false otherwise
        """
        game_state = self.game.get_game_state()

        if game_state == GameStates.ONGOING:
            return True
        self._show_end_game_message(game_state)
        return False

    def _show_end_game_message(self, game_result):
        """
        Method displaying message after the game has ended
        :param game_result: GameStates enum telling who has won
        :return:
        """
        if game_result == GameStates.PLAYER1WIN:
            print("{0} has won!".format(self.player1.name))
        elif game_result == GameStates.PLAYER2WIN:
            print("{0} has won!".format(self.player2.name))
        elif game_result == GameStates.DRAW:
            print("Game has resulted in a draw!")
        else:
            raise ValueError("Incorrect argument passed to _show_end_game_message method")
