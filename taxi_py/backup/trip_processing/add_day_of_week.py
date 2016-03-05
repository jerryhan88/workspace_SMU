from __future__ import division

from support._setting import tsdt_dir
import csv, datetime
#
def run():
    with open('%s/%s' % (tsdt_dir, 'whole-driver-tm.csv'), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        #
        id_yy, id_mm, id_dd = headers.index('yy'), headers.index('mm'), headers.index('dd')
        id_did, id_tm, id_tmm, id_fs = headers.index('driver-id'), headers.index('trip-mode'), headers.index('trip-mode-num'), headers.index('fare-sum')
        #
        
        with open('%s/%s' % (tsdt_dir, 'whole-driver-tm_.csv'), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['yy', 'mm', 'dd', 'dow', 'driver-id', 'trip-mode', 'trip-mode-num', 'fare-sum']
            writer.writerow(new_headers)
            for row in reader:
                yy, mm, dd = int(row[id_yy]), int(row[id_mm]), int(row[id_dd])
                cur_period = datetime.datetime(2000+yy, mm, dd)
                dow = cur_period.strftime("%a")
                writer.writerow([row[id_yy], row[id_mm], row[id_dd], dow,
                                 row[id_did], row[id_tm],row[id_tmm],row[id_fs]])
    
if __name__ == '__main__':
    run()
