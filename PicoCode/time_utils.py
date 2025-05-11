# time_utils.py
import time
from config import TIMEZONE_OFFSET

def localtime_offset(offset_hours=TIMEZONE_OFFSET):
    return time.localtime(time.time() + offset_hours * 3600)
