from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports.handling_pkl import load_picle_file
from supports.etc_functions import get_all_files, remove_creat_dir
from supports._setting import trips_dir, for_full_driver_dir, individual_detail_dir
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
trip_prefix = 'whole-trip-'
full_time_drivers, _, _, _, _, _, _, _, _, _, _ = load_picle_file('%s/productivities_ext.pkl' % (individual_detail_dir))
driver_full_or_not = [False] * (max(full_time_drivers) + 1)
for did in full_time_drivers:
    driver_full_or_not[did] = True
#
check_progress = 10000000
def run():
    remove_creat_dir(for_full_driver_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for fn in get_all_files(trips_dir, trip_prefix, '.csv'):
#         process_file(fn)
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(fn):
    _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (trips_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_did = headers.index('did')
        count = 0
        with open('%s/whole-trip-%s.csv' % (for_full_driver_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
        for row in reader:
            did = row[id_did]
            if did <= len(driver_full_or_not) and driver_full_or_not[did]:
                writer.writerow(row)
            count +=1
            if count % check_progress == 0:
                print '%s-----%d' % (yymm, count) 
                logging_msg('%s-----%d' % (yymm, count))
    print 'end the file; %s' % yymm 
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
