from __future__ import division
#
from Q_learning import reinforce_learning
from time import time

def run():
    old_time = time()
    Qsa = reinforce_learning()
    tmp_list = []
    for k, v in Qsa.iteritems():
        tmp_list.append([k, v])
    with open('temp_%d.txt' % (time()), 'w') as tf:
        for x in sorted(tmp_list):
            k, v = x
            s = 'S: %s, A: %s, %s' % (str(k), 'HIT' if v[0] >= v[1] else 'STICK', str(v))
            tf.write('%s\n' % s)
    print time() - old_time

if __name__ == '__main__':
    run()
    