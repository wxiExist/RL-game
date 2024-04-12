import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from tic_tac_toe import TicTacToe 

class Agent:
    def __init__(self, input_dim, output_dim, hidden_dim, learning_rate):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dim = hidden_dim

        self.i2h = nn.Linear(input_dim + hidden_dim, hidden_dim)
        self.i2o = nn.Linear(input_dim + hidden_dim, output_dim)
        self.softmax = nn.Softmax(dim=1)

        self.hidden = np.zeros((1, hidden_dim))
        self.optimizer = optim.Adam(list(self.i2h.parameters()) + list(self.i2o.parameters()), lr=learning_rate)

    def forward(self, x):
        combined = torch.cat((x, torch.from_numpy(self.hidden).float()), 1)
        hidden = self.i2h(combined)
        hidden = nn.Tanh()(hidden)
        output = self.i2o(combined)
        output = self.softmax(output)
        self.hidden = hidden.detach().numpy()
        return output

    def train(agent, env, num_episodes):
        for episode in range(num_episodes):
            state = env.reset()
            done = False
            episode_reward = 0

            while not done:
                action = agent.get_action(state)
                next_state, reward, done, _ = env.step(action)
                agent.train(state, action, reward, next_state, done)
                state = next_state
                episode_reward += reward

            print(f"Episode {episode + 1}/{num_episodes}, reward: {episode_reward}")



def main():
    input_dim = 9
    output_dim = 3
    hidden_dim = 128
    learning_rate = 0.001

    agent = Agent(input_dim, output_dim, hidden_dim, learning_rate)
    env = TicTacToe()

    num_episodes = 10000
    print('123 0--ekf')
    Agent.train(agent, env, num_episodes)
    

if __name__ == '__main__':
    main()
