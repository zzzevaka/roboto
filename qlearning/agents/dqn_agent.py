import random
import logging
from collections import deque

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam



def mlp(n_obs, n_action, n_hidden_layer=10, n_neuron_per_layer=32, activation='relu', loss='mse'):
  """ A multi-layer perceptron """
  # import pdb; pdb.set_trace()
  model = Sequential()
  model.add(Dense(n_neuron_per_layer, input_dim=209, activation=activation))
  for _ in range(n_hidden_layer):
    model.add(Dense(n_neuron_per_layer, activation=activation))
  model.add(Dense(n_action, activation='linear'))
  model.compile(loss=loss, optimizer=Adam())
  print(model.summary())
  return model


class DQNAgent(object):
    def __init__(self, model, action_size, max_memory_len=2000):
        self.max_memory_len = max_memory_len
        self.memory = None
        self.gamma = 0.95  # discount rate
        self.epsilon = 1  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.action_size = action_size
        self.model = model

        self.flush_memory()

        self.model = model

        print(model.summary())

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        # act_values = self.model.predict(state.reshape(1,state.shape[0]))
        act_values = self.model.predict(np.array([state]))
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size=32):
        logging.debug('replay')
        minibatch = random.sample(self.memory, batch_size)

        states = np.array([tup[0] for tup in minibatch])
        actions = np.array([tup[1] for tup in minibatch])
        rewards = np.array([tup[2] for tup in minibatch])
        next_states = np.array([tup[3] for tup in minibatch])
        done = np.array([tup[4] for tup in minibatch])

        # Q(s', a)
        target = rewards + self.gamma * np.amax(self.model.predict(next_states), axis=1)
        # end state target is reward itself (no lookahead)
        target[done] = rewards[done]

        # Q(s, a)
        target_f = self.model.predict(states)
        # make the agent to approximately map the current state to future discounted reward
        target_f[range(batch_size), actions] = target

        self.model.fit(states, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
          self.epsilon *= self.epsilon_decay

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def flush_memory(self):
        self.memory = deque(maxlen=self.max_memory_len)

    def save(self, name):
        self.model.save_weights(name)
