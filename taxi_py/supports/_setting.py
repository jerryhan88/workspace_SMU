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

DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)

shift_dir = prefix + '/shifts'
full_shift_dir = shift_dir + '/full_time_drivers' 
#
log_ext_dir = prefix + '/logs'
log_last_day_dir = log_ext_dir + '/logs_last_day'

# log_ext_dir = prefix + '/logs_ext_backup'
# log_last_day_dir = log_ext_dir + '/logs_last_day'

#
trip_ext_dir = prefix + '/trips'