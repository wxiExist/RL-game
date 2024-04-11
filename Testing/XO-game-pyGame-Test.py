import sys
import pygame

# Initialize Pygame
pygame.init()

# Set up constants
WIDTH, HEIGHT = 600, 600
SIZE = 200
MARGIN = (WIDTH - 3 * SIZE) // 2
FONT_SIZE = 64
FONT = pygame.font.SysFont("Arial", FONT_SIZE)

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Set up player
player = 'X'

# Set up Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Function to draw board
def draw_board():
    for i in range(3):
        for j in range(3):
            x, y = MARGIN + j * SIZE, MARGIN + i * SIZE
            if board[i][j] == 'X':
                pygame.draw.line(screen, RED, (x, y), (x + SIZE, y + SIZE), 15)
                pygame.draw.line(screen, RED, (x, y + SIZE), (x + SIZE, y), 15)
            elif board[i][j] == 'O':
                pygame.draw.circle(screen, BLUE, (x + SIZE // 2, y + SIZE // 2), SIZE // 2, 15)

    # Draw black lines between fields
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (MARGIN + i * SIZE, MARGIN), (MARGIN + i * SIZE, MARGIN + 3 * SIZE), 5)
        pygame.draw.line(screen, BLACK, (MARGIN, MARGIN + i * SIZE), (MARGIN + 3 * SIZE, MARGIN + i * SIZE), 5)

# Function to handle events
def handle_events():
    global player  # Declare player as a global variable
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // SIZE
            col = x // SIZE
            if board[row][col] == ' ':
                mark_spot(row, col, player)
                player = switch_player(player)

# Function to mark spot on board
def mark_spot(row, col, player):
    board[row][col] = player

# Function to switch player
def switch_player(player):
    if player == 'O':
        return 'X'
    else:
        return 'O'

# Function to check if there is a winner
def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False

# Function to check if board is full
def check_full():
    for row in board:
        if ' ' in row:
            return False
    return True

# Game loop
while True:
    screen.fill(WHITE)
    draw_board()
    handle_events()
    if check_winner():
        player = switch_player(player)
        text = FONT.render(f"Player {player} wins!", True, RED)
        screen.blit(text, (MARGIN, HEIGHT - FONT_SIZE - MARGIN))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    elif check_full():
        text = FONT.render("It's a draw!", True, RED)
        screen.blit(text, (MARGIN, HEIGHT - FONT_SIZE - MARGIN))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    else:
        pygame.display.flip()