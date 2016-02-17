from __future__ import division
#
from _setting import RED, BLACK
from _setting import STICK, HIT
from card_handling import get_card
#
player_cards, dealer_cards = [], []
Qsa = {}

def run(way_to_decision):
    # Initialize a game
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
    rv_player = player_turn(way_to_decision)
    while True:
        player_choice = way_to_decision()
        player_choice = S_A[(s1, s2)]
        if player_choice == HIT:
            player_cards.append(get_card())
            s = get_sum(player_cards) 
            if s > 21 or s < 1 :
                return BUST
        else:
            assert player_choice == STICK
            return STICK
    
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

def manual_decision():
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

def q_learning_decision():
    if not Qsa:
        pass
    
if __name__ == '__main__':
    run(manual_decision)