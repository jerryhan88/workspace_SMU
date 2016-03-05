from __future__ import division
import os, sys, shutil, csv
sys.path.append(os.getcwd() + '/..')
#
from support._setting import ms_dir
from support.logger import logging_msg
from support.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from traceback import format_exc
#
prefix = '/home/sfcheng/toolbox'
# prefix = '.'
#

def run():
    if os.path.exists(ms_dir):
        shutil.rmtree(ms_dir)
    os.makedirs(ms_dir)
#     process_file('shift-hour-state-0901.csv', '0901')
    init_multiprocessor()
    count_num_jobs = 0
    cvs_files = [fn for fn in os.listdir(prefix) if fn.startswith('shift') and fn.endswith('.csv')]
    for fn in cvs_files:
        _, _, _, yymm = fn[:-len('.csv')].split('-')
        if yymm.startswith('11') or yymm.startswith('12'):
            continue
        try:
            put_task(process_file, [fn, yymm])
        except Exception as _:
            logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
            raise
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(fn, yymm):        
    is_driver_vehicle = {}
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (prefix, fn), 'rt') as r_csvfile:
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
        with open('%s/temp_%s' % (ms_dir, fn), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['year', 'month', 'day', 'hour', 'vehicle-id', 'driver-id', 'productive-duration', 'x-productive-duration']
            writer.writerow(new_headers)
            for row in reader:
                vid, did = row[id_vid], row[id_did] 
                if not is_driver_vehicle.has_key(vid):
                    is_driver_vehicle[vid] = set()
                is_driver_vehicle[vid].add(did)
                productive_duration = sum(int(row[x]) for x in productive_state)
                x_productive_duration = sum(int(row[x]) for x in x_productive_state)
                writer.writerow([row[id_year], row[id_month], row[id_day], row[id_hour], vid, did, productive_duration, x_productive_duration])
    #
    with open('%s/temp_%s' % (ms_dir, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_year, id_month, id_day, id_hour = headers.index('year'), headers.index('month'), headers.index('day'), headers.index('hour')
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id')
        id_productive, id_x_productive = headers.index('productive-duration'), headers.index('x-productive-duration')
        with open('%s/%s' % (ms_dir, fn), 'wt') as w_csvfile:
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
    os.remove('%s/temp_%s' % (ms_dir, fn))
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
#     test()
    run()
#     process_file(None, '0902')
