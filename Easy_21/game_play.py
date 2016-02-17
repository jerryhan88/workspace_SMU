from __future__ import division
#
import os, csv
#
from _setting import RED, BLACK
from _setting import STICK, HIT
from _setting import WIN, DRAW, LOSE
from _setting import BUST
from _setting import Q_LEARNING_DIR
from card_handling import get_card
#
Qsa = {}

get_sum = lambda cards: sum([cn for cc, cn in cards if cc == BLACK]) - sum([cn for cc, cn in cards if cc == RED])

DISPLAY= True
 
def play_round(way_to_decision):
    # Initialize a game
    player_cards, dealer_cards = [], []
    while True:
        new_card = get_card()
        if new_card[0] == RED:
            continue
        else:
            break
    player_cards.append(new_card)
    while True:
        new_card = get_card()
        if new_card[0] == RED:
            continue
        else:
            break 
    dealer_cards.append(new_card)
    #
    rv_player = None
    while True:
        if DISPLAY:
            print "Player's turn"
            display_current(player_cards, dealer_cards)
        player_choice = way_to_decision(player_cards, dealer_cards)
        if player_choice == HIT:
            nc = get_card()
            if DISPLAY:
                print 'New card is (%s, %d)' %('Red' if nc[0]==RED else 'Black', nc[1])
            player_cards.append(nc)
            s = get_sum(player_cards) 
            if s < 1  or s > 21:
                rv_player = BUST
                break
        else:
            assert player_choice == STICK
            rv_player = STICK
            break
    #
    if rv_player != BUST:
        # the player did not go bust
        rv_dealer = None
        while True:
            if DISPLAY:
                print "Dealer's turn"
                display_current(player_cards, dealer_cards)
            s = get_sum(dealer_cards)
            if s < 1  or s > 21:
                rv_dealer = BUST
                break
            elif s >= 17:
                rv_dealer = STICK
                break
            else:
                # HIT
                nc = get_card()
                if DISPLAY:
                    print 'New card is (%s, %d)' %('Red' if nc[0]==RED else 'Black', nc[1])
                dealer_cards.append(nc)
        if rv_dealer == BUST:
            return WIN
    player_sum, dealer_sum = get_sum(player_cards), get_sum(dealer_cards)
    if player_sum == dealer_sum:
        return DRAW
    return WIN if player_sum > dealer_sum else LOSE

def manual_decision(player_cards, dealer_cards):
    # In here, we need to suggest a Q-larning algorithm
    while True:
        player_choice = raw_input("Stick (%d) or Hit (%d):" % (STICK, HIT))
        try:
            rv = int(player_choice)
            if rv == HIT or rv == STICK :
                break
            else:
                print 'Please type the number 0 or 1'
        except ValueError:
            print 'Please type the number 0 or 1'
    return rv

def q_learning_decision(player_cards, dealer_cards):
    if not Qsa:
        # read all files
        cvs_files = [fn for fn in os.listdir(Q_LEARNING_DIR) if fn.endswith('.csv')]
        results = []
        for fn in cvs_files:
            temp_Qsa = {}
            with open('%s/%s'%(Q_LEARNING_DIR, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                for row in reader:
                    s1, s2, a = row
                    temp_Qsa[(s1, s2)] = a
            results.append(temp_Qsa)
        for k in results[0].iterkeys():
            num_HIT, num_STICK = 0,0
            for i in xrange(len(results)):
                v = results[i][k]
                if v == 'HIT':
                    num_HIT +=1
                else:
                    assert v == 'STICK'
                    num_STICK +=1
            Qsa[k] = HIT if num_HIT >= num_STICK else STICK
    else:
        s1, s2 = get_sum(player_cards), get_sum(dealer_cards)
        return Qsa[(s1, s2)]
    
def play_game_many_time(way_to_decision, num_game):
    result = []
    for _ in xrange(num_game):
        rv = play_round(way_to_decision)
        result.append(rv)
    print 'Wining rate is %.2f' % sum(rv for rv in result if rv == WIN) / len(result)

def display_current(player_cards, dealer_cards):
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
    
if __name__ == '__main__':
#     print play_round(manual_decision)
    play_game_many_time(q_learning_decision)
