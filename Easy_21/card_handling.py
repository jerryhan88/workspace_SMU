from __future__ import division
from random import random, choice
from _setting import RED, RED_PROB, BLACK, CARDS_NUM

def get_card():
    # cc: card's color
    # cn: card's number
    cc = RED if random() <= RED_PROB else BLACK 
    cn = choice(CARDS_NUM)
    return cc, cn