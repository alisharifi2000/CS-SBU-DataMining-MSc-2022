from utils import *
from models import *
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler


def handle_undersampling(x, y):
    """
    Fix data imbalance via undersampling.
    """
    # Create undersampling object w/ random selection strategy. This specific strategy undersamples the majority class until it matches the number of minority class samples
    undersample = RandomUnderSampler(sampling_strategy="majority")
    x_under, y_under = undersample.fit_resample(x, y)
    return reconstruct_data(
        x_under, y_under
    )  # Return reconstructed, un-split data to send back


def handle_oversampling(x, y):
    """
    Fix data imbalance via oversampling.
    """
    # Create oversampling object w/ random selection strategy. This specific strategy oversamples the minority class until it matches the number of majority class samples
    oversample = RandomOverSampler(sampling_strategy="minority")
    x_over, y_over = oversample.fit_resample(x, y)  # Resample
    return reconstruct_data(
        x_over, y_over
    )  # Return reconstructed, un-split data to send back


def handle_smote(x, y):
    """
    Fix data imbalance via the SMOTE method.
    """
    # Create oversampling object w/ SMOTE
    smote = SMOTE(k_neighbors=3)  # A low number so it works with (very) small datasets
    x_smote, y_smote = smote.fit_resample(x, y)  # Resample
    return reconstruct_data(
        x_smote, y_smote
    )  # Return reconstructed, un-split data to send back


def minority_class_handle(data, config):
    """
    Input:
        data: The np.ndarray-like data we'll be performing operations on. Shape is (n, k) where n is the number of samples and k-1 is the number of features. The last element in every row (kth element) corresponds to the class label
        config: The configuration as specified in ./models, majority class, minority class, etc.
    Output: The resampled data in the form of a list with the shape (n, k), ready to be sent back to the requester.
    """

    x, y = split_data(data)

    # NO NEED TO PASS MAJORITY/MINORITY CLASS.
    # imblearn handles this automatically
    if config.method is ImbalanceFixMethod.undersampling:
        return handle_undersampling(x, y)

    elif config.method is ImbalanceFixMethod.oversampling:
        return handle_oversampling(x, y)

    elif config.method is ImbalanceFixMethod.smote:
        return handle_smote(x, y)
