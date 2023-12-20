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

# ASCII representations of the pieces
PIECE_SYMBOLS = {
    EMPTY: ' . ',
    PAWN | WHITE: '\'p\'',
    KNIGHT | WHITE: '\'n\'',
    BISHOP | WHITE: '\'b\'',
    ROOK | WHITE: '\'r\'',
    QUEEN | WHITE: '\'q\'',
    KING | WHITE: '\'k\'',
    PAWN | BLACK: '\'P\'',
    KNIGHT | BLACK: '\'N\'',
    BISHOP | BLACK: '\'B\'',
    ROOK | BLACK: '\'R\'',
    QUEEN | BLACK: '\'Q\'',
    KING | BLACK: '\'K\'',
}

# Initialize the chessboard with 32-bit integers for each row
class ChessBoard:
    # Existing ChessBoard methods...

    def render(self):
        board_str = '  A  B  C  D  E  F  G  H\n'
        for row in range(8):
            board_str += str(8 - row) + ' '
            for col in range(8):
                piece = self.get_piece_at_position(row, col)
                board_str += PIECE_SYMBOLS[piece] + ' '
            board_str += str(8 - row) + '\n'
        board_str += '  A  B  C  D  E  F  G  H\n'
        return board_str

class GameState:
    # Existing GameState methods...

if __name__ == '__main__':
    game_state = GameState()
    print(game_state.chessboard.render())
    while True:
        parsed_move = game_state.input_handler()
        if parsed_move:
            game_state.make_move(*parsed_move)
            print(game_state.chessboard.render())
        else:
            continue
