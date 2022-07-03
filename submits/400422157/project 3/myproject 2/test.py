from sklearn.cluster import DBSCAN
import numpy as np
from numpy import random, where
from random import seed
seed(1)
random_data = np.random.randn(100,2)  * 20 + 20
print(len(random_data))
outlier_detection = DBSCAN(min_samples = 2, eps = 3)
clusters = outlier_detection.fit_predict(random_data)
print(clusters)