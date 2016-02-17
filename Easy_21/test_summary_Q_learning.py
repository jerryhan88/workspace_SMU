from __future__ import division
#
import os
from Q_learning import reinforce_learning
from time import time
from _setting import Q_LEARNING_DIR
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

if __name__ == '__main__':
    run()
    