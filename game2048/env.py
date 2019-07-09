import numpy as np
from copy import deepcopy
from numba import jit


@jit(nopython=True)
def do_right_action(state):
    reward = 0
    height, width = state.shape
    new_state = state.copy()
    for i in range(height):
        #move part
        for j in range(width - 1, -1, -1):
            if new_state[i, j] == 0:
                for k in range(j - 1, -1, -1):
                    if new_state[i, k] != 0:
                        new_state[i, j] = new_state[i, k]
                        new_state[i, k] = 0
                        break
        #merge part
        for j in range(width-1, 0, -1):
            if new_state[i, j] == 0:continue
            if  new_state[i, j] == new_state[i, j-1]:
                new_state[i, j] <<= 1
                new_state[i, j-1] = 0
                reward += new_state[i, j]
        #move part
        for j in range(width - 1, 0, -1):
            if new_state[i, j] == 0:
                for k in range(j - 1, -1, -1):
                    if new_state[i, k] != 0:
                        new_state[i, j] = new_state[i, k]
                        new_state[i, k] = 0
                        break 
    return new_state, reward


@jit(nopython=True)
def do_left_action(state):
    reward = 0
    height, width = state.shape
    new_state = state.copy()
    for i in range(height):
        for j in range(width):
            if new_state[i, j] == 0:
                for k in range(j+1, width):
                    if new_state[i, k] != 0:
                        new_state[i, j] = new_state[i, k]
                        new_state[i, k] = 0
                        break
        #merge part
        for j in range(width-1):
            if new_state[i, j] == 0:continue
            if  new_state[i, j] == new_state[i, j+1]:
                new_state[i, j] <<= 1
                new_state[i, j+1] = 0
                reward += new_state[i, j]
        for j in range(width):
            if new_state[i, j] == 0:
                for k in range(j+1, width):
                    if new_state[i, k] != 0:
                        new_state[i, j] = new_state[i, k]
                        new_state[i, k] = 0
                        break
    return new_state, reward


@jit(nopython=True)
def do_up_action(state):
    reward = 0
    height, width = state.shape
    new_state = state.copy()
    for j in range(width):
        for i in range(height):
            if new_state[i, j] == 0:
                for k in range(i+1, height):
                    if new_state[k, j] != 0:
                        new_state[i, j] = new_state[k, j]
                        new_state[k, j] = 0
                        break
        #merge part
        for i in range(height-1):
            if new_state[i, j] == 0:continue
            if  new_state[i, j] == new_state[i+1, j]:
                new_state[i, j] <<= 1
                new_state[i+1, j] = 0
                reward += new_state[i, j]
        for i in range(height):
            if new_state[i, j] == 0:
                for k in range(i+1, height):
                    if new_state[k, j] != 0:
                        new_state[i, j] = new_state[k, j]
                        new_state[k, j] = 0
                        break
    return new_state, reward


@jit(nopython=True)
def do_down_action(state):
    reward = 0
    height, width = state.shape
    new_state = state.copy()
    for j in range(width):
        for i in range(height - 1, -1, -1):
            if new_state[i, j] == 0:
                for k in range(i - 1, -1, -1):
                    if new_state[k, j] != 0:
                        new_state[i, j] = new_state[k, j]
                        new_state[k, j] = 0
                        break
        #merge part
        for i in range(height-1, 0, -1):
            if new_state[i, j] == 0:continue
            if  new_state[i, j] == new_state[i-1, j]:
                new_state[i, j] <<= 1
                new_state[i-1, j] = 0
                reward += new_state[i, j]
        for i in range(height - 1, -1, -1):
            if new_state[i, j] == 0:
                for k in range(i - 1, -1, -1):
                    if new_state[k, j] != 0:
                        new_state[i, j] = new_state[k, j]
                        new_state[k, j] = 0
                        break
    return new_state, reward


@jit(nopython=True)
def do_action(state, direction):
    if direction == 'RIGHT':
        return do_right_action(state)
    if direction == 'LEFT':
        return do_left_action(state)
    if direction == 'UP':
        return do_up_action(state)
    if direction == 'DOWN':
        return do_down_action(state)


class Game2048Env:
    def __init__(self, init_state=np.array([], dtype=np.int32)):
        self.score = 0
        self.state = init_state
        self.turn = 'MOVE'
    
    def init(self, state=np.array([], dtype=np.int32)):
        self.score = 0
        self.turn = 'MOVE'
        if np.all(state != 0):
            self.state = state
        else:
            self.state = np.zeros((4, 4), dtype=np.int)
            for i in range(2):
                self.add_random_tile()
        
        return self.state

    def get_available_tiles(self):
        tiles = []
        view_state = self.state.reshape(-1)
        for i in range(len(view_state)):
            if view_state[i] == 0:
                tiles.append((i // 4, i % 4))
        return tiles

    def add_random_tile(self):
        tiles = self.get_available_tiles()
        assert len(tiles) > 0
        pick = np.random.randint(len(tiles))
        self.add_tile(np.random.randint(1, 3) * 2, *tiles[pick])

    def add_tile(self, n, x, y):
        assert self.state[x, y] == 0
        self.state[x, y] = n

    def copy(self):
        return deepcopy(self)

    @property
    def successors(self):
        envs = []
        actions = self.action_space
        for action in actions:
            env = deepcopy(self)
            env.step(action)
            envs.append(env)
        return envs

    @property
    def action_space(self):
        actions = []
        if self.turn == 'MOVE':
            for d in ['RIGHT', 'LEFT', 'UP', 'DOWN']:
                new_state, _ = do_action(self.state, d)
                if np.any(new_state != self.state):
                    actions.append(d)
        elif self.turn == 'ADD_TILE':
            tiles = self.get_available_tiles()
            for tile in tiles:
                actions.append((2, tile))
                actions.append((4, tile))
        return actions
    
    def is_terminal(self):
        actions = self.action_space
        if len(actions) == 0:
            return True
        return False

    def step(self, action):
        reward = 0
        info = {}
        if self.turn == 'MOVE':
            self.state, reward = do_action(self.state, action)
            self.score += reward
            self.turn = 'ADD_TILE'
        elif self.turn == 'ADD_TILE':
            n, tile = action
            self.add_tile(n, *tile)
            self.turn = 'MOVE'
        done = self.is_terminal()
        info['score'] = self.score
        return self.state, done, reward, info

    def reset(self):
        self.init()
        return self.state
    
    def render(self):
        print('--------------------------------')
        print('score:', self.score)
        print(self.state)
        print('--------------------------------')
