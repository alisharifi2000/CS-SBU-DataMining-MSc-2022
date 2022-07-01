from collections import Counter
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


def balance_data(data, config, classes):
    if config['method'] == "SMOTE":
        n_samples = Counter(classes)
        if (n_samples[0] or n_samples[1]) < 6:
            return f"for SMOTE method each class must have more than 6 samples, {n_samples}", "False"
        else:
            smote = SMOTE(random_state=2)
            x, y = smote.fit_resample(data, classes)
            return x, y

    if config['method'] == "oversampling":
        ros = RandomOverSampler()
        x, y = ros.fit_resample(data, classes)
        return x, y

    if config['method'] == "undersampling":
        rus = RandomUnderSampler()
        x, y = rus.fit_resample(data, classes)
        return x, y
