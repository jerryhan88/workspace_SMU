from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports.etc_functions import get_all_files
from supports._setting import individual_dir
#
import csv
#
def run():
    csv_files = get_all_files(individual_dir, 'individual-', '.csv')
    for yy in ['09', '10']:
        with open('%s/Y%s-summary-individual.csv' % (individual_dir, yy), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['yy', 'mm', 'did', 'ap-queue-time', 'ap-dur', 'ap-fare', 'ap-prod', 'op-cost', 'ap-eco-profit', 'total-pro-dur', 'total-fare', 'total-prod']
            writer.writerow(new_headers)
            for fn in csv_files:
                _, yymm = fn[:-len('.csv')].split('-')
                fn_yy = yymm[:2] 
                if fn_yy != yy:
                    continue
                with open('%s/%s' % (individual_dir, fn), 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    id_ap_fare, id_total_fare = headers.index('ap-fare'), headers.index('total-fare')
                    id_total_dur = headers.index('total-pro-dur')
                    for row in reader:
                        if eval(row[id_ap_fare]) == 0 or eval(row[id_total_fare]) == 0 or eval(row[id_total_dur]) == 0:
                            continue
                        writer.writerow(row)

if __name__ == '__main__':
    run()
