from ast import Raise
import pandas as pd
import json 

def interpolate_function(series, config):
    # df2 = pd.read_json(series, orient ='index').T
    # if config['type'] == 'miladi':
    #     if config['time'] == 'daily':
    #         df = df2.copy()
    #         df['time'] = pd.to_datetime(df['time'])

    #         df.index = df['time']
    #         del df['time']
    #         df['vol'] = df['vol'].interpolate()
    # raise Exception(df)
    # return df.to_dict()

    import khayyam as kh 
    import pandas as pd         
    data = pd.DataFrame(series)
    config = pd.Series(config)    
    if config['type'] == 'shamsi':
        dates = []
        for d in data.time:
            x = list(d.split('/'))
            temp = kh.JalaliDatetime(x[0], x[1], x[2]).todatetime()
            temp = pd.to_datetime(temp)
            dates.append(temp)
        data.time = dates
    else:
        data.time = pd.to_datetime(data.time, infer_datetime_format=True)


    if config['time'] == 'daily':
        data.time = pd.to_datetime(data.time.dt.strftime('%Y-%m-%d'), infer_datetime_format=True)
    else:
        data.time = pd.to_datetime(data.time.dt.strftime('%Y-%m'), infer_datetime_format=True)


    start = data.time[0]
    end = data.time[-1]
    if config['time'] == 'daily':
        index = pd.date_range(start=start, end=end, freq=eval('pd.offsets.Day(1)'))
    else:
        index = pd.date_range(start=start, end=end, freq=eval('pd.offsets.MonthBegin(1)'))


    data.index = data.time
    for i in index:
        if i not in data.time.to_list():
            data.loc[i] = None

    data = data.sort_index()
    out = data.drop('time', axis=1)

    if config.interpolation == 'linear':
        out.vol = out.vol.interpolate()
    elif config.interpolation == 'polynomial':
        out.vol = out.vol.interpolate(method='polynomial', order=int(config.interpolation[5:]))

    out = out.reset_index().to_json()
    out = json.loads(out)
    out = {'data': out}

    return out

def interpolate_convert(series, config):
    import khayyam as kh 
    import pandas as pd         
    data = pd.DataFrame(series)
    config = pd.Series(config)    

    data.time = pd.to_datetime(data.time, infer_datetime_format=True)  

    if config['time'] == 'daily':
        data.time = pd.to_datetime(data.time.dt.strftime('%Y-%m-%d'), infer_datetime_format=True)
    else:
        data.time = pd.to_datetime(data.time.dt.strftime('%Y-%m'), infer_datetime_format=True)


    start = data.time[0]
    end = data.time[-1]
    if config['time'] == 'daily':
        index = pd.date_range(start=start, end=end, freq=eval('pd.offsets.Day(1)'))
    else:
        index = pd.date_range(start=start, end=end, freq=eval('pd.offsets.MonthBegin(1)'))


    data.index = data.time
    for i in index:
        if i not in data.time.to_list():
            data.loc[i] = None

    data = data.sort_index()
    out = data.drop('time', axis=1)

    if config.interpolation == 'linear':
        out.vol = out.vol.interpolate()
    elif config.interpolation == 'polynomial':
        out.vol = out.vol.interpolate(method='polynomial', order=int(config.interpolation[5:]))

    out = out.reset_index().to_json()
    out = json.loads(out)
    out = {'data': out}

    return out

def OutlierDetector(data, config, feature):
    import pandas as pd 
    THRESHOLDS = [0.4, 0.6]
    df = data.copy()
    Q1 = df.quantile(THRESHOLDS[0])
    Q3 = df.quantile(THRESHOLDS[1])
    IQR = Q3 - Q1
    idx = df[((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)].index
    idx = idx.to_list()
    outliers1 = ['true' if data.index[i] in idx else 'false' for i in range(len(data))]



    from statsmodels.tsa.ar_model import AutoReg
    model = AutoReg(feature, lags=len(feature)//3)
    model_fit = model.fit()
    predictions = model_fit.predict(start=0, end=len(feature))

    outliers2 = ['false' for i in range(len(feature))]
    for i in range(1, len(feature)): 
        if abs(predictions[i] - feature[i]) >= 0.2: 
            outliers2[i] = 'true' 





    import numpy as np
    from sklearn.cluster import DBSCAN
    def Scaler(data):
        values = data.feature.copy()
        min_val = abs(values.min())
        values += min_val
        values /= values.max()
        return values
    feature = Scaler(data)
    X = feature.to_numpy().reshape((len(feature), 1))

    clustering = DBSCAN(eps=0.1, min_samples=len(feature)//20 + 2).fit(X)

    outliers3 = list(map(lambda x:'true' if x==-1 else 'false', 
            clustering.labels_))

    if config.time_series: 
        data['method1'] = outliers1
        data['method2'] = outliers2
    else: 
        data['method1'] = outliers1
        data['method2'] = outliers3
        
    
    out = data.reset_index().to_json()
    out = json.loads(out)
    out = str({'data': out})

    return out

def balance_imbalance(data, config): 
    import pandas as pd 
    if config.method == 'SMOTE': 
        min_num = data['class'].value_counts().values[-1]
        if min_num <= 1: 
            data = pd.concat([data, data]).reset_index().drop('index', axis=1)
        from imblearn.over_sampling import SMOTE
        oversample = SMOTE(k_neighbors = min(min_num, 6))
        X, y = oversample.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])

    elif config.method == 'Oversampling': 
        from imblearn.over_sampling import RandomOverSampler 
        ros = RandomOverSampler(random_state=1)
        X, y = ros.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])

    elif config.method == 'Tomeklinks': 
        from imblearn.under_sampling import TomekLinks 
        tl = TomekLinks(sampling_strategy = 'auto')
        X, y = tl.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])

    elif config.method == 'Clustercentroids': 
        from imblearn.under_sampling import ClusterCentroids 
        cc = ClusterCentroids()
        X, y = cc.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])

    elif config.method == 'UnderSampling': 
        from imblearn.over_sampling import RandomUnderSampler  
        rus = RandomUnderSampler(random_state=1)
        X, y = rus.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])


    X['class'] = y
    X['id'] = X.index.to_numpy() + 1

    out = pd.DataFrame(X, columns=data.columns)
    out = out.reset_index().to_json()
    out = json.loads(out)
    out = {'data': out}

    return out