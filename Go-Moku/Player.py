class Player:
    def __init__(self, player_number, is_human=True):

        self.player_id = player_number
        self.is_human = is_human

    def make_move(self, board, row, col):
        
        if board.is_square_available(row, col):
            board.mark_square(row, col, self.player_id)
            return True
        return False

    def __str__(self):
        """Devuelve una representación legible del jugador."""
        return f"Player {self.player_id} ({'Human' if self.is_human else 'AI'})"
