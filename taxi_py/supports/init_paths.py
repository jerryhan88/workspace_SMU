from __future__ import division

import platform, os, sys

# Add the root path for packages I made  
sys.path.append(os.getcwd() + '/..')

# Check environments and set a prefix for finding files and libraries
plf = platform.platform()
if plf.startswith('Linux'):
    # This would be the server
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
    pass
else:
    # TODO
    assert False, 'Windows?'

def get_prefix():
    if plf.startswith('Linux'):
        # This would be the server
        prefix = '/home/ckhan/taxi'
    elif plf.startswith('Darwin'):
        # This is my Macbook Pro
        prefix = '/Users/JerryHan88/taxi'
    else:
        # TODO
        assert False, 'Windows?'
    assert prefix
    return prefix