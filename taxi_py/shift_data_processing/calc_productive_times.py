from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
from traceback import format_exc
#
from supports._setting import shift_dir 
from supports.etc_functions import remove_creat_dir, get_all_csv_files
from supports.logger import logging_msg
from supports.handling_pkl import save_pickle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#

server_prefix = '/home/sfcheng/toolbox'
#
def run():
    remove_creat_dir(shift_dir)
    csv_files = get_all_csv_files(server_prefix)
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        _, _, _, yymm = fn[:-len('.csv')].split('-')
        if yymm.startswith('11') or yymm.startswith('12'):
            continue
        try:
            put_task(process_file, [fn])
        except Exception as _:
            logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
            raise
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(fn):
    _, _, _, yymm = fn[:-len('.csv')].split('-')        
    is_driver_vehicle = {}
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (server_prefix, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_year, id_month, id_day, id_hour = headers.index('year'), headers.index('month'), headers.index('day'), headers.index('hour')
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id') 
        id_dur0, id_dur1, id_dur2 = headers.index('dur0'), headers.index('dur1'), headers.index('dur2')
        id_dur3, id_dur4, id_dur5 = headers.index('dur3'), headers.index('dur4'), headers.index('dur5') 
        id_dur6, id_dur7, id_dur8 = headers.index('dur6'), headers.index('dur7'), headers.index('dur8')
        id_dur9, id_dur10 = headers.index('dur9'), headers.index('dur10')
        x_productive_state = [id_dur1, id_dur2]
        productive_state = [id_dur0, id_dur3, id_dur4, id_dur5, id_dur6, id_dur7, id_dur8, id_dur9, id_dur10]
        with open('%s/shift-all-%s.csv' % (shift_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['yy', 'mm', 'dd', 'hh', 'vid', 'did', 'pro-dur', 'x-pro-dur']
            writer.writerow(new_headers)
            for row in reader:
                vid, did = row[id_vid], row[id_did]
                productive_duration = sum(int(row[x]) for x in productive_state)
                x_productive_duration = sum(int(row[x]) for x in x_productive_state)
                writer.writerow([row[id_year][-2:], row[id_month], row[id_day], row[id_hour], vid, did, productive_duration, x_productive_duration])
                is_driver_vehicle.setdefault('a',set()).add(did)
    save_pickle_file('%s/driver-vehicle-%s.pkl' % (shift_dir, yymm), is_driver_vehicle)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
    
if __name__ == '__main__':
    run()