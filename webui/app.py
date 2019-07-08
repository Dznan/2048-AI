#! /usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import os
import random
import json


app = Flask(__name__)


import numpy as np
from game2048env import Game2048Env
from minimax import MiniMaxPlayer


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

        if k > 0:
            for i in range(len(s[tiles[k]])):
                for j in range(len(s[tiles[k-1]])):
                    d_ += dis(s[tiles[k]][i], s[tiles[k-1]][j])
        
        d += np.log2(tiles[k] + 1) * d_
    return d


def eval_func(env):
    max_tile = np.max(env.state)
    score = env.score
    empty_tiles = len(env.state[env.state == 0])
    adis = avg_dis(env.state)
    return max_tile + 0.5 * score + empty_tiles * np.average(env.state) - 0.5 * adis


action_map = {
    'DOWN': 'D',
    'LEFT': 'L',
    'UP': 'U',
    'RIGHT': 'R',
}


def ai_func(grid):
    """
    在这个函数中调用AI接口
    输入:
        grid: 2048矩阵
    返回:
        0 移动方向(U L D R)
    """

    env = Game2048Env(init_state=np.array(grid))
    player = MiniMaxPlayer(eval_func, max_depth=5, max_child=4)

    action = player.choose_action(env)
    print(action)

    return action_map[action]
    

@app.route("/")
def indexPage():
    return render_template("index.html")


@app.route("/api/nextstep", methods=["POST"])
def nextstepApi():
    grid = json.loads(request.form['grid'])
    return jsonify({
        "action": ai_func(grid)
    })
    

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host="0.0.0.0", port=8099)
