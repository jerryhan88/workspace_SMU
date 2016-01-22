from __future__ import division
#
import os
from time import strftime
#
log_fn = 'log.txt'

if os.path.exists(log_fn):
    os.remove(log_fn)

with open(log_fn, 'w') as f:
    f.write(strftime("%a, %d %b %Y %H:%M:%S---") + 'Start logging' + '\n')

def logging_msg(msg):
    with open(log_fn, 'a') as f:
        f.write(strftime("%a, %d %b %Y %H:%M:%S---") + msg + '\n')
            
if __name__ == '__main__':
    logging_msg('test')