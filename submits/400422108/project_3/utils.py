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
    """
    Convert string into datetime.datetime. Datetime strings are assumed to have the format: Year-Month-DayTHour:Minute:second
    """
    time_format_string = timeformat
    if is_jalali:
        return JalaliDatetime.strptime(date_string, time_format_string).todate()
    return datetime.strptime(date_string, time_format_string)


def np_dt_to_dt(dt64, is_jalali=False):
    """
    Convert numpy.datetime64 to datetime.datetime
    """
    seconds_since_epoch = (dt64 - unix_epoch) / one_second
    fixed_dt = datetime.utcfromtimestamp(seconds_since_epoch)
    if is_jalali:
        return JalaliDatetime(fixed_dt)
    return fixed_dt


def datetime_to_string(date_string):
    """
    Convert datetime into string with format: Year-Month-DayTHour:Minute:second
    """
    return date_string.strftime(timeformat)


def calculate_z_score(data):
    """
    Calculate z-score.
    Input:
        data: np.ndarray-like data type containing numerical values
    Output:
        Corresponding z-scores for every element.
    """
    z_score_array = stats.zscore(data)
    return z_score_array


def split_data(data):
    """
    Given a np.ndarray with the shape (n, k), split the array into two lists with the shapes (n, k-1) and (n, 1) where the second array only consists of the last element of each row. (Aka the class labels)
    """
    return np.array_split(np.asarray(data), len(data[0]) - 1, axis=1)


def reconstruct_data(x, y):
    """
    Given 2 np.ndarrays with the shape (n, k-1) & (n, 1), reconstruct into one list ready to send back to the requester
    """

    y = y.reshape((-1, 1))
    return np.append(x, y, axis=1).tolist()
