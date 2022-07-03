import pandas as pd
import json
import numpy as np


def handle_outlier(odata):
    odata['data']['method1'] = outlier_detection1(odata)
    d_df = pd.DataFrame(list(odata['data']['method1']))
    d_df['id'] = pd.DataFrame(list(odata['data']['id'].values()))
    odata['data']['method2'] = outlier_detection2(odata)

    output = {'data': {}}
    for K in ['id', 'method1', 'method2']:
        output['data'][K] = {}

    for i, (k, v) in enumerate(odata['data']['id'].items()):
        output['data']['id'][k] = v
        output['data']['method1'][k] = odata['data']['method1'][i]
        output['data']['method2'][k] = odata['data']['method2'][i]

    return output


def outlier_detection1(data):
    jdata = json.dumps(data)
    data = pd.read_json(jdata)

    idd = data['data']['id']
    feature = data['data']['feature'].values()
    a = []
    a = list(data['data']['feature'].values())
    a = np.array(a)
    upper_limit = np.mean(a) + 3 * np.std(a)
    lower_limit = np.mean(a) - 3 * np.std(a)
    o1 = []
    for i in a:
        if i > upper_limit:
            o1.append('False')
        elif i < lower_limit:
            o1.append('False')
        else:
            o1.append('True')
    return o1


def outlier_detection2(data):
    jdata = json.dumps(data)
    data = pd.read_json(jdata)

    idd = data['data']['id']
    feature = data['data']['feature'].values()
    a = []
    a = list(data['data']['feature'].values())
    a = np.array(a)
    q1, q3 = np.percentile(sorted(a), [25, 75])

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    o2 = []
    for i in a:
        if i > upper_bound:
            o2.append('False')
        elif i < lower_bound:
            o2.append('False')
        else:
            o2.append('True')
    return o2


odata = {
    "data": {
        "id": {
            "0": 1,
            "1": 2,
            "2": 3,
            "3": 4,
            "4": 5,
            "5": 6
        },
        "feature": {
            "0": 100,
            "1": 20,
            "2": 35,
            "3": 67,
            "4": 89,
            "5": 90
        }
    },
    "config": {
        "time_series": 'false'
    }
}
handle_outlier(odata)
