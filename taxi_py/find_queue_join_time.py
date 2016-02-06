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
    for yymm in ['0907','0904','1001','1002']:
        try:
            put_task(process_file, [yymm])
        except Exception as _:
            logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
            raise
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
#         
#     
#     for y in xrange(9, 11):
#         for m in xrange(1, 13):
#             try:
#                 put_task(process_file, ['%02d%02d' % (y, m)])
#             except Exception as _:
#                 logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
#                 raise
#             count_num_jobs += 1
#     end_multiprocessor(count_num_jobs)
    
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
        process_file('%02d%02d' % (9, 7))
    except Exception as _:
        logging_msg('Algorithm runtime exception (%02d%02d)\n' % (9, 2) + format_exc())
        raise

def process_file(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    # labels of trips
    l_did, l_st, l_et, l_tid, l_tm, l_fare = 'driver-id', 'start-time', 'end-time', 'trip-id', 'trip-mode', 'fare'
    # labels of logs
    l_lt, l_ap = 'time', 'ap-or-not'
    #
    processing_day = 1
    if yymm == '0901':
        pl_df = None
    elif yymm == '1001':
        pl_df = None
    elif yymm == '1010':
        pl_df = None
    else:
        yy, mm = int(yymm[:2]), int(yymm[2:])
        pre_yymm = '%02d%02d' % (yy, mm - 1)
        pt_prev_dir = '%s/%s' % (l_dir, pre_yymm)
        csvs= sorted([fn for fn in os.listdir(pt_prev_dir) if fn.endswith('.csv')])
        last_day_csv = csvs.pop()
        pl_df = pd.read_csv('%s/%s' % (pt_prev_dir, last_day_csv))
    cl_df = pd.read_csv('%s/%s/logs-%s%02d.csv' % (l_dir, yymm, yymm, processing_day))
    t_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, yymm))
    #
    pt_new_csv = '%s/queue-%s.csv' % (q_dir, yymm)
    with open(pt_new_csv, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['trip-id', 'start-time', 'end-time', 'driver-id', 'fare', 'trip-mode', 'join-queue-time']
        writer.writerow(header)
        
        # only consider trips which depart from the airport
        da_df = t_df.loc[(t_df[l_tm] != 3), l_tid]
        for _, tid in da_df.iteritems():
            target_trip = t_df.loc[(t_df[l_tid] == tid)].unstack()
            did = target_trip.get(l_did).iloc[0]
            t_st = target_trip.get(l_st).iloc[0]  # unit sec.
            t_et = target_trip.get(l_et).iloc[0]
            tm = target_trip.get(l_tm).iloc[0]
            fare = target_trip.get(l_fare).iloc[0]
            #
            dt_obj = datetime.fromtimestamp(t_st)
            if processing_day < dt_obj.day:
                processing_day += 1
                del pl_df
                pl_df = cl_df
                cl_df = pd.read_csv('%s/%s/logs-%s%02d.csv' % (l_dir, yymm, yymm, processing_day))
            logs = cl_df[(cl_df[l_did] == did) & (cl_df[l_lt] <= t_st) & (cl_df[l_ap] == 'X')]
            the_last_logging_time_out_ap = logs[l_lt].max()
            join_queue_time = None
            if not the_last_logging_time_out_ap == float('nan'):
                if not isinstance(pl_df, pd.DataFrame):
                    # This case is only for 0901 and the vehicle was located at the airport at first
                    join_queue_time = mktime(datetime(dt_obj.year, dt_obj.month, dt_obj.day).timetuple())
                else:
                    # The last log would be in data in the previous month
                    logs = pl_df[(pl_df[l_did] == did) & (pl_df[l_lt] <= t_st) & (pl_df[l_ap] == 0)]
                    join_queue_time = logs[l_lt].max()
            else:
                join_queue_time = the_last_logging_time_out_ap
            writer.writerow([tid, t_st, t_et, did, fare, tm, join_queue_time])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
#     run()
    single_run()
