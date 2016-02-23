from __future__ import division
#
import os
#
prefix = '/home/sfcheng/toolbox'

cvs_files = [fn for fn in os.listdir(prefix) if fn.startswith('shift') and fn.endswith('.csv')]
for x in cvs_files:
    _,_,_, yymm = x[:-len('.csv')].split('-')
    
    print yymm, x 
