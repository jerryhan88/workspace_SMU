from __future__ import division
#
import os, shutil, csv
#
from support._setting import ds_dir, path_to_ori_data
from support.logger import logging_msg
#
def run():
#     if os.path.exists(ds_dir):
#         shutil.rmtree(ds_dir)
#     os.makedirs(ds_dir)
    ori_sdir_path = '%s/%s' % (path_to_ori_data, 'shift')
    single_file_run(ori_sdir_path, 'shift-1011.csv')
#     print ori_sdir_path
#     for fn in os.listdir(ori_sdir_path):
#         _, yymm = fn.split('-')
#         print fn
#         if yymm != '1011':
#             continue
#         if not (yymm.startswith('09') or yymm.startswith('10')):
#             continue
        
#         pt_log_csv = '%s/%s' % (ori_sdir_path, fn)
#         #
#         print 'handle the file; %s' % pt_log_csv
#         logging_msg('handle the file; %s' % pt_log_csv)
#         with open(pt_log_csv, 'rb') as csvfile:
#             reader = csv.reader(csvfile)
#             for _ in xrange(3):
#                 reader.next()
#             headers = reader.next()
#             index_did = headers.index('driver-id')
#             for row in reader:        
#                 driver_id = row[index_did]
#                 write_driver_log(headers, driver_id, row) 

def single_file_run(ori_sdir_path, fn):
    pt_log_csv = '%s/%s' % (ori_sdir_path, fn)
    #
    print 'handle the file; %s' % pt_log_csv
    logging_msg('handle the file; %s' % pt_log_csv)
    with open(pt_log_csv, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for _ in xrange(3):
            reader.next()
        headers = reader.next()
        index_did = headers.index('driver-id')
        for row in reader:        
            driver_id = row[index_did]
            write_driver_log(headers, driver_id, row)
    

def write_driver_log(headers, driver_id, row):
    fn = '%s/driver_%s_shfits.csv' % (ds_dir, driver_id)
    if not os.path.exists(fn):
        with open(fn, 'wt') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
    with open(fn, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

if __name__ == '__main__':
    run()
