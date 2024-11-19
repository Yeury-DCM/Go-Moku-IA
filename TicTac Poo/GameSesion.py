class Game:
    def __init__(self):
        self.board = Board()
        self.human = Player(player_type=1)
        self.ai = MinimaxSolver(player_type=2)
        self.ui = UI(self)
        self.player = 1
        self.game_over = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    mouseX = event.pos[0] // SQUARE_SIZE
                    mouseY = event.pos[1] // SQUARE_SIZE
                    if self.board.available_square(mouseY, mouseX):
                        self.board.mark_square(mouseY, mouseX, self.player)
                        if self.board.check_win(self.player):
                            self.game_over = True
                        self.player = self.player % 2 + 1
                        if not self.game_over:
                            row, col = self.ai.best_move(self.board)
                            self.board.mark_square(row, col, 2)
                            if self.board.check_win(2):
                                self.game_over = True
                            self.player = self.player % 2 + 1
                        if not self.game_over and self.board.is_full():
                            self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.ui.restart_game()
                        self.game_over = False
                        self.player = 1
            self.ui.update(self.game_over)

if __name__ == "__main__":
    game = Game()
    game.run()