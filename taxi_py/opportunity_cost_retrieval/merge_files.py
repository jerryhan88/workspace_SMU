from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import op_costs_dir, op_cost_summary
from supports.etc_functions import get_all_files
#
import datetime, csv

def run():
    dur_fare = {}
    cur_timestamp = datetime.datetime(2009, 1, 1, 0) 
    last_timestamp = datetime.datetime(2011, 1, 1, 0)
    time_period_order = []
    while cur_timestamp < last_timestamp:
        yyyy, mm, dd, hh = cur_timestamp.year, cur_timestamp.month, cur_timestamp.day, cur_timestamp.hour
        time_period_order.append((str(yyyy - 2000), str(mm), str(dd), str(hh)))
        cur_timestamp += datetime.timedelta(hours=1)
    #
    print 'start the file; summary'
    csv_files = get_all_files(op_costs_dir, 'op-cost-', '.csv')
    for fn in csv_files:
        with open('%s/%s' % (op_costs_dir, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            #
            id_yy, id_mm, id_dd, id_hh = headers.index('yy'), headers.index('mm'), headers.index('dd'), headers.index('hh')
            id_total_dur, id_total_fare = headers.index('total-duration'), headers.index('total-fare')
            id_ap_queue, id_ap_dur, id_ap_fare = headers.index('ap-queue'), headers.index('ap-duration'), headers.index('ap-fare')
            id_op_cost = headers.index('op-cost-sec')
            values_indices = [id_total_dur, id_total_fare, id_ap_queue, id_ap_dur, id_ap_fare, id_op_cost]
            for row in reader:
                yy, mm, dd, hh = row[id_yy], row[id_mm], row[id_dd], row[id_hh]
                k = (yy, mm, dd, hh)
                if not dur_fare.has_key(k):
                    dur_fare[k] = [0 for _ in values_indices]
                for i, iv in enumerate(values_indices):
                    dur_fare[k][i] += eval(row[iv])
                     
    with open(op_cost_summary, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh', 'total-duration', 'total-fare', 'ap-queue', 'ap-duration', 'ap-fare', 'op-cost-sec']
        writer.writerow(header)
        for k in time_period_order:
            if not dur_fare.has_key(k):
                continue
            total_dur, total_fare, ap_queue, ap_dur, ap_fare, _ = dur_fare[k]
            yy, mm, dd, hh = k
            ap_out_fare = total_fare - ap_fare
            ap_out_dur = total_dur - (ap_queue + ap_dur)
            if ap_out_dur == 0:
                continue
            op_cost = ap_out_fare / ap_out_dur
            writer.writerow([
                             yy, mm, dd, hh,
                             total_dur, total_fare, ap_queue, ap_dur, ap_fare,
                             op_cost
                             ])
    print 'end the file; summary'
if __name__ == '__main__':
    run()
