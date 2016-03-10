from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import shifts_dir, trips_dir, aiport_trips_dir, op_costs_dir
from supports.etc_functions import remove_creat_dir
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.logger import logging_msg
#
import datetime, time, csv
import pandas as pd
from traceback import format_exc
#
sh_prefix, trip_prefix, ap_trip_prefix = 'shift-all-', 'whole-trip-', 'airport-trip-'
TOTAL_DUR, TOTAL_FARE, AP_QUEUE, AP_DUR, AP_FARE = range(5)
SEC = 60
Q_LIMIT_MIN, Q_LIMIT_MAX = 0, 3600
#
def run():
    remove_creat_dir(op_costs_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                yymm = '%02d%02d' % (y, m) 
                if yymm in ['0912', '1010']:
                    continue
                put_task(process_files, [yymm])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    dur_fare = {}
    cur_timestamp = datetime.datetime(2009, 1, 1, 0) 
    last_timestamp = datetime.datetime(2011, 1, 1, 0)
    time_period_order = []
    while cur_timestamp < last_timestamp:
        yyyy, mm, dd, hh = cur_timestamp.year, cur_timestamp.month, cur_timestamp.day, cur_timestamp.hour
        dur_fare[(yyyy, mm, dd, hh)] = [0 for _ in range(len([TOTAL_DUR, TOTAL_FARE, AP_QUEUE, AP_DUR, AP_FARE]))]
        time_period_order.append((yyyy, mm, dd, hh))
        cur_timestamp += datetime.timedelta(hours=1)
    #
    s_df = pd.read_csv('%s/%s%s.csv' % (shifts_dir, sh_prefix, yymm))
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (aiport_trips_dir, ap_trip_prefix, yymm))
    #
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    dd, hh = 1, 0
    cur_day_time = datetime.datetime(yyyy, mm, dd, hh)
    if mm == 12:
        next_yyyy, next_mm = yyyy + 1, 1
    else:
        next_yyyy, next_mm = yyyy, mm + 1
    last_day_time = datetime.datetime(next_yyyy, next_mm, dd, hh)
    #
    st_label, et_label = 'start-time', 'end-time'
    fare_label = 'fare'
    while cur_day_time != last_day_time:
        prev_day_time = cur_day_time - datetime.timedelta(hours=1)
        next_day_time = cur_day_time + datetime.timedelta(hours=1)
        st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
        #
        yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
        filtered_sh = s_df[(s_df['dd'] == dd) & (s_df['hh'] == hh)]
        total_dur = sum(filtered_sh['pro-dur']) * SEC
        #    
        filtered_trip = trip_df[(st_timestamp <= trip_df[st_label]) & (trip_df[et_label] < et_timestamp)]
        filtered_trip['in-p-ratio'] = filtered_trip.apply(lambda row:
                                            (min(row[et_label], et_timestamp) - row[st_label]) / (row[et_label] - row[st_label]), axis=1)
        filtered_trip['in-fare'] = filtered_trip[fare_label] * filtered_trip['in-p-ratio']
        filtered_trip['out-fare'] = filtered_trip[fare_label] * (1 - filtered_trip['in-p-ratio'])
        total_fare = sum(filtered_trip['in-fare'])
        next_total_fare = sum(filtered_trip['out-fare'])
        #
        filtered_ap_trip = ap_trip_df[(st_timestamp <= ap_trip_df[st_label]) & (ap_trip_df[et_label] < et_timestamp)]
        #
        q_limit_max_ex = filtered_ap_trip[(Q_LIMIT_MAX < filtered_ap_trip['queue-time'])]
        q_limit_max_ex['join-queue-time'] = q_limit_max_ex[st_label] - Q_LIMIT_MAX
        q_limit_max_ex['prev-queue-time'] = st_timestamp - q_limit_max_ex['join-queue-time'] 
        q_limit_max_ex['cur-queue-time'] = q_limit_max_ex[st_label] - st_timestamp
        prev_queue_time = sum(q_limit_max_ex['prev-queue-time'])
        cur_queue_time = sum(q_limit_max_ex['cur-queue-time'])
        #
        q_normal = filtered_ap_trip[(Q_LIMIT_MIN <= filtered_ap_trip['queue-time']) & \
                                   (filtered_ap_trip['queue-time'] <= Q_LIMIT_MAX)]
        q_normal['prev-queue-time'] = st_timestamp - q_normal['join-queue-time'] 
        q_normal['cur-queue-time'] = q_normal[st_label] - st_timestamp
        prev_queue_time += sum(q_normal['prev-queue-time'])
        cur_queue_time += sum(q_normal['cur-queue-time'])
        #
        filtered_ap_trip['in-p-ratio'] = filtered_ap_trip.apply(lambda row:
                                            (min(row[et_label], et_timestamp) - row[st_label]) / (row[et_label] - row[st_label]), axis=1)
        filtered_ap_trip['in-fare'] = filtered_ap_trip[fare_label] * filtered_ap_trip['in-p-ratio']
        filtered_ap_trip['out-fare'] = filtered_ap_trip[fare_label] * (1 - filtered_ap_trip['in-p-ratio'])
        filtered_ap_trip['in-duration'] = filtered_ap_trip['duration'] * filtered_ap_trip['in-p-ratio']
        filtered_ap_trip['out-duration'] = filtered_ap_trip['duration'] * (1 - filtered_ap_trip['in-p-ratio'])
        #
        ap_fare = sum(filtered_ap_trip['in-fare'])
        next_ap_fare = sum(filtered_ap_trip['out-fare'])
        ap_duration = sum(filtered_ap_trip['in-duration'])
        next_ap_duration = sum(filtered_ap_trip['out-duration'])
        #
        # prev
        p_yyyy, p_mm, p_dd, p_hh = prev_day_time.year, prev_day_time.month, prev_day_time.day, prev_day_time.hour
        if dur_fare.has_key((p_yyyy, p_mm, p_dd, p_hh)):   
            dur_fare[(p_yyyy, p_mm, p_dd, p_hh)][AP_QUEUE] += prev_queue_time
        # current
        dur_fare[(yyyy, mm, dd, hh)][TOTAL_DUR] += total_dur 
        dur_fare[(yyyy, mm, dd, hh)][TOTAL_FARE] += total_fare
        dur_fare[(yyyy, mm, dd, hh)][AP_QUEUE] += cur_queue_time 
        dur_fare[(yyyy, mm, dd, hh)][AP_DUR] += ap_duration  
        dur_fare[(yyyy, mm, dd, hh)][AP_FARE] += ap_fare 
        # next
        n_yyyy, n_mm, n_dd, n_hh = next_day_time.year, next_day_time.month, next_day_time.day, next_day_time.hour
        if dur_fare.has_key((n_yyyy, n_mm, n_dd, n_hh)):   
            dur_fare[(n_yyyy, n_mm, n_dd, n_hh)][TOTAL_DUR] += next_total_fare
            dur_fare[(n_yyyy, n_mm, n_dd, n_hh)][AP_FARE] += next_ap_fare
            dur_fare[(n_yyyy, n_mm, n_dd, n_hh)][AP_DUR] += next_ap_duration
        cur_day_time = next_day_time
    with open('%s/op-cost-%s.csv' % (op_costs_dir, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh', 'total-duration', 'total-fare', 'ap-queue', 'ap-duration', 'ap-fare', 'op-cost-sec']
        writer.writerow(header)
        for yyyy, mm, dd, hh in time_period_order:
            total_dur, total_fare, ap_queue, ap_dur, ap_fare = dur_fare[(yyyy, mm, dd, hh)]
            ap_out_fare = total_fare - ap_fare
            ap_out_dur = total_dur - (ap_queue + ap_dur)
            op_cost = ap_out_fare / ap_out_dur
            writer.writerow([
                             yyyy-2000, mm, dd, hh,
                             total_dur, total_fare, ap_queue, ap_dur, ap_fare,
                             op_cost
                             ])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
if __name__ == '__main__':
    run()
