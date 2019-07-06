import sys
import numpy as np

from game2048env import Game2048Env


demo_state = np.array([
    [2, 2, 4, 0],
    [2, 2, 4, 0],
    [2, 2, 4, 0],
    [2, 2, 4, 0]
])


def main(argv):
    env = Game2048Env()
    env.init(state=demo_state)
    while not env.is_terminal():
        env.render()
        actions = env.action_space
        if env.turn == 'MOVE':
            print('Actions:')
            for i, a in enumerate(actions):
                print('{}: {}'.format(i, a), end='; ')
            print()
            pick = int(input('Input action id: '))
        else:
            pick = np.random.randint(len(actions))
        state, done, reward, info = env.step(actions[pick])


if __name__ == '__main__':
    main(sys.argv)
