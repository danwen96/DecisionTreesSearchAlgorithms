"""Module containing board of the checkers game and methods for
manipulating it"""
import re
from enum import Enum

from decision_games_with_ai.games.game_board_abc import GameBoardABC
from decision_games_with_ai.games.utils.coords_formatters import CoordsFormatter
from decision_games_with_ai.games.utils.events_exceptions import InvalidMoveException, \
    MoveCheckOutsideOfArray
from decision_games_with_ai.games.utils.view_modificators import create_string_board_from_output


class GameBoard(GameBoardABC):
    """Stores game board tabs and provides method to manipulate on them"""

    class BoardSigns(Enum):
        """Enum with possible board signs"""
        PLAYER1_CHECKER = 'o'
        PLAYER1_KING = 'O'
        PLAYER2_CHECKER = 'x'
        PLAYER2_KING = 'X'
        EMPTY_WHITE = '.'
        EMPTY_BLACK = '_'

    class Players(Enum):
        """Enum with players"""
        PLAYER1 = 0
        PLAYER2 = 1
        UNKNOWN = 2

    class Direction(Enum):
        """Enum with possible move directions"""
        LEFT_UP = 0
        RIGHT_UP = 1
        RIGHT_DOWN = 2
        LEFT_DOWN = 3

    allowed_pawns = {
        Players.PLAYER1: (
            BoardSigns.PLAYER1_CHECKER.value,
            BoardSigns.PLAYER1_KING.value
        ),
        Players.PLAYER2: (
            BoardSigns.PLAYER2_CHECKER.value,
            BoardSigns.PLAYER2_KING.value
        )
    }

    opposite_player = {
        Players.PLAYER1: Players.PLAYER2,
        Players.PLAYER2: Players.PLAYER1
    }

    players_checkers_directions = {
        Players.PLAYER1: (
            Direction.RIGHT_UP,
            Direction.LEFT_UP
        ),
        Players.PLAYER2: (
            Direction.LEFT_DOWN,
            Direction.RIGHT_DOWN
        )
    }

    king_pawns = (BoardSigns.PLAYER1_KING,
                  BoardSigns.PLAYER2_KING)

    checker_pawns = (BoardSigns.PLAYER1_CHECKER,
                     BoardSigns.PLAYER2_CHECKER)

    pawn_ranges = {
        BoardSigns.PLAYER1_CHECKER: 1,
        BoardSigns.PLAYER2_CHECKER: 2,
        BoardSigns.PLAYER1_KING: 1,
        BoardSigns.PLAYER2_KING: 2
    }

    pawn_check_backwards = {
        BoardSigns.PLAYER1_CHECKER: False,
        BoardSigns.PLAYER2_CHECKER: False,
        BoardSigns.PLAYER1_KING: True,
        BoardSigns.PLAYER2_KING: True
    }

    def __init__(self):
        self.board_size = 8
        self._initialize_board()

    def _initialize_board(self):
        """
        Initializes board with the values for the game start
        :return:
        """
        self.board_arrays = [
            [GameBoard.BoardSigns.EMPTY_BLACK.value if x % 2 == y % 2 else
             GameBoard.BoardSigns.EMPTY_WHITE.value for x in range(self.board_size)]
            for y in range(self.board_size)]

        self.moves_list = []
        self.fill_board_with_starting_positions()

    def fill_board_with_starting_positions(self, board_to_fill=None):
        """
        Fills board with starting pawns positions
        :param board_to_fill: Board that will get filled, if not specified,
        the main board of the class will be filled
        :return: Board with filled starting positions
        """
        if board_to_fill is None:
            board_to_fill = self.board_arrays

        for row in board_to_fill[:3]:
            for i, part_el in enumerate(row):
                if part_el == self.BoardSigns.EMPTY_BLACK.value:
                    row[i] = self.BoardSigns.PLAYER1_CHECKER.value

        for row in board_to_fill[-3:]:
            for i, part_el in enumerate(row):
                if part_el == self.BoardSigns.EMPTY_BLACK.value:
                    row[i] = self.BoardSigns.PLAYER2_CHECKER.value

    def check_game_state(self):
        """
        Checks the state of the game
        :return: Game state in a form of GameStates enum
        """
        print("skipping check for win")
        # raise NotImplementedError("TODO")

    def make_move(self, player_id, move_coords):
        """
        Makes move on the board on the specific coords
        :type player_id: Players enum value
        :param player_id: Which player is moving
        :param move_coords: Move coords in UCI format
        :return:
        """
        move_pattern = re.compile('[a-z][0-9]+')
        move_coords_as_list = move_pattern.findall(move_coords)
        if len(move_coords_as_list) != 2:
            raise InvalidMoveException("Invalid move format")
        start_x_ind, start_y_ind = CoordsFormatter.translate_from_uci_to_xy(move_coords_as_list[0])
        end_x_ind, end_y_ind = CoordsFormatter.translate_from_uci_to_xy(move_coords_as_list[1])

        if self.board_arrays[start_y_ind][start_x_ind] not in self.allowed_pawns[player_id]:
            raise InvalidMoveException("There is no pawn of the actual player on given field")

        possible_moves = self._find_moves_for_pawn(
            x_ind=start_x_ind,
            y_ind=start_y_ind,
            player_id=player_id
        )

        move_done = False
        for mov_ind, pawn_rem_list in possible_moves:
            if (end_x_ind, end_y_ind) == mov_ind:
                print("move possible")
                self.board_arrays[end_y_ind][end_x_ind] = \
                    self.board_arrays[start_y_ind][start_x_ind]
                self.board_arrays[start_y_ind][start_x_ind] = GameBoard.BoardSigns.EMPTY_BLACK.value
                for x_rm_ind, y_rm_ind in pawn_rem_list:
                    self.board_arrays = self.get_board_without_pawn(
                        board_to_get=self.board_arrays,
                        rem_pawn_x=x_rm_ind,
                        rem_pawn_y=y_rm_ind
                    )
                move_done = True
                break
        if not move_done:
            raise InvalidMoveException("Wrong move coordinates given")


    # def _find_possible_moves_for_player(self, player_id):
    #     """
    #     Finds all moves that player can make, first it searches for capture
    #     possibility, then for normal moves
    #     :param player_id: Enum that tells which player's moves should be
    #     searched
    #     :return: List of possible moves for pawns
    #     """
    #
    #     pawns_to_be_checked = self._find_players_pawns(player_id)
    #
    #     # possible_moves_list = self._find_possible_moves_with_capture(
    #     #     player_id, pawns_to_be_checked)

    def _find_moves_for_pawn(self, x_ind, y_ind, player_id):
        """
        Method that finds moves for given pawn position and given player
        :param x_ind: X index of the given pawn
        :param y_ind: Y index of the given pawn
        :param player_id: Whose player move it is
        :return: List of possible moves for a given pawn and indexes of pawns
        to be removed by capture in a form of list with
        (x_ind, y_ind), [(x_rm_ind, y_rm_ind), ... ]
        """

        board_to_check = self.get_board_copy(self.board_arrays)
        board_el = self.get_board_element_enum(
            x_ind=x_ind, y_ind=y_ind, board=board_to_check)

        if board_el in GameBoard.checker_pawns:
            pawn_range = 1
            check_backwards = False
        elif board_el in GameBoard.king_pawns:
            pawn_range = 10
            check_backwards = True
        else:
            raise TypeError("Incorrect field has been given to _find_move_for_pawn method")

        captures_position = self._find_captures_positions(
            pawn_range=pawn_range,
            player_id=player_id,
            x_ind=x_ind,
            y_ind=y_ind,
            board_2d_container=board_to_check,
            check_backwards=check_backwards
        )

        moves_list = []

        if captures_position:
            for cap_pos_x, cap_pos_y, cap_dir in captures_position:
                moves_list += self._find_capture_moves(
                    cap_x_ind=cap_pos_x,
                    cap_y_ind=cap_pos_y,
                    direction=cap_dir,
                    pawn_range=pawn_range,
                    player_id=player_id
                )
        else:
            if self._check_for_other_captures(player_id, board_to_check):
                raise InvalidMoveException("You must make moves with captures possibility first")
            else:
                moves_list += self._find_simple_moves(
                    pawn_range=pawn_range,
                    x_ind=x_ind,
                    y_ind=y_ind,
                    board_to_check=board_to_check,
                    player_id=player_id,
                    check_backwards=check_backwards
                )
        return moves_list

    def _check_for_other_captures(self, player_id, board_to_check):
        """
        Checks if there are other captures on board, returns true if so, false
        otherwise
        :param player_id: Id of the player`s turn
        :return: True if there are other captures possible, false otherwise
        """
        players_pawns = self._find_players_pawns(player_id)
        for pawn_x_ind, pawn_y_ind, pawn_enum in players_pawns:
            found_pawn_range = GameBoard.pawn_ranges[pawn_enum]
            found_check_backwards_pos = GameBoard.pawn_check_backwards[pawn_enum]

            pawn_capt_pos = self._find_captures_positions(
                pawn_range=found_pawn_range,
                player_id=player_id,
                x_ind=pawn_x_ind,
                y_ind=pawn_y_ind,
                board_2d_container=board_to_check,
                check_backwards=found_check_backwards_pos
            )

            if pawn_capt_pos:
                return True
        return False

    # def get_pawn_range_and_backward_check(self, pawn):
    #     """
    #     Method that returns pawn range
    #     :param pawn: Pawn in the form of proper enum value
    #     :return: Pawn range as int and bool telling if the pawn can move
    #     backward
    #     """
    #     if pawn in GameBoard.checker_pawns:
    #         pawn_range = 1
    #         check_backwards = False
    #     elif pawn in GameBoard.king_pawns:
    #         pawn_range = 10
    #         check_backwards = True
    #     else:

    # def _find_possible_moves_with_capture(self, player_id, pawns_to_be_checked):
    #     """
    #     Finds possible moves with capture possibility
    #     :param player_id: Enum witch tells whose player's move it is
    #     :param pawns_to_be_checked: List of pawns data that should be checked,
    #     the list should contain tuples with (x_index, y_index, BoardSigns enum)
    #     :return: List of possible moves in a form of tuple (start_x_index,
    #     start_y_index, end_x_index, end_y_index, (pawns of the enemy to be
    #     removed in a form of list of tuples(enemy_pawn_x_index,
    #     enemy_pawn_y_index))
    #     """
    #     king_pawns = (GameBoard.BoardSigns.PLAYER1_KING,
    #                   GameBoard.BoardSigns.PLAYER2_KING)
    #
    #     checker_pawns = (GameBoard.BoardSigns.PLAYER1_CHECKER,
    #                      GameBoard.BoardSigns.PLAYER2_CHECKER)
    #
    #     possible_capture_moves = []
    #
    #     board_tuples = self.get_board_copy(self.board_arrays)
    #
    #     for x_ind, y_ind, player_pawn_enum in pawns_to_be_checked:
    #         if player_pawn_enum in checker_pawns:
    #             capture_moves = self._find_possible_capture_moves(
    #                 1, x_ind, y_ind, board_tuples, check_backwards=False)
    #
    #         if capture_moves:
    #           return capture_moves

    def _find_capture_moves(self, cap_x_ind, cap_y_ind, direction, pawn_range, player_id,
                            board=None, cap_positions=None):
        """
        Finds capture moves for given capture indexes and direction
        :param cap_x_ind: X index of the pawn that is going to be captured
        :param cap_y_ind: Y index of the pawn that is going to be captured
        :param direction: Direction of the ongoing capture
        :param pawn_range: Range of the pawn
        :return: List of the possible moves with indexes of captures in a form
        of : [((x_ind, y_ind), [(x_rm_ind, y_rm_ind), ...]), ...]
        """
        if cap_positions is None:
            cap_positions = []

        if board is None:
            board = self.get_board_copy(self.board_arrays)

        next_x_ind = cap_x_ind
        next_y_ind = cap_y_ind

        capture_moves = []

        try:
            for i in range(pawn_range):
                next_x_ind, next_y_ind, next_el = self._find_next_cross_tab_el(
                    next_x_ind, next_y_ind, direction, board_arrays=board)
                if next_el == GameBoard.BoardSigns.EMPTY_BLACK.value:
                    cap_positions.append((cap_x_ind, cap_y_ind))
                    new_container = self.get_board_without_pawn(
                        board_to_get=board,
                        rem_pawn_x=cap_x_ind,
                        rem_pawn_y=cap_y_ind
                    )

                    pos_cap_postions = self._find_captures_positions(
                        pawn_range=pawn_range,
                        player_id=player_id,
                        x_ind=next_x_ind,
                        y_ind=next_y_ind,
                        check_backwards=True,
                        board_2d_container=new_container
                    )
                    if not pos_cap_postions:
                        capture_moves.append(((next_x_ind, next_y_ind), cap_positions))
                    else:
                        for cap_x_pos, cap_y_pos, cap_dir in pos_cap_postions:
                            capture_moves += self._find_capture_moves(
                                cap_x_ind=cap_x_pos,
                                cap_y_ind=cap_y_pos,
                                direction=cap_dir,
                                pawn_range=pawn_range,
                                player_id=player_id,
                                board=new_container,
                                cap_positions=list(cap_positions)
                            )
                else:
                    break
        except MoveCheckOutsideOfArray:
            pass

        return capture_moves

        # if not capture_moves:
        #     return []
        #
        # for cap_x_move, cap_y_move in capture_moves:
        #     pos_cap_postions = self._find_captures_positions(
        #         pawn_range=pawn_range,
        #         player_id=player_id,
        #         x_ind=cap_x_move,
        #         y_ind=cap_y_move
        #     )

    def get_board_without_pawn(self, board_to_get, rem_pawn_x, rem_pawn_y):
        """
        Returns new board without particular pawn in it
        :param rem_pawn_y: Y index of pawn to be removed
        :param rem_pawn_x: X index of pawn to be removed
        :param board_to_get: Board to be changed
        :return: New board lists
        """
        new_list = []

        for j, row in enumerate(board_to_get):
            new_row = [x if rem_pawn_x != i or rem_pawn_y != j else
                       GameBoard.BoardSigns.EMPTY_BLACK.value for i, x in enumerate(row)]
            new_list.append(new_row)

        return new_list

    def _find_captures_positions(self, pawn_range, player_id, x_ind, y_ind, board_2d_container,
                                 check_backwards=False):
        """
        Find captures positions for given positions
        :param pawn_range: Range of the player's pawn
        :param player_id: Which player are captures checked for
        :param x_ind: X index of the pawn that being capture positions checked on
        :param y_ind: Y index of the pawn that being capture positions checked on
        :param board_2d_container: Board arrays in a form of tuples
        :param check_backwards: Should algorithm check for captures backwards
        :return: List of possible capture positions in a format of list of
        (x_ind, y_ind, direction) tuples
        """
        if check_backwards:
            directions = [x for x in GameBoard.Direction]
        else:
            directions = GameBoard.players_checkers_directions[player_id]

        # directions = [x for x in GameBoard.Direction] if check_backwards else [
        #     GameBoard.Direction.LEFT_UP, GameBoard.Direction.RIGHT_UP]

        enemy_pawns = GameBoard.allowed_pawns[GameBoard.opposite_player[player_id]]

        possible_captures = []

        for direction in directions:
            try:
                next_x_ind = x_ind
                next_y_ind = y_ind

                capture_pawn_indexes_and_direction = self.__find_capture_in_given_dir(
                    pawn_range, direction, enemy_pawns, board_2d_container, next_x_ind, next_y_ind)
                if capture_pawn_indexes_and_direction is not None:
                    possible_captures.append(capture_pawn_indexes_and_direction)

            except MoveCheckOutsideOfArray:
                pass

        return possible_captures

    def __find_capture_in_given_dir(self, pawn_range, direction, enemy_pawns, board_2d_container,
                                    next_x_ind, next_y_ind):
        """
        Method that find captures in given direction and pawn range
        :param pawn_range: Range of the pawn
        :param direction: Direction in which check will be don
        :param enemy_pawns: Tuple of enemy pawns
        :param board_2d_container: Board arrays in a form of two dimensional tuples
        :param next_x_ind: Starting x index, that will iterate
        :param next_y_ind: Starting y index, that will iterate
        :return: X ind, Y ind, direction of given capture move, None when capture is not found
        """
        for i in range(pawn_range):
            next_x_ind, next_y_ind, next_el = \
                self._find_next_cross_tab_el(next_x_ind, next_y_ind, direction, board_2d_container)
            if next_el in enemy_pawns:
                check_x_ind, check_y_ind, check_el = self._find_next_cross_tab_el(
                    next_x_ind, next_y_ind, direction, board_2d_container)
                if check_el == GameBoard.BoardSigns.EMPTY_BLACK:
                    return next_x_ind, next_y_ind, direction
                return None
            elif next_el == GameBoard.BoardSigns.EMPTY_BLACK:
                pass
            else:
                return None

    def _find_simple_moves(self, pawn_range, x_ind, y_ind, board_to_check, player_id,
                           check_backwards=False):
        """
        Finds normal moves that pawn can move on
        :param pawn_range: Range of the pawn for the move
        :param player_id: Which player is moving
        :param x_ind: X index of the pawn
        :param y_ind: Y index of the pawn
        :param board_to_check: Board arrays
        :param check_backwards: Should there be a check backwards
        :return: List with possible move indexes
        """
        if check_backwards:
            directions = [x for x in GameBoard.Direction]
        else:
            directions = GameBoard.players_checkers_directions[player_id]

        # directions = [x for x in GameBoard.Direction] if check_backwards else [
        #     GameBoard.Direction.LEFT_UP, GameBoard.Direction.RIGHT_UP]

        possible_moves = []

        for direction in directions:
            try:
                next_x_ind = x_ind
                next_y_ind = y_ind
                for i in range(pawn_range):
                    next_x_ind, next_y_ind, next_el = self._find_next_cross_tab_el(
                        next_x_ind, next_y_ind, direction, board_to_check)
                    if next_el == GameBoard.BoardSigns.EMPTY_BLACK.value:
                        possible_moves.append(((next_x_ind, next_y_ind), []))
                    elif next_el == GameBoard.BoardSigns.EMPTY_WHITE.value:
                        raise TypeError("Incorrect white value field")
                    else:
                        break
            except MoveCheckOutsideOfArray:
                pass
        return possible_moves

    #     def _find_possible_capture_moves(self, pawn_range, player_id, x_ind, y_ind, board_tuples,
    #                                      check_backwards=False):
    #         """
    #         Finds possible capture move for given board, then searches for more
    #         moves using recurrence call
    #         :param player_id: Id of the player in a form of Players enum
    #         :param x_ind: X index of the pawn that is going to get check capture
    #         moves
    #         :param y_ind: Y index of the pawn that is going to get check capture
    #         moves
    #         :param board_tuples: Board arrays where checks should be performed
    #         :return: List of possible moves in a form of tuple (start_x_index,
    #         start_y_index, end_x_index, end_y_index, (pawns of the enemy to be
    #         removed in a form of list of tuples(enemy_pawn_x_index,
    #         enemy_pawn_y_index))
    #         """
    #         directions = [x for x in GameBoard.Direction] if check_backwards else [
    #             GameBoard.Direction.LEFT_UP, GameBoard.Direction.RIGHT_UP]
    #
    #         enemy_pawns = GameBoard.allowed_pawns[GameBoard.opposite_player[player_id]]
    #
    #         possible_capture_pawns = []
    #
    #         for direction in directions:
    #             next_x_ind = x_ind
    #             next_y_ind = y_ind
    #             try:
    #                 for i in range(pawn_range):
    #                     next_x_ind, next_y_ind, next_el = self._find_next_cross_tab_el(
    #                         next_x_ind, next_y_ind, direction)
    #                     raise NotImplementedError("something went wrong")
    #
    #                     # if next_el in enemy_pawns:
    #                     #     possible_capture_pawns += \
    #                     #         self._find_possible_capture_moves(
    #                     #             pawn_range, player_id,
    #
    #
    #             except MoveCheckOutsideOfArray:
    #                 pass
    #
    #
    # #    def _find_next_capture(self, next_x_ind, next_y_ind)

    def _find_players_pawns(self, player_id):
        """
        Finds list of players pawns
        :param player_id: Enum telling whose player pawns should be searched
        :return: List with players pawns in a form of a tuple with x_ind, y_ind,
        pawn type
        """
        players_pawns = GameBoard.allowed_pawns[player_id]
        players_pawns = [x for x in players_pawns]

        list_of_players_pawns = []

        for y_ind, part_row in enumerate(self.board_arrays):
            for x_ind, part_field in enumerate(part_row):
                if part_field in players_pawns:
                    part_field_enum = GameBoard.BoardSigns(part_field)
                    list_of_players_pawns.append((x_ind, y_ind, part_field_enum))
        return list_of_players_pawns

    def _find_next_cross_tab_el(self, x_ind, y_ind, direction, board_arrays=None):
        """
        Finds next cross element in tab, throws MoveCheckOutsideOfArray when
        goes out of array
        :param direction: Enum with direction of cross move
        :return: New indexes in given direction and element under the new
        indexes
        """
        if board_arrays is None:
            board_arrays = self.board_arrays

        direction_map = {
            GameBoard.Direction.LEFT_UP: (x_ind - 1, y_ind + 1),
            GameBoard.Direction.RIGHT_UP: (x_ind + 1, y_ind + 1),
            GameBoard.Direction.RIGHT_DOWN: (x_ind + 1, y_ind - 1),
            GameBoard.Direction.LEFT_DOWN: (x_ind - 1, y_ind - 1)
        }

        new_x_ind, new_y_ind = direction_map[direction]

        if new_x_ind < 0 or new_y_ind < 0:
            raise MoveCheckOutsideOfArray(
                "_find_next_cross_tab_el in checkers game board class has"
                "moved outside the array")

        try:
            el_to_ret = board_arrays[new_y_ind][new_x_ind]
        except IndexError:
            raise MoveCheckOutsideOfArray(
                "_find_next_cross_tab_el in checkers game board class has"
                "moved outside the array")
        return new_x_ind, new_y_ind, el_to_ret

    # def _find_possible_moves_for_given_pawn(self, player_id, x_ind, y_ind):
    #     """
    #     Finds possible simple move coords for the pawn
    #     :param player_id: Whose player pawn this method should check
    #     :return: List of possible final coords for pawn
    #     """
    #
    #     opposite_players_pawns = self.allowed_pawns[self.opposite_player[player_id]]
    #     empty_alllowed_field = self.BoardSigns.EMPTY_BLACK
    #
    #     player_checker = self.allowed_pawns[player_id][0]
    #     player_king = self.allowed_pawns[player_id][1]
    #
    #     if self.board_arrays[y_ind][x_ind] == player_checker:
    #         possible_moves_positions = self._find_pawns_on_diagonal_positions(
    #             1, x_ind, y_ind, opposite_players_pawns)

    # def _find_pawns_on_diagonal_positions(self, pawn_range, x_ind, y_ind, pawns_to_capture,
    #                                       check_backwards=False):
    #     """
    #     Finds possible positions for a given checker
    #     :param pawn_range: Range of the pawn
    #     :param x_ind: Board x index
    #     :param y_ind: Board y index
    #     :param pawns_to_capture: Types of pawns that can be captured
    #     :param check_backwards: Should check be also done backward
    #     :return: List of possible positions after capturing
    #     """
    #     list_of_possible_moves = []
    #     directions_to_check = [x for x in GameBoard.Direction] if check_backwards else\
    #         [GameBoard.Direction.LEFT_UP, GameBoard.Direction.RIGHT_UP]
    #
    #     for direction in directions_to_check:
    #         try:
    #             next_x_ind, next_y_ind = x_ind, y_ind
    #             for i in range(pawn_range):
    #                 next_x_ind, next_y_ind, next_el = self._find_next_cross_tab_el(
    #                     next_x_ind, next_y_ind, direction)
    #                 if next_el == GameBoard.BoardSigns.EMPTY_BLACK:
    #                     list_of_possible_moves.append((next_x_ind, next_y_ind))
    #                 elif next_el in pawns_to_capture:
    #                     raise NotImplementedError("agains something wrong")
    #         except MoveCheckOutsideOfArray:
    #             pass

    # def _find_moves_for_found_capture(self, pawn_range, capt_x_int, capt_y_ind, direction):
    #     """
    #     Finds possible moves for given pawn
    #     :param pawn_range:
    #     :param capt_x_int:
    #     :param capt_y_ind:
    #     :return:
    #     """
    #     # TODO verify if this is a good approach, maybe i should check if capturing
    #     # is possible first and then check possible moves after capture, if its not possible
    #     # then user can move wherever he wants

    # def _get_positions_after_capture(self, pawn_range, capt_x_ind, capt_y_ind, direction):
    #     """
    #     Returns the list of positions after capturing
    #     :param capt_x_ind: X index of the pawn that's going to be captured
    #     :param capt_y_ind: Y index of the pawn that's going to be captured
    #     :return: List of possible positions, empty list if capturing is not
    #     possible
    #     """
    #
    #     next_x_ind = capt_x_ind
    #     next_y_ind = capt_y_ind
    #     list_of_positions = []
    #
    #     try:
    #         for i in range(pawn_range):
    #             next_x_ind, next_y_ind, next_el = self._find_next_cross_tab_el(
    #                 next_x_ind, next_y_ind, direction)
    #             if next_el == GameBoard.BoardSigns.EMPTY_BLACK:
    #                 list_of_positions.append((next_x_ind, next_y_ind))
    #             else:
    #                 break
    #     except MoveCheckOutsideOfArray:
    #         pass
    #
    #     return list_of_positions

    def get_board_element_enum(self, x_ind, y_ind, board=None):
        """
        Returns board element enum under given
        :param board:
        :param x_ind:
        :param y_ind:
        :return:
        """
        if board is None:
            board = self.board_arrays

        board_el = board[y_ind][x_ind]
        return GameBoard.BoardSigns(board_el)


if __name__ == '__main__':
    game_board = GameBoard()
    game_board._initialize_board()
    print(game_board.board_arrays)
    game_board.fill_board_with_starting_positions()
    print(game_board.board_arrays)
    # print(game_board.get_board_without_pawn(game_board.board_arrays, 0, 0))
    game_board.make_move(
        GameBoard.Players.PLAYER1, 'c3b4'
    )
    game_board.make_move(
        GameBoard.Players.PLAYER2, 'd6c5'
    )
    get_board_str = create_string_board_from_output(should_add_indexes=True)(
        game_board.get_board_view)
    print(get_board_str())

