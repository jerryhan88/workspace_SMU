from __future__ import division
#
import os, csv
from Q_learning import reinforce_learning
from time import time
from _setting import Q_LEARNING_DIR, SUMMARY_FNAME
from _setting import HIT, STICK
from multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    if not os.path.exists(Q_LEARNING_DIR):
        os.makedirs(Q_LEARNING_DIR)
    init_multiprocessor()
    num = 20
    for _ in xrange(num):
        put_task(get_q_learning_result, [])
    end_multiprocessor(num)

def get_q_learning_result():
    old_time = time()
    Qsa = reinforce_learning()
    tmp_list = []
    for k, v in Qsa.iteritems():
        tmp_list.append([k, v])
    with open('%s/q_result_%d.csv' % (Q_LEARNING_DIR, time()), 'w') as tf:
        for x in sorted(tmp_list):
            k, v = x
            s = '%s,%s,%s' % (str(k[0]), str(k[1]), 'HIT' if v[0] >= v[1] else 'STICK')
            tf.write('%s\n' % s)
    print time() - old_time

def summary():
    # read all files
    cvs_files = [fn for fn in os.listdir(Q_LEARNING_DIR) if fn.endswith('.csv')]
    results = []
    for fn in cvs_files:
        temp_Qsa = {}
        with open('%s/%s' % (Q_LEARNING_DIR, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            for row in reader:
                s1, s2, a = row
                temp_Qsa[(s1, s2)] = a
        results.append(temp_Qsa)
        
    with open(SUMMARY_FNAME, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        temp_list = []
        for k in results[0].iterkeys():
            num_HIT, num_STICK = 0, 0
            for i in xrange(len(results)):
                v = results[i][k]
                if v == 'HIT':
                    num_HIT += 1
                else:
                    assert v == 'STICK'
                    num_STICK += 1
            temp_list.append([eval(k[0]), eval(k[1]), HIT if num_HIT >= num_STICK else STICK])
        for r in sorted(temp_list):
            writer.writerow(r)

if __name__ == '__main__':
#     run()
    summary()
    
