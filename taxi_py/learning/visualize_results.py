from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports._setting import IN_AIRPORT, OUT_AIRPORT
from supports.handling_pkl import load_picle_file
from supports.charts import grid_charts
#

day_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
id_dow = {dow : i for i, dow in enumerate(day_of_week)}
time_slots = range(24)
locations = [IN_AIRPORT, OUT_AIRPORT]

def run():
    process_files('0901')
#     for y in xrange(9, 11):
#         for m in xrange(1, 13):
#             yymm = '%02d%02d' % (y, m) 
#             if yymm in ['0912', '1010']:
#                 continue
#             process_files(yymm)
    
def process_files(yymm):
    Qsa_value, _ = load_picle_file('%s/q-value-prods-%s.pkl' % (for_learning_dir, yymm))
    decision_inAP, decision_outAP = [], []
    for s1 in day_of_week:
        for s2 in time_slots:
            for s3 in locations:
                print (s1, s2, s3), Qsa_value[(s1, s2, s3, IN_AIRPORT)], Qsa_value[(s1, s2, s3, OUT_AIRPORT)]
                max_a = IN_AIRPORT if Qsa_value[(s1, s2, s3, IN_AIRPORT)] >= Qsa_value[(s1, s2, s3, OUT_AIRPORT)] else OUT_AIRPORT
                if s3 == IN_AIRPORT:
                    decision_inAP.append([s1, s2, max_a])
                else:
                    decision_outAP.append([s1, s2, max_a])
#     draw_chart()
    for s1, s2, a in decision_inAP:
        print s1, s2, a 
    _data = [
             [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP],
             [(s2, id_dow[s1], a) for s1, s2, a in decision_outAP]
             ]
    titles = ['Decision in the airport', 'Decision outside of the airport']
    grid_charts(('24 Time slots', []), ('', day_of_week), ['In Airport', 'Out Airport'], titles, _data, '%s/q-value-prods-%s.pdf' % (for_learning_dir, yymm))
    
    
if __name__ == '__main__':
    run()
