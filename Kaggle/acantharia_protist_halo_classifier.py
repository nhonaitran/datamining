import glob
import os
import numpy as np
import pandas as pd

from skimage.io import imread
from skimage.transform import resize
from skimage import morphology
from skimage import measure

from sklearn.svm import SVC, l1_min_c
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold as KFold
from sklearn.metrics import classification_report

# get the classnames from the directory structure
directory_names = list(set(glob.glob(os.path.join("data","train", "*"))).difference(set(glob.glob(os.path.join("data","train","*.*")))))
directory_names.sort()

# take top 10 directories
top_10 = directory_names[0:8]

#get the total training images
numberofImages = 0
for folder in top_10:
    for fileNameDir in os.walk(folder):   
        for fileName in fileNameDir[2]:
             # Only read in the images
            if fileName[-4:] != ".jpg":
              continue
            numberofImages += 1

print "Total number of images: ", numberofImages, "\n"
# rescale the images to be 25x25
maxPixel = 25
imageSize = maxPixel * maxPixel
num_rows = numberofImages # one row for each image in the entire dataset
num_features = imageSize #+ 1 # 1 for height/width ratio, 1 for point-based ORB feature, 1 for point-based SIFT feature, 1 for point-based SURF feature

# label images
print "Labeling images"
# class 1 = "acantharia_protist_halo", 0 = "other classes"

# X is the feature vector with one row of features per image
# consisting of the pixel values and our metric
X = np.zeros((num_rows, num_features), dtype=float)
# y is the numeric class label 
y = np.zeros((num_rows))

files = []
# Generate training data
i = 0    
label = 0
# List of string of class names
namesClasses = list()

for folder in top_10:
    if (folder == "data/train/acantharia_protist_halo"):
        label = 1.0
    else:
        label = 0.0
        
    # Append the string class name for each class
    currentClass = folder.split(os.pathsep)[-1]
    for fileNameDir in os.walk(folder):   
        for fileName in fileNameDir[2]:
            # Only read in the images
            if fileName[-4:] != ".jpg":
              continue
            
            # Read in the images and create the features
            nameFileImage = "{0}{1}{2}".format(fileNameDir[0], os.sep, fileName)            
            image = imread(nameFileImage, as_grey=True)
            files.append(nameFileImage)
            image = resize(image, (maxPixel, maxPixel))
            
            # Store the rescaled image pixels
            X[i, 0:imageSize] = np.reshape(image, (1, imageSize))
            
            # Store the classlabel
            y[i] = label
            i += 1
            # report progress for each 5% done  
            report = [int((j+1)*num_rows/20.) for j in range(20)]
            if i in report: 
                print np.ceil(i *100.0 / num_rows), "% done"

#Create a DataFrame object to make subsetting the data on the class 
#df = pd.DataFrame({"class": y[:], "ratio": X[:, num_features-1]})
print y.shape

print
print "Training & Predict"

cv_folds = 10
model = SVC(kernel='rbf', C=1, gamma=0.01)
scores = cross_validation.cross_val_score(model, X, y, cv=cv_folds)
print("10-fold accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print scores
