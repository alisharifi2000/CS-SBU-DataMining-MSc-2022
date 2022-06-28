import pandas as pd
from prophet import Prophet
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import numpy as np


def z_score(df, score):
    upper_range = df['feature'].mean() + score * df['feature'].std()
    lower_range = df['feature'].mean() - score * df['feature'].std()
    df['z_score'] = df['feature'].apply(lambda x: x > upper_range or x < lower_range)
    return df

def iqr(df):
    q1 = df['feature'].quantile(0.25)
    q3 = df['feature'].quantile(0.75)
    iqr = q3 - q1
    df['iqr'] = df['feature'].apply(lambda x: x > q3 + 1.5 * iqr or x < q1 - 1.5 * iqr)
    return df

def vanilla(data, score):
    df = pd.DataFrame(data)
    df = iqr(z_score(df, score))
    df.drop(['feature'], axis=1, inplace=True)
    return df.to_json()


def prophet(df):
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])
    model = Prophet()
    model.fit(df)
    forecast = model.predict(df)
    df = pd.merge(df, forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], on='ds')
    df['prophet'] = df.apply(lambda x: x.y<x.yhat_lower or x.y>x.yhat_upper, axis = 1)
    df.drop(['yhat', 'yhat_lower', 'yhat_upper'], axis=1, inplace=True)
    df.columns = ['time', 'vol', 'prophet']
    return df

def isolation(df):
    outliers_fraction = float(.01)
    scaler = StandardScaler()
    vol = pd.DataFrame(scaler.fit_transform(df['vol'].values.reshape(-1, 1)), columns=['vol'])
    model =  IsolationForest(contamination=outliers_fraction)
    model.fit(vol)
    df['isolation_forest'] = model.predict(vol)
    df['isolation_forest'] = df['isolation_forest'].apply(lambda x: x == -1)
    return df

def time_series(data):
    df = pd.DataFrame(data)
    df = prophet(df)
    df['time'] = df['time'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df = isolation(df)
    df.drop(['vol'], axis=1, inplace=True)
    return df.to_json()