from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports.etc_functions import remove_creat_dir
from supports._setting import HOUR
from supports._setting import sh_prefix, trip_prefix
from supports._setting import shifts_dir, trips_dir 
from supports._setting import general_dur_fare_dir, general_dur_fare_prefix
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime, time
#
GEN_DUR, GEN_FARE = range(2)
#
def run():
    remove_creat_dir(general_dur_fare_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
#             process_files('1007')
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    begin_timestamp = datetime.datetime(2009, 1, 1, 0) 
    last_timestamp = datetime.datetime(2011, 1, 1, 0)
    hourly_total, time_period_order = {}, []
    while begin_timestamp < last_timestamp:
        yyyy, mm, dd, hh = begin_timestamp.year, begin_timestamp.month, begin_timestamp.day, begin_timestamp.hour
        k = (yyyy, mm, dd, hh)
        hourly_total[k] = [0 for _ in range(len([GEN_DUR, GEN_FARE]))]
        time_period_order.append(k)
        begin_timestamp += datetime.timedelta(hours=1)
    #
    st_label, et_label, dur_label, fare_label = 'start-time', 'end-time', 'duration', 'fare'
    # Productive duration
    with open('%s/%s%s.csv' % (shifts_dir, sh_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        for row in reader:
            dd, hh = row[hid['hh']], row[hid['hh']]
            hourly_total[(yyyy, mm, dd, hh)][GEN_DUR] += eval(row[hid['pro-dur']]) * 60  # unit change; Minute -> Second 
    # Total fare
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        for row in reader:
            st_ts, et_ts = eval(row[st_label]), eval(row[et_label])
            dur, fare = eval(row[dur_label]), eval(row[fare_label])
            #
            st_dt, et_dt = datetime.datetime.fromtimestamp(st_ts), datetime.datetime.fromtimestamp(et_ts)
            #
            if st_dt.hour == et_dt.hour: 
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][GEN_FARE] += fare
            else:
                assert dur > HOUR
                next_ts_dt = datetime.datetime(st_dt.year, st_dt.month, st_dt.day, st_dt.hour) + datetime.timedelta(hours=1)
                tg_year, tg_month, tg_day, tg_hour = \
                        next_ts_dt.year, next_ts_dt.month, next_ts_dt.day, next_ts_dt.hour
                tg_dt = datetime.datetime(tg_year, tg_month, tg_day, tg_hour)
                tg_ts = time.mktime(tg_dt.timetuple())
                prop = (tg_ts - st_ts) / dur
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][GEN_FARE] += fare * prop
                while True:
                    if tg_dt.hour == et_dt.hour:
                        prop = (et_ts - tg_ts) / dur
                        hourly_total[(et_dt.year, et_dt.month,
                              et_dt.day, et_dt.hour)][GEN_FARE] += fare * prop
                        break
                    prop = HOUR / dur
                    hourly_total[(tg_dt.year, tg_dt.month,
                              tg_dt.day, tg_dt.hour)][GEN_FARE] += fare * prop
                    tg_dt += datetime.timedelta(hours=1)
    with open('%s/%s%s.csv' % (general_dur_fare_dir, general_dur_fare_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh', 'gen-duration', 'gen-fare']
        writer.writerow(header)
        for yyyy, mm, dd, hh in time_period_order:
            gen_dur, gen_fare = hourly_total[(yyyy, mm, dd, hh)] 
            writer.writerow([yyyy - 2000, mm, dd, hh, gen_dur, gen_fare])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
          
if __name__ == '__main__':
    run()