import gzip
import khayyam
from flask import make_response, json
import pandas as pd
import numpy as np
from flask import request

def response_message(data=None, status=200):
    if status in range(200, 400):
        content = gzip.compress(json.dumps(data, ensure_ascii=False, indent=3, default=convert,
                                           sort_keys=False).encode('utf8'), 5)
    else:
        content = gzip.compress(
            json.dumps({'message': data, 'status': 'error'}, ensure_ascii=False, indent=3).encode('utf-8'), 5)
    response = make_response(content, status)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


def convert(o):
    if isinstance(o, np.int64):
        return int(o)
    if isinstance(o, np.bool_):
        if o:
            return True
        else:
            return False
    if pd.isna(o):
        return None


def read_json_time_series(data):
    json_data = json.dumps(data)
    data = pd.read_json(json_data)
    data.time = pd.to_datetime(data.time, unit='ms')
    return data


def convert_json_to_df(data):
    json_data = json.dumps(data)
    data = pd.read_json(json_data)
    return data


def get_requests_and_convert_to_json():
    req = request.get_json()
    data = read_json_time_series(req["data"])
    return data, req


def convert_date_to_shamsi(data):
    data2 = data
    shamsi = []
    for i in data.time:
        date = khayyam.JalaliDate(i)
        shamsi.append(date)
    shamsi_df = pd.DataFrame(shamsi, columns=['shamsi'])
    data2.time = shamsi_df.shamsi
    return data2
