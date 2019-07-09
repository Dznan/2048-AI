import numpy as np
from numba import jit


@jit(nopython=True)
def find_near_tile(state, x, y, d):
    if d == 0: # UP
        for i in range(x-1, -1, -1):
            if state[i][y] != 0:
                return state[i][y]
    if d == 1: # DOWN
        for i in range(x+1, 4):
            if state[i][y] != 0:
                return state[i][y]
    if d == 2: # RIGHT
        for i in range(y+1, 4):
            if state[x][i] != 0:
                return state[x][i]
    if d == 3: # UP
        for i in range(y-1, -1, -1):
            if state[x][i] != 0:
                return state[x][i]
    return 0


@jit(nopython=True)
def smoothness(state):
    s = 0.
    height, width = state.shape
    for i in range(height):
        for j in range(width):
            a = state[i][j]
            if a == 0:
                continue
            for d in range(4):
                b = find_near_tile(state, i, j, d)
                s -= np.abs(np.log2(a + 0.1) - np.log2(b + 0.1))
    return s


@jit(nopython=True)
def tonicity(state):
    t = 0
    a, b = 0, 0
    height, width = state.shape
    for i in range(height):
        for j in range(width):
            if state[i, j] == 0:
                continue
            c = state[i, j]
            n = find_near_tile(state, i, j, 2) # RIGHT
            if n != 0:
                if c > n:
                    a += np.log2(c + 0.1) - np.log2(n + 0.1)
                if n > c:
                    b += np.log2(n + 0.1) - np.log2(c + 0.1)
    t += max(a, b)
    a, b = 0, 0
    for j in range(width):
        for i in range(height):
            if state[i, j] == 0:
                continue
            c = state[i, j]
            n = find_near_tile(state, i, j, 1) # DOWN
            if n != 0:
                if c > n:
                    a += np.log2(c + 0.1) - np.log2(n + 0.1)
                if n > c:
                    b += np.log2(n + 0.1) - np.log2(c + 0.1)
    t += max(a, b)
    return t


def avg_dis(state):
    def dis(a, b):
        return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])
    s = {}
    d = 0.
    height, width = state.shape
    tiles = np.unique(state)
    tiles = np.sort(tiles)
    for tile in tiles:
        s[tile] = []
    for i in range(height):
        for j in range(width):
            s[state[i, j]].append((i, j))
    
    for k in range(len(tiles)):
        d_ = 0.
        for i in range(len(s[tiles[k]])):
            for j in range(i):
                d_ += dis(s[tiles[k]][i], s[tiles[k]][j])
        
        d += 2 * np.log2(tiles[k] + 1) * d_
        d_ = 0.
        if k > 0:
            for i in range(len(s[tiles[k]])):
                for j in range(len(s[tiles[k-1]])):
                    d_ += 0.3 * dis(s[tiles[k]][i], s[tiles[k-1]][j])
        
        d += np.log2(tiles[k-1] + 1) * d_
    return d


def get_greatest_exp_of_2(n):
    i = 2
    while i <= n:
        i <<= 1
    return i >> 1


def get_count(state):
    s = np.sum(state)
    c = 0
    res = {}
    while s > 0:
        n = get_greatest_exp_of_2(s)
        if n not in res:
            res[n] = 1
        else:
            res[n] += 1
        s -= n
        c += 1
    return res, c


@jit
def eval_func(env):
    max_tile = np.max(env.state)
    score = env.score
    tonic = tonicity(env.state)
    smooth = smoothness(env.state)
    # tiles = len(env.state[env.state != 0])
    empty_tiles = len(env.state[env.state == 0])
    # adis = avg_dis(env.state)
    # stat, c = get_count(env.state)
    return max_tile + 0.6 * smooth + tonic + 1.2 * np.log2(np.average(env.state)) * empty_tiles
