
class MinimaxSolver:
    def __init__(self, player_type):
        self.player_type = player_type

    def minimax(self, board, depth, is_maximizing):
        if board.check_win(2):
            return float('inf')
        elif board.check_win(1):
            return float('-inf')
        elif board.is_full():
            return 0

        if is_maximizing:
            best_score = -1000
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board.available_square(row, col):
                        board.mark_square(row, col, 2)
                        score = self.minimax(board, depth + 1, False)
                        board.mark_square(row, col, 0)
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = 1000
            for row in range(BOARD_ROWS):
                for col in range(BOARD_COLS):
                    if board.available_square(row, col):
                        board.mark_square(row, col, 1)
                        score = self.minimax(board, depth + 1, True)
                        board.mark_square(row, col, 0)
                        best_score = min(score, best_score)
            return best_score

    def best_move(self, board):
        best_score = -1000
        move = (-1, -1)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board.available_square(row, col):
                    board.mark_square(row, col, 2)
                    score = self.minimax(board, 0, False)
                    board.mark_square(row, col, 0)
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move