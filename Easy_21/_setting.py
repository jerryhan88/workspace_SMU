from __future__ import division
from math import sqrt
BLACK, RED = range(2)
BLACK_PROB, RED_PROB = 2 / 3, 1 / 3
CARDS_NUM = range(1, 11)
#
STICK, HIT = range(2)
GAME_RESULT = WIN, DRAW, LOSE = 1, 0, -1
BUST = 'BUST'
#
PLAYER_STATES = range(1, 21)
DEALER_STATES = range(1, 11)
#
ALPHA, GAMMA = 0.1, 0.5
#
GR_dev_2 = [pow(v - sum(GAME_RESULT)/len(GAME_RESULT), 2) for v in GAME_RESULT]
CONVERGENCE_CONDITION = sqrt(sum(GR_dev_2)/len(GR_dev_2)) 
#
Q_LEARNING_DIR = 'Q_learning_results'