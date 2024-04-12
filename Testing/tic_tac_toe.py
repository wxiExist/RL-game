import sys
import pygame

class TicTacToe:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 600, 600
        self.SIZE = 200
        self.MARGIN = (self.WIDTH - 3 * self.SIZE) // 2
        self.FONT_SIZE = 64
        self.FONT = pygame.font.SysFont("Arial", self.FONT_SIZE)

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)

        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.player = 'X'

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tic Tac Toe")

    def draw_board(self):
        for i in range(3):
            for j in range(3):
                x, y = self.MARGIN + j * self.SIZE, self.MARGIN + i * self.SIZE
                if self.board[i][j] == 'X':
                    pygame.draw.line(self.screen, self.RED, (x, y), (x + self.SIZE, y + self.SIZE), 15)
                    pygame.draw.line(self.screen, self.RED, (x, y + self.SIZE), (x + self.SIZE, y), 15)
                elif self.board[i][j] == 'O':
                    pygame.draw.circle(self.screen, self.BLUE, (x + self.SIZE // 2, y + self.SIZE // 2), self.SIZE // 2, 15)

        for i in range(1, 3):
            pygame.draw.line(self.screen, self.BLACK, (self.MARGIN + i * self.SIZE, self.MARGIN), (self.MARGIN + i * self.SIZE, self.MARGIN + 3 * self.SIZE), 5)
            pygame.draw.line(self.screen, self.BLACK, (self.MARGIN, self.MARGIN + i * self.SIZE), (self.MARGIN + 3 * self.SIZE, self.MARGIN + i * self.SIZE), 5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row = y // self.SIZE
                col = x // self.SIZE
                if self.board[row][col] == ' ':
                    self.mark_spot(row, col, self.player)
                    self.player = self.switch_player(self.player)

    def mark_spot(self, row, col, player):
        self.board[row][col] = player

    def switch_player(self, player):
        if player == 'O':
            return 'X'
        else:
            return 'O'

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def check_full(self):
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def run(self):
        while True:
            self.screen.fill(self.WHITE)
            self.draw_board()
            self.handle_events()
            if self.check_winner():
                self.player = self.switch_player(self.player)
                text = self.FONT.render(f"Player {self.player} wins!", True, self.RED)
                self.screen.blit(text, (self.MARGIN, self.HEIGHT - self.FONT_SIZE - self.MARGIN))
                pygame.display.flip()
                
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                            self.reset()
            elif self.check_full():
                text = self.FONT.render("It's a draw!", True, self.RED)
                self.screen.blit(text, (self.MARGIN, self.HEIGHT - self.FONT_SIZE - self.MARGIN))
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        #print("quit")
                        if event.type == pygame.QUIT:
                           # print("quit")
                            pygame.quit()
                            sys.exit()
                            self.reset()
            else:
                pygame.display.flip()
    
    def reset(self):
        print("123")
        self.run()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
