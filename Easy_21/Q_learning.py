from __future__ import division
#
from random import choice
#
from _setting import PLAYER_STATES, DEALER_STATES, RED, BLACK
from _setting import WIN, DRAW, LOSE
from _setting import ALPHA, GAMMA
from _setting import CONVERGENCE_CONDITION 
from card_handling import get_card 

def reinforce_learning():
    Qsa, Csa = {}, {}
    for s1 in PLAYER_STATES:
        # s1 means sum of player's cards
        for s2 in DEALER_STATES:
            # s2 means the first card of dealer
            # about action
            # k=0  -> Hit, k=1  -> Stick
            Qsa[(s1, s2)] = [0, 0]
            Csa[(s1, s2)] = False
    while True:
        s1, s2 = choice(PLAYER_STATES), choice(DEALER_STATES)
        if Csa[(s1, s2)]:
            # if the state are converged at once, q-value will not be updated any more for speedy convergence
            continue
        for a in xrange(2):
            if a == 0:
                # HIT
                new_card = get_card()
                if new_card[0] == RED:
                    new_s1 = s1 - new_card[1]
                else:
                    assert new_card[0] == BLACK
                    new_s1 = s1 + new_card[1]
                if new_s1 < 1 or new_s1 > 21:
                    qrs = LOSE
                elif new_s1 == 21:
                    qrs = WIN
                else:
                    new_Q = []
                    for k, v in Qsa.iteritems():
                        _s1, _s2 = k 
                        if _s1 == new_s1:
                            new_Q += v
                    qrs = 0 + GAMMA * max(new_Q)
            elif a == 1:
                # STICK
                # Dealer's turn
                new_s2 = s2 
                while True:
                    if new_s2 < 1 or new_s2 > 21:
                        qrs = WIN
                        break
                    elif new_s2 >= 17:
                        if s1 == new_s2:
                            qrs = DRAW
                        elif s1 > new_s2:
                            qrs = WIN
                        else:
                            assert s1 < new_s2
                            qrs = LOSE
                        break
                    else:
                        # HIT
                        new_card = get_card()
                        if new_card[0] == RED:
                            new_s2 -= new_card[1]
                        else:
                            assert new_card[0] == BLACK
                            new_s2 += new_card[1]
            else:
                assert False
            Qsa[(s1, s2)][a] = (1 - ALPHA) * Qsa[(s1, s2)][a] + ALPHA * qrs
        # Check where the state is converged or not
        if abs(Qsa[(s1, s2)][0] - Qsa[(s1, s2)][1]) > CONVERGENCE_CONDITION:
            Csa[(s1, s2)] = True
        # If all states are converged, end reinforce learning         
        for v in Csa.itervalues():
            if not v:
                break
        else:
            break 
    return Qsa
    
if __name__ == '__main__':
    reinforce_learning()