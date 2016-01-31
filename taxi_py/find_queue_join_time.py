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
    multi_process_run()
    

def multi_process_run():
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
    
def single_core_process_run():
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                process_file('%02d%02d' % (y, m))
            except Exception as _:
                logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
                raise
    
def single_run():
    if os.path.exists(q_dir):
        shutil.rmtree(q_dir)
    os.makedirs(q_dir)
    try:
        process_file('%02d%02d' % (9, 2))
    except Exception as _:
        logging_msg('Algorithm runtime exception (%02d%02d)\n' % (9, 2) + format_exc())
        raise

def process_file(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
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
        processing_day = 1
        if yymm == '0901':
            pl_df = None
        else:
            yy, mm = int(yymm[:2]), int(yymm[2:])
            prev_m = mm - 1
            if prev_m == 0:
                # 1001 month
                pre_yymm = '%02d%02d' % (yy - 1, 12)
            else:
                pre_yymm = '%02d%02d' % (yy, mm - 1)
            pt_prev_dir = '%s/%s' % (l_dir, pre_yymm)
            last_day_csv = [fn for fn in os.listdir(pt_prev_dir) if fn.endswith('.csv')].pop()
            pl_df = pd.read_csv('%s/%s' % (pt_prev_dir, last_day_csv))
        cl_df = pd.read_csv('%s/%s/logs-%s%02d.csv' % (l_dir, yymm, yymm, processing_day))
        # only consider trips which depart from the airport
        t_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, yymm))
        da_df = t_df.loc[(t_df[l_tm] == 0) | (t_df[l_tm] == 1), l_tid]
        for _, tid in da_df.iteritems():
            target_trip = t_df.loc[(t_df[l_tid] == tid)].unstack()
            did = target_trip.get(l_vid).iloc[0]
            t_st = target_trip.get(l_st).iloc[0]  # unit sec.
            tm = target_trip.get(l_tm).iloc[0]
            #
            dt_obj = datetime.fromtimestamp(t_st)
            if processing_day < dt_obj.day:
                processing_day += 1
                pl_df = cl_df
                cl_df = pd.read_csv('%s/%s/logs-%s%02d.csv' % (l_dir, yymm, yymm, processing_day))
            logs = cl_df[(cl_df[l_vid] == did) & (cl_df[l_lt] <= t_st) & (cl_df[l_ap] == 0)]
            the_last_logging_time_out_ap = logs[l_lt].max()
            join_queue_time = None
            if not the_last_logging_time_out_ap == float('nan'):
                if not isinstance(pl_df, pd.DataFrame):
                    # This case is only for 0901 and the vehicle was located at the airport at first
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
