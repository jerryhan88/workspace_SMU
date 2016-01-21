from __future__ import division
#
import os, time, csv
#
from _setting import dt_dir
# TODO  
# set driver_ext_folder 
driver_ext_folder = None

def calc_monthly_stats():
    for fn in os.listdir(driver_ext_folder):
        if not fn.endswith('.csv'): continue
        monthly_stats = {}
        with open('%s/%s' % (driver_ext_folder, fn), 'rb') as rCsvfile:
            reader = csv.reader(rCsvfile)
            headers = reader.next()
            index_s_time = headers.index('start-time')
            index_t_mode, index_fare = headers.index('trip-mode'), headers.index('fare')
            for r in reader:
                yymm = time.strftime('%y%m', time.localtime(eval(r[index_s_time])))
                t_mode, fare = eval(r[index_t_mode]), eval(r[index_fare])
                if not monthly_stats.has_key(yymm):
                    monthly_stats[yymm] = [0] * len(['DInAP-PInAP_num', 'DInAP-POutAP_num', 'DOutAP-PInAP_num', 'DOutAP-POutAP_num',
                                                     'DInAP-PInAP_fare', 'DInAP-POutAP_fare', 'DOutAP-PInAP_fare', 'DOutAP-POutAP_fare' 
                                                     ])
                monthly_stats[yymm][t_mode] += 1
                monthly_stats[yymm][t_mode + 4] += fare 
            
            
        with open('%s/ext/summary_%s' % (driver_folder, fn), 'wt') as wCsvfile:
            writer = csv.writer(wCsvfile)
            
            new_headers = ['YYMM',
                            'DInAP-PInAP_num', 'DInAP-POutAP_num', 'DOutAP-PInAP_num', 'DOutAP-POutAP_num',
                            'DInAP-PInAP_fare', 'DInAP-POutAP_fare', 'DOutAP-PInAP_fare', 'DOutAP-POutAP_fare' ]
            
            writer.writerow(new_headers)
            for k, v in monthly_stats.iteritems():
                writer.writerow([k] + v)