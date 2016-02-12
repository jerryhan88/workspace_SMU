from __future__ import division
#
from _setting import l_dir, t_dir, q_dir
#
import os, shutil, csv
from traceback import format_exc
#
from logger import logging_msg
from multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    if os.path.exists(q_dir):
        shutil.rmtree(q_dir)
    os.makedirs(q_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            try:
#                 process_file(yymm)
                put_task(process_file, [yymm])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    # labels of trips
    l_did, l_st, l_et, l_tid, l_tm, l_fare = 'driver-id', 'start-time', 'end-time', 'trip-id', 'trip-mode', 'fare'
    # labels of logs
    l_lt, l_ap = 'time', 'ap-or-not'
    l_vid = 'vehicle-id'
    #
    prev_day_csv = None
    if yymm == '0901':
        prev_day_csv = None
    elif yymm == '1001':
        prev_day_csv = None
    elif yymm == '1010':
        prev_day_csv = None
    else:
        yy, mm = int(yymm[:2]), int(yymm[2:])
        pre_yymm = '%02d%02d' % (yy, mm - 1)
        pt_prev_dir = '%s/%s' % (l_dir, pre_yymm)
        csvs = sorted([fn for fn in os.listdir(pt_prev_dir) if fn.endswith('.csv')])
        last_day_csv = csvs.pop()
        prev_day_csv = '%s/%s' % (pt_prev_dir, last_day_csv)
    # Record the last log which occurred just before entering the airport zone
    last_logging_time = {}
    if prev_day_csv != None:
        with open(prev_day_csv, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            id_lt, id_vid, id_ap = headers.index(l_lt), headers.index(l_vid), headers.index(l_ap)
            for row in reader:
                lt, vid, ap = eval(row[id_lt]), row[id_vid], row[id_ap]
                if ap == 'X':
                    last_logging_time[vid] = lt
    #
    pt_new_csv = '%s/queue-%s.csv' % (q_dir, yymm)
    with open(pt_new_csv, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = [l_tid, l_st, l_et, l_did,l_fare, l_tm, 'join-queue-time']
        writer.writerow(header)
        with open('%s/trips-%s.csv' % (t_dir, yymm), 'rb') as trip_csvfile:
            trip_reader = csv.reader(trip_csvfile)
            trip_headers = trip_reader.next()
            id_tid, id_st, id_et = trip_headers.index(l_tid), trip_headers.index(l_st), trip_headers.index(l_et) 
            id_did, id_tm, id_fare = trip_headers.index(l_did), trip_headers.index(l_tm), trip_headers.index(l_fare)
            id_vid_trip = trip_headers.index(l_vid)
            with open('%s/logs-%s-normal.csv' % (l_dir, yymm), 'rb') as log_csvfile:
                log_reader = csv.reader(log_csvfile)
                log_headers = log_reader.next()
                id_lt, id_vid_log, id_ap = log_headers.index(l_lt), log_headers.index(l_vid), log_headers.index(l_ap)
                lastly_checked_log = None
                for trip_row in trip_reader:
                    t_st, tm = eval(trip_row[id_st]), eval(trip_row[id_tm])
                    if tm == 3:
                        continue
                    while True:
                        if lastly_checked_log:
                            lt, vid_log, ap = eval(lastly_checked_log[id_lt]), lastly_checked_log[id_vid_log], lastly_checked_log[id_ap]
                            if t_st <= lt:
                                break
                            else:
                                last_logging_time[vid_log] = lt
                                lastly_checked_log = None
                        log_row = log_reader.next()
                        lt, vid_log, ap = eval(log_row[id_lt]), log_row[id_vid_log], log_row[id_ap]
                        if t_st <= lt:
                            lastly_checked_log = log_row
                            break
                        if ap == 'X':
                            last_logging_time[vid_log] = lt 
                    vid_trip = trip_row[id_vid_trip]
                    tid, t_et = trip_row[id_tid], trip_row[id_et]
                    did, fare = trip_row[id_did], trip_row[id_fare]
                    if not last_logging_time.has_key(vid_trip):
                        join_queue_time = t_st
                    else:
                        join_queue_time = last_logging_time[vid_trip]  
                    writer.writerow([tid, t_st, t_et, did, fare, tm, join_queue_time])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
if __name__ == '__main__':
    run()
