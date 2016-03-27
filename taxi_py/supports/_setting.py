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
    assert False, 'Windows?'
assert prefix
#
DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)
Q_LIMIT_MIN, Q_LIMIT_MAX = 0, 3600
#
shifts_dir = prefix + '/shifts'
full_shift_dir = shifts_dir + '/full_time_drivers' 
#
logs_dir = prefix + '/logs'
log_last_day_dir = logs_dir + '/logs_last_day'
#
trips_dir = prefix + '/trips'
aiport_trips_dir = trips_dir + '/airport_trips' 
#
op_costs_dir = prefix + '/op_costs'
op_cost_summary = op_costs_dir + '/op-cost-summary.csv' 
#
individual_dir = prefix + '/individual-summary'
individual_detail_dir = prefix + '/individual-detail-summary'