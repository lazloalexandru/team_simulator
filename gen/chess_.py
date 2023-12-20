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
# print(chessboard)