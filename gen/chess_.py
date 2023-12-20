class BitboardChess(object):
    def __init__(self):
        # Representing each row of the chessboard with a 32-bit integer
        self.rows = [0b00000000] * 8

        # Initial positions for pieces using 4 bits each
        # 1st and 8th row for pieces, 2nd and 7th row for pawns
        self.rows[0] = 0b10011101001110100000000000000000 # Rooks, Knights, Bishops, Queen, King
        self.rows[1] = 0b01010101010101010000000000000000 # Pawns
        self.rows[6] = 0b00000000000000000101010101010101 # Pawns
        self.rows[7] = 0b00000000000000001001110100111010 # Rooks, Knights, Bishops, Queen, King

    def get_piece_at_position(self, row, col):
        # Assuming col is 0-indexed, from left to right
        # Extracting 4 bits representing the piece at the given position
        mask = 0b1111 << (28 - col * 4)
        piece_code = (self.rows[row] & mask) >> (28 - col * 4)
        return piece_code

    def set_piece_at_position(self, row, col, piece_code):
        # Assuming piece_code is a 4-bit representation of a piece
        # Clearing the position first
        mask = ~(0b1111 << (28 - col * 4))
        self.rows[row] &= mask
        # Setting the new piece
        self.rows[row] |= (piece_code << (28 - col * 4))

    def print_board(self):
        # Mapping from piece_code to Unicode characters
        piece_to_unicode = {
            0b0000: '.', # Empty square
            0b0001: 'P', # Pawn
            0b0010: 'N', # Knight
            0b0011: 'B', # Bishop
            0b0100: 'R', # Rook
            0b0101: 'Q', # Queen
            0b0110: 'K', # King
            # Add other piece codes and their representations as needed
        }

        for row in self.rows:
            for col in range(8):
                piece_code = self.get_piece_at_position(row, col)
                print(piece_to_unicode.get(piece_code, '?'), end=' ')
            print() # Newline for each row

    def is_valid_move(self, start_pos, end_pos):
        # TODO: Implement the move validation logic according to the rules of chess
        # This is a placeholder function and should be expanded to cover all chess rules
        # For now, it just checks if the move is within the bounds of the board
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        if 0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8:
            return True
        return False

    def move_piece(self, start_pos, end_pos):
        # TODO: Implement the logic to move a piece from start_pos to end_pos
        # This should include capturing, pawn promotion, and en passant
        # For now, it just moves a piece without any rule checks
        if not self.is_valid_move(start_pos, end_pos):
            return False

        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece_code = self.get_piece_at_position(start_row, start_col)
        self.set_piece_at_position(end_row, end_col, piece_code)
        self.set_piece_at_position(start_row, start_col, 0b0000) # Clear the start position
        return True

# Example usage
# chess_game = BitboardChess()
# chess_game.print_board()
# if chess_game.move_piece((1,0), (2,0)):
#     chess_game.print_board()
# else:
#     print('Invalid move!')