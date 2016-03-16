from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import full_shift_dir, trips_dir, aiport_trips_dir, individual_dir
from supports.etc_functions import remove_creat_dir
from supports.handling_pkl import load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.logger import logging_msg
#
import csv
import pandas as pd
from traceback import format_exc
#
sh_full_prefix, trip_prefix, ap_trip_op_ep_prefix = 'shift-full-time-', 'whole-trip-', 'ap-trip-op-ep-'
monthly_full_did_prefix = 'full-time-drivers-'
#
SEC = 60
#
def run():
    remove_creat_dir(individual_dir)
#     process_files('1007')
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                yymm = '%02d%02d' % (y, m) 
                if yymm in ['0912', '1010']:
                    continue
                put_task(process_files, [yymm])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    full_dids = sorted([eval(x) for x in load_picle_file('%s/%s%s.pkl' % (full_shift_dir, monthly_full_did_prefix, yymm))])
    s_df = pd.read_csv('%s/%s%s.csv' % (full_shift_dir, sh_full_prefix, yymm))
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (aiport_trips_dir, ap_trip_op_ep_prefix, yymm))
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    with open('%s/individual-%s.csv' % (individual_dir, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did',
                'ap-queue-time', 'ap-dur', 'ap-fare', 'ap-prod', 'op-cost', 'ap-eco-profit',
                'total-pro-dur', 'total-fare', 'total-prod']
        writer.writerow(headers)
    
        for did in full_dids:
            did_ap = ap_trip_df[(ap_trip_df['did'] == did)]
            ap_qu, ap_dur, ap_fare, ap_prod, ap_op_cost, ap_eco_profit = 0, 0, 0, 0, 0, 0
            if len(did_ap) != 0:
                ap_qu, ap_dur = sum(did_ap['queue-time']), sum(did_ap['duration'])
                ap_fare = sum(did_ap['fare'])
                ap_prod = ap_fare / (ap_qu + ap_dur)
                ap_op_cost, ap_eco_profit = sum(did_ap['op-cost']), sum(did_ap['economic'])
            #
            did_sh = s_df[(s_df['driver-id'] == did)]
            pro_dur = sum(did_sh['productive-duration']) * SEC
        
            did_wt = trip_df[(trip_df['did'] == did)]
            total_fare = sum(did_wt['fare'])
            total_prod = total_fare / pro_dur
            writer.writerow([yy, mm, did,
                             ap_qu, ap_dur, ap_fare, ap_prod, ap_op_cost, ap_eco_profit,
                             pro_dur, total_fare, total_prod])
        
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
    
