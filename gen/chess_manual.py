class ChessGame:
    def __init__(self):
        self.board = self.initialize_board()
        self.piece_map = self.create_piece_map()
        self.current_player = 'White'

    def initialize_board(self):
        # Initialize the board with the correct starting position
        return [
            0b00100011001001010011001000100010,  # Black major pieces: Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook
            0b00010001000100010001000100010001,  # Black pawns
            0, 0, 0, 0,                           # Empty squares
            0b10010001000100010001000100010001,  # White pawns
            0b10100011001001010110001000100010   # White major pieces: Rook, Knight, Bishop, King, Queen, Bishop, Knight, Rook
        ]

    def create_piece_map(self):
        # Map the 4-bit representation to Unicode characters
        return {
            0: ' ',  # Empty
            1: '♟',  # Black pawn
            2: '♜',  # Black rook
            3: '♞',  # Black knight
            4: '♝',  # Black bishop
            5: '♛',  # Black queen
            6: '♚',  # Black king
            9: '♙',  # White pawn
            10: '♖', # White rook
            11: '♘', # White knight
            12: '♗', # White bishop
            13: '♔', # White king
            14: '♕'  # White queen
        }

    def print_board(self):
        print("  a b c d e f g h")
        for i, row in enumerate(self.board):
            print(8 - i, end=' ')
            print(self.format_row(row))

    def format_row(self, row):
        row_str = ""
        for i in range(8):
            piece_code = (row >> (4 * (7 - i))) & 0b1111
            row_str += self.piece_map[piece_code] + " "
        return row_str

    def is_valid_move(self, start_row, start_col, end_row, end_col, piece):
        # Check if a move is valid for the given piece
        if piece == 1 or piece == 9:  # Black Pawn or White Pawn
            return self.is_valid_pawn_move(start_row, start_col, end_row, end_col, piece)
        elif piece == 2 or piece == 10:  # Black Rook or White Rook
            return self.is_valid_rook_move(start_row, start_col, end_row, end_col)
        elif piece == 3 or piece == 11:  # Black Knight or White Knight
            return self.is_valid_knight_move(start_row, start_col, end_row, end_col)
        elif piece == 4 or piece == 12:  # Black Bishop or White Bishop
            return self.is_valid_bishop_move(start_row, start_col, end_row, end_col)
        elif piece == 5 or piece == 14:  # Black Queen or White Queen
            return self.is_valid_queen_move(start_row, start_col, end_row, end_col)
        elif piece == 6 or piece == 13:  # Black King or White King
            return self.is_valid_king_move(start_row, start_col, end_row, end_col)
        return False

    def move_piece(self, move):
        # Simplified move logic: 'e2e4' format
        if len(move) != 4 or not move.isalnum():
            print("Invalid move format. Please use 'e2e4' format.")
            return False
            
        if not self.is_valid_move(start_row, start_col, end_row, end_col, piece):
            print("Invalid move for the piece.")
            return False


        start_col = ord(move[0]) - ord('a')
        start_row = 8 - int(move[1])
        end_col = ord(move[2]) - ord('a')
        end_row = 8 - int(move[3])

        if start_col == end_col and start_row == end_row:
            print("Invalid move. Start and end positions are the same.")
            return False

        # Extract piece from start position
        piece = (self.board[start_row] >> (4 * (7 - start_col))) & 0b1111

        # Clear start position
        self.board[start_row] &= ~(0b1111 << (4 * (7 - start_col)))

        # Place piece at end position
        self.board[end_row] &= ~(0b1111 << (4 * (7 - end_col)))  # Clear destination
        self.board[end_row] |= piece << (4 * (7 - end_col))

        self.current_player = 'Black' if self.current_player == 'White' else 'White'
        return True

    def play_game(self):
        while True:
            print(f"\n{self.current_player}'s turn")
            self.print_board()
            move = input("Enter your move (e.g., e2e4) or 'quit' to exit: ")
            if move.lower() == 'quit':
                print("Game Over")
                break
            if not self.move_piece(move):
                print("Please enter a valid move.")

game = ChessGame()
game.play_game()
