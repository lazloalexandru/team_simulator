import numpy as np

# Constants for the bit representation of pieces
EMPTY = 0b0000
PAWN = 0b0001
KNIGHT = 0b0010
BISHOP = 0b0011
ROOK = 0b0100
QUEEN = 0b0101
KING = 0b0110
WHITE = 0b1000
BLACK = 0b0000

# Initialize the chessboard with 32-bit integers for each row
class ChessBoard:
    def __init__(self):
        self.board = np.zeros((8,), dtype=np.uint32)
        self.initialize_board()

    def initialize_board(self):
        # Setup white pieces
        self.board[0] = (ROOK | WHITE) | ((KNIGHT | WHITE) << 4) | ((BISHOP | WHITE) << 8) | ((QUEEN | WHITE) << 12) | ((KING | WHITE) << 16) | ((BISHOP | WHITE) << 20) | ((KNIGHT | WHITE) << 24) | ((ROOK | WHITE) << 28)
        self.board[1] = (PAWN | WHITE) * 0x11111111

        # Setup black pieces
        self.board[6] = (PAWN | BLACK) * 0x11111111
        self.board[7] = (ROOK | BLACK) | ((KNIGHT | BLACK) << 4) | ((BISHOP | BLACK) << 8) | ((QUEEN | BLACK) << 12) | ((KING | BLACK) << 16) | ((BISHOP | BLACK) << 20) | ((KNIGHT | BLACK) << 24) | ((ROOK | BLACK) << 28)

    def get_piece_at_position(self, row, col):
        # Extract the piece from the bitboard
        shift = col * 4
        piece = (self.board[row] >> shift) & 0b1111
        return piece

    def set_piece_at_position(self, row, col, piece):
        # Set the piece on the bitboard
        shift = col * 4
        self.board[row] &= ~(0b1111 << shift)
        self.board[row] |= piece << shift

    def __str__(self):
        board_str = ''
        for row in range(8):
            for col in range(8):
                piece = self.get_piece_at_position(row, col)
                board_str += f'{piece:04b} '
            board_str += '\n'
        return board_str

class GameState:
    def __init__(self):
        self.chessboard = ChessBoard()
        self.current_turn = WHITE
        self.move_history = []

    def switch_turn(self):
        self.current_turn ^= 0b1000

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # Placeholder for move validation logic
        # Needs to be implemented based on chess rules
        return True

    def make_move(self, start_row, start_col, end_row, end_col):
        if self.is_valid_move(start_row, start_col, end_row, end_col):
            piece = self.chessboard.get_piece_at_position(start_row, start_col)
            self.chessboard.set_piece_at_position(end_row, end_col, piece)
            self.chessboard.set_piece_at_position(start_row, start_col, EMPTY)
            self.move_history.append(((start_row, start_col), (end_row, end_col)))
            self.switch_turn()

    def undo_move(self):
        if self.move_history:
            last_move = self.move_history.pop()
            start_pos, end_pos = last_move
            piece = self.chessboard.get_piece_at_position(end_pos[0], end_pos[1])
            self.chessboard.set_piece_at_position(start_pos[0], start_pos[1], piece)
            self.chessboard.set_piece_at_position(end_pos[0], end_pos[1], EMPTY)
            self.switch_turn()

# Example usage
if __name__ == '__main__':
    game_state = GameState()
    print(game_state.chessboard)
    game_state.make_move(1, 0, 2, 0) # Example move: Pawn from A2 to A3
    print(game_state.chessboard)
    game_state.undo_move()
    print(game_state.chessboard)
