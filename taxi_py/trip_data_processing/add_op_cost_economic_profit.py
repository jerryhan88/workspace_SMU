from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv, datetime, time
from traceback import format_exc
#
from supports.etc_functions import get_all_files
from supports._setting import aiport_trips_dir, op_cost_summary
from supports._setting import Q_LIMIT_MIN, Q_LIMIT_MAX
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
op_costs = {}
with open(op_cost_summary) as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    header = ['yy', 'mm', 'dd', 'hh', 'total-duration', 'total-fare', 'ap-queue', 'ap-duration', 'ap-fare', 'op-cost-sec']
    id_yy, id_mm, id_dd, id_hh = headers.index('yy'), headers.index('mm'), headers.index('dd'), headers.index('hh')
    id_op_cost = headers.index('op-cost-sec')
    for row in reader:
        yyyy, mm, dd, hh = 2000 + eval(row[id_yy]), eval(row[id_mm]), eval(row[id_dd]), eval(row[id_hh])
        op_costs[(yyyy, mm, dd, hh)] = eval(row[id_op_cost]) 
#
def run():
    csv_files = get_all_files(aiport_trips_dir, 'airport-trip-', '.csv')
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        try:
            put_task(process_file, [fn])
        except Exception as _:
            logging_msg('Algorithm runtime exception (%s)\n' % (fn) + format_exc())
            raise
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_file(fn):
    _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (aiport_trips_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        
        id_tid, id_vid, id_did = headers.index('tid'), headers.index('vid'), headers.index('did')
        id_st, id_et, id_dur = headers.index('start-time'), headers.index('end-time'), headers.index('duration')
        id_fare = headers.index('fare')
        id_tm, id_pt_et = headers.index('trip-mode'), headers.index('prev-trip-end-time')
        id_jqt, id_qt = headers.index('join-queue-time'), headers.index('queue-time')
        
        with open('%s/ap-trip-op-ep-%s.csv' % (aiport_trips_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did', 'start-time', 'end-time', 'duration', 'fare', 'trip-mode', 'prev-trip-end-time', 'join-queue-time', 'queue-time',
                           'op-cost', 'economic']
            writer.writerow(new_headers)
            for row in reader:
                jqt, st, et = eval(row[id_jqt]), eval(row[id_st]), eval(row[id_et])
                dur, fare = eval(row[id_dur]), eval(row[id_fare]) 
                if st - jqt < Q_LIMIT_MIN:
                    qt = Q_LIMIT_MIN
                elif Q_LIMIT_MAX < st - jqt:
                    qt = Q_LIMIT_MAX
                else:
                    qt = st - jqt
                modi_jqt = st - qt
                jqt_datetime = datetime.datetime.fromtimestamp(modi_jqt)
                st_datetime = datetime.datetime.fromtimestamp(st)
                et_datetime = datetime.datetime.fromtimestamp(et)
                op_cost = 0
                st_yyyy, st_mm, st_dd, st_hh = st_datetime.year, st_datetime.month, st_datetime.day, st_datetime.hour
                if jqt_datetime.hour == st_datetime.hour:
                    op_cost += qt * op_costs[(st_yyyy, st_mm, st_dd, st_hh)]
                else:
                    tp = datetime.datetime(st_datetime.year, st_datetime.month, st_datetime.day, st_datetime.hour)
                    tp_timestamp = time.mktime(tp.timetuple())
                    p_jqt_st = (tp_timestamp - modi_jqt) / qt
                    prev_dt = st_datetime - datetime.timedelta(hours=1)
                    op_cost += op_costs[(prev_dt.year, prev_dt.month, prev_dt.day, prev_dt.hour)] * qt * p_jqt_st
                    op_cost += op_costs[(st_yyyy, st_mm, st_dd, st_hh)] * qt * (1 - p_jqt_st)
                if st_datetime.hour == et_datetime.hour:
                    op_cost += dur * op_costs[(st_yyyy, st_mm, st_dd, st_hh)]
                else:
                    # This part don't regards cases when duration is more than a hour
                    tp = datetime.datetime(et_datetime.year, et_datetime.month, et_datetime.day, et_datetime.hour)
                    tp_timestamp = time.mktime(tp.timetuple())
                    p_st_et = (tp_timestamp - st) / dur
                    next_dt = st_datetime + datetime.timedelta(hours=1)
                    op_cost += op_costs[(st_yyyy, st_mm, st_dd, st_hh)] * qt * p_st_et
                    op_cost += op_costs[(next_dt.year, next_dt.month, next_dt.day, next_dt.hour)] * qt * (1 - p_st_et)
                economic_profit = fare - op_cost
                #
                writer.writerow([row[id_tid], row[id_vid], row[id_did],
                                st, et, dur, fare,
                                row[id_tm], row[id_pt_et],
                                modi_jqt, qt,
                                op_cost, economic_profit])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
    
if __name__ == '__main__':
    run()
