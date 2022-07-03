from collections import Counter

from imblearn.under_sampling import RandomUnderSampler
from sklearn.datasets import make_classification
from imblearn.over_sampling import SMOTE, RandomOverSampler
import numpy as np
import pandas as pd


def over_under_sample(inputdata):
    if inputdata['config']['method'] == 'SMOTE':
        df = pd.DataFrame(inputdata['data'])
        if df.groupby(['class']).count()['feature1'][0] == 1:
            df['class'][0] = 0
        oversample = SMOTE(k_neighbors=1)
        X, y = oversample.fit_resample(np.array(df['feature1']).reshape(-1, 1), np.array(df['class']))
        X = np.array(X)
        data = pd.DataFrame({'feature': X.T[0], 'class': y})
        d4 = data.to_dict()
        output4 = {'data': d4}
        # output4
        return output4

    elif inputdata['config']['method'] == 'over_sampling':
        df = pd.DataFrame(inputdata['data'])

        oversample = RandomOverSampler(sampling_strategy='minority')
        X, y = oversample.fit_resample(np.array(df['feature1']).reshape(-1, 1), np.array(df['class']))
        X = np.array(X)
        data = pd.DataFrame({'feature': X.T[0], 'class': y})
        d4 = data.to_dict()
        output4 = {'data': d4}
        # output4
        return output4

    elif inputdata['config']['method'] == 'under_sampling':
        df = pd.DataFrame(inputdata['data'])

        undersample = RandomUnderSampler(sampling_strategy=0.5)
        X, y = undersample.fit_resample(np.array(df['feature1']).reshape(-1, 1), np.array(df['class']))
        X = np.array(X)
        data = pd.DataFrame({'feature': X.T[0], 'class': y})
        d4 = data.to_dict()
        output4 = {'data': d4}
        # output4
        return output4