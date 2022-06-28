from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd

def handle_imbalance(data, method):
    df = pd.DataFrame(data)
    df.set_index('id', inplace=True)
    X, y = df.drop('class', axis=1), df['class']
    if method == "SMOTE":
        sampler = SMOTE()
    elif method == "Undersampling":
        sampler = RandomUnderSampler()
    elif method == "Oversampling":
        sampler = RandomOverSampler()
    else:
        raise Exception("Method not supported")
    out = sampler.fit_resample(X, y)
    df = out[0]
    df['class'] = out[1]
    df.reset_index(inplace=True)
    return df.to_json()
    