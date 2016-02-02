from __future__ import division
#
import os, shutil, csv
#
from _setting import tm_dir, t_dir
from location_check import check_terminal_num
from logger import logging_msg
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
#

def run():
    if os.path.exists(t_dir):
        shutil.rmtree(t_dir)
    os.makedirs(t_dir)
    cvs_files = [fn for fn in os.listdir(tm_dir) if fn.endswith('.csv')]
    #
    init_multiprocessor()
    count_num_jobs = len(cvs_files)
    for fn in sorted(cvs_files):
        pt_log_csv = '%s/%s' % (tm_dir, fn)
        put_task(ext_trip_file, [pt_log_csv])
    end_multiprocessor(count_num_jobs)

def ext_trip_file(pt_log_csv):
    print 'handle the file; %s' % pt_log_csv
    logging_msg('handle the file; %s' % pt_log_csv)
    with open(pt_log_csv, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        #
        id_trip_id, id_job_id = headers.index('trip-id'), headers.index('job-id')
        id_st, id_et = headers.index('start-time'), headers.index('end-time')
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id')
        id_fare = headers.index('fare')
        id_s_long, id_s_lat = headers.index('start-long'), headers.index('start-lat')
        id_e_long, id_e_lat = headers.index('end-long'), headers.index('end-lat')
        #
        driver_prev_lacation = {}
        pt_new_csv = '%s/%s' % (t_dir, pt_log_csv.split('/')[-1])
        with open(pt_new_csv, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['trip-id', 'job-id', 'start-time', 'end-time', 'vehicle-id', 'fare', 'driver-id', 'trip-mode']
            writer.writerow(new_headers)
            for row in reader:
                driver_id = eval(row[id_did])
                s_long, s_lat = eval(row[id_s_long]), eval(row[id_s_lat])
                e_long, e_lat = eval(row[id_e_long]), eval(row[id_e_lat])
                c_s_ter, c_e_ter = check_terminal_num(s_long, s_lat), check_terminal_num(e_long, e_lat)
                '''
                Set a trip mode
                Trips for servicing passengers are classified according to positions 
                  where the driver dropped the previous passenger off and picks the current passenger up. 
                Positions are categorised as in the airport (InAP) or outside of airport (OutAP). 
                As a result, four trip modes can be derived;
                    - drop off InAP - pick up InAP             -> 0
                    - drop off InAP - pick up OutAP            -> 1
                    - drop off OutAP - pick up InAP            -> 2
                    - drop off OutAP - pick up OutAP           -> 3
                Also, one more mode is added to represent trip of which previous trip was handled more than 12 hours ago.
                    - previous trip occured 12 hours before    -> -1
                '''
                if not driver_prev_lacation.has_key(driver_id):
                    # ASSUMPTION
                    # If this trip is the driver's first trip in a month,
                    # let's assume that the previous trip occurred out of the airport
                    driver_prev_lacation[driver_id] = -1
                #
                p_e_ter = driver_prev_lacation[driver_id]
                if p_e_ter != -1 and c_s_ter != -1 :
                    trip_mode = 0
                elif p_e_ter != -1 and c_s_ter == -1:
                    trip_mode = 1
                elif p_e_ter == -1 and c_s_ter != -1:
                    trip_mode = 2
                elif p_e_ter == -1 and c_s_ter == -1:
                    trip_mode = 3
                else:
                    assert False
                driver_prev_lacation[driver_id] = c_e_ter
                #
                new_row = [eval(row[id_trip_id]), eval(row[id_job_id]), eval(row[id_st]), eval(row[id_et]),
                           eval(row[id_vid]), driver_id, eval(row[id_fare]), trip_mode]
                writer.writerow(new_row)

if __name__ == '__main__':
    run()
