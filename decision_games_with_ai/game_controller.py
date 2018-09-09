import decision_games_with_ai.games.tic_tac_toe.game
from decision_games_with_ai.players.human_player.console_interface_player import \
    ConsoleInterfacePlayer
import decision_games_with_ai.user_interfaces.tui.tic_tac_toe_console_interface


class GameController:
    """Class that creates proper object instances and controls flow of the
     program by changing proper variable references"""

    def __init__(self):
        self.control_interface = None
        self.player1 = None
        self.player2 = None
        self.game = None

    def play_tic_tac_toe_two_players(self):
        """
        Initializes proper objects for player vs player tic tac toe game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Darek otworz")
        self.player2 = ConsoleInterfacePlayer("Gigi dagostino")
        self.game = decision_games_with_ai.games.tic_tac_toe.game.Game()
        self.control_interface = decision_games_with_ai.user_interfaces.tui.\
            tic_tac_toe_console_interface.TicTacToeConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)


if __name__ == '__main__':
    game_controller = GameController()
    game_controller.play_tic_tac_toe_two_players()
