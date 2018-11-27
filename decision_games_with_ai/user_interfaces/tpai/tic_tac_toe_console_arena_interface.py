"""Module providing console arena interface for tic tac toe game, which is
designed for playing large number of games between players. Mostly used to
determine which computer player works better.
"""
from decision_games_with_ai.games.tic_tac_toe.game_implementation.game_board import GameBoard
from decision_games_with_ai.games.utils.events_exceptions import InvalidMoveException
from decision_games_with_ai.games.utils.game_states_enums import GameStates
from decision_games_with_ai.user_interfaces.control_interface_abc import ControlInterfaceABC


class TicTacToeConsoleArenaInterface(ControlInterfaceABC):

    def __init__(self, game, number_of_games, print_val_interval=100):
        self.player1 = None
        self.player2 = None
        self.game = game
        self.number_of_games = number_of_games
        self.print_val_interval = print_val_interval
        self.player1_wins = 0
        self.player2_wins = 0
        self.games_played = 0

    def play(self, player1, player2):
        """
        Player multiple games between
        :param player1:
        :param player2:
        :return:
        """
        self.player1 = player1
        self.player2 = player2
        for i in range(self.number_of_games):
            self._play_one_game()
            if i % self.print_val_interval == 9:
                self.print_results_so_far()

        separation_line = "".join(['#']*40)
        print(separation_line)
        print("Simulation has been finished:")
        self.print_results_so_far()
        print(separation_line)

    def _play_one_game(self):
        """
        Players one game between saved in object players
        :return:
        """
        self._control_flow_of_the_game()

    def _control_flow_of_the_game(self):
        """
        Controls flow of the game
        :return:
        """
        self._start_game()

        while self._check_if_the_game_is_ongoing():
            try:
                self._make_move()
            except InvalidMoveException:
                print("Chosen field is not empty. Chose another one: ")
            except IndexError:
                print("The field you chosen is not existent, chose another one: ")

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
            GameBoard.BoardSigns.PLAYER1: self.player1,
            GameBoard.BoardSigns.PLAYER2: self.player2
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
        self._add_end_game_results(game_state)
        return False

    def _add_end_game_results(self, game_result):
        """
        Method adding results after the end of game
        :param game_result: GameStates enum telling who has won
        :return:
        """
        self.games_played += 1
        if game_result == GameStates.PLAYER1WIN:
            self.player1_wins += 1
        elif game_result == GameStates.PLAYER2WIN:
            self.player2_wins += 1
        elif game_result == GameStates.DRAW:
            pass
        else:
            raise ValueError("Incorrect argument passed to _show_end_game_message method")

    def print_results_so_far(self):
        print("DEBUG: starting player - {}".format(self.game.current_players_turn))
        print("Games played - {}\nPlayer 1 wins - {}\nPlayer 2 wins - {}\n".format(
            self.games_played, self.player1_wins, self.player2_wins))
