import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtCore import Qt

class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = "X"

        self.layout = QGridLayout()

        for i in range(3):
            for j in range(3):
                button = QPushButton('')
                button.clicked.connect(lambda ch, r=i, c=j: self.make_move(r, c))
                self.layout.addWidget(button, i, j)

        self.setLayout(self.layout)

        self.setWindowTitle('Tic Tac Toe')
        self.show()

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.display_board()
            if self.check_win():
                self.game_over()
                self.disable_buttons()
            self.current_player = "O" if self.current_player == "X" else "X"

    def display_board(self):
        for i in range(3):
            for j in range(3):
                button = self.layout.itemAtPosition(i, j).widget()
                button.setText(self.board[i][j])

    def check_win(self):
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

    def game_over(self):
        winner_label = QLabel(f"Player {self.current_player} wins!")
        winner_label.setAlignment(Qt.AlignCenter)
        
        self.layout.addWidget(winner_label, 3, 0, 1, 3)
        self.setLayout(self.layout)

    def disable_buttons(self):
        for i in range(3):
            for j in range(3):
                button = self.layout.itemAtPosition(i, j).widget()
                button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TicTacToe()
    sys.exit(app.exec_())