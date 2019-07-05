import numpy as np
from copy import deepcopy


class Game2048Env:
    def __init__(self, init_state=None):
        self.state = init_state
        self.score = 0
    
    def init(self, state=None):
        if state is not None:
            self.state = state
        else:
            self.state = np.zeros((4, 4), dtype=np.int)
            for i in range(2):
                self.add_random_tile()
    
    def get_available_tiles(self):
        tiles = []
        view_state = self.state.reshape(-1)
        for i in range(len(view_state)):
            if view_state[i] == 0:
                tiles.append((i // 4, i % 4))
        return tiles

    def add_random_tile(self):
        tiles = self.get_available_tiles()
        pick = np.random.randint(len(tiles))
        self.add_tile(np.random.randint(1, 3) * 2, *tiles[pick])

    def add_tile(self, n, x, y):
        assert self.state[x, y] == 0
        self.state[x, y] = n

    @property
    def action_space(self):
        return None

    def step(self, action):
        return self.state

    def reset(self):
        self.init()
        return self.state
    
    def render(self):
        return None