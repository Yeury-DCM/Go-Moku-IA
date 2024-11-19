import pygame

# Define Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCUL_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

class UI:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tic Tac Toe IA Minimax')
        self.screen.fill(BLACK)
        self.draw_lines()

    def draw_lines(self, color=WHITE):
        for i in range(1, BOARD_ROWS):
            pygame.draw.line(self.screen, color, start_pos=(0, SQUARE_SIZE * i), end_pos=(WIDTH, SQUARE_SIZE * i), width=LINE_WIDTH)
            pygame.draw.line(self.screen, color, start_pos=(SQUARE_SIZE * i, 0), end_pos=(SQUARE_SIZE * i, WIDTH), width=LINE_WIDTH)

    def draw_figures(self, board, color=WHITE):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                value_position = board[row][col]
                if value_position == 1:
                    pygame.draw.circle(self.screen, color, center=(int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                       radius=CIRCUL_RADIUS, width=CIRCLE_WIDTH)
                elif value_position == 2:
                    pygame.draw.line(self.screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                     (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), width=CROSS_WIDTH)
                    pygame.draw.line(self.screen, color, (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                     (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), width=CROSS_WIDTH)

    def update(self, game_over):
        if not game_over:
            self.draw_figures(self.game.board.board)
        else:
            if self.game.board.check_win(1):
                self.draw_lines(GREEN)
                self.draw_figures(self.game.board.board, GREEN)
            elif self.game.board.check_win(2):
                self.draw_lines(RED)
                self.draw_figures(self.game.board.board, RED)
            else:
                self.draw_lines(GRAY)
                self.draw_figures(self.game.board.board, GRAY)
        pygame.display.update()

    def restart_game(self):
        self.screen.fill(BLACK)
        self.draw_lines()
        self.game.board.reset()