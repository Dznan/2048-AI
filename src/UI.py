import random
import sys
import pygame
from pygame.locals import *


PIXEL = 150
SCORE_PIXEL = 100
SIZE = 4


# 更新屏幕
def show(game, screen, block, map_font, score_font, score_block):
    for i in range(SIZE):
        for j in range(SIZE):
            # 背景颜色块
            screen.blit(game.state[i,j] == 0 and block[(i + j) % 2] or block[2 + (i + j) % 2], (PIXEL * j, PIXEL * i))
            # 数值显示
            if game.state[i,j] != 0:
                map_text = map_font.render(str(game.state[i,j]), True, (106, 90, 205))
                text_rect = map_text.get_rect()
                text_rect.center = (PIXEL * j + PIXEL / 2, PIXEL * i + PIXEL / 2)
                screen.blit(map_text, text_rect)
    # 分数显示
    screen.blit(score_block, (0, PIXEL * SIZE))
    score_text = score_font.render((game.is_terminal() and "Game over with score " or "Score: ") + str(game.score), True, (106, 90, 205))
    score_rect = score_text.get_rect()
    score_rect.center = (PIXEL * SIZE / 2, PIXEL * SIZE + SCORE_PIXEL / 2)
    screen.blit(score_text, score_rect)
    pygame.display.update()
