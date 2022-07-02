from utils import *
from models import *


def preprocess_data(data, is_jalali=False):
    fixed_data = [[string_to_datetime(entry[0], is_jalali), entry[1]] for entry in data]
    df = pd.DataFrame(fixed_data, columns=["date", "value"])
    df.sort_values(by="date", ascending=True, inplace=True)
    df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
    return df


def interpolate_data(data, config):
    is_jalali = config.type is DateFormatEnum.shamsi
    df = preprocess_data(data, is_jalali)

    # Scale to config timescale
    timescale = "M"
    if config.time is InterpolationTimeEnum.daily:
        timescale = "D"
    elif config.time is InterpolationTimeEnum.hourly:
        timescale = "h"
    elif config.time is InterpolationTimeEnum.minute:
        timescale = "1T"
    df = df.resample(timescale).mean()

    # Interpolate
    if config.interpolation is InterpolationType.linear:
        df = df.interpolate(method="linear", axis=0)
    elif config.interpolation is InterpolationType.nearest:
        df = df.interpolate(method="nearest", axis=0)
    elif config.interpolation is InterpolationType.spline:
        df = df.interpolate(method="spline", axis=0, order=3)
    elif config.interpolation is InterpolationType.polynomial:
        df = df.interpolate(method="polynomial", axis=0, order=3)
    elif config.interpolation is InterpolationType.slinear:
        df = df.interpolate(method="slinear", axis=0)

    # Properly format date string to return
    dates = [datetime_to_string(np_dt_to_dt(x, is_jalali)) for x in df.index.values]
    values = df.value.tolist()
    return [list(x) for x in zip(dates, values)]