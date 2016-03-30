from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv, datetime, math
#
from supports._setting import trips_dir, for_learning_dir
from supports.etc_functions import get_all_files, remove_creat_dir 
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor

HOUR = 60 * 60

def run():
    remove_creat_dir(for_learning_dir)
    csv_files = get_all_files(trips_dir, 'whole-trip-', '.csv')
    #
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
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
        id_tid = headers.index('tid')
        id_st, id_duration = headers.index('start-time'), headers.index('duration') 
        id_fare, id_tm, id_prev_tet = headers.index('fare'), headers.index('trip-mode'), headers.index('prev-trip-end-time')
        #
        with open('%s/trip-for-learning-%s.csv' % (for_learning_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'trip-mode',
                           'prev-trip-end-time', 'start-time',
                           'day-of-week', 'hh',
                           'setup-time', 'duration',
                           'setup-time_HOUR', 'duration_HOUR', 
                           'fare']
            writer.writerow(new_headers)
            for row in reader:
                st = eval(row[id_st]) 
                st_datetime = datetime.datetime.fromtimestamp(st)
                prev_tet = eval(row[id_prev_tet])
                setup_time = st - prev_tet
                setup_time_hour = int(math.ceil(setup_time / HOUR))
                duration = eval(row[id_duration])
                duration_hour = int(math.ceil(duration/ HOUR))
                writer.writerow([row[id_tid], row[id_tm],
                                prev_tet, st,
                                st_datetime.strftime("%a"), st_datetime.hour,
                                setup_time, duration,
                                setup_time_hour, duration_hour, row[id_fare]])
    print 'end the file; %s' % yymm 
    logging_msg('end the file; %s' % yymm)
        
if __name__ == '__main__':
    run()
