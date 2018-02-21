import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kt_tv_ch import *

def test_get_channel():
    channels = get_all_channels()
    print(channels)
    assert len(channels) > 0

print(get_schedule(85))

#test_get_channel()


