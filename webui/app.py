#! /usr/bin/env python3
from flask import Flask, render_template, jsonify, request
import sys
import os
import random
import json


app = Flask(__name__)

filepath = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.abspath(filepath + '/../'))

import numpy as np
from game2048 import Game2048Env, MiniMaxPlayer, eval_func


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
