from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
#
from supports._setting import trips_dir
from supports.etc_functions import remove_creat_dir, get_all_files
from supports.logger import logging_msg
#
ori_prefix = '/Users/JerryHan88/taxi/trips_ext'

def run():
    remove_creat_dir(trips_dir)
    csv_files = get_all_files(ori_prefix, 'trips', '.csv')
    #
    for fn in csv_files: 
        process_file(fn)
    
def process_file(fn):
    _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (ori_prefix, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        #
        id_tid, id_vid, id_did = headers.index('trip-id'), headers.index('vehicle-id'), headers.index('driver-id')
        id_st, id_et = headers.index('start-time'), headers.index('end-time')
        id_fare = headers.index('fare')
        id_tm = headers.index('trip-mode')
        vehicle_prev_trip_end_time = {}
        with open('%s/whole-trip-%s.csv' % (trips_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did', 'start-time', 'end-time', 'duration', 'fare', 'trip-mode', 'prev-trip-end-time']
            writer.writerow(new_headers)
            for row in reader:
                vid = row[id_vid]
                start_time, end_time = eval(row[id_st]), eval(row[id_et]),
                if not vehicle_prev_trip_end_time.has_key(vid):
                    # ASSUMPTION
                    # If this trip is the driver's first trip in a month,
                    # Assume that the previous trip's end time is the current trip's start time 
                    vehicle_prev_trip_end_time[vid] = start_time
                prev_trip_end_time = vehicle_prev_trip_end_time[vid]
                #
                new_row = [row[id_tid], vid, row[id_did],
                           start_time, end_time, end_time - start_time,
                           row[id_fare],
                           row[id_tm], prev_trip_end_time]
                writer.writerow(new_row)
                #
                vehicle_prev_trip_end_time[vid] = end_time
if __name__ == '__main__':
    run()
