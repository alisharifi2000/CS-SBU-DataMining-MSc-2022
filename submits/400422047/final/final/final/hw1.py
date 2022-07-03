import json

import khayyam
import pandas as pd


def json_to_timeseries(dictdata):
    jdata=json.dumps(dictdata)
    data=pd.read_json(jdata)
    data.time = pd.to_datetime(data.time)
    return data


def interpolate1(inputdata):
    config = inputdata['config']

    if config['type'] == 'miladi':

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

        elif config['time'] == 'monthly':
            data = data.set_index('time')
            data = data.resample('MS')
            if config['interpolation'] == 'polynomial':
                data = data.interpolate(method=config['interpolation'], order=2)
                data.reset_index(inplace=True)
            else:
                data = data.interpolate(method=config['interpolation'])
                data.reset_index(inplace=True)
        d = data.to_dict()
        output1 = {'data': d}
        return output1

    if config['type'] == 'shamsi':
        jdata = json.dumps(inputdata['data'])
        data = pd.read_json(jdata)
        #data = pd.DataFrame(inputdata['data'])

        ntime = []
        aa = data['time'].apply(lambda x: x.split('-'))
        for j in aa:
            aaa = []
            for i in j:
                aaa.append(int(i))
            ntime.append(khayyam.JalaliDate(aaa[0], aaa[1], aaa[2]).todate())
        data['time'] = ntime
        data.time = pd.to_datetime(data.time)
        data = data.set_index('time')
        if config['time'] == 'daily':

            data = data.resample('D').mean()

        elif config['time'] == 'monthly':

            data = data.resample('M').mean()

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
        output1 = {'data': d}
        output1

        return output1




