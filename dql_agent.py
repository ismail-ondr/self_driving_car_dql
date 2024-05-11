from collections import deque
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random


class DQLAgent:
    def __init__(self, env, model_path=""):
        # parameter / hyperparameter
        self.env = env
        self.state_size = len(env.get_observation_space())
        self.action_size = len(env.get_action_space())

        self.gamma = 0.95
        self.learning_rate = 0.001

        self.epsilon = 1  # explore
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.memory = deque([], maxlen=10000)
        self.model = self.build_model()
        self.model_path = model_path

        if not self.model_path == "":
            self.model.load_state_dict(torch.load(self.model_path))
            self.model.eval()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(self.device)

        self.criterion = nn.MSELoss()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.learning_rate)

    def build_model(self):
        # neural network for deep q learning

        model = nn.Sequential(
            nn.Linear(self.state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, self.action_size)
        )
        model.cuda()
        return model

    def remember(self, state, action, reward, next_state, done):
        # storage
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # acting: explore or exploit
        if random.uniform(0, 1) <= self.epsilon and self.model_path == "":
            return random.choice(self.env.action_space)
        else:
            state_tensors = torch.tensor(np.array(state), dtype=torch.float32, device=self.device)
            q_values = self.model(state_tensors)
            a = torch.argmax(q_values).item()
            return a

    def replay(self, batch_size):
        # training
        if len(self.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:

            state_tensor = torch.tensor(np.array(state), dtype=torch.float32, device=self.device)
            next_state_tensor = torch.tensor(next_state, dtype=torch.float32, device=self.device)

            if done:
                target = reward
            else:
                next_q_values = self.model(next_state_tensor)
                target = reward + self.gamma * torch.max(next_q_values).item()

            target_f = self.model(state_tensor)
            target_f[action] = target

            self.optimizer.zero_grad()
            loss = self.criterion(self.model(state_tensor), target_f)
            loss.backward()
            self.optimizer.step()

    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
