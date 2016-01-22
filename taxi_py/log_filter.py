from __future__ import division
#
import os, shutil, csv
#
from _setting import path_to_ori_data, dl_dir
from location_check import is_in_airport, ap_poly
from logger import logging_msg
#
driver_prev_lacation_time = {}

'''
Only process logs from 2009~2010
'''
TARGET_YEARS = ['2009', '2010']

def run():
    if os.path.exists(dl_dir):
        shutil.rmtree(dl_dir)
    os.makedirs(dl_dir)
    for yd in os.listdir(path_to_ori_data):
        yd_path = '%s/%s' % (path_to_ori_data, yd)
        if not (os.path.isdir(yd_path) and yd.startswith('20')):
            continue
        if yd not in TARGET_YEARS:
            continue 
        for md in os.listdir(yd_path):
            md_path = '%s/%s' % (yd_path, md)
            if not os.path.isdir(md_path):
                continue
            fn = 'logs-%s%s-normal.csv' % (yd[-2:], md)
            pt_log_csv = '%s/%s/%s' % (md_path, 'logs', fn)
            filter_log(pt_log_csv) 
            
def filter_log(pt_log_csv):
    logging_msg('handlie the file; pt_log_csv')
    with open(pt_log_csv, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        print headers
        index_did = headers.index('driver-id')
        for row in reader:        
            driver_id = row[index_did]
            write_driver_log(headers, driver_id, row)
             
#         index_did = headers.index('driver-id')
#         for row in reader:
#             
#             write_driver_trip(headers, driver_id, row, term_polys)
#     
#     fn = '%s/driver_%s_trips.csv' % (dt_dir, driver_id)
#     if not os.path.exists(fn):
#         with open(fn, 'wt') as csvfile:
#             writer = csv.writer(csvfile)
#             new_headers = headers + ['start-terminal', 'end-terminal', 'trip-mode']
#             writer.writerow(new_headers)

def write_driver_log(headers, driver_id, row):
    fn = '%s/driver_%s_logs.csv' % (dl_dir, driver_id)
    index_s_time, index_e_time = headers.index('start-time'), headers.index('end-time')
    
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvfile:
            writer = csv.writer(csvfile)
            new_headers = headers + ['cur-location']
            new_headers = headers + ['start-terminal', 'end-terminal', 'trip-mode']
            writer.writerow(new_headers)
    
#     if not driver_prev_lacation_time.has_key(driver_id):
#         driver_prev_lacation_time[driver_id] = (c_e_ter, eval(row[index_e_time]))
    
    print headers, driver_id, row
    pass
    
if __name__ == '__main__':
    run()
