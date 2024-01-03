class Chessboard:
    def __init__(self):
        # Representing each row with a 32-bit integer
        self.rows = [0b00000000,  # Row 8 (from white's perspective)
                     0b00000000,  # Row 7
                     0b00000000,  # Row 6
                     0b00000000,  # Row 5
                     0b00000000,  # Row 4
                     0b00000000,  # Row 3
                     0b00000000,  # Row 2
                     0b00000000]  # Row 1

        # Initialize the chessboard with the starting positions of pieces
        self.initialize_board()

    def initialize_board(self):
        # Setting up pawns
        self.rows[1] = 0b11111111  # Row 7: Black Pawns
        self.rows[6] = 0b11111111  # Row 2: White Pawns

        # Setting up other pieces (Rooks, Knights, Bishops, Queen, King)
        # Encoding: Rook = 1, Knight = 2, Bishop = 3, Queen = 4, King = 5
        self.rows[0] = 0b01010011  # Row 8: Black Rooks, Knights, Bishops, Queen, King
        self.rows[7] = 0b01010011  # Row 1: White Rooks, Knights, Bishops, Queen, King

    def display_board(self):
        # Display the board using Unicode characters
        piece_symbols = {
            0: ' ',
            1: '\u265C',  # Rook
            2: '\u265E',  # Knight
            3: '\u265D',  # Bishop
            4: '\u265B',  # Queen
            5: '\u265A',  # King
            8: '\u265F',  # Pawn
        }

        for row in self.rows:
            for i in range(8):
                piece = (row >> (4 * (7-i))) & 0b1111
                print(piece_symbols.get(piece, '?'), end=' ')
            print()

    def validate_move(self, move):
        # Implement move validation logic
        # This function should be implemented with the rules of chess
        # For simplicity, this example only includes logic for pawn moves
        # A real implementation should include all pieces and special moves
        if len(move) != 4 or not move.isalpha():
            return False
        start_col, start_row, end_col, end_row = move.lower()
        start_col = ord(start_col) - ord('a')
        start_row = 8 - int(start_row)
        end_col = ord(end_col) - ord('a')
        end_row = 8 - int(end_row)
        if start_col < 0 or start_col > 7 or end_col < 0 or end_col > 7:
            return False
        if start_row < 0 or start_row > 7 or end_row < 0 or end_row > 7:
            return False
        start_piece = (self.rows[start_row] >> (4 * (7 - start_col))) & 0b1111
        end_piece = (self.rows[end_row] >> (4 * (7 - end_col))) & 0b1111
        if start_piece == 8:  # Pawn
            if start_col == end_col and (end_row == start_row - 1 or (start_row == 6 and end_row == 4 and self.rows[5] == 0)):
                if end_piece == 0:  # Normal move
                    return True
            if abs(start_col - end_col) == 1 and end_row == start_row - 1 and end_piece != 0:  # Capture
                return True
        return False

    def make_move(self, move):
        if self.validate_move(move):
            # Implement the logic to update the board with the new move
            start_col, start_row, end_col, end_row = move.lower()
            start_col = ord(start_col) - ord('a')
            start_row = 8 - int(start_row)
            end_col = ord(end_col) - ord('a')
            end_row = 8 - int(end_row)
            piece = (self.rows[start_row] >> (4 * (7 - start_col))) & 0b1111
            self.rows[start_row] &= ~(0b1111 << (4 * (7 - start_col)))
            self.rows[end_row] |= piece << (4 * (7 - end_col))
            print('Move made!')
        else:
            print('Invalid move!')

    def is_game_over(self):
        # Implement game over conditions
        # For simplicity, this example only checks for lack of kings
        for row in self.rows:
            if (row & 0b0101010101010101) != 0:  # Checks for white king
                return False
            if (row & 0b1010101010101010) != 0:  # Checks for black king
                return False
        return True

# Example usage:
chessboard = Chessboard()
chessboard.display_board()

# Implement game loop and player interaction
while not chessboard.is_game_over():
    move = input('Enter your move (e.g., A2A4): ')
    chessboard.make_move(move)
    chessboard.display_board()
