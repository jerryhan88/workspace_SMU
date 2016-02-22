from __future__ import division

from support._setting import t_dir, tsdt_dir
import pandas as pd

import time, csv, os, shutil
import datetime

from support.logger import logging_msg

EPSILON = 0.00001

'''
    TODO
    consider boundary condition in case when trip start in a day but ended in the next day 
'''
if os.path.exists(tsdt_dir):
    shutil.rmtree(tsdt_dir)
os.makedirs(tsdt_dir)

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
            print 'handle the file; %s' % yymm 
            logging_msg('handle the file; %s' % yymm)
            fn = 'trips-%s.csv' % (yymm)
            pt_csv = '%s/%s' % (t_dir, fn)
            df = pd.read_csv(pt_csv)
            l_st = 'start-time'
            for x in xrange((datetime.date(next_y, next_m, 1) - datetime.date(cur_y, cur_m, 1)).days):
                cur_d = x + 1
                dd = '%02d' % cur_d
                cur_d_datetime = datetime.datetime(cur_y, cur_m, cur_d)
                next_d_datetime = cur_d_datetime + datetime.timedelta(days=1) 
                #
                tstemp_st = time.mktime(cur_d_datetime.timetuple())
                tstemp_et = time.mktime(next_d_datetime.timetuple()) - EPSILON
                #
                day_trips = df[(tstemp_st <= df[l_st]) & (df[l_st] <= tstemp_et)]
                day_trips['hh'] = 
                
                
                grouped = day_trips.groupby(['driver-id', 'trip-mode'], sort=True)
                tm_counting = grouped.size().to_frame('trip-mode-num')
                fare_sum = grouped.sum()['fare'].to_frame('fare-sum')
                fare_mean = grouped.mean()['fare'].to_frame('fare-mean')
                fare_std = grouped.std()['fare'].to_frame('fare-std')
                result = tm_counting.join(fare_sum, how='inner')
                result = result.join(fare_mean, how='inner')
                result = result.join(fare_std, how='inner')
                re_df = result.reset_index()
                re_df['yy'] = yy
                re_df['mm'] = mm
                re_df['dd'] = dd
                save_as_csv(yy, mm, re_df)
            print 'end the file; %s' % yymm
            logging_msg('end the file; %s' % yymm)

def save_as_csv(yy, mm, df):
    fn = '%s/driver-tm-%s.csv' % (tsdt_dir, yy + mm)
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvFile:
            writer = csv.writer(csvFile)
            header = ['yy', 'mm', 'dd', 'hh', 'trip-mode', 'trip-mode-num', 'fare-sum', 'fare-mean', 'fare-std']
            writer.writerow(header)
    with open(fn, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for _, row in df.iterrows():
            writer.writerow([row['yy'], row['mm'], row['dd'],
                             
                             # TODO
                             
                             row['driver-id'], row['trip-mode'], row['trip-mode-num'],
                             row['fare-sum'], row['fare-mean'], row['fare-std']])
    
if __name__ == '__main__':
    run()
