import decision_games_with_ai.games.tic_tac_toe.game
import decision_games_with_ai.games.checkers.game

import decision_games_with_ai.user_interfaces.tui.tic_tac_toe_console_interface
import decision_games_with_ai.user_interfaces.tpai.tic_tac_toe_console_arena_interface
import decision_games_with_ai.user_interfaces.tui.checkers_console_interface
from decision_games_with_ai.games.checkers.tree_builder import CheckersTreeBuilder
from decision_games_with_ai.games.tic_tac_toe.tree_builder import TicTacToeTreeBuilder
from decision_games_with_ai.players.human_player.console_interface_player import \
    ConsoleInterfacePlayer

from decision_games_with_ai.players.virtual_player.search_algorithms.minimax_search import \
    MinimaxSearchAlgorithms
from decision_games_with_ai.players.virtual_player.search_algorithms.montecarlo_search import \
    MonteCarloSearchAlghoritm
from decision_games_with_ai.players.virtual_player.virtual_enemy import \
    VirtualEnemy


class GameController:
    """Class that creates proper object instances and controls flow of the
     program by changing proper variable references"""

    def __init__(self):
        self.control_interface = None
        self.player1 = None
        self.player2 = None
        self.game = None

    def play_tic_tac_toe_two_console_players(self):
        """
        Initializes proper objects for player vs player tic tac toe game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human 1")
        self.player2 = ConsoleInterfacePlayer("Human 2")
        self.game = decision_games_with_ai.games.tic_tac_toe.game.Game()
        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            tic_tac_toe_console_interface.TicTacToeConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_tic_tac_toe_with_computer(self):
        """
        Initializes proper objects for player vs computer tic tac toe game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human 1")

        self.game = decision_games_with_ai.games.tic_tac_toe.game.Game()
        self.player2 = VirtualEnemy(
            name="Computer player mini max",
            tree_builder=TicTacToeTreeBuilder(self.game),
            search_algorithm=MinimaxSearchAlgorithms(depth=5),
            search_depth=3
        )

        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            tic_tac_toe_console_interface.TicTacToeConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_checkers_two_console_players(self):
        """
        Initializes proper objects for player vs player checkers game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human 1")
        self.player2 = ConsoleInterfacePlayer("Human 2")
        self.game = decision_games_with_ai.games.checkers.game.Game()
        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            checkers_console_interface.CheckersConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_checkers_with_computer(self):
        """
        Initializes proper objects for player vs computer game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human player")
        self.game = decision_games_with_ai.games.checkers.game.Game()
        self.player2 = VirtualEnemy(
            name="Computer player minimax",
            tree_builder=CheckersTreeBuilder(self.game),
            search_algorithm=MinimaxSearchAlgorithms(depth=3),
            search_depth=3
        )
        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            checkers_console_interface.CheckersConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_tic_tac_toe_with_computer_monte_carlo(self):
        """
        Initializes proper objects for player vs computer tic tac toe game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human player")

        self.game = decision_games_with_ai.games.tic_tac_toe.game.Game()
        self.player2 = VirtualEnemy(
            name="Computer player monte carlo",
            tree_builder=TicTacToeTreeBuilder(self.game),
            search_algorithm=MonteCarloSearchAlghoritm(find_time=5),
            search_depth=3
        )

        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            tic_tac_toe_console_interface.TicTacToeConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_checkers_with_computer_monte_carlo(self):
        """
        Initializes proper objects for player vs computer checkers game
        :return:
        """
        self.player1 = ConsoleInterfacePlayer("Human player")

        self.game = decision_games_with_ai.games.checkers.game.Game()
        self.player2 = VirtualEnemy(
            name="Computer player monet carlo",
            tree_builder=CheckersTreeBuilder(self.game),
            search_algorithm=MonteCarloSearchAlghoritm(find_time=5),
            search_depth=3
        )

        self.control_interface = decision_games_with_ai.user_interfaces.tui. \
            checkers_console_interface.CheckersConsoleInterface(self.game)
        self.control_interface.play(self.player1, self.player2)

    def play_multiple_games_between_computers_monte_carlo(self):
        """
        Initializes proper objects for arena play between virtual players
        :return:
        """
        self.game = decision_games_with_ai.games.tic_tac_toe.game.Game()

        self.player1 = VirtualEnemy(
            name="Virtual player 1",
            tree_builder=TicTacToeTreeBuilder(self.game),
            search_algorithm=MonteCarloSearchAlghoritm(find_time=5),
            search_depth=3
        )

        self.player2 = VirtualEnemy(
            name="Virtual player 2",
            tree_builder=TicTacToeTreeBuilder(self.game),
            search_algorithm=MonteCarloSearchAlghoritm(find_time=5),
            search_depth=3
        )

        self.control_interface = decision_games_with_ai.user_interfaces.tpai. \
            tic_tac_toe_console_arena_interface.TicTacToeConsoleArenaInterface(
                self.game, 1000, print_val_interval=10)
        self.control_interface.play(self.player1, self.player2)


if __name__ == '__main__':
    game_controller = GameController()
    # game_controller.play_tic_tac_toe_two_console_players()
    # game_controller.play_checkers_two_console_players()
    # game_controller.play_tic_tac_toe_with_computer()
    # game_controller.play_checkers_with_computer()
    # game_controller.play_tic_tac_toe_with_computer_monte_carlo()
    # game_controller.play_checkers_with_computer_monte_carlo()
    game_controller.play_multiple_games_between_computers_monte_carlo()
