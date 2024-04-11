import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

debug = False
iter = 0

class Game:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.player = 1

    def make_move(self, x, y):
        if self.board[x][y] == 0 and self.check_draw():
            self.board[x][y] = self.player

    def get_empty_cells(self):
        empty_cells = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def check_win(self, player):
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def check_draw(self):
        return all(all(cell != 0 for cell in row) for row in self.board)

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(9, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 9)

    def forward(self, x):
        x = x.view(1, -1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class Agent:
    def __init__(self):
        self.model = Model()
        self.optimizer = optim.Adam(self.model.parameters())
        self.game = Game()

    def train(self, batch_size, epochs):
        global iter
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        #device = torch.device("cuda:0")
        if device == "cuda":
            print("Model is training on GPU")
        if device == "cpu":
            print("cant find cuda device | WORK ON CPU!")
        print(device)
        self.model.to(device)

        for epoch in range(1, epochs + 1):
            states = []
            actions = []
            rewards = []
            dones = []
            total_loss = 0
            for _ in range(batch_size):
                game = Game()
                state = torch.tensor(game.board.reshape(-1), dtype=torch.float).to(device)
                while True:
                    if game.player == 1:
                        action = np.random.randint(0, 9)
                        if debug == True:
                            print("[debug] action was randomly select")
                    else:
                        logits = self.model(state)
                        action = torch.argmax(logits).item()
                    next_state, reward, done = self.step(game, action)
                    next_state = torch.tensor(next_state.reshape(-1), dtype=torch.float).to(device)
                    if debug == True:
                            print("[debug] NN was make some action")
                    states.append(state)
                    actions.append(action)
                    rewards.append(reward)
                    dones.append(done)
                    if debug == True:
                            print("[debug] NN take benefits BTW")
                    if done:
                        break
                    state = next_state
                    if debug == True:
                        print(f'[debug] ITREATION {iter}')
                        iter += 1
                states = torch.stack(states).to(device)
                actions = torch.tensor(actions).to(device)
                rewards = torch.tensor(rewards, dtype=torch.float).to(device)
                dones = torch.tensor(dones, dtype=torch.float).to(device)
                target_values = rewards + 0.9 * torch.max(self.model(states), dim=1)[0] * (1 - dones)
                loss = nn.MSELoss()(torch.gather(self.model(states), 1, actions.view(-1, 1)), target_values.view(-1, 1))
                total_loss += loss.item()
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                if debug == True:
                    print(f'[debug] ITREATION {iter}')
                    iter += 1
                avg_loss = total_loss / batch_size
                print(f"Epoch {epoch}/{epochs}, Average Loss: {avg_loss}")

    def step(self, game, action):
        x, y = divmod(action, 3)
        game.make_move(x, y)
        if game.check_win(game.player):
            reward = 1
        elif game.check_draw():
            reward = 0
        else:
            reward = -1
        next_state = game.board
        done = game.check_draw() or game.check_win(game.player)
        return next_state, reward, done

def play_game():
    game = Game()
    state = torch.tensor(game.board.reshape(-1), dtype=torch.float)
    while True:
        if game.player == 1:
            print("Player 1 turn")
            x = int(input("Enter x: "))
            y = int(input("Enter y: "))
            game.make_move(x, y)
            print_board(game.board)
            if game.check_win(1):
                print("Player 1 wins!")
                break
            if game.check_draw():
                print("Draw!")
                break
        else:
            print("Player 2 turn")
            logits = agent.model(state)
            action = torch.argmax(logits).item()
            x, y = divmod(action, 3)
            game.make_move(x, y)
            print_board(game.board)
            if game.check_win(2):
                print("Player 2 wins!")
                break
            if game.check_draw():
                print("Draw!")
                break
        game.player = 3 - game.player
        state = torch.tensor(game.board.reshape(-1), dtype=torch.float)

def print_board(board):
    for row in board:
        print(row)

if __name__ == "__main__":
    torch.cuda.is_available() 
    print(torch.cuda.is_available())
    agent = Agent()
    agent.train(batch_size=1000, epochs=1000)
    play_game()