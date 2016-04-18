from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports._setting import DAY_OF_WEEK, TIME_SLOTS, IN_AP, OUT_AP
from supports.handling_pkl import load_picle_file
from supports.charts import grid_charts
#
id_dow = {dow : i for i, dow in enumerate(DAY_OF_WEEK)}

def run():
    process_files('0903')
#     for y in xrange(9, 11):
#         for m in xrange(1, 13):
#             yymm = '%02d%02d' % (y, m) 
#             if yymm in ['0912', '1010']:
#                 continue
#             process_files(yymm)
    
def process_files(yymm):
#     Qsa_value, _ = load_picle_file('%s/q-value-fare-dur-%s.pkl' % (for_learning_dir, yymm))
    Qsa_value, _ = load_picle_file('/Users/JerryHan88/taxi/for_learning/ALPHA-0.70-GAMMA-0.30/ALPHA-0.70-GAMMA-0.30-q-value-fare-dur-0904.pkl')
    decision_inAP, decision_outAP = [], []
    for s1 in DAY_OF_WEEK:
        for s2 in TIME_SLOTS:
            for s3 in [IN_AP, OUT_AP]:
#                 print (s1, s2, s3), Qsa_value[(s1, s2, s3, IN_AP)], Qsa_value[(s1, s2, s3, OUT_AP)]
                max_a = IN_AP if Qsa_value[(s1, s2, s3, IN_AP)] >= Qsa_value[(s1, s2, s3, OUT_AP)] else OUT_AP
                c = 0 if max_a == IN_AP else 1
                if s3 == IN_AP:
                    decision_inAP.append([s1, s2, c])
                else:
                    decision_outAP.append([s1, s2, c])
    for s1, s2, a in decision_inAP:
        print 'inAP', s1, s2, a
    for s1, s2, a in decision_outAP:
        print 'outAP', s1, s2, a  
    _data = [
             [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP],
             [(s2, id_dow[s1], a) for s1, s2, a in decision_outAP]
             ]
    titles = ['Decision in the airport', 'Decision outside of the airport']
    grid_charts(('24 Time slots', []), ('', DAY_OF_WEEK), ['In Airport', 'Out Airport'], titles, _data, '%s/q-value-fare-dur-%s.pdf' % (for_learning_dir, yymm))
    
    
if __name__ == '__main__':
    process_files('')
