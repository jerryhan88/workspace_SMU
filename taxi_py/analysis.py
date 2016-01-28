from __future__ import division
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from _setting import prefix

def run():
    pt_csv = '%s/%s' %(prefix, 'all_trips.csv')
    trip_data = pd.read_csv(pt_csv)
    
    print list(trip_data.columns.values)
    
    pass

if __name__ == '__main__':
    run()