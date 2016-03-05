from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
from traceback import format_exc
#
from supports._setting import shift_dir, full_shift_dir
from supports.etc_functions import remove_creat_dir, get_all_csv_files
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    remove_creat_dir(full_shift_dir)
    csv_files = get_all_csv_files(shift_dir)
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
    is_driver_vehicle = load_picle_file('%s/driver-vehicle-%s.pkl' % (shift_dir, yymm))
    full_drivers = set()
    with open('%s/%s' % (shift_dir, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_year, id_month, id_day, id_hour = headers.index('year'), headers.index('month'), headers.index('day'), headers.index('hour')
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id')
        id_productive, id_x_productive = headers.index('productive-duration'), headers.index('x-productive-duration')
        with open('%s/shift-full-time-%s.csv' % (full_shift_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['year', 'month', 'day', 'hour', 'vehicle-id', 'driver-id', 'productive-duration', 'x-productive-duration']
            writer.writerow(new_headers)
            for row in reader:
                if len(is_driver_vehicle[row[id_vid]]) > 1:
                    continue
                productive_duration, x_productive_duration = int(row[id_productive]), int(row[id_x_productive]) 
                if productive_duration == 0 and x_productive_duration == 0:
                    continue
                writer.writerow([row[id_year], row[id_month], row[id_day], row[id_hour], row[id_vid], row[id_did], productive_duration, x_productive_duration])
                full_drivers.add(row[id_did])
    save_pickle_file('%s/full-time-drivers-%s.pkl' % (full_shift_dir, yymm), full_drivers)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)