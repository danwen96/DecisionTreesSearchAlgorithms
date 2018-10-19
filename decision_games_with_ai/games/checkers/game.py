"""Module providing methods for controling flow of the game of Checkers"""
import random

from decision_games_with_ai.games.gameabc import GameABC
from decision_games_with_ai.games.checkers.game_implementation.game_board import GameBoard


class Game(GameABC):
    """Provides games interface for player"""

    class GameNotStartedException(TypeError):
        """Exception thrown when incorrect method is called when game has not
        started"""
        pass

    def __init__(self, starting_player=GameBoard.Players.UNKNOWN):
        """
        The game should be started for start_game method after initialization
        :param starting_player: Tells which player will be moving first, when
        enum value is set to EMPTY, first player will be drawn
        (GameBoard.BoardSigns enum value)
        """
        self.game_board = None
        self.current_players_turn = None
        self.starting_player = starting_player

    def make_move(self, move_coords):
        """
        Makes move on the board with self.current_players_turn, then swaps
        current player value to opponent
        :param move_coords: Move cord in UCI format (String) - Example: 'a1'
        :return:
        """
        if self.current_players_turn is None:
            raise TypeError("Method make_move from checkers was run before game "
                            "was initialized")

        self.game_board.make_move(self.current_players_turn, move_coords)

        next_player_dict = {
            GameBoard.Players.PLAYER1: GameBoard.Players.PLAYER2,
            GameBoard.Players.PLAYER2: GameBoard.Players.PLAYER1
        }
        self.current_players_turn = next_player_dict[self.current_players_turn]

    def get_game_state(self):
        """
        Method that returns actual game state
        :return: GameStates enum representing actual game state
        """
        if self.current_players_turn is None:
            raise TypeError("Method get_game_state from checkers was run before game "
                            "was initialized")
        return self.game_board.check_game_state(self.current_players_turn)

    def get_board(self):
        """
        Method that return board values in a form of lists
        :return: List of lists with lines of board values
        """
        return self.game_board.get_board_view()

    def tell_whose_turn_it_is(self):
        """
        Return enum telling whose sign will be placed next
        :return: GameBoard.BoardSigns enum (PLAYER1 or PLAYER2)
        """
        if self.current_players_turn is None:
            raise Game.GameNotStartedException("Can`t tell whose turn it is when game has not "
                                               "started yet")
        return self.current_players_turn

    def start_game(self):
        self.game_board = GameBoard()
        if self.starting_player == GameBoard.Players.UNKNOWN:
            self.current_players_turn = random.choice([
                GameBoard.Players.PLAYER1, GameBoard.Players.PLAYER2])
        else:
            self.current_players_turn = self.starting_player


