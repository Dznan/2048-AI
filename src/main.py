import sys
import numpy as np

from game2048env import Game2048Env


state = np.array([
    [2, 2, 4, 0],
    [2, 2, 4, 0],
    [2, 2, 4, 0],
    [2, 2, 4, 0]
])


def main(argv):
    env = Game2048Env()
    env.init(state=state)
    # env.add_random_tile()
    # env.add_random_tile()
    # env.add_random_tile()
    print(env.state)
    print(env.do_right_action(env.state))
    print(env.do_left_action(env.state))
    print(env.do_up_action(env.state))
    print(env.do_down_action(env.state))
    print(env.action_space)

    env.step(env.action_space[0])

    print(env.state)
    print(env.action_space)

    env.step(env.action_space[0])

    print(env.state)
    print(env.do_right_action(env.state))
    print(env.do_left_action(env.state))
    print(env.do_up_action(env.state))
    print(env.do_down_action(env.state))
    print(env.action_space)


if __name__ == '__main__':
    main(sys.argv)
