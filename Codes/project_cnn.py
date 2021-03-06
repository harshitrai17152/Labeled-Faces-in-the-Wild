# -*- coding: utf-8 -*-
"""project_cnn.ipynb

Automatically generated by Colaboratory.

# Reading the data
"""

from tensorflow.python.keras.layers import Dense,Conv2D,Flatten,MaxPooling2D,ZeroPadding2D,Dropout,Softmax
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.python.keras import Sequential
from sklearn.datasets import fetch_lfw_people
from sklearn.datasets import fetch_lfw_pairs
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import scikitplot as skplt
!pip install scikit-plot
import numpy as np
import random

# Commented out IPython magic to ensure Python compatibility.
from __future__ import absolute_import, division, print_function, unicode_literals
try:
#   %tensorflow_version 2.x
except Exception:
  pass
  
import tensorflow_datasets as tfds
import tensorflow as tf
tf.test.gpu_device_name()

from google.colab import drive
drive.mount('/content/drive')

data=fetch_lfw_people(resize=0.4,min_faces_per_person=40,funneled=False)

l=list(data.keys())
X=data[l[0]]
Y=data[l[2]]
target_name=data[l[3]]

_,W,H=data[l[1]].shape
features=X.shape[1]
m=X.shape[0]
classes=data[l[3]].shape[0]

print("Samples:",m)
print("Features:",features)
print("Classes:",classes)
print("Dimension:",(W,H))

"""# Shuffling the data"""

temp=list(zip(X,Y)) 
random.shuffle(temp) 
X,Y=zip(*temp)

X=np.array(X)
Y=np.array(Y)

"""# Train and test splitting of data"""

training_data_X,testing_data_X,training_data_Y,testing_data_Y=train_test_split(X,Y,test_size=0.20,random_state=42)

"""# CNN"""

model=Sequential()

model.add(Conv2D(64,kernel_size=3,activation='relu',input_shape=(W,H,1)))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(Conv2D(128,kernel_size=3,activation='relu'))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(Conv2D(256,kernel_size=5,activation='relu'))
model.add(MaxPooling2D((2,2),strides=(2,2)))
model.add(Dropout(0.25))
#model.add(Conv2D(512,kernel_size=3,activation='relu'))
#model.add(MaxPooling2D((2,2),strides=(2,2)))

model.add(Flatten())
model.add(Dense(classes,activation='softmax'))

from keras.utils import to_categorical

training_data_Y=to_categorical(training_data_Y)
testing_data_Y=to_categorical(testing_data_Y)

training_data_X=training_data_X.reshape(training_data_X.shape[0],W,H,1)
testing_data_X=testing_data_X.reshape(testing_data_X.shape[0],W,H,1)

model.compile(optimizer='Adamax',loss='categorical_crossentropy',metrics=['accuracy'])
model.fit(training_data_X,training_data_Y,validation_data=(testing_data_X,testing_data_Y),batch_size=100,epochs=50)

score=model.evaluate(testing_data_X,testing_data_Y,verbose=0)
print(score[1]*100)

"""# ROC"""

k=model.history.history
keys=k.keys()
loss=k['val_loss']
lin=[i+1 for i in range(50)]

plt.plot(lin,loss)  
plt.xlabel('Epoches')
plt.ylabel('Cross-Entropy Loss')
plt.title("Loss-per-epoch for Test Set")
plt.show()

model.summary()

