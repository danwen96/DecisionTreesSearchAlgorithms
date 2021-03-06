from enum import Enum

from decision_games_with_ai.games.game_board_abc import GameBoardABC
from decision_games_with_ai.games.utils.events_exceptions import InvalidMoveException
from decision_games_with_ai.games.utils.coords_formatters import CoordsFormatter
from decision_games_with_ai.games.utils.global_enums import GameStates
from decision_games_with_ai.games.utils.view_modificators import create_string_board_from_output


class GameBoard(GameBoardABC):
    """Stores game board and provides method to manipulate on it"""

    class BoardSigns(Enum):
        """Enum with possible board signs"""
        PLAYER1 = 'x'
        PLAYER2 = 'o'
        EMPTY = '-'

    def __init__(self):
        self.board_size = 3
        self.winning_combination = 3
        self._initialize_board()

    def _initialize_board(self):
        """
        Initializes board with the values for the game start
        :return:
        """

        self.board_arrays = [
            [GameBoard.BoardSigns.EMPTY.value for x in range(self.board_size)]
            for y in range(self.board_size)]
        self.moves_list = []

    # @create_string_board_from_output(should_add_indexes=True)
    # def get_board_view(self):
    #     """
    #     Returns the view of board
    #     :return: Lists with the board values
    #     """
    #     return [list(act_list) for act_list in reversed(self.board_arrays)]

    def get_possible_moves(self, board):
        """
        Gets possible moves for given board
        :param board: Board for which the moves will be found
        :return: List of possible moves in list of strnig in UCI format
        """
        possible_moves = []
        for i, row in enumerate(board):
            for j, el in enumerate(row):
                if el == self.BoardSigns.EMPTY.value:
                    possible_moves.append(CoordsFormatter.translate_from_xy_to_uci(j, i))
        return possible_moves

    def check_game_state(self, board=None):
        """
        Checks if game has ended
        :return: GameStates state in which game is now
        """
        if isinstance(board, tuple):
            board = self.get_board_copy(board)

        if board is None:
            board = self.board_arrays

        wining_lines_list = []

        # I copy the references of the actual boards lists, be careful not to
        # modify them there
        wining_lines_list += [*board]
        wining_lines_list += [[part_line[i] for part_line in board]
                              for i in range(self.board_size)]

        for possible_combination_num in range(len(board)):
            new_row_list = []
            try:
                for row_ind, row in enumerate(board[possible_combination_num:]):
                    new_row_list.append(row[row_ind])
            except IndexError:
                pass
            wining_lines_list.append(new_row_list)

            new_row_list = []
            try:
                for row_ind, row in enumerate(board):
                    new_row_list.append((row[row_ind + possible_combination_num]))
            except IndexError:
                pass
            wining_lines_list.append(new_row_list)

            new_row_list = []
            try:
                for row_ind, row in enumerate(reversed(board[:possible_combination_num])):
                    new_row_list.append(row[row_ind])
            except IndexError:
                pass
            wining_lines_list.append(new_row_list)

            new_row_list = []
            try:
                for row_ind, row in enumerate(reversed(board)):
                    new_row_list.append((row[row_ind + possible_combination_num]))
            except IndexError:
                pass
            wining_lines_list.append(new_row_list)

        for par_win_line in wining_lines_list:
            previous_sign = GameBoard.BoardSigns.EMPTY.value
            signs_counter = 0
            for sign in par_win_line:
                if sign == GameBoard.BoardSigns.EMPTY.value:
                    previous_sign = GameBoard.BoardSigns.EMPTY.value
                    signs_counter = 0
                else:
                    if sign == previous_sign:
                        signs_counter += 1
                        if signs_counter >= self.winning_combination:
                            if sign == GameBoard.BoardSigns.PLAYER1.value:
                                return GameStates.PLAYER1WIN
                            elif sign == GameBoard.BoardSigns.PLAYER2.value:
                                return GameStates.PLAYER2WIN
                            else:
                                return TypeError("Unexpected sign type")
                    else:
                        signs_counter = 1
                        previous_sign = sign

        if all(GameBoard.BoardSigns.EMPTY.value not in part_win_line for
               part_win_line in wining_lines_list):
            return GameStates.DRAW

        return GameStates.ONGOING

    def make_move(self, player_id, move_coords, board=None):
        """
        Makes move on the board on the specific coords
        :param board: Board that will be checked
        :type player_id: BoardSigns enum value
        :param player_id: Which player is moving
        :param move_coords: Move coords in UCI format
        :return: Board after making move
        """
        was_tuple = False
        if isinstance(board, tuple):
            board = self.get_board_copy(board, copy_format='list')
            was_tuple = True
        if board is None:
            board = self.board_arrays

        x_ind, y_ind = CoordsFormatter.translate_from_uci_to_xy(move_coords)

        if board[y_ind][x_ind] == GameBoard.BoardSigns.EMPTY.value:
            board[y_ind][x_ind] = player_id.value
        else:
            raise InvalidMoveException("The chosen field is not empty. Move is invalid.")
        if not was_tuple:
            return board
        else:
            return self.get_board_copy(board, copy_format='tuple')
        # self.moves_list.append(move_coords)


if __name__ == "__main__":
    game_board = GameBoard()
    # print(game_board.get_board_view())
    print(create_string_board_from_output(should_add_indexes=True)(game_board.get_board_view)())
