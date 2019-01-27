"""Module responsible for building of the decision trees of tic tac toe game"""
import datetime
from copy import deepcopy
from math import log, sqrt
from enum import Enum
from random import choice

import anytree
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from decision_games_with_ai.games.tic_tac_toe.game import Game
from decision_games_with_ai.games.tic_tac_toe.game_implementation.game_board import GameBoard
from decision_games_with_ai.games.tree_builder_abc import TreeBuilderABC

from decision_games_with_ai.games.utils.global_enums import GameStates
from decision_games_with_ai.games.utils.iter_functions import previous_and_next

MAX_VAL = 100000
MIN_VAL = -100000


class TicTacToeTreeBuilder(TreeBuilderABC):
    """Class providing tree builders method for tic tac toe game"""

    class PlayerFactor(Enum):
        MAX = 0
        MIN = 1

    next_player_dict = {
        GameBoard.BoardSigns.PLAYER1: GameBoard.BoardSigns.PLAYER2,
        GameBoard.BoardSigns.PLAYER2: GameBoard.BoardSigns.PLAYER1
    }

    player_desired_game_state = {
        GameBoard.BoardSigns.PLAYER1: GameStates.PLAYER1WIN,
        GameBoard.BoardSigns.PLAYER2: GameStates.PLAYER2WIN
    }

    players_pawns_values = {
        GameBoard.BoardSigns.PLAYER1: GameBoard.BoardSigns.PLAYER1.value,
        GameBoard.BoardSigns.PLAYER2: GameBoard.BoardSigns.PLAYER2.value
    }

    players_pawns = (
        GameBoard.BoardSigns.PLAYER1.value,
        GameBoard.BoardSigns.PLAYER2.value
    )

    def __init__(self, game):
        # monte carlo variables
        self.game = game
        self.max_moves_mt = 100
        self.mt_wins = {}
        self.mt_plays = {}
        self.mt_C = 3
        self.max_depth = 0
        self.print_info = False

        # minimax variables
        self.value_of_neigh_signs = 5
        self.value_of_near_empty_field = 1

    def build_monte_carlo_tree(self, num_of_sim):
        """
        Builds tree using monte carlo method
        :param num_of_sim: Time limit in seconds after which this method will
        return built tree
        :return:
        """
        self.max_depth = 0
        # raise NotImplementedError("Monte Carlo tree search to do")
        actual_board = self.game.game_board.get_board_copy(copy_format='tuple')
        player = self.game.current_players_turn
        possible_moves = self.game.game_board.get_possible_moves(actual_board)

        # Return if there is no choice to be made
        if not possible_moves:
            return
        if len(possible_moves) == 1:
            return possible_moves[0]

        games = 0

        time_for_move = datetime.timedelta(seconds=time_limit)
        start_time = datetime.datetime.utcnow()
        # while datetime.datetime.utcnow() - start_time < time_for_move:
        while games <= 100:
            self._run_monte_carlo_simulation(actual_board, player, player)
            games += 1

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
        """
        Runs one simulation of game till the terminal condition
        :param actual_board: Actual board of the game
        :param actual_player: Actual player that is going to make move
        :param player: Player that wants to have the best score
        :return:
        """
        visited_states = set()
        board_copy = self.game.game_board.get_board_copy(actual_board, copy_format='tuple')

        expand = True
        for i in range(self.max_moves_mt):
            possible_moves = self.game.game_board.get_possible_moves(board_copy)

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
            game_state = self.game.game_board.check_game_state(board_copy)
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

        return main_root.children[0]

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
            return Node(MAX_VAL-depth, parent=parent_node, move=move)
        elif game_state == undesired_game_state:
            return Node(MIN_VAL, parent=parent_node, move=move)

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

    def build_alphabeta_tree(self, depth):
        """
        Builds alpha beta tree move possibilities
        :param depth: Depth at which the algorithms will stop building tree
        :return: Built tree
        """

        main_root = anytree.Node(None)

        move_node = self._create_one_tree_layer_alphabeta(
            depth=depth,
            player=self.game.current_players_turn,
            actual_player=self.game.current_players_turn,
            parent_node=main_root,
            actual_board=self.game.game_board.get_board_copy(),
            move=None,
            alpha=Node(MIN_VAL),
            beta=Node(MAX_VAL)
        )
        # print(RenderTree(main_root))
        # print(move_node)
        # return move_node.move

        return main_root.children[0]

    def _create_one_tree_layer_alphabeta(self, depth, actual_player, player, parent_node,
                                         actual_board, move, alpha, beta):
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
            return Node(MAX_VAL, parent=parent_node, move=move)
        elif game_state == undesired_game_state:
            return Node(MIN_VAL, parent=parent_node, move=move)

        if actual_player == player:
            layer_factor = self.PlayerFactor.MAX
        else:
            layer_factor = self.PlayerFactor.MIN

        possible_moves = self.game.game_board.get_possible_moves(actual_board)

        nodes_le_lambda = lambda x, y: x.name <= y.name

        actual_node = Node(None, parent=parent_node, move=move)
        if layer_factor == self.PlayerFactor.MAX:
            best = Node(MIN_VAL)
            for pos_move in possible_moves:
                board_copy = self.game.game_board.get_board_copy(actual_board)
                board_copy = self.game.game_board.make_move(
                    player_id=actual_player,
                    move_coords=pos_move,
                    board=board_copy
                )
                val_returned = self._create_one_tree_layer_alphabeta(
                    depth=depth - 1,
                    actual_player=self.next_player_dict[actual_player],
                    player=player,
                    parent_node=actual_node,
                    actual_board=board_copy,
                    move=pos_move,
                    alpha=alpha,
                    beta=beta
                )
                try:
                    best = max([val_returned, best], key=lambda x: x.name)
                    alpha = max([val_returned, alpha], key=lambda x: x.name)
                    if nodes_le_lambda(beta, alpha):
                        break
                except TypeError:
                    print("Val returned - {}\n Best value - {}\n alpha - {}\nbeta - {}\n\n".format(
                        val_returned, best, alpha, beta))
                    raise
        else:
            best = Node(MAX_VAL)
            for pos_move in possible_moves:
                board_copy = self.game.game_board.get_board_copy(actual_board)
                board_copy = self.game.game_board.make_move(
                    player_id=actual_player,
                    move_coords=pos_move,
                    board=board_copy
                )
                val_returned = self._create_one_tree_layer_alphabeta(
                    depth=depth - 1,
                    actual_player=self.next_player_dict[actual_player],
                    player=player,
                    parent_node=actual_node,
                    actual_board=board_copy,
                    move=pos_move,
                    alpha=alpha,
                    beta=beta
                )
                try:
                    best = min([val_returned, best], key=lambda x: x.name)
                    beta = min([val_returned, beta], key=lambda x: x.name)
                    if nodes_le_lambda(beta, alpha):
                        break
                except TypeError:
                    print("Val returned - {}\n Best value - {}\n beta - {}\nalpha - {}\n\n".format(
                        val_returned, best, beta, alpha))
                    raise

        return best

    def _static_evaluation_value(self, actual_board, player):
        """
        Function for static evaluation of the board for minimax algorithm
        :param actual_board: Board that will get evaluated
        :param player: Player for which evaluated score of the board will be
        returned
        :return: Value of evaluated board
        """
        # Returns always equal board for test purpose
        total_value = 0

        player_pawn = TicTacToeTreeBuilder.players_pawns_values[player]
        empty_field_val = GameBoard.BoardSigns.EMPTY.value

        for prev_line, act_line, next_line in previous_and_next(actual_board):
            if prev_line is None:
                prev_line = [None] * len(act_line)
            if next_line is None:
                next_line = [None] * len(act_line)
            # print(" prev_line - {},  act_line - {},  next_line - {}".format(
            #     prev_line, act_line, next_line))

            for up_els, cen_els, dn_els in zip(previous_and_next(prev_line),
                                               previous_and_next(act_line),
                                               previous_and_next(next_line)):
                # print("{}    {}    {}".format(up_els, cen_els, dn_els))
                if cen_els[1] == player_pawn:
                    total_value += up_els.count(player_pawn)*self.value_of_neigh_signs
                    total_value += dn_els.count(player_pawn)*self.value_of_neigh_signs
                    total_value += (cen_els.count(player_pawn)-1)*self.value_of_neigh_signs

                    total_value += up_els.count(empty_field_val)*self.value_of_near_empty_field
                    total_value += dn_els.count(empty_field_val)*self.value_of_near_empty_field
                    total_value += cen_els.count(empty_field_val)*self.value_of_near_empty_field

        return total_value


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
    #
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
    #
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
