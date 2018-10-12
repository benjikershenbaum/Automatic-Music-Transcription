import tensorflow as tf
from tensorflow import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import random
import seaborn as sns


def plot_confusion_matrix(cm, classes=None, title='Confusion matrix'):
    """Plots a confusion matrix."""
    if classes is not None:
        sns.heatmap(cm, xticklabels=classes, yticklabels=classes, vmin=0., vmax=1., annot=True)
    else:
        sns.heatmap(cm, vmin=0., vmax=1.)
    plt.title(title)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')



print('Start')
# Read in files
out_file_path = 'C:\\Users\\Benji\\Desktop\\Work\\Music\\Data\\Isolated Only\\Processed\\Output\\output.txt'
in_file_path = 'C:\\Users\\Benji\\Desktop\\Work\\Music\\Data\\Isolated Only\\Processed\\Input\\input.txt'
inp= pd.read_csv(in_file_path,sep="	",header=None)
out = pd.read_csv(out_file_path,sep="	",header=None)
print('Done: Read Files')

# Combine X and y for cleaning
data = pd.concat([inp,out],axis=1)

# Count instances with no notes played
count_empty=int(np.sum(data,axis=0).iloc[496])
count_not_empty=data.shape[0]-count_empty

# Get binary array if notes played
empty=data.iloc[:,496].get_values()

# Number of empty notes in cleaned set
num_empty_clean = 800

# Get indices where empty
empty_idx = np.where(empty==1)[0]
not_empty_idx = np.where(empty==0)[0]

# Get random num_empty_clean indices where empty
ii=random.sample(range(0,empty_idx.shape[0]),num_empty_clean)
rand_idx=empty_idx[ii]

# Get indices where only 1 note played
count_notes=np.sum(out,axis=1)
single_note_idx=np.where(count_notes==1)[0]

# Get set of indices of clean data
i1=np.intersect1d(not_empty_idx,single_note_idx)
i2=np.intersect1d(rand_idx,single_note_idx)

# Combine clean data
data_clean = pd.concat([data.iloc[i1,:],data.iloc[not_empty_idx,:]],axis=0)
print('Done: Data Cleaning')

# Extract input and output
X=data_clean.iloc[:,0:396]
y=data_clean.iloc[:,396:497]
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.80,test_size=0.20)

# Initialize Neural Net
model = keras.Sequential()
model.add(keras.layers.Dense(units=101, activation='relu',input_dim=396))	# 1st layer
model.add(keras.layers.Dense(units=101, activation='softmax'))	#2d layer
model.compile(loss='categorical_crossentropy', optimizer='sgd',metrics=['accuracy'])
model.fit(X_train,y_train,epochs=50, batch_size=32)
print('Done: Training')

# Predict test
y_pred_prob = model.predict(X_test, batch_size=32)

threshold_preds=y_pred_prob.copy()
threshold_preds[threshold_preds<0.2]=0
threshold_preds[threshold_preds>0.2]=1

y_pred=threshold_preds.copy()

# Calculate test accuracy
acc = accuracy_score(y_pred=y_pred, y_true=y_test)
print('Test Accuracy:', acc)

#print(y_pred_prob)
print('Done All')