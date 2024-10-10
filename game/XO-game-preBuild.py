import pygame
import sys
from math import inf as infinity
from random import choice
import numpy as np

pygame.init()

# Константы
SCREEN_SIZE = (300, 300)
LINE_COLOR = (23, 145, 135)
BG_COLOR = (28, 170, 156)
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Глобальные переменные
board = np.zeros((BOARD_ROWS, BOARD_COLS))
player = 1  # 1 - Играет человек, -1 - играет компьютер

# Окно игры
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Крестики-нолики')
screen.fill(BG_COLOR)

def draw_lines():
    # Горизонтальные линии
    pygame.draw.line(screen, LINE_COLOR, (0, 100), (300, 100), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (300, 200), LINE_WIDTH)
    # Вертикальные линии
    pygame.draw.line(screen, LINE_COLOR, (100, 0), (100, 300), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 300), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * 100 + 100 / 2), int(row * 100 + 100 / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == -1:
                pygame.draw.line(screen, CROSS_COLOR, (col * 100 + SPACE, row * 100 + 100 - SPACE), (col * 100 + 100 - SPACE, row * 100 + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * 100 + SPACE, row * 100 + SPACE), (col * 100 + 100 - SPACE, row * 100 + 100 - SPACE), CROSS_WIDTH)

def check_win(player):
    for col in range(BOARD_COLS):
        if board[:, col].sum() == 3 * player:
            
            return True
    for row in range(BOARD_ROWS):
        if board[row, :].sum() == 3 * player:
            
            return True
    if board.trace() == 3 * player:
        
        return True
    if np.fliplr(board).trace() == 3 * player:
        return True
    return False

def check_draw():
    return np.all(board != 0)

def empty_cells():
    return [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] == 0]

def minimax(state, depth, player):
    if player == 1:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or check_win(-1) or check_win(1):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells():
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == 1:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def evaluate(state):
    if check_win(1):
        score = +1
    elif check_win(-1):
        score = -1
    else:
        score = 0
    return score

def ai_turn():
    depth = len(empty_cells())
    if depth == 0 or check_win(1) or check_win(-1):
        return

    move = minimax(board, depth, -1)
    row, col = move[0], move[1]
    board[row][col] = -1

def player_move(row, col):
    board[row][col] = 1

draw_lines()

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not check_win(player) and not check_win(-player):
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y
            clicked_row = int(mouseY // 100)
            clicked_col = int(mouseX // 100)

            if board[clicked_row][clicked_col] == 0:
                player_move(clicked_row, clicked_col)
                if check_draw():
                    running = False
                    print('draw')
                ai_turn()
        draw_figures()
        pygame.display.update()

    if check_win(1) or check_win(-1) or check_draw():
        running = False

#pygame.quit()