def display_welcome_message():
    """
    Displays the welcome message and game instructions.
    """
    print("Welcome to the Chess Game!")
    print("Instructions:")
    print(" - The game is for two players on a single PC.")
    print(" - Players will make moves using commands in the format 'A2B3'.")
    print(" - Type 'exit' to quit the game.\n")

def get_player_move(player):
    """
    Captures and validates the player's move.
    Args:
    - player: The player number (1 or 2).

    Returns:
    - A string representing the move or 'exit' if the player wants to quit.
    """
    while True:
        move = input(f"Player {player}, enter your move (e.g., A2B3): ").strip().upper()
        if move.lower() == 'exit':
            return 'exit'
        if len(move) == 4 and move[0].isalpha() and move[2].isalpha() \
           and move[1].isdigit() and move[3].isdigit():
            return move
        print("Invalid input. Please use the format 'A2B3'.")

def initialize_chessboard():
    """
    Initializes the chessboard with pieces in starting positions.
    Returns:
    - A 2D list representing the chessboard.
    """
    board = [
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ["P"] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        [" "] * 8,
        ["p"] * 8,
        ["r", "n", "b", "q", "k", "b", "n", "r"]
    ]
    return board

def print_chessboard(board):
    """
    Prints the chessboard in a readable format.
    Args:
    - board: The 2D list representing the chessboard.
    """
    print("  A B C D E F G H")
    print(" +-----------------+")
    row_number = 8
    for row in board:
        print(f"{row_number}| {' '.join(row)} |")
        row_number -= 1
    print(" +-----------------+")



def parse_move(move):
    """
    Parses the chess move string into board indices.
    Args:
    - move: The move string (e.g., 'A2B3').

    Returns:
    - Tuple of start and end coordinates (row_start, col_start, row_end, col_end).
    """
    col_start, row_start, col_end, row_end = ord(move[0]) - ord('A'), 8 - int(move[1]), ord(move[2]) - ord('A'), 8 - int(move[3])
    return row_start, col_start, row_end, col_end

def path_is_clear(start_row, start_col, end_row, end_col, board):
    """
    Checks if the path between the start and end positions is clear.
    """
    row_step = 1 if end_row > start_row else -1 if end_row < start_row else 0
    col_step = 1 if end_col > start_col else -1 if end_col < start_col else 0

    current_row, current_col = start_row + row_step, start_col + col_step
    while current_row != end_row or current_col != end_col:
        if board[current_row][current_col] != ' ':
            return False
        current_row += row_step
        current_col += col_step
    return True

def basic_piece_movement_rules(start_row, start_col, end_row, end_col, piece, board):
    """
    Validates moves based on basic movement rules of each chess piece.
    """
    # Pawn movement
    if piece.lower() == 'p':
        direction = 1 if piece.islower() else -1
        if start_col == end_col and ((end_row == start_row + direction) or (start_row == (1 if piece.islower() else 6) and end_row == start_row + 2 * direction and board[start_row + direction][start_col] == ' ')):
            return True  # Forward move
        if abs(start_col - end_col) == 1 and end_row == start_row + direction and board[end_row][end_col] != ' ':
            return True  # Diagonal capture

    # Rook movement
    elif piece.lower() == 'r':
        if start_row == end_row or start_col == end_col:
            return path_is_clear(start_row, start_col, end_row, end_col, board)

    # Knight movement
    elif piece.lower() == 'n':
        if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
            return True

    # Bishop movement
    elif piece.lower() == 'b':
        if abs(start_row - end_row) == abs(start_col - end_col):
            return path_is_clear(start_row, start_col, end_row, end_col, board)

    # Queen movement
    elif piece.lower() == 'q':
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            return path_is_clear(start_row, start_col, end_row, end_col, board)

    # King movement
    elif piece.lower() == 'k':
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            return True

    return False

def is_valid_move(move, board, player):
    """
    Validates the chess move.
    Args:
    - move: The move string (e.g., 'A2B3').
    - board: The current state of the chessboard.
    - player: The player number (1 or 2).

    Returns:
    - A boolean indicating whether the move is valid.
    """
    row_start, col_start, row_end, col_end = parse_move(move)
    if 0 <= row_start < 8 and 0 <= col_start < 8 and 0 <= row_end < 8 and 0 <= col_end < 8:
        piece = board[row_start][col_start]
        if piece != ' ' and ((piece.isupper() and player == 1) or (piece.islower() and player == 2)):
            return basic_piece_movement_rules(row_start, col_start, row_end, col_end, piece, board)
    return False

def update_board(move, board, player):
    """
    Updates the board based on the player's move.
    Args:
    - move: The move string (e.g., 'A2B3').
    - board: The current state of the chessboard.
    - player: The player number (1 or 2).
    """
    col_start, row_start, col_end, row_end = ord(move[0]) - ord('A'), 8 - int(move[1]), ord(move[2]) - ord('A'), 8 - int(move[3])
    piece = board[row_start][col_start]
    board[row_start][col_start] = ' '
    board[row_end][col_end] = piece

def main():
    display_welcome_message()
    chessboard = initialize_chessboard()
    print_chessboard(chessboard)

    current_player = 1

    while True:
        player_move = get_player_move(current_player)
        if player_move.lower() == 'exit':
            print(f"Player {current_player} has exited the game.")
            break

        if is_valid_move(player_move, chessboard, current_player):
            update_board(player_move, chessboard, current_player)
            print_chessboard(chessboard)
            current_player = 1 if current_player == 2 else 2  # Switch player
        else:
            print("Invalid move. Try again.")

        # Add check/checkmate logic here

if __name__ == "__main__":
    main()
