from flask import Flask, render_template, jsonify, request
import os
import random
import json


app = Flask(__name__)


import numpy as np
from game2048env import Game2048Env
from minimax import MiniMaxPlayer


def eval_func(state):
    return np.sum(state) + len(state[state == 0]) * np.average(state)


def ai_func(grid):
    """
    在这个函数中调用AI接口
    输入:
        grid: 2048矩阵
    返回:
        0 移动方向(U L D R)
    """
    action_map = {
        'DOWN': 'D',
        'LEFT': 'L',
        'UP': 'U',
        'RIGHT': 'R',
    }
    env = Game2048Env(init_state=np.array(grid))
    player = MiniMaxPlayer(eval_func, max_depth=3)

    action = player.choose_action(env)
    print(action)

    # rndList = ["U", "L", "D", "R"]
    # random.shuffle(rndList)
    # return rndList[0]

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
