import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np
import random


class FlipperEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, p=0.5, horizon=100):
        self.p = p
        self.horizon = horizon

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            np.array([-np.inf, 0]), np.array([np.inf, np.inf]), dtype=np.float32)

        self.reset()

    def step(self, action):
        if action == 0:
            if random.random() < self.p:
                self.x += 1
            else:
                self.x -= 1
        else:
            if random.random() < 0.5:
                self.x += 2
            else:
                self.x -= 2

        self.t -= 1

        if self.t == 0:
            reward = 1 if self.x > 0 else 0
            done = True
        else:
            reward = 0
            done = False

        return self._get_state(), reward, done, {}


    def reset(self):
        self.x = 0
        self.t = self.horizon
        return self._get_state()

    def _get_state(self):
        return np.array([self.x, self.t])

    def render(self, mode='human'):
        pass

    def close(self):
        pass
