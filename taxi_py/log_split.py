from __future__ import division
import csv, os
from datetime import datetime
from traceback import format_exc
from logger import logging_msg
from _setting import l_dir
#
def run():
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                process_file('%02d%02d' % (y, m))
            except Exception as _:
                logging_msg('Algorithm runtime exception (%02d%02d)\n' % (y, m) + format_exc())
                raise

def process_file(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    pt_csv = '%s/logs-%s-normal.csv' % (l_dir, yymm)
    with open(pt_csv, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        headers = reader.next()
        index_lt = headers.index('time')
        current_day = 1
        for row in reader:
            lt = eval(row[index_lt])
            lt_day = datetime.fromtimestamp(lt).day
            if lt_day == current_day:
                yymm_dir = '%s/%s' % (l_dir, yymm)
                if not os.path.exists(yymm_dir):
                    os.makedirs(yymm_dir)
                pt_day_csv = '%s/logs-%s%02d.csv' % (yymm_dir, yymm, current_day)
                if not os.path.exists(pt_day_csv):
                    with open(pt_day_csv, 'wt') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(headers)
                else:
                    with open(pt_day_csv, 'a') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(row)
            else:
                current_day += 1
                pt_day_csv = '%s/logs-%s%02d.csv' % (yymm_dir, yymm, current_day)
                with open(pt_day_csv, 'wt') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()