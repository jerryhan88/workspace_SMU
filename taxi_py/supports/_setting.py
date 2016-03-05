from __future__ import division

import platform, os, sys
#, csv

# Add the root path for packages I made  
sys.path.append(os.getcwd() + '/..')

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
    path_to_ori_data = '/home/taxi'
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi'
    path_to_ori_data = '/Users/JerryHan88/taxi'
else:
    # TODO
    assert False, 'Windows?'
assert prefix

DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)

shift_dir = prefix + '/shifts'


