from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import IN_AIRPORT, OUT_AIRPORT
from supports._setting import DAY_OF_WEEK, TIME_SLOTS
from supports._setting import for_learning_dir
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports.logger import logging_msg
#
import csv, datetime
#
MOD_STAN = 100000
HOUR = 60 * 60
ALPHA = 0.4
GAMMA = 0.2
#
def run():
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    if yymm == '0901':
        prev_yymm = None
    elif yymm == '1001':
        prev_yymm = '0911'
    elif yymm == '1011':
        prev_yymm = '1009'
    else:
        yy, mm = int(yymm[:2]), int(yymm[2:]) 
        prev_yymm = '%02d%02d' % (yy, mm - 1)
    #
    if not prev_yymm:
        Qsa_value, state_prodSum_num = {}, {}
        locations = [IN_AIRPORT, OUT_AIRPORT]
        actions = [IN_AIRPORT, OUT_AIRPORT]
        for s1 in DAY_OF_WEEK:
            for s2 in TIME_SLOTS:
                for s3 in locations:
                    state_prodSum_num[(s1, s2, s3)] = [0, 0]
                    for a in actions:
                        Qsa_value[(s1, s2, s3, a)] = 0
    else:
        Qsa_value, state_prodSum_num = load_picle_file('%s/q-value-prods-%s.pkl' % (for_learning_dir, prev_yymm))
    #
    count = 0
    with open('%s/trip-for-learning-%s.csv' % (for_learning_dir, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        _, id_dow, id_hh = headers.index('start-time'), headers.index('day-of-week'), headers.index('hh')
        id_tm = headers.index('trip-mode')
        id_prev_tet = headers.index('prev-trip-end-time')
        id_setup_time = headers.index('setup-time')
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        for row in reader:
            setup_time = eval(row[id_setup_time])
            if setup_time < 0 or setup_time > HOUR / 2:
                continue
            #
            prev_datetime = datetime.datetime.fromtimestamp(eval(row[id_prev_tet])) 
            s1, s2 = prev_datetime.strftime("%a"), prev_datetime.hour
            s1_new, s2_new = row[id_dow], eval(row[id_hh])
            #
            tm = eval(row[id_tm])
            #
            if tm == DInAP_PInAP:
                s3, a, s3_new = IN_AIRPORT, IN_AIRPORT, IN_AIRPORT
            elif tm == DInAP_POutAP:
                s3, a, s3_new = IN_AIRPORT, OUT_AIRPORT, OUT_AIRPORT
            elif tm == DOutAP_PInAP:
                s3, a, s3_new = OUT_AIRPORT, IN_AIRPORT, IN_AIRPORT
            elif tm == DOutAP_POutAP:
                s3, a, s3_new = OUT_AIRPORT, OUT_AIRPORT, OUT_AIRPORT
            else:
                assert False    
            #
            fare, dur = eval(row[id_fare]), eval(row[id_dur])
            prod = fare / dur
            if tm == DInAP_PInAP or tm == DOutAP_PInAP:
                state_prodSum_num[(s1_new, s2_new, IN_AIRPORT)][0] += prod
                state_prodSum_num[(s1_new, s2_new, IN_AIRPORT)][1] += 1
            else:
                state_prodSum_num[(s1_new, s2_new, OUT_AIRPORT)][0] += prod
                state_prodSum_num[(s1_new, s2_new, OUT_AIRPORT)][1] += 1
            #
#             if tm == DInAP_PInAP or tm == DOutAP_POutAP:
#                 setup_cost = 0
            if tm == DInAP_PInAP or tm == DInAP_POutAP:
                if state_prodSum_num[(s1, s2, IN_AIRPORT)][1] == 0:
                    setup_cost = 0
                else:
                    setup_cost = setup_time * state_prodSum_num[(s1, s2, IN_AIRPORT)][0] / state_prodSum_num[(s1, s2, IN_AIRPORT)][1]
            elif tm == DOutAP_POutAP or tm == DOutAP_PInAP:
                if state_prodSum_num[(s1, s2, OUT_AIRPORT)][1] ==0:
                    setup_cost = 0
                else:
                    setup_cost = setup_time * state_prodSum_num[(s1, s2, OUT_AIRPORT)][0] / state_prodSum_num[(s1, s2, OUT_AIRPORT)][1]
            else:
                assert False
            #
            if Qsa_value[(s1_new, s2_new, s3_new, IN_AIRPORT)] > Qsa_value[(s1_new, s2_new, s3_new, OUT_AIRPORT)] :
                future_q_value = Qsa_value[(s1_new, s2_new, s3_new, IN_AIRPORT)]
            else:
                future_q_value = Qsa_value[(s1_new, s2_new, s3_new, OUT_AIRPORT)]
            #
            qrs = fare - setup_cost + GAMMA * future_q_value
            Qsa_value[(s1, s2, s3, a)] = \
                        (1 - ALPHA) * Qsa_value[(s1, s2, s3, a)] + ALPHA * qrs
            count += 1
            if count % MOD_STAN == 0:
                print '%s, %d' % (yymm, count)
                logging_msg('%s, %d' % (yymm, count))
                save_pickle_file('%s/q-value-prods-%s.pkl' % (for_learning_dir, yymm), [Qsa_value, state_prodSum_num])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
