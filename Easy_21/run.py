from __future__ import division
from random import random, choice

BUST = 'BUST'

MANUALLY, Q_LEARNING, RAN = range(3)
EXPLORATION = True

EPSILON = 0.0001

def play_round(way_to_decision):
    # Initialize a game
    player_cards.append((BLACK, choice(CARDS_NUM))) 
    dealer_cards.append((BLACK, choice(CARDS_NUM)))
    rv_player = player_turn(way_to_decision)
    if rv_player != BUST:
        # the player did not go bust
        rv_dealer = dealer_turn()
        if rv_dealer == BUST:
            return WIN
        player_sum, dealer_sum = get_sum(player_cards), get_sum(dealer_cards)
        if player_sum == dealer_sum:
            return DRAW
        return WIN if player_sum > dealer_sum else LOSE
    else:
        return LOSE 

def player_turn(S_A, way_to_decision):
    while True:
        s1, s2
#         player_choice = way_to_decision()
        player_choice = S_A[(s1, s2)]
        if player_choice == HIT:
            player_cards.append(get_card())
            s = get_sum(player_cards) 
            if s > 21 or s < 1 :
                return BUST
        else:
            assert player_choice == STICK
            return STICK

def random_decision():
    pass
def q_learning_decision():
    if EXPLORATION:
        pass
    else:
        pass
    pass

def get_sum(cards):
    return sum([cn for cc, cn in cards if cc == BLACK]) - sum([cn for cc, cn in cards if cc == RED])
    
def display_current():
    # about dealer
    dealer_sum, dealer_current = 0, {'Black':[], 'Red':[]}
    for cc, cn in dealer_cards:
        if cc == BLACK:
            dealer_sum += cn
            dealer_current['Black'].append(cn)
        else:
            assert cc == RED
            dealer_sum -= cn
            dealer_current['Red'].append(cn)
    # about player
    player_sum, player_current = 0, {'Black':[], 'Red':[]}
    for cc, cn in player_cards:
        if cc == BLACK:
            player_sum += cn
            player_current['Black'].append(cn)
        else:
            assert cc == RED
            player_sum -= cn
            player_current['Red'].append(cn)
    print 'Player: Black cards %s, Red cards %s, Sum %d' % (str(player_current['Black']), str(player_current['Red']), player_sum)
    print 'Dealer: Black cards %s, Red cards %s, Sum %d' % (str(dealer_current['Black']), str(dealer_current['Red']), dealer_sum)

def reinforce_learning():
    # TODO
    # design reinforce_learning
    Qsa = {}
    Nsa = {}
    Csa = {}
    for i in xrange(20):
        # s1 means sum of player's cards
        s1 = i + 1
        for j in xrange(10):
            # s1 means the first card of dealer
            s2 = j + 1
            # about action
            # k=0  -> Hit, k=1  -> Stick
            Qsa[(s1, s2)] = [0, 0]
            Nsa[(s1, s2)] = 0
            Csa[(s1, s2)] = False
    #
    
    from time import time
    old_time = time()
    print old_time
    count = 0
    while True:
        s1, s2 = choice(PLAYER_STATES), choice(DEALER_STATES)
        if Csa[(s1, s2)]:
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
#         if abs(Qsa[(s1, s2)][0] - Qsa[(s1, s2)][1]) > 2 / 3:
#             Csa[(s1, s2)] = True
#         
#         for v in Csa.itervalues():
#             if not v:
#                 break
#         else:
#             break 
        
#         if np.std(Qsa[(s1, s2)] + prev_Q_value) != 0 and abs(Qsa[(s1, s2)][0] - prev_Q_value[0]) < EPSILON and abs(Qsa[(s1, s2)][1] - prev_Q_value[1]) < EPSILON:
#             break 
#         count += 1
        if count == 100000000000:
            break
    tmp_list = []
    for k, v in Qsa.iteritems():
        tmp_list.append([k, v])
    with open('temp_%d.txt' % (time()), 'w') as tf:
        for x in sorted(tmp_list):
            k, v = x
            s = 'S: %s, A: %s, %s' % (str(k), 'HIT' if v[0] >= v[1] else 'STICK', str(v))
            tf.write('%s\n' % s)
    print time() - old_time

def dealer_turn(dealer_cards):
    while True:
        s = get_sum(dealer_cards)
        if s > 21:
            return BUST
        elif s >= 17:
            return  STICK
        else:
            # HIT
            dealer_cards.append(get_card())

if __name__ == '__main__':
    
    reinforce_learning()
#     S_A=reinforce_learning()
#     S_A ={(s1,s2):HIT or STICK}
    assert False
    
    way_to_decision = manual_decision 
    if way_to_decision.__name__ == 'q_learning_decision':
        # Exploration
        # Run play round many times
        for _ in xrange(10000):
            rv = play_round(way_to_decision)
            reinforce_learning(rv)
        EXPLORATION = False
    num_of_WIN = 0
#     for x in range(10000)
#         rv = play_round(S_A, way_to_decision)
#         if rv == WIN:
#             num_of_WIN+=1
#     print num_of_WIN/10000 => 1
    
    print ''
    if rv == WIN:
        print 'The player wins'
    elif rv == DRAW:
        print 'Draw'
    else:
        assert rv == LOSE
        print 'The player lose'
    display_current()
