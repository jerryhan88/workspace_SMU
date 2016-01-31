from __future__ import division
#
from _setting import l_dir, t_dir, q_dir
#
import pandas as pd
from datetime import datetime
from time import mktime
import csv, os, shutil
from traceback import format_exc
#
from logger import logging_msg
from multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    if os.path.exists(q_dir):
        shutil.rmtree(q_dir)
    os.makedirs(q_dir)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                process_file('%02d%02d' % (y, m))
            except Exception as _:
                logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
                raise

def multi_process_run():
    if os.path.exists(q_dir):
        shutil.rmtree(q_dir)
    os.makedirs(q_dir)
    #
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                put_task(process_file, ['%02d%02d' % (y, m)])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    

def single_run():
    if os.path.exists(q_dir):
        shutil.rmtree(q_dir)
    os.makedirs(q_dir)
    process_file('%02d%02d' % (9, 1))

def process_file(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    if mm == 1:
        if yy == 9:
            prev_month = None
        else:
            prev_month = '0912'
    else:
        prev_month = '%02d%02d' % (yy, mm - 1)
    #
    pl_df = pd.read_csv('%s/logs-%s-normal.csv' % (l_dir, prev_month)) if prev_month else None        
    cl_df = pd.read_csv('%s/logs-%s-normal.csv' % (l_dir, yymm))
    t_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, yymm))
    # labels of trips
    l_vid, l_st, l_tid, l_tm = 'vehicle-id', 'start-time', 'trip-id', 'trip-mode'
    # labels of logs
    l_lt, l_ap = 'time', 'ap-or-not'
    #
    pt_new_csv = '%s/queue-%s.csv' % (q_dir, yymm)
    with open(pt_new_csv, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['trip-id', 'start-time', 'trip-mode', 'join-queue-time']
        writer.writerow(header)
        # only consider trips which depart from the airport
        da_df = t_df.loc[(t_df[l_tm] == 0) | (t_df[l_tm] == 1), l_tid]
        for _, tid in da_df.iteritems():
            target_trip = t_df.loc[(t_df[l_tid] == tid)].unstack()
            did = target_trip.get(l_vid).iloc[0]
            t_st = target_trip.get(l_st).iloc[0]  # unit sec.
            tm = target_trip.get(l_tm).iloc[0]
            # 
            logs = cl_df[(cl_df[l_vid] == did) & (cl_df[l_lt] <= t_st) & (cl_df[l_ap] == 0)]
            the_last_logging_time_out_ap = logs[l_lt].max()
            join_queue_time = None
            if not the_last_logging_time_out_ap == float('nan'):
                if not pl_df:
                    # This case is only for 0901 and the vehicle was located at the airport at first
                    dt_obj = datetime.fromtimestamp(t_st)
                    join_queue_time = mktime(datetime(dt_obj.year, dt_obj.month, dt_obj.day).timetuple())
                else:
                    # The last log would be in data in the previous month
                    logs = pl_df[(pl_df[l_vid] == did) & (pl_df[l_lt] <= t_st) & (pl_df[l_ap] == 0)]
                    join_queue_time = logs[l_lt].max()
            else:
                join_queue_time = the_last_logging_time_out_ap
            writer.writerow([tid, t_st, tm, join_queue_time])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
#     single_run()
