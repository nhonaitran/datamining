import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from itertools import combinations
from utils import DATA_DIR, CHART_DIR

#load iris datasets
data = load_iris()
features = data.data
feature_names = data.feature_names
target = data.target
target_names = data.target_names

fig,axes = plt.subplots(2,3)
feature_pairs = combinations(range(features.shape[1]), 2)
colors = 'rgb'
markers = '>ox'

for i, (x, y) in enumerate(feature_pairs):
    ax = axes.flat[i]
    for t,marker,c in zip(range(3), markers, colors):
        ax.scatter(features[target == t, x], features[target == t, y], marker=marker, c=c, label=target_names[t])
    ax.set_xlabel(feature_names[x])
    ax.set_ylabel(feature_names[y])
    #ax.legend(loc='upper left')

# loc=7 centers the legend in the middle
# values for bbox_to_anchor:
#   the value 2.3 specifes the x direction on the plot; 
#     2.4 moves ledend upward, 2.2 moves legend downward; -0.1 puts the legend at the bottom below
#     the subplots
#   the value 0.5 specifies the y direction on the plot
# ncol - setting the value of this param changes the ledend items from displayed vertically
#   to horizontally.  the value 3 equals the number of legend items to be displayed.
plt.legend(loc=7, bbox_to_anchor=(0.5,2.3), ncol=3)
fig.set_size_inches(10, 8)
fig.savefig(os.path.join(CHART_DIR, 'scatter_plot_of_iris_dataset.png'))
