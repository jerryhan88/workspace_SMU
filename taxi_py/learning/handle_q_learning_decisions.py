from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports.logger import logging_msg
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports._setting import IN_AP, OUT_AP
from supports._setting import DAY_OF_WEEK, TIME_SLOTS
from supports.etc_functions import get_all_files
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
HOUR = 60 * 60
MOD_STAN = 100000
#
def run():
    init_multiprocessor()
    counter = 0
    for i in xrange(1, 11): 
        ALPHA = i / 10 
        for j in xrange(1, 11):
            GAMMA = j / 10
            process_files(ALPHA, GAMMA)
#             put_task(process_files, [ALPHA, GAMMA])
            counter += 1
    end_multiprocessor(counter)

def process_files(ALPHA, GAMMA):
    ALPHA_GAMMA_dir = for_learning_dir + '/ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA)
    if not os.path.exists(ALPHA_GAMMA_dir):
        return None
    pickle_files = get_all_files(ALPHA_GAMMA_dir, 'ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA), '.pkl')
    for pkl_file in pickle_files:
        yymm = pkl_file[:-len('.pkl')].split('-')[-1]
        Qsa_value, state_action_fare_dur = load_picle_file('%s/%s' % (ALPHA_GAMMA_dir, pkl_file))
        #
        argmax_as = {}
        for s1 in DAY_OF_WEEK:
            for s2 in TIME_SLOTS:
                for s3 in [IN_AP, OUT_AP]:
                    argmax_as[(s1, s2, s3)] = IN_AP if Qsa_value[(s1, s2, s3, IN_AP)] >= Qsa_value[(s1, s2, s3, OUT_AP)] else OUT_AP
        #
        whole_rev, whole_count = 0, 0
        sub_rev, sub_count = 0, 0
        count = 0        
        with open('%s/whole-trip-%s.csv' % (for_learning_dir, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            id_prev_tetime, id_prev_teloc = headers.index('prev-trip-end-time'), headers.index('prev-trip-end-location')
            id_stime, id_sloc = headers.index('start-time'), headers.index('start-location'),
            id_dur, id_fare = headers.index('duration'), headers.index('fare')
            for row in reader:
                prev_tetime, stime = eval(row[id_prev_tetime]), eval(row[id_stime]) 
                setup_time = stime - prev_tetime
                #
                prev_tetime_datetime = datetime.datetime.fromtimestamp(prev_tetime)
                s1, s2 = prev_tetime_datetime.strftime("%a"), prev_tetime_datetime.hour
                s3 = row[id_prev_teloc]
                #
                a = row[id_sloc]
                #
                dur, fare = eval(row[id_dur]), eval(row[id_fare])
                alter_a = OUT_AP if a == IN_AP else IN_AP
                if state_action_fare_dur[(s1, s2, s3, alter_a)][1] == 0:
                    op_cost = 0
                else:
                    op_cost = (setup_time + dur) * state_action_fare_dur[(s1, s2, s3, alter_a)][0] / state_action_fare_dur[(s1, s2, s3, alter_a)][1] 
                economic_profit = fare - op_cost
                #
                whole_rev += economic_profit
                whole_count += 1
                if argmax_as[(s1, s2, s3)] == a:
                    sub_rev += economic_profit
                    sub_count += 1
                count += 1
                if count % MOD_STAN == 0:
                    print '%s, %d' % (yymm, count)
                    logging_msg('%s, %d' % (yymm, count))
                    save_pickle_file('%s/results-%s.pkl' % (ALPHA_GAMMA_dir, yymm), [whole_rev, whole_count, sub_rev, sub_count])
        save_pickle_file('%s/results-%s.pkl' % (ALPHA_GAMMA_dir, yymm), [whole_rev, whole_count, sub_rev, sub_count])
                
        
if __name__ == '__main__':
    run()