from utils import *
from models import *

# Z-Score
def outlier_method_1(data_column, thresh=1.25):
    """
    Calculate z-score for every given element in a column.
    Input:
        data_column: np.ndarray-like structure of values.
        thresh: maximum z-score before a specific value is considered to be an outlier.
    Output:
        List with the same shape as data_column containing booleans. If each corresponsing value in data_column had a higher z-score than thresh, the corresponding value in the output would be True. Otherwise, False.
    """
    z_scores = calculate_z_score(data_column)
    return [abs(score) > thresh for score in z_scores]


# IQR
def outlier_method_2(data_column):
    """
    Find outliers via IQR
    Input:
        data_column: np.ndarray-like structure of values.
    Output:
        List with the same shape as data_column containing booleans. If each corresponsing value in data_column was not in the middle section of the distribution, the corresponding value in the output would be True. Otherwise, False.
    """
    q1 = data_column.quantile(0.25)
    q3 = data_column.quantile(0.75)
    iqr = q3 - q1
    return (data_column < (q1 - 1.5 * iqr)) | (data_column > (q3 + 1.5 * iqr))


def detect_outliers(data, config):
    """
    Input:
        data: The np.ndarray-like data we'll be performing operations on
        config: The configuration as specified in ./models, denoting if index is a time series or not
    Output: The outlier detection results in the form of a list with the shape (n, 3), with each row being [index: datetime_str or number, is outlier via method 1: Bool, is outlier via method 2: Bool], ready to be sent back to the requester..
    """
    df = None
    if config.time_series:
        fixed_data = [[string_to_datetime(entry[0]), entry[1]] for entry in data]
        df = pd.DataFrame(fixed_data, columns=["date", "value"])
        df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
    else:
        df = pd.DataFrame(data, columns=["idx", "value"])
        df.set_index(df["idx"], inplace=True)

    method_1_res = outlier_method_1(df["value"])
    df["method_1"] = method_1_res

    method_2_res = outlier_method_2(df["value"])
    df["method_2"] = method_2_res

    idx = df.index
    if config.time_series:
        idx = [datetime_to_string(np_dt_to_dt(x)) for x in df.index.values]
    return [list(x) for x in zip(idx, method_1_res, method_2_res)]
