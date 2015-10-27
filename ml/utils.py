import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
CHART_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "charts")

for d in [DATA_DIR, CHART_DIR]:
    if not os.path.exists(d):
        os.mkdir(d)


def load_dataset(name, delimiter='\t'):
    features = []
    labels = []
    with open(os.path.join(DATA_DIR, name)) as ifile:
        for line in ifile:
            tokens = line.strip('').split(delimiter)
            features.append([float(token) for token in tokens[:-1]])
            labels.append(tokens[-1])
    return np.array(features), np.array(labels)