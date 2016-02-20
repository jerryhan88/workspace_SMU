from __future__ import division
from _setting import t_dir, s_dir, q_dir, wf_dir
from _setting import DInAP_PInAP, DOutAP_PInAP
#
import os, shutil, csv, datetime, time
import pandas as pd
from traceback import format_exc
#
from logger import logging_msg
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
SEC = 60

def run():
    if os.path.exists(wf_dir):
        shutil.rmtree(wf_dir)
    os.makedirs(wf_dir)
    #
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(2, 13):
            try:
                yymm = '%02d%02d' % (y, m) 
                if yymm in ['0912', '1010']:
                    continue
                put_task(process_a_month, [yymm])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_a_month(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    yy, mm = int(yymm[:2]), int(yymm[2:])
    if yymm == '0901':
        prev_yymm = None
    elif yymm == '1001':
        prev_yymm = None
    elif yymm == '1011':
        prev_yymm = None
    else:
        prev_yymm = '%02d%02d' % (yy, mm - 1)
    l_did = 'driver-id'
    s_df = pd.read_csv('%s/shift-%s.csv' % (s_dir, yymm))
    ct_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, yymm))
    cq_df = pd.read_csv('%s/queue-%s.csv' % (q_dir, yymm))
    #
    s_df = s_df[(s_df[l_did] != -1)]
    ct_df = ct_df[(ct_df[l_did] != -1)]
    cq_df = cq_df[(cq_df[l_did] != -1)]
    #
    cq_df = cq_df[(cq_df['trip-mode'] == DInAP_PInAP) | (cq_df['trip-mode'] == DOutAP_PInAP)]
    if prev_yymm:
        pt_df = pd.read_csv('%s/trips-%s.csv' % (t_dir, prev_yymm))
        pq_df = pd.read_csv('%s/queue-%s.csv' % (q_dir, prev_yymm))
        #
        pt_df = pt_df[(pt_df[l_did] != -1)]
        pq_df = pq_df[(pq_df[l_did] != -1)]
        #
        pq_df = pq_df[(pq_df['trip-mode'] == DInAP_PInAP) | (pq_df['trip-mode'] == DOutAP_PInAP)]
    #
    pt_op_csv = '%s/wt_and_fare-%s.csv' % (wf_dir, yymm)
    with open(pt_op_csv, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'dow', 'hh', 'total-duration', 'ap-duration', 'total-fare', 'ap-fare', 'op-cost-sec', 'op-cost-min']
        writer.writerow(header)
        #
        groupbed_s_dh = s_df.groupby(['day', 'hour'])
        dh_duration_df = groupbed_s_dh.sum()['duration'].to_frame('total-duration-min').reset_index()       
        #
        y, m = int('20' + yymm[:2]), int(yymm[2:])
        for _, (dd, hh, total_duration) in dh_duration_df.iterrows():
            cur_period = datetime.datetime(y, m, dd, hh)
            prev_period = cur_period - datetime.timedelta(hours=1)
            next_period = cur_period + datetime.timedelta(hours=1)
            prev_timestamp, cur_timestamp, next_timestamp = \
            time.mktime(prev_period.timetuple()), time.mktime(cur_period.timetuple()), time.mktime(next_period.timetuple())
            # pp => previous period
            pp_total_fare, pp_ap_fare = 0, 0
            pp_ap_queue_trip_time = 0
            pp_t_df, pp_q_df = None, None
            if hh == 0:
                if prev_yymm:
                    pp_t_df, pp_q_df = pt_df, pq_df
            else:
                assert hh > 0
                pp_t_df, pp_q_df = ct_df, cq_df        
            if type(pp_t_df) == type(pd.DataFrame) and pp_q_df == type(pd.DataFrame):
                pp_total_fare += get_fare_in_period('start-time', 'end-time', \
                                                  prev_timestamp, cur_timestamp, pp_t_df, is_previous=True)
                pp_ap_fare += get_fare_in_period('join-queue-time', 'end-time', \
                                                  prev_timestamp, cur_timestamp, pp_q_df, is_previous=True)
                pp_ap_queue_trip_time += get_queue_trip_time_in_period('join-queue-time', 'end-time', \
                                                  prev_timestamp, cur_timestamp, pp_q_df, is_previous=True)
            # cp => current period
            cp_total_fare = get_fare_in_period('start-time', 'end-time', cur_timestamp, next_timestamp, ct_df)
            cp_ap_fare = get_fare_in_period('join-queue-time', 'end-time', cur_timestamp, next_timestamp, cq_df)
            cp_ap_queue_trip_time = get_queue_trip_time_in_period('join-queue-time', 'end-time', \
                                          cur_timestamp, next_timestamp, cq_df)
            total_fare = pp_total_fare + cp_total_fare
            ap_fare = pp_ap_fare + cp_ap_fare
            ap_duration = pp_ap_queue_trip_time + cp_ap_queue_trip_time
            op_cost_sec = (total_fare - ap_fare) / (total_duration * SEC - ap_duration)
            #
            writer.writerow([yy, mm, dd, cur_period.strftime("%a"), hh, \
                             total_duration, ap_duration, total_fare, ap_fare, op_cost_sec, op_cost_sec * SEC])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
        
def get_fare_in_period(st_label, et_label, st_timestamp, et_timestamp, df, is_previous=False):
    # is_previous: For calculating fares occured in the previous period but trip time for the trip prolong in the current perios
    dh_trips_df = df[(st_timestamp <= df[st_label]) & (df[st_label] < et_timestamp)]
    dh_trips_df['within-period-trip-ratio'] = dh_trips_df.apply(lambda row:
                                        (min(row[et_label], et_timestamp) - row[st_label]) / (row[et_label] - row[st_label]), axis=1)
    if not is_previous:
        dh_trips_df['within-period-trip-fare'] = dh_trips_df['fare'] * dh_trips_df['within-period-trip-ratio']
    else:
        dh_trips_df['within-period-trip-fare'] = dh_trips_df['fare'] * (1 - dh_trips_df['within-period-trip-ratio'])
    return dh_trips_df['within-period-trip-fare'].sum()

def get_queue_trip_time_in_period(st_label, et_label, st_timestamp, et_timestamp, df, is_previous=False):
    # is_previous: For calculating fares occured in the previous period but trip time for the trip prolong in the current perios
    dh_trips_df = df[(st_timestamp <= df[st_label]) & (df[st_label] < et_timestamp)]
    if not is_previous:
        dh_trips_df['within-period-duration'] = dh_trips_df.apply(lambda row:
                                                              min(row[et_label], et_timestamp) - row[st_label], axis=1)
    else:
        dh_trips_df['within-period-duration'] = dh_trips_df.apply(lambda row:
                                                              max(0, row[et_label] - et_timestamp), axis=1)
    return dh_trips_df['within-period-duration'].sum()

if __name__ == '__main__':
    run()
