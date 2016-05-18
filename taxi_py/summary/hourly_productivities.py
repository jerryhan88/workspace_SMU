from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import airport_trips_dir
from supports.etc_functions import check_dir_create
from supports._setting import summary_dir
from supports._setting import CENT
from supports.handling_pkl import save_pickle_file
#
import pandas as pd
#
def run():
    check_dir_create(summary_dir)

    

if __name__ == '__main__':
    run()