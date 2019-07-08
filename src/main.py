import sys
import numpy as np
from UI import *
from game2048env import Game2048Env
import pygame
from pygame.locals import *
import time


def main(argv):
    env = Game2048Env()
    env.init()
    
    pygame.init()
    screen = pygame.display.set_mode((PIXEL * SIZE, PIXEL * SIZE + SCORE_PIXEL))
    pygame.display.set_caption("2048")
    block = [pygame.Surface((PIXEL, PIXEL)) for i in range(4)]
    # 设置颜色
    block[0].fill((152, 251, 152))
    block[1].fill((240, 255, 255))
    block[2].fill((0, 255, 127))
    block[3].fill((225, 255, 255))
    score_block = pygame.Surface((PIXEL * SIZE, SCORE_PIXEL))
    score_block.fill((245, 245, 245))
    # 设置字体
    map_font = pygame.font.Font(None, PIXEL * 2 // 3)
    score_font = pygame.font.Font(None, SCORE_PIXEL * 2 // 3)
    clock = pygame.time.Clock()
    show(env, screen, block, map_font, score_font, score_block)

    while not env.is_terminal():
        clock.tick(2)
        env.render()
        actions = env.action_space
        if env.turn == 'MOVE':
            print('Actions:')
            for i, a in enumerate(actions):
                print('{}: {}'.format(i, a))
            pick = np.random.randint(0, len(actions)-1)
            # pick = int(input('Input action id: '))
        else:
            pick = np.random.randint(len(actions))
        state, done, reward, info = env.step(actions[pick])
        show(env, screen, block, map_font, score_font, score_block)


if __name__ == '__main__':
    main(sys.argv)
    time.sleep(5)
