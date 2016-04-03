from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS
from supports._setting import trips_dir
from supports.logger import logging_msg
#
import datetime, time, csv
import pandas as pd
#
trip_prefix = 'whole-trip-'
ap_fn = '%s/whole-ap-tm-num-dur-fare.csv' % (trips_dir)
ns_fn = '%s/whole-ns-tm-num-dur-fare.csv' % (trips_dir)
#
def run():
    with open(ap_fn, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        header = ['yy', 'mm', 'ap-trip-mode', 'num-tm', 'total-dur', 'total-fare']
        writer.writerow(header)
    
    with open(ns_fn, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        header = ['yy', 'mm', 'ns-trip-mode', 'num-tm', 'total-dur', 'total-fare']
        writer.writerow(header)
    
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
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
    st_label = 'start-time'
    ap_tm_lable, ns_tm_lable = 'ap-trip-mode', 'ns-trip-mode' 
    dur_lable, fare_label = 'duration', 'fare'
    #
    ap_tm = [DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP]
    ns_tm = [DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS]
    #
    while cur_day_time != last_day_time:
        next_day_time = cur_day_time + datetime.timedelta(hours=1)
        st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
        #
        yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
        #    
        filtered_trip = trip_df[(st_timestamp <= trip_df[st_label]) & (trip_df[st_label] < et_timestamp)]
        #
        gp_f_trip = filtered_trip.groupby([ap_tm_lable])
        tm_num_totalDuration_totalFare = zip(ap_tm, list(gp_f_trip.count()[fare_label]), list(gp_f_trip.sum()[dur_lable]), list(gp_f_trip.sum()[fare_label]))
        save_as_csv(ap_fn, yymm, tm_num_totalDuration_totalFare)
        #
        gp_f_trip = filtered_trip.groupby([ns_tm_lable])
        tm_num_totalDuration_totalFare = zip(ns_tm, list(gp_f_trip.count()[fare_label]), list(gp_f_trip.sum()[dur_lable]), list(gp_f_trip.sum()[fare_label]))
        save_as_csv(ns_fn, yymm, tm_num_totalDuration_totalFare)
        cur_day_time = next_day_time
        
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)

def save_as_csv(fn, yymm, _data):
    yy, mm = yymm[:2], yymm[2:]
    with open(fn, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for tm, num, totalDur, totalFare in _data:
            writer.writerow([yy, mm, tm, num, totalDur, totalFare])

if __name__ == '__main__':
    run()    
