from __future__ import division
#
from _setting import t_dir
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
#
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
from logger import logging_msg

def run():
    cvs_files = [fn for fn in os.listdir(t_dir) if fn.endswith('.csv')]
    init_multiprocessor()
    count_num_jobs = len(cvs_files)
    for fn in cvs_files:
        put_task(monthly_driver_income_trip_mode, [fn])
    end_multiprocessor(count_num_jobs)
    
def monthly_driver_income_trip_mode(fn):
    print 'handle the file; %s' % fn
    logging_msg('handle the file; %s' % fn)
    pt_csv = '%s/%s' % (t_dir, fn)
    df = pd.read_csv(pt_csv)
    a = df.groupby('driver-id', sort=True).sum()['fare'].to_frame('fare')
    b = df.groupby(['driver-id', 'trip-mode'], sort=True).size().to_frame('trip-mode-num')
    result = a.join(b, how='inner')
    pt_new_csv = '%s/summary-%s' % (t_dir, fn)
    result.reset_index().to_csv(pt_new_csv, index=False)
    print 'end the file; %s' % fn
    logging_msg('end the file; %s' % fn)
    
#     headers = list(df.columns.values)
#     print  df.iloc[:, headers.index('start-time')] 
    
    
#     df2 = df.loc[(df['start-time'] <= 1232405340)]
#     print df2.groupby('driver-id').sum()['fare']
    
#     print df.loc[(df['start-time'] <= 1232405340), ['fare', 'driver-id']]
#     
#     print df.loc[(df['start-time'] <= 1232405340)].groupby('driver-id').sum('fare')
    
#     df2.test == 'foo'
#     print df.loc[:, 'driver-id']
#     print df.groupby('driver-id').sum()['fare']   
if __name__ == '__main__':
    run()
