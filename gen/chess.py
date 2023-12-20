class Chessboard:
    def __init__(self):
        self.rows = [0b00010001000100010001000100010001,
                     0b00000000000000000000000000000000,
                     0b00000000000000000000000000000000,
                     0b00000000000000000000000000000000,
                     0b00000000000000000000000000000000,
                     0b00000000000000000000000000000000,
                     0b00010001000100010001000100010001,
                     0b00010001000100010001000100010001]

    def encode_piece(self, piece):
        encoding = {
            'K': 0b0001, # King
            'Q': 0b0010, # Queen
            'R': 0b0011, # Rook
            'B': 0b0100, # Bishop
            'N': 0b0101, # Knight
            'P': 0b0110, # Pawn
            '.': 0b0000, # Empty square
        }
        return encoding.get(piece, 0b0000)

    def set_piece(self, row, col, piece):
        encoded_piece = self.encode_piece(piece)
        self.rows[row] &= ~(0b1111 << (col * 4)) # Clear the bits where the piece will go
        self.rows[row] |= encoded_piece << (col * 4) # Set the piece bits

    def get_piece(self, row, col):
        piece_code = (self.rows[row] >> (col * 4)) & 0b1111
        for piece, code in self.encode_piece('').items():
            if code == piece_code:
                return piece
        return '.'

    def __str__(self):
        board_str = ''
        for row in self.rows:
            for col in range(8):
                board_str += self.get_piece(row, col) + ' '
            board_str += '\n'
        return board_str

def input_handler(prompt='Your move (e.g., A2 to B3): '):
    while True:
        user_input = input(prompt).strip()
        if move_parser(user_input):
            return user_input
        else:
            print('Invalid move format. Please try again.')

def move_parser(command):
    try:
        start_pos, end_pos = command.lower().split(' to ')
        start_col, start_row = ord(start_pos[0]) - ord('a'), int(start_pos[1]) - 1
        end_col, end_row = ord(end_pos[0]) - ord('a'), int(end_pos[1]) - 1
        if 0 <= start_col < 8 and 0 <= start_row < 8 and 0 <= end_col < 8 and 0 <= end_row < 8:
            return start_row, start_col, end_row, end_col
        else:
            return None
    except (ValueError, IndexError):
        return None

def display_manager(chessboard):
    piece_symbols = {
        'K': '\\u2654', # King
        'Q': '\\u2655', # Queen
        'R': '\\u2656', # Rook
        'B': '\\u2657', # Bishop
        'N': '\\u2658', # Knight
        'P': '\\u2659', # Pawn
        '.': ' '
    }

    board_str = '  a b c d e f g h\n'
    for row_index, row in enumerate(chessboard.rows):
        board_str += str(8 - row_index) + ' '
        for col in range(8):
            piece = chessboard.get_piece(7 - row_index, col)
            board_str += piece_symbols[piece] + ' '
        board_str += str(8 - row_index) + '\n'
    board_str += '  a b c d e f g h\n'
    return board_str


class GameStateManager:
    def __init__(self, chessboard):
        self.chessboard = chessboard
        self.current_turn = 'white'
        self.move_history = []

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def make_move(self, start_row, start_col, end_row, end_col):
        # TODO: Implement move validation based on chess rules
        piece = self.chessboard.get_piece(start_row, start_col)
        self.chessboard.set_piece(end_row, end_col, piece)
        self.chessboard.set_piece(start_row, start_col, '.')
        self.move_history.append((start_row, start_col, end_row, end_col))
        self.switch_turn()

    def is_valid_move(self, start_row, start_col, end_row, end_col):
        # TODO: Implement detailed move validation
        return True

    def undo_move(self):
        if not self.move_history:
            return
        last_move = self.move_history.pop()
        self.chessboard.set_piece(last_move[2], last_move[3], '.')
        self.chessboard.set_piece(last_move[0], last_move[1], self.chessboard.get_piece(last_move[2], last_move[3]))
        self.switch_turn()

# Example usage:
# game_state_manager = GameStateManager(chessboard)
# game_state_manager.make_move(1, 4, 3, 4) # Move pawn from E2 to E4
# print(chessboard)
# game_state_manager.undo_move()

# Initialize the chessboard
chessboard = Chessboard()

# Set initial positions for pieces
# This is just an example and should be replaced with actual game starting positions
chessboard.set_piece(0, 0, 'R')
chessboard.set_piece(0, 1, 'N')
chessboard.set_piece(0, 2, 'B')
chessboard.set_piece(0, 3, 'Q')
chessboard.set_piece(0, 4, 'K')
chessboard.set_piece(0, 5, 'B')
chessboard.set_piece(0, 6, 'N')
chessboard.set_piece(0, 7, 'R')
for col in range(8):
    chessboard.set_piece(1, col, 'P')
    chessboard.set_piece(6, col, 'P')
chessboard.set_piece(7, 0, 'R')
chessboard.set_piece(7, 1, 'N')
chessboard.set_piece(7, 2, 'B')
chessboard.set_piece(7, 3, 'Q')
chessboard.set_piece(7, 4, 'K')
chessboard.set_piece(7, 5, 'B')
chessboard.set_piece(7, 6, 'N')
chessboard.set_piece(7, 7, 'R')

# Print the chessboard
print(chessboard)