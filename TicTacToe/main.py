import sys
import pygame
import numpy as np

print(1 % 2)
pygame.init()

# IMPORTANT TO REMEMBER:
# The player #1 is the human
# The player #2 Is the Minimax IA

# Define Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Proportions
WIDTH = 300
HEIGHT = 300
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCUL_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe IA Minimax')
screen.fill(BLACK)

board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, start_pos=(0, SQUARE_SIZE * i), end_pos=(WIDTH, SQUARE_SIZE * i), width=LINE_WIDTH)
        pygame.draw.line(screen, color, start_pos=(SQUARE_SIZE * i, 0), end_pos=(SQUARE_SIZE * i, WIDTH), width=LINE_WIDTH)


# Player #1 is human, #2 is IA
def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            value_position = board[row][col]
            if value_position == 1:
                pygame.draw.circle(screen, color, center=(int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   radius=CIRCUL_RADIUS, width=CIRCLE_WIDTH)
            elif value_position == 2:
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), width=CROSS_WIDTH)
                pygame.draw.line(screen, color, (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), width=CROSS_WIDTH)


def mark_square(row, column, player):
    board[row][column] = player


def available_square(row, column):
    return board[row][column] == 0


def is_board_full(check_board=board):
    for row in range(BOARD_ROWS):
        for column in range(BOARD_COLS):
            if check_board[row][column] == 0:
                return False
    return True


def check_win(player, check_board=board):
    for col in range(BOARD_COLS):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[2][0] == player and check_board[1][1] == player and check_board[0][2] == player:
        return True

    return False


draw_lines()


def minimax(minimax_board, depth, is_maximaxing):
    # Base cases
    if check_win(2, minimax_board):
        return float('inf')
    elif check_win(1, minimax_board):
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximaxing:
        best_score = -1000

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score

    else:
        best_score = 1000

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -1000
    move = (-1, -1)

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    else:
        return False


def restart_game():
    screen.fill(BLACK)
    draw_lines()

    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_lines()

player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move():
                        if check_win(2):
                            game_over = True
                        player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_lines(GREEN)
            draw_figures(GREEN)
        elif check_win(2):
            draw_lines(RED)
            draw_figures(RED)
        else:
            draw_lines(GRAY)
            draw_figures(GRAY)

    pygame.display.update()  
