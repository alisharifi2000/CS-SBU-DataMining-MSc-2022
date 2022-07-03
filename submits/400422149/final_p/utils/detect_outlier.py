import pandas as pd
from scipy import stats
import numpy as np


def clean_pd(df):
    df1 = df.copy()
    if 'time' in df.columns:
        df1.drop(['time'], axis=1, inplace=True)

        return df1

    else:
        df1.drop(['id'], axis=1, inplace=True)
        return df1


def method1(df):
    df1 = df.copy()
    c_names = df1.columns
    new = [c + '_method1' for c in c_names]
    df1.columns = new
    mean = df1.mean()
    mask = df1 > mean
    return mask


def method2(df):
    df1 = df.copy()
    c_names = df1.columns
    new = [c + '_method2' for c in c_names]
    df1.columns = new
    z = np.abs(stats.zscore(df1))
    threshold = 1.8
    mask = z > threshold
    return mask


def method3(df):
    df1 = df.copy()
    c_names = df.columns
    new = [c + '_method3' for c in c_names]
    df1.columns = new

    q1 = np.percentile(df1, 25,
                       interpolation='midpoint')
    Q3 = np.percentile(df1, 75,
                       interpolation='midpoint')
    IQR = Q3 - q1
    upper_n = Q3 + (1.5 * IQR)
    lower_n = q1 - (1.5 * IQR)
    #upper = df >= upper_n
    upper = df1 <= upper_n
    #lower = df <= lower_n
    lower = df1 >= lower_n


    mask = lower & upper
    mask = ~mask
    return mask


def detect_outlier(data, is_timeseries):
    clean_data = clean_pd(data)
    if is_timeseries:
        mask1 = method1(clean_data)
        mask2 = method2(clean_data)
        mask3 = method3(clean_data)
        mask1['time_method1'] = data.time
        mask2['time_method2'] = data.time
        mask3['time_method3'] = data.time
        result = pd.concat([mask1, mask2, mask3], axis=1)

        return result

    else:
        mask1 = method1(clean_data)
        mask2 = method2(clean_data)
        mask3 = method3(clean_data)
        mask1['id_method1'] = data.id
        mask2['id_method2'] = data.id
        mask3['id_method3'] = data.id
        result = pd.concat([mask1, mask2, mask3], axis=1)
        return result
