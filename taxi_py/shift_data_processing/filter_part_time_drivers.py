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

def run():
    remove_creat_dir(full_shift_dir)
    csv_files = get_all_csv_files(shift_dir)
    
def process_file(fn):
    with open('%s/%s' % (shift_dir, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_year, id_month, id_day, id_hour = headers.index('year'), headers.index('month'), headers.index('day'), headers.index('hour')
        id_vid, id_did = headers.index('vehicle-id'), headers.index('driver-id')
        id_productive, id_x_productive = headers.index('productive-duration'), headers.index('x-productive-duration')
        with open('%s/%s' % (full_shift_dir, fn), 'wt') as w_csvfile:
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