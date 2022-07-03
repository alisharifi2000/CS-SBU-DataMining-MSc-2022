import json

import khayyam as khayyam
import pandas as pd


def json_to_timeseries(dictdata):
    jdata = json.dumps(dictdata)
    data = pd.read_json(jdata)
    data.time = pd.to_datetime(data.time)
    return data


def interpolate2(inputdata):
    data = json_to_timeseries(inputdata['data'])
    config = inputdata['config']

    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D')
        if config['interpolation'] == 'polynomial':
            data = data.interpolate(method=config['interpolation'], order=2)
            data.reset_index(inplace=True)
        else:
            data = data.interpolate(method=config['interpolation'])
            data.reset_index(inplace=True)
        m = []
        for i in data['time']:
            k = khayyam.JalaliDate(i)
            m.append(k.isoformat())
        data['time'] = m

    elif config['time'] == 'monthly':
        data = data.set_index('time')

        data = data.resample('MS')
        if config['interpolation'] == 'polynomial':
            data = data.interpolate(method=config['interpolation'], order=2)
            data.reset_index(inplace=True)
        else:
            data = data.interpolate(method=config['interpolation'])
            data.reset_index(inplace=True)
        m = []
        for i in data['time']:
            k = khayyam.JalaliDate(i)
            m.append(k.isoformat())
        data['time'] = m

    d = data.to_dict()
    output2 = {'data': d}
    output2

    return output2


inputdata={
  "data": {
    "time": {
      "0": "2020-01-01",
      "1": "2020-02-01",
      "2": "2020-04-01"
    },
    "vol": {
      "0": 20,
      "1": 40,
      "2": 100
    }
  },
  "config": {
    "type": "miladi",
    "time": "monthly",
    "interpolation": "linear"
  }
}
