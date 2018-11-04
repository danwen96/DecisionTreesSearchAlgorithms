"""Module containing board of the checkers game and methods for
manipulating it"""
import re
from enum import Enum

from decision_games_with_ai.games.game_board_abc import GameBoardABC
from decision_games_with_ai.games.utils.coords_formatters import CoordsFormatter
from decision_games_with_ai.games.utils.events_exceptions import InvalidMoveException, \
    MoveCheckOutsideOfArray
from decision_games_with_ai.games.utils.game_states_enums import GameStates
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
        BoardSigns.PLAYER2_CHECKER: 1,
        BoardSigns.PLAYER1_KING: 8,
        BoardSigns.PLAYER2_KING: 8
    }

    pawn_check_backwards = {
        BoardSigns.PLAYER1_CHECKER: False,
        BoardSigns.PLAYER2_CHECKER: False,
        BoardSigns.PLAYER1_KING: True,
        BoardSigns.PLAYER2_KING: True
    }

    max_moves_without_capture = 50

    def __init__(self):
        self.board_size = 8
        self.move_count = 0
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

    def get_possible_moves(self, player_id, actual_board):
        """
        :param player_id: Id of the player that all moves will be find
        :param actual_board: Board to find the moves on
        :return: List of possible moves in a form of list of strings with move
        in UCI format
        """
        players_pawns = self._find_players_pawns(player_id, actual_board)
        all_possible_moves = []

        for start_x_ind, start_y_ind, start_pawn_type in players_pawns:
            try:
                possible_moves_for_pawn = self._find_moves_for_pawn(
                    x_ind=start_x_ind,
                    y_ind=start_y_ind,
                    player_id=player_id,
                    board=actual_board)
            except InvalidMoveException:
                pass
            else:
                start_ind_str = CoordsFormatter.translate_from_xy_to_uci(
                    start_x_ind, start_y_ind)
                for end_indexes, pawns_to_remove in possible_moves_for_pawn:
                    end_ind_str = CoordsFormatter.translate_from_xy_to_uci(
                        *end_indexes)
                    all_possible_moves.append(start_ind_str + end_ind_str)
        return all_possible_moves


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

    def check_game_state(self, player_id, board=None):
        """
        Checks the state of the game for the actual player
        :return: Game state in a form of GameStates enum
        """
        if board is None:
            board = self.board_arrays
        player1_pawns = self._find_players_pawns(GameBoard.Players.PLAYER1,
                                                 board)
        if not player1_pawns:
            return GameStates.PLAYER2WIN
        elif player_id == GameBoard.Players.PLAYER1:
            for p_x_ind, p_y_ind, p_el in player1_pawns:
                try:
                    if self._find_moves_for_pawn(p_x_ind, p_y_ind, player_id,
                                                 board):
                        break
                except InvalidMoveException:
                    break
            else:
                return GameStates.PLAYER2WIN

        player_2_pawns = self._find_players_pawns(GameBoard.Players.PLAYER2,
                                                  board)
        if not player_2_pawns:
            return GameStates.PLAYER1WIN
        elif player_id == GameBoard.Players.PLAYER2:
            for p_x_ind, p_y_ind, p_el in player_2_pawns:
                try:
                    if self._find_moves_for_pawn(p_x_ind, p_y_ind, player_id,
                                                 board):
                        break
                except InvalidMoveException:
                    break
            else:
                return GameStates.PLAYER1WIN

        if self.move_count == GameBoard.max_moves_without_capture:
            return GameStates.DRAW

        return GameStates.ONGOING

    def make_move(self, player_id, move_coords, board=None):
        """
        Makes move on the board on the specific coords
        :param board: Board on which the given move will be done
        :type player_id: Players enum value
        :param player_id: Which player is moving
        :param move_coords: Move coords in UCI format
        :return: Board after making move
        """
        changing_class_board = False
        if board is None:
            board = self.board_arrays
            changing_class_board = True
        move_pattern = re.compile('[a-z][0-9]+')
        move_coords_as_list = move_pattern.findall(move_coords)
        if len(move_coords_as_list) != 2:
            raise InvalidMoveException("Invalid move format")
        start_x_ind, start_y_ind = CoordsFormatter.translate_from_uci_to_xy(move_coords_as_list[0])
        end_x_ind, end_y_ind = CoordsFormatter.translate_from_uci_to_xy(move_coords_as_list[1])

        if board[start_y_ind][start_x_ind] not in self.allowed_pawns[player_id]:
            raise InvalidMoveException("There is no pawn of the actual player on given field")

        possible_moves = self._find_moves_for_pawn(
            x_ind=start_x_ind,
            y_ind=start_y_ind,
            player_id=player_id,
            board=board
        )

        move_done = False
        for mov_ind, pawn_rem_list in possible_moves:
            if (end_x_ind, end_y_ind) == mov_ind:
                self.move_count += 1
                board[end_y_ind][end_x_ind] = \
                    board[start_y_ind][start_x_ind]
                board[start_y_ind][start_x_ind] = GameBoard.BoardSigns.EMPTY_BLACK.value
                self.__change_checker_to_king_if_can(end_x_ind, end_y_ind, board)

                for x_rm_ind, y_rm_ind in pawn_rem_list:
                    self.move_count = 0
                    if changing_class_board:
                        self.board_arrays = self.get_board_without_pawn(
                            board_to_get=self.board_arrays,
                            rem_pawn_x=x_rm_ind,
                            rem_pawn_y=y_rm_ind
                        )
                        board = self.board_arrays
                    else:
                        board = self.get_board_without_pawn(
                            board_to_get=board,
                            rem_pawn_x=x_rm_ind,
                            rem_pawn_y=y_rm_ind
                        )
                move_done = True
                break
        if not move_done:
            raise InvalidMoveException("Wrong move coordinates given")
        return board

    def __change_checker_to_king_if_can(self, end_x_ind, end_y_ind, board=None):
        """
        Transform checker to king when the condtitions are set(getting to the
        end of the board)
        :param end_x_ind: Index x of checker that is going to be checked after
        making move
        :param end_y_ind: Index y of checker that is going to be checked after
        making move
        :return:
        """
        if board is None:
            board = self.board_arrays
        checker_to_king_y_index = {
            self.BoardSigns.PLAYER1_CHECKER.value: self.board_size - 1,
            self.BoardSigns.PLAYER2_CHECKER.value: 0
        }
        moved_pawn = board[end_y_ind][end_x_ind]

        if moved_pawn in checker_to_king_y_index.keys() and \
                checker_to_king_y_index[moved_pawn] == end_y_ind:
            if moved_pawn == self.BoardSigns.PLAYER1_CHECKER.value:
                board[end_y_ind][end_x_ind] = self.BoardSigns.PLAYER1_KING.value
            elif moved_pawn == self.BoardSigns.PLAYER2_CHECKER.value:
                board[end_y_ind][end_x_ind] = self.BoardSigns.PLAYER2_KING.value

    def _find_moves_for_pawn(self, x_ind, y_ind, player_id, board=None):
        """
        Method that finds moves for given pawn position and given player
        :param x_ind: X index of the given pawn
        :param y_ind: Y index of the given pawn
        :param player_id: Whose player move it is
        :return: List of possible moves for a given pawn and indexes of pawns
        to be removed by capture in a form of list with
        (x_ind, y_ind), [(x_rm_ind, y_rm_ind), ... ]
        """
        if board is None:
            board = self.board_arrays

        board_to_check = self.get_board_copy(board)
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
            check_backwards=True
        )

        moves_list = []

        if captures_position:
            for cap_pos_x, cap_pos_y, cap_dir in captures_position:
                moves_list += self._find_capture_moves(
                    cap_x_ind=cap_pos_x,
                    cap_y_ind=cap_pos_y,
                    direction=cap_dir,
                    pawn_range=pawn_range,
                    player_id=player_id,
                    board=board
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
        players_pawns = self._find_players_pawns(player_id, board_to_check)
        for pawn_x_ind, pawn_y_ind, pawn_enum in players_pawns:
            found_pawn_range = GameBoard.pawn_ranges[pawn_enum]
            # found_check_backwards_pos = GameBoard.pawn_check_backwards[pawn_enum]

            pawn_capt_pos = self._find_captures_positions(
                pawn_range=found_pawn_range,
                player_id=player_id,
                x_ind=pawn_x_ind,
                y_ind=pawn_y_ind,
                board_2d_container=board_to_check,
                check_backwards=True
            )

            if pawn_capt_pos:
                return True
        return False

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
                if check_el == GameBoard.BoardSigns.EMPTY_BLACK.value:
                    return next_x_ind, next_y_ind, direction
                return None
            elif next_el == GameBoard.BoardSigns.EMPTY_BLACK.value:
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

    def _find_players_pawns(self, player_id, board=None):
        """
        Finds list of players pawns
        :param player_id: Enum telling whose player pawns should be searched
        :return: List with players pawns in a form of a tuple with x_ind, y_ind,
        pawn type
        """
        if board is None:
            board = self.board_arrays
        players_pawns = GameBoard.allowed_pawns[player_id]
        players_pawns = [x for x in players_pawns]

        list_of_players_pawns = []

        for y_ind, part_row in enumerate(board):
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
    game_board.board_arrays = [
            [GameBoard.BoardSigns.EMPTY_BLACK.value if x % 2 == y % 2 else
             GameBoard.BoardSigns.EMPTY_WHITE.value for x in range(game_board.board_size)]
            for y in range(game_board.board_size)]
    get_board_str = create_string_board_from_output(should_add_indexes=True)(
        game_board.get_board_view)
    game_board.board_arrays[6][6] = GameBoard.BoardSigns.PLAYER2_CHECKER.value
    game_board.board_arrays[7][5] = GameBoard.BoardSigns.PLAYER2_CHECKER.value
    game_board.board_arrays[7][7] = GameBoard.BoardSigns.PLAYER2_CHECKER.value
    game_board.board_arrays[5][7] = GameBoard.BoardSigns.PLAYER1_CHECKER.value

    print(game_board.check_game_state(GameBoard.Players.PLAYER1))

    print(get_board_str())
    # print(game_board.board_arrays)
    # game_board.fill_board_with_starting_positions()
    # print(game_board.board_arrays)
    # # print(game_board.get_board_without_pawn(game_board.board_arrays, 0, 0))
    # game_board.make_move(
    #     GameBoard.Players.PLAYER1, 'c3b4'
    # )
    # game_board.make_move(
    #     GameBoard.Players.PLAYER2, 'd6c5'
    # )

    # print(get_board_str())
    # print("\nCapture moves:")
    # x_ind = 1
    # y_ind = 3
    # board_enum = game_board.get_board_element_enum(x_ind, y_ind)
    # print(game_board._find_captures_positions(
    #     pawn_range=game_board.pawn_ranges[board_enum],
    #     player_id=game_board.Players.PLAYER1,
    #     x_ind=x_ind,
    #     y_ind=y_ind,
    #     board_2d_container=game_board.board_arrays,
    #     check_backwards=False
    # ))

    # game_board._initialize_board()
    # game_board
