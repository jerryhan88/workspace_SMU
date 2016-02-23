prefix = '/home/sfcheng/toolbox'

import os

cvs_files = [fn for fn in os.listdir(prefix) if fn.endswith('.csv')]
for x in cvs_files:
    print x
