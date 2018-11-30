"""Module responsible for building of the decision trees of tic tac toe game"""
import datetime
from enum import Enum
from math import log, sqrt
from random import choice

from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from decision_games_with_ai.games.checkers.game_implementation.game_board import GameBoard
from decision_games_with_ai.games.tree_builder_abc import TreeBuilderABC

import anytree

from decision_games_with_ai.games.utils.global_enums import GameStates, SearchMethods


class CheckersTreeBuilder(TreeBuilderABC):
    """Class providing tree builders method for tic tac toe game"""

    class PlayerFactor(Enum):
        MAX = 0
        MIN = 1

    next_player_dict = {
        GameBoard.Players.PLAYER1: GameBoard.Players.PLAYER2,
        GameBoard.Players.PLAYER2: GameBoard.Players.PLAYER1
    }

    player_desired_game_state = {
        GameBoard.Players.PLAYER1: GameStates.PLAYER1WIN,
        GameBoard.Players.PLAYER2: GameStates.PLAYER2WIN
    }

    def __init__(self, game):
        self.max_moves_mt = 100
        self.mt_wins = {}
        self.mt_plays = {}
        self.mt_C = 1.4
        self.max_depth = 0
        self.game = game
        self.print_info = False
        # self.game_board = self.game.game_board

    def build_monte_carlo_tree(self, time_limit):
        """
        Builds tree using monte carlo method
        :param time_limit: Time limit in seconds after which this method will
        return built tree
        :return:
        """
        self.max_depth = 0
        # raise NotImplementedError("Monte Carlo tree search to do")
        actual_board = self.game.game_board.get_board_copy(copy_format='tuple')
        player = self.game.current_players_turn
        possible_moves = self.game.game_board.get_possible_moves(player, actual_board)

        # Return if there is no choice to be made
        if not possible_moves:
            print("No possible moves, something went wrong")
            return
        if len(possible_moves) == 1:
            if self.print_info:
                print("Only one move possible, returning it")
            return possible_moves[0]

        games = 0

        # time_for_move = datetime.timedelta(seconds=time_limit)
        # start_time = datetime.datetime.utcnow()
        # while datetime.datetime.utcnow() - start_time < time_for_move:
        while games <= 100:
            self._run_monte_carlo_simulation(actual_board, player, player)
            games += 1
            if games % 10 == 0 and self.print_info:
                print(games)
        if self.print_info:
            print("Number of games: {}".format(games))

        moves_tuples = [(move_cords, self.game.game_board.make_move(
            player_id=player,
            move_coords=move_cords,
            board=actual_board,
        )) for move_cords in possible_moves]

        percent_wins, move = max(
            (self.mt_wins.get((player, act_board), 0) /
             self.mt_plays.get((player, act_board), 1),
             move) for move, act_board in moves_tuples
        )

        if self.print_info:
            for x in sorted(
                    ((100 * self.mt_wins.get((player, S), 0) /
                      self.mt_plays.get((player, S), 1),
                      self.mt_wins.get((player, S), 0),
                      self.mt_plays.get((player, S), 0), p)
                     for p, S in moves_tuples),
                    reverse=True
            ):
                print("{3}: {0:.2f}% ({1} /{2})".format(*x))
            print("Maximum depth searched:", self.max_depth)

        return move

    def _run_monte_carlo_simulation(self, actual_board, actual_player, player):
        visited_states = set()
        board_copy = self.game.game_board.get_board_copy(actual_board, copy_format='tuple')

        expand = True
        for i in range(self.max_moves_mt):
            possible_moves = self.game.game_board.get_possible_moves(actual_player, board_copy)

            moves_boards = [(p, self.game.game_board.get_board_copy(
                self.game.game_board.make_move(
                    actual_player, p, self.game.game_board.get_board_copy(board_copy)),
                copy_format='tuple'
            )) for p in possible_moves]

            if all(self.mt_plays.get((actual_player, S)) for p, S in moves_boards):
                log_total = log(
                    sum(self.mt_plays[(actual_player, S)] for p, S in moves_boards))
                value, play, brd = max(
                    ((self.mt_wins[(actual_player, S)] / self.mt_plays[(actual_player, S)]) +
                     self.mt_C * sqrt(log_total / self.mt_plays[(actual_player, S)]), p, S)
                    for p, S in moves_boards
                )
            else:
                play, brd = choice(moves_boards)

            board_copy = brd
            #     self.game.game_board.make_move(
            #     player_id=actual_player,
            #     move_coords=play,
            #     board=board_copy
            # )

            if expand and (actual_player, board_copy) not in self.mt_plays:
                expand = False
                self.mt_plays[(actual_player, board_copy)] = 0
                self.mt_wins[(actual_player, board_copy)] = 0
                if i > self.max_depth:
                    self.max_depth = i

            visited_states.add((actual_player, board_copy))

            actual_player = self.next_player_dict[actual_player]
            game_state = self.game.game_board.check_game_state(actual_player, board_copy)
            if game_state in (GameStates.PLAYER1WIN, GameStates.PLAYER2WIN, GameStates.DRAW):
                break

        for act_player, act_board in visited_states:
            if (act_player, act_board) not in self.mt_plays:
                continue
            self.mt_plays[(act_player, act_board)] += 1
            # game_state = self.game.game_board.check_game_state(act_board)
            if game_state == self.player_desired_game_state[player]:
                self.mt_wins[(act_player, act_board)] += 1

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

        game_state = self.game.game_board.check_game_state(actual_player,
                                                           actual_board)

        if player == GameBoard.Players.PLAYER1:
            desired_game_state = GameStates.PLAYER1WIN
            undesired_game_state = GameStates.PLAYER2WIN
        elif player == GameBoard.Players.PLAYER2:
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

        possible_moves = self.game.game_board.get_possible_moves(actual_player,
                                                                 actual_board)

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
