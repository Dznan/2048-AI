from flask import Flask, render_template, jsonify, request
import os
import random
import json

app = Flask(__name__)

def ai_func(grid):
    """
    在这个函数中调用AI接口
    输入:
        grid: 2048矩阵
    返回:
        0 移动方向(U L D R)
    """

    # fake
    rndList = ["U", "L", "D", "R"]
    random.shuffle(rndList)
    return rndList[0]
    

@app.route("/")
def indexPage():
    return render_template("index.html")

@app.route("/api/nextstep", methods=["POST"])
def nextstepApi():
    grid = json.dumps(request.form['grid'])
    return jsonify({
        "action": ai_func(grid)
    })
    

if __name__ == '__main__':
    app.run(threaded=True, debug=True, host="0.0.0.0", port=8099)
