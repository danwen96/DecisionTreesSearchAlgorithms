"""Module responsible for building of the decision trees of tic tac toe game"""
from enum import Enum

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from decision_games_with_ai.games.tic_tac_toe.game_implementation.game_board import GameBoard
from decision_games_with_ai.games.tree_builder_abc import TreeBuilderABC

import anytree

from decision_games_with_ai.games.utils.game_states_enums import GameStates


class TicTacToeTreeBuilder(TreeBuilderABC):
    """Class providing tree builders method for tic tac toe game"""

    class PlayerFactor(Enum):
        MAX = 0
        MIN = 1

    next_player_dict = {
        GameBoard.BoardSigns.PLAYER1: GameBoard.BoardSigns.PLAYER2,
        GameBoard.BoardSigns.PLAYER2: GameBoard.BoardSigns.PLAYER1
    }

    def __init__(self, game):
        self.game = game
        # self.game_board = self.game.game_board

    def build_monte_carlo_tree(self, time_limit):
        raise NotImplementedError("Monte Carlo tree search to do")

    def build_minimax_tree(self, depth):
        """
        Builds minimax tree move possibilities
        :param depth: Depth at witch the algorithms will stop building tree
        :return: Built tree
        """

        main_root = anytree.Node(None)

        self._create_one_tree_layer_minimax(
            depth=depth,
            player=self.game.current_players_turn,
            actual_player=self.game.current_players_turn,
            parent_node=main_root,
            actual_board=self.game.game_board.get_board_copy(),
            move=None
        )

        # print(RenderTree(main_root))

        return main_root.children[0]
        # input("pause")

    def _create_one_tree_layer_minimax(self, depth, actual_player, player, parent_node,
                                       actual_board, move):
        """
        Creates one tree layer for one move of a particular player, then finds
        self recursively value of its nodes
        :param depth: Depth at which this particular branch can search further
        :param actual_player: Enum signalising if the tree should find minimum
        moves, or maximum
        :param player: The player for which the move is discovered
        :param parent_node: Node that is the parent of current node
        :param actual_board: Board arrays with actually estimated board
        simulation
        :param move: Last move in tuple
        :return: Node containing possible moves
        """
        if depth == 0:
            return Node(self._static_evaluation_value(actual_board=actual_board,
                                                      player=player),
                        parent=parent_node, move=move)

        game_state = self.game.game_board.check_game_state(actual_board)

        if player == GameBoard.BoardSigns.PLAYER1:
            desired_game_state = GameStates.PLAYER1WIN
            undesired_game_state = GameStates.PLAYER2WIN
        elif player == GameBoard.BoardSigns.PLAYER2:
            desired_game_state = GameStates.PLAYER2WIN
            undesired_game_state = GameStates.PLAYER1WIN
        else:
            raise TypeError("Not predicted player state")

        if game_state == GameStates.DRAW:
            return Node(0, parent=parent_node, move=move)
        elif game_state == desired_game_state:
            return Node(1000, parent=parent_node, move=move)
        elif game_state == undesired_game_state:
            return Node(-1000, parent=parent_node, move=move)

        possible_moves = self.game.game_board.get_possible_moves(actual_board)

        actual_node = Node(None, parent=parent_node, move=move)

        for pos_move in possible_moves:
            board_copy = self.game.game_board.get_board_copy(actual_board)
            board_copy = self.game.game_board.make_move(
                player_id=actual_player,
                move_coords=pos_move,
                board=board_copy
            )
            self._create_one_tree_layer_minimax(
                depth=depth - 1,
                actual_player=self.next_player_dict[actual_player],
                player=player,
                parent_node=actual_node,
                actual_board=board_copy,
                move=pos_move
            )

    def _static_evaluation_value(self, actual_board, player):
        """
        Function for static evaluation of the board for minimax algorithm
        :param actual_board: Board that will get evaluated
        :param player: Player for which evaluated score of the bard will be
        returned
        :return: Value of evaluated board
        """
        # Returns always equal board for test purpose
        return 0


if __name__ == '__main__':
    pass
    # print("Anytree test")
    #
    # udo = Node("Udo")
    # marc = Node("Marc", parent=udo)
    # lian = Node("Lian", parent=marc)
    # dan = Node("Dan", parent=udo)
    # jet = Node("Jet", parent=dan)
    # jan = Node("Jan", parent=dan)
    # joe = Node("Joe", parent=dan)
    #
    # for pre, fill, node in RenderTree(udo):
    #     print("%s%s" % (pre, node.name))
    #
    # #DotExporter(udo).to_picture("udo.png")
    # DotExporter(udo).to_dotfile("udo.dot")

    # from anytree import Node
    # root = Node("root")
    # s0 = Node("sub0", parent=root)
    # s0b = Node("sub0B", parent=s0)
    # s0a = Node("sub0A", parent=s0)
    # s1 = Node("sub1", parent=root)
    # s1a = Node("sub1A", parent=s1)
    # s1b = Node("sub1B", parent=s1)
    # s1c = Node("sub1C", parent=s1)
    # s1ca = Node("sub1Ca", parent=s1c)
    #
    # DotExporter(root).to_dotfile("tree.dot")

    # from graphviz import Digraph
    #
    # dot = Digraph(comment='The Round Table')
    #
    # dot.node('A', 'King Arthur')
    # dot.node('B', 'Sir Bedevere the Wise')
    # dot.node('L', 'Sir Lancelot the Brave')
    #
    # dot.edges(['AB', 'AL'])
    # dot.edge('B', 'L', constraint='false')
    #
    # print(dot.source)
    #
    # dot.render('test-output/round-table.gv', view=True)
