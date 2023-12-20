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

# Example of how to use the display_manager function:
# print(display_manager(chessboard))
