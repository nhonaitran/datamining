#Import libraries for doing image analysis
from skimage.io import imread
from skimage.transform import resize
from sklearn.ensemble import RandomForestClassifier as RF
import glob
import os
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold as KFold
from sklearn.metrics import classification_report
from matplotlib import pyplot as plt
from matplotlib import colors
from pylab import cm
from skimage import segmentation
from skimage.morphology import watershed
from skimage import measure
from skimage import morphology
import numpy as np
import pandas as pd
from scipy import ndimage
from skimage.feature import peak_local_max

# make graphics inline ( run this in python console, not within this script)
#%matplotlib inline

import warnings
warnings.filterwarnings("ignore")

# get the classnames from the directory structure
directory_names = list(set(glob.glob(os.path.join("data","train", "*"))).difference(set(glob.glob(os.path.join("data","train","*.*")))))

# Example image
# This example was chosen for because it has two noncontinguous pieces
# that will make the segmentation example more illustrative
example_file = glob.glob(os.path.join(directory_names[5],"*.jpg"))[9]
print example_file
im = imread(example_file, as_grey=True)
plt.imshow(im, cmap=cm.gray)
plt.show()

# First we threshold the image by only taking values greater than the mean to reduce noise in the image
# to use later as a mask
f = plt.figure(figsize=(12,3))
imthr = im.copy()
imthr = np.where(im > np.mean(im),0.,1.0)
sub1 = plt.subplot(1,4,1)
plt.imshow(im, cmap=cm.gray)
sub1.set_title("Original Image")

sub2 = plt.subplot(1,4,2)
plt.imshow(imthr, cmap=cm.gray_r)
sub2.set_title("Thresholded Image")

imdilated = morphology.dilation(imthr, np.ones((4,4)))
sub3 = plt.subplot(1, 4, 3)
plt.imshow(imdilated, cmap=cm.gray_r)
sub3.set_title("Dilated Image")

labels = measure.label(imdilated)
labels = imthr*labels
labels = labels.astype(int)
sub4 = plt.subplot(1, 4, 4)
sub4.set_title("Labeled Image")
plt.imshow(labels)

# calculate common region properties for each region within the segmentation
regions = measure.regionprops(labels)

# find the largest nonzero region
def getLargestRegion(props=regions, labelmap=labels, imagethres=imthr):
    regionmaxprop = None
    for regionprop in props:
        # check to see if the region is at least 50% nonzero
        if sum(imagethres[labelmap == regionprop.label])*1.0/regionprop.area < 0.50:
            continue
        if regionmaxprop is None:
            regionmaxprop = regionprop
        if regionmaxprop.filled_area < regionprop.filled_area:
            regionmaxprop = regionprop
    return regionmaxprop

regionmax = getLargestRegion()
plt.imshow(np.where(labels == regionmax.label,1.0,0.0))
plt.show()

print regionmax.minor_axis_length/regionmax.major_axis_length

def getMinorMajorRatio(image):
    image = image.copy()
    # Create the thresholded image to eliminate some of the background
    imagethr = np.where(image > np.mean(image),0.,1.0)

    #Dilate the image
    imdilated = morphology.dilation(imagethr, np.ones((4,4)))

    # Create the label list
    label_list = measure.label(imdilated)
    label_list = imagethr*label_list
    label_list = label_list.astype(int)
    
    region_list = measure.regionprops(label_list)
    maxregion = getLargestRegion(region_list, label_list, imagethr)
    
    # guard against cases where the segmentation fails by providing zeros
    ratio = 0.0
    if ((not maxregion is None) and (maxregion.major_axis_length != 0.0)):
        ratio = 0.0 if maxregion is None else maxregion.minor_axis_length*1.0 / maxregion.major_axis_length
    return ratio

print getMinorMajorRatio(im)