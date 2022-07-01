from flask import Flask, request
from utils.common import response_message, read_json_time_series
from utils.interpolation_methods import linear_interpolation
from khayyam import *
from datetime import datetime
import json
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from prophet import Prophet
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

@app.errorhandler(500)
def handle_500_error(e):
    return response_message("Internal error(have you checked formatting?)")
@app.errorhandler(400)
def handle_400_error(e):
    return response_message("Couldn't process your request, check the structure of your request before trying again.")

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')

def tomiladi(lis):
  a = int(lis.split("-")[0])
  b= int(lis.split("-")[1])
  c= int(lis.split("-")[2])
  d= int(lis.split("-")[3])
  e= int(lis.split("-")[4])
  return JalaliDatetime(a,b,c,d,e).todatetime()
def tomiladiM(lis):
  a = int(lis.split("-")[0])
  b= int(lis.split("-")[1])
  return JalaliDatetime(a,b,1).todatetime()
def shamsi(lis):
  a = int(lis.split("-")[0])
  b = int(lis.split("-")[1])
  c = int(lis.split("-")[2])
  d= int(lis.split("-")[3])
  e= int(lis.split("-")[4])
  res = JalaliDatetime(datetime(a,b,c,d,e))
  return res

def O_interpolation(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)
        data = data.interpolate(method=config['interpolation'],order=config['order'])
        data.reset_index(inplace=True)

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M').ffill(limit=1)
        data = data.interpolate(method=config['interpolation'],order=config['order'])
        data.reset_index(inplace=True)
    elif config['time'] == 'hourly':
        data = data.set_index('time')
        data = data.resample('H').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)
        data = data.interpolate(method=config['interpolation'],order=config['order'])
        data.reset_index(inplace=True)
    elif config['time'] == 'minutes':
        data = data.set_index('time')
        data = data.resample('1min').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)
        data = data.interpolate(method=config['interpolation'],order=config['order'])
        data.reset_index(inplace=True)

    else:
        data = None
        
    return data


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    config = req['config']

    if config['type'] == 'miladi':
        data = read_json_time_series(req['data'])
        if config['interpolation'] == 'linear':
            result = linear_interpolation(data,config)
        else:
            result = O_interpolation(data,config)
        result = result.to_json()
        return response_message(dict({"data": result}))
    elif config['type'] == 'shamsi':
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        x = list(data.time)
        if config['time'] == 'monthly':
            data.time = [tomiladiM(i) for i in x]
        else:
            data.time = [tomiladi(i) for i in x]
        data.time = pd.to_datetime(data.time, format='%Y-%m')
        if config['interpolation'] == 'linear':
            result = linear_interpolation(data,config)
        else:
            result = O_interpolation(data,config)
        z = result['time'].dt.strftime('%Y-%m-%d-%H-%M').tolist()
        result['time'] = [shamsi(i) for i in z]
        result = result.to_json(default_handler=str)
        return response_message(dict({"data": result}))


@app.route('/service2', methods=['GET', 'POST'])
def interpolation2():
    req = request.get_json()
    data = read_json_time_series(req['data'])
    config = req['config']
    data.time = pd.to_datetime(data.time, format='%Y-%m-%d-%H-%M')
    if config['interpolation'] == 'linear':
        result = linear_interpolation(data,config)
    else:
        result = O_interpolation(data,config)    
#    if (config['skip_holiday']==True) and (config['time'] == 'daily'):
#        result = result.drop(result[result['time'].dt.strftime('%A')=='Thursday'].index)
#        result = result.drop(result[result['time'].dt.strftime('%A')=='Friday'].index)
    z = result['time'].dt.strftime('%Y-%m-%d-%H-%M').tolist()
    result['time'] = [shamsi(i) for i in z]
    result = result.to_json(default_handler=str)
    return response_message(dict({"data": result}))


@app.route('/service3', methods=['GET', 'POST'])
def outlierdetection():
    req = request.get_json()
    config = req['config']

    if config['time_series'] == 1:
        
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        data['Time'] = pd.to_datetime(data.Time, format='%Y-%m-%d %H:%M:%S')
        data = data.reset_index()[['Time', 'vol']].rename({'Time':'ds', 'vol':'y'}, axis='columns')
        m = Prophet()
        m.fit(data)
        forecast = m.predict(data)
        result = pd.concat([data.set_index('ds')['y'], forecast.set_index('ds')[['yhat','yhat_lower','yhat_upper']]], axis=1)
        result['error'] = result['y'] - result['yhat']
        result['uncertainty'] = result['yhat_upper'] - result['yhat_lower']
        result['method1'] = result.apply(lambda x: 'True' if(np.abs(x['error']) > 1.5*x['uncertainty']) else 'False', axis = 1)
        result['method2'] = result.apply(lambda rows: 'True' if ((rows.y<rows.yhat_lower)|(rows.y>rows.yhat_upper)) else 'False', axis = 1)
        model =  IsolationForest(contamination=0.004)
        model.fit(result[['y']].values)
        result['method3']=pd.Series(model.predict(result[['y']].values)).apply(lambda x: 'True' if (x == -1) else 'False' ).values
        result = result[['y','method1','method2','method3']]
        result = result.to_json(default_handler=str)
        return response_message(dict({"data": result}))
    else:
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        data['feature'] = (data['feature']-data['feature'].mean())/data['feature'].std()
        mean, std = np.mean(data.feature), np.std(data.feature) 
        lower, upper = mean - std*3, mean + std*3
        data['method1'] = data['feature'].apply((lambda x: 'True' if 
                                         x>upper or x<lower else 'False'))
        Q1 = np.percentile(data['feature'], 25)
        Q3 = np.percentile(data['feature'], 75)
        IQR = Q3 - Q1
        outlier_step = 1.5 * IQR
        data['method2'] = data['feature'].apply((lambda x: 'True' if x > (Q3+outlier_step)
                                        or x<(Q1 - outlier_step) else 'False'))
        result = data.to_json(default_handler=str)
        return response_message(dict({"data": result}))

@app.route('/service4', methods=['GET', 'POST'])
def imbalanced():
    req = request.get_json()
    config = req['config']

    if config['method'] == 'undersampling':
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        dataset = data.groupby('class').apply(lambda x: x.sample(data['class'].value_counts().min()))
        result = dataset.reset_index(drop=True)
        result = result.to_json()
        return response_message(dict({"data": result}))
    elif config['method'] == 'oversampling':
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        max_size = data['class'].value_counts().max()
        lst = [data]
        for class_index, group in data.groupby('class'):
            lst.append(group.sample(max_size-len(group), replace=True))
        result = pd.concat(lst)
        result = result.reset_index(drop=True)
        result = result.to_json(default_handler=str)
        return response_message(dict({"data": result}))
    elif config['method'] == 'SMOTE':
        j_data = json.dumps(req['data'])
        data = pd.read_json(j_data)
        data = data.append({'id':7, 'feature1':1000,'class':0}, ignore_index=True)
        X = data.drop(columns=['class'])
        y = data['class']
        sm = SMOTE(k_neighbors=1)
        X_train, y_train = sm.fit_resample(X, y)
        X_train['class'] = y_train
        result = X_train
        result = result.to_json(default_handler=str)
        return response_message(dict({"data": result}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
