from __future__ import division
import os, sys
sys.path.append(os.getcwd()+'/..')
#
from support._setting import t_dir, tsht_dir
from support.logger import logging_msg

import time, csv, shutil, datetime
import pandas as pd

if os.path.exists(tsht_dir):
    shutil.rmtree(tsht_dir)
os.makedirs(tsht_dir)

def run():
    for yy in ['09', '10']:
        for mm in ['%02d' % x for x in xrange(1, 13)]:
            if yy + mm in ['0912', '1010']:
                continue
            cur_y, cur_m = int('20' + yy), int(mm)
            if mm == '12':
                next_y = cur_y + 1
                next_m = 1
            else:
                next_y = cur_y
                next_m = cur_m + 1
            yymm = yy + mm
            l_st = 'start-time'
            print 'handle the file; %s' % yymm
            logging_msg('handle the file; %s' % yymm)
            #
            fn = 'trips-%s.csv' % (yymm)
            pt_csv = '%s/%s' % (t_dir, fn)
            df = pd.read_csv(pt_csv)
            #
            
            for x in xrange((datetime.date(next_y, next_m, 1) - datetime.date(cur_y, cur_m, 1)).days):
                cur_d = x + 1
                for cur_h in xrange(24):
                    cur_period = datetime.datetime(cur_y, cur_m, cur_d, cur_h)
                    next_period = cur_period + datetime.timedelta(hours=1)
                    cur_timestamp, next_timestamp = time.mktime(cur_period.timetuple()), time.mktime(next_period.timetuple())
                    dd_hh_trips = df[(cur_timestamp <= df[l_st]) & (df[l_st] < next_timestamp)]
            
                    tm_grouped = dd_hh_trips.groupby(['trip-mode'], sort=True)
                    tm_counting = tm_grouped.size().to_frame('trip-mode-num')
                    fare_sum = tm_grouped.sum()['fare'].to_frame('fare-sum')
                    result = tm_counting.join(fare_sum, how='inner')
                    re_df = result.reset_index()
                    re_df['yy'] = cur_y
                    re_df['mm'] = cur_m
                    re_df['dd'] = cur_d
                    re_df['hh'] = cur_h
                    re_df['dow'] = cur_period.strftime("%a")
                    save_as_csv(yy, mm, re_df)
            print 'end the file; %s' % yymm
            logging_msg('end the file; %s' % yymm)

def save_as_csv(yy, mm, df):
    fn = '%s/hour-tm-%s.csv' % (tsht_dir, yy + mm)
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvFile:
            writer = csv.writer(csvFile)
            header = ['yy', 'mm', 'dd', 'dow', 'hh', 'trip-mode', 'trip-mode-num', 'fare-sum']
            writer.writerow(header)
    with open(fn, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for _, row in df.iterrows():
            writer.writerow([row['yy'], row['mm'], row['dd'], row['dow'], row['hh'], 
                             row['trip-mode'], row['trip-mode-num'], row['fare-sum']])
    
if __name__ == '__main__':
    run()
