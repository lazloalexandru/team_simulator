"""
... Add reviewer after each step ???

this is a whole file.
fix this chess game, and make sure you give me whole modified source code, not just parts! generate just the code!
review it in the background and fix problems.
"""

import numpy as np

# Constants for the bit representation of pieces
EMPTY, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110
WHITE, BLACK = 0b1000, 0b0000

# ASCII representations of the pieces
PIECE_SYMBOLS = {
    EMPTY: ' . ',
    PAWN | WHITE: ' P ',
    KNIGHT | WHITE: ' N ',
    BISHOP | WHITE: ' B ',
    ROOK | WHITE: ' R ',
    QUEEN | WHITE: ' Q ',
    KING | WHITE: ' K ',
    PAWN | BLACK: ' p ',
    KNIGHT | BLACK: ' n ',
    BISHOP | BLACK: ' b ',
    ROOK | BLACK: ' r ',
    QUEEN | BLACK: ' q ',
    KING | BLACK: ' k ',
}

class ChessBoard:
    def __init__(self):
        self.board = np.zeros((8,), dtype=np.uint32)
        self.initialize_board()

    def initialize_board(self):
        # Setup pieces for both colors
        self.set_initial_row(0, WHITE)
        self.set_initial_row(7, BLACK)
        self.board[1] = (PAWN | WHITE) * 0x11111111
        self.board[6] = (PAWN | BLACK) * 0x11111111

    def set_initial_row(self, row, color):
        self.board[row] = (ROOK | color) | ((KNIGHT | color) << 4) | ((BISHOP | color) << 8) | ((QUEEN | color) << 12) | ((KING | color) << 16) | ((BISHOP | color) << 20) | ((KNIGHT | color) << 24) | ((ROOK | color) << 28)

    def get_piece_at_position(self, row, col):
        shift = col * 4
        return (self.board[row] >> shift) & 0b1111

    def set_piece_at_position(self, row, col, piece):
        shift = col * 4
        self.board[row] &= ~(0b1111 << shift)
        self.board[row] |= piece << shift

    def render(self):
        board_str = '  A  B  C  D  E  F  G  H\n'
        for row in range(8):
            board_str += str(8 - row) + ' '
            for col in range(8):
                piece = self.get_piece_at_position(row, col)
                board_str += PIECE_SYMBOLS[piece]
            board_str += ' ' + str(8 - row) + '\n'
        board_str += '  A  B  C  D  E  F  G  H\n'
        return board_str

class GameState:
    def __init__(self):
        self.chessboard = ChessBoard()
        self.current_turn = WHITE
        self.move_history = []

    def switch_turn(self):
        self.current_turn ^= 0b1000

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # Basic validation: Check if positions are within the board boundaries
        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Get the piece at the start position
        piece = self.chessboard.get_piece_at_position(start_row, start_col)
        if piece == EMPTY or (piece & 0b1000) != self.current_turn:
            return False  # No piece at the start position or wrong color

        # Basic movement rules for each piece type
        if piece & 0b0111 == PAWN:
            # TODO: Add pawn-specific rules (e.g., two-step move, en passant)
            pass
        elif piece & 0b0111 == KNIGHT:
            # TODO: Add knight-specific rules
            pass
        elif piece & 0b0111 == BISHOP:
            # TODO: Add bishop-specific rules
            pass
        elif piece & 0b0111 == ROOK:
            # TODO: Add rook-specific rules
            pass
        elif piece & 0b0111 == QUEEN:
            # TODO: Add queen-specific rules
            pass
        elif piece & 0b0111 == KING:
            # TODO: Add king-specific rules
            pass

        # Add more comprehensive movement rules here

        return True  # Placeholder for actual validation logic

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

    def parse_move(self, move_str):
        try:
            start_pos, end_pos = move_str.split()[::2]
            start_col, start_row = ord(start_pos[0].upper()) - ord('A'), 8 - int(start_pos[1])
            end_col, end_row = ord(end_pos[0].upper()) - ord('A'), 8 - int(end_pos[1])
            return start_row, start_col, end_row, end_col
        except Exception as e:
            print(f'Error parsing move: {e}')
            return None

def input_handler(game_state):
    move_str = input('Enter your move (e.g., A2 to A3): ').strip()
    if not move_str or 'to' not in move_str:
        print('Invalid move format. Use the format: A2 to A3')
        return None
    return game_state.parse_move(move_str)

if __name__ == '__main__':
    game_state = GameState()
    print(game_state.chessboard.render())
    while True:
        parsed_move = input_handler(game_state)
        if parsed_move:
            game_state.make_move(*parsed_move)
            print(game_state.chessboard.render())
        else:
            continue
