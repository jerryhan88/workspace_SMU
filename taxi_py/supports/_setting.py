from __future__ import division

import platform, sys

# Check environments and set a prefix for finding files and libraries
plf = platform.platform()
if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi'
    py_vinfo = sys.version_info
    if py_vinfo.major == 2 and py_vinfo.minor == 7:
        sys.path.append('/home/ckhan/local/lib/python2.7/site-packages')
        sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
    else:
        print 'This python is not 2.7 version'
        assert False
    #
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi'
else:
    # TODO
#     assert False, 'Windows?'
    prefix = 'C:\Users/ckhan.2015/taxi'
assert prefix
#
ap_poly_info = '../airport_polygons'
IN_AP, OUT_AP = 'O', 'X'
ns_poly_info = '../night_safari_polygon'
IN_NS, OUT_NS = 'O', 'X'
#
DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)
DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS = range(4)
#
HOUR, MINUTE = 60 * 60, 60
CENT = 100
Q_LIMIT_MIN, Q_LIMIT_MAX = 0, HOUR * 3
MAX_DURATION = HOUR 
PROD_LIMIT = 65 / HOUR * CENT
#
sh_prefix, trip_prefix, ap_trip_prefix, ns_trip_prefix = 'shift-all-', 'whole-trip-', 'airport-trip-', 'nightsafari-trip-'
general_dur_fare_prefix, ap_dur_fare_q_time_prefix, ns_dur_fare_q_time_prefix = 'gdf-', 'adfqt-', 'ndfqt-'
#
shifts_dir = prefix + '/shifts'
full_shift_dir = shifts_dir + '/full_time_drivers' 
#
logs_dir = prefix + '/logs'
log_last_day_dir = logs_dir + '/logs_last_day'
#
merged_trip_dir = prefix + '/trips_merged'
trips_dir = prefix + '/trips'
for_learning_dir = prefix + '/for_learning'
for_full_driver_dir = prefix + '/full_drivers_trips_q_comparision'
aiport_trips_dir = trips_dir + '/airport_trips'
nightsafari_trips_dir = trips_dir + '/nightsafari_trips'
hourly_summary = trips_dir + '/hourly_summary'
#
op_costs_dir = prefix + '/op_costs'
general_dur_fare_dir = op_costs_dir + '/general_dur_fare'
ap_dur_fare_q_time_dir = op_costs_dir + '/ap_dur_fare_q_time'
ns_dur_fare_q_time_dir = op_costs_dir + '/ns_dur_fare_q_time'
op_cost_summary = op_costs_dir + '/op-cost-summary.csv'
out_ap_prod_dir = prefix + '/out_ap_prod'
out_ns_prod_dir = prefix + '/out_ns_prod'
 
#
individual_dir = prefix + '/individual-summary'
individual_detail_dir = prefix + '/individual-detail-summary'
#
# For Q-learning
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)
#
TIME_ALARM = MINUTE * 5