prefix = '/home/sfcheng/toolbox'

import os

cvs_files = [fn for fn in os.listdir(prefix) if fn.startswith('shift') and fn.endswith('.csv')]
for x in cvs_files:
    print x
