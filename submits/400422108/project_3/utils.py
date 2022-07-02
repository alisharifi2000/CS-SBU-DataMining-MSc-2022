import pandas as pd
from khayyam import JalaliDatetime
from datetime import datetime
import numpy as np
from pandas.tseries.offsets import DateOffset
from scipy import stats


unix_epoch = np.datetime64(0, "s")
one_second = np.timedelta64(1, "s")
timeformat = "%Y-%m-%dT%H:%M:%S"


def string_to_datetime(date_string, is_jalali=False):
    time_format_string = timeformat
    if is_jalali:
        return JalaliDatetime.strptime(date_string, time_format_string).todate()
    return datetime.strptime(date_string, time_format_string)


def np_dt_to_dt(dt64, is_jalali=False):
    seconds_since_epoch = (dt64 - unix_epoch) / one_second
    fixed_dt = datetime.utcfromtimestamp(seconds_since_epoch)
    if is_jalali:
        return JalaliDatetime(fixed_dt)
    return fixed_dt


def datetime_to_string(date_string):
    return date_string.strftime(timeformat)


def calculate_z_score(data):
    z_score_array = stats.zscore(data)
    return z_score_array
