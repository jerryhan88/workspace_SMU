from __future__ import division
#
import os, shutil, csv
#
from _setting import path_to_ori_data, dl_dir
from location_check import is_in_airport
from logger import logging_msg
'''
Only process logs from 2009~2010
And this module only save log data when the location (in airport or not) changes
But if there was breaks (BREAK_LIMIT) the log will be stored.
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
            #
            print 'handle the file; %s' % pt_log_csv
            logging_msg('handle the file; %s' % pt_log_csv)
            with open(pt_log_csv, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                headers = reader.next()
                index_did = headers.index('driver-id')
                for row in reader:        
                    driver_id = row[index_did]
                    write_driver_log(headers, driver_id, row)

def write_driver_log(headers, driver_id, row):
    fn = '%s/driver_%s_logs.csv' % (dl_dir, driver_id)
    index_long, index_lat = headers.index('longitude'), headers.index('latitude')
    ap_or_not = is_in_airport(eval(row[index_long]), eval(row[index_lat]))
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvfile:
            writer = csv.writer(csvfile)
            new_headers = headers + ['ap-or-not']
            writer.writerow(new_headers)
    new_row = row + [ap_or_not]
    with open(fn, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row)
    
if __name__ == '__main__':
    run()
