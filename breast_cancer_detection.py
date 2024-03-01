# -*- coding: utf-8 -*-
"""Breast Cancer Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WFGQ-sPdykUe3Pf4za-VkdhVuxUV9RgU
"""

# Documentation: https://randerson112358.medium.com/breast-cancer-detection-using-machine-learning-38820fe98982
# Tutori: https://www.youtube.com/watch?v=NSSOyhJBmWY&t=471s
# Data set: https://www.kaggle.com/datasets/uciml/breast-cancer-wisconsin-data?resource=download
print('This is Breast Cancer Detection.')

#import libraries
#NumPy can be used to perform a wide variety of mathematical operations on arrays.
#Pandas allows us to analyze big data and make conclusions based on statistical theories.
#Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
#matplotlib. pyplot is a collection of command style functions that make matplotlib work like MATLAB.
#Python Seaborn library is a widely popular data visualization library that is commonly used for data science and machine learning tasks.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Load the data
#Here diagnosis = M means Malignant indicate cancer cell & B not
from google.colab import files # Use to load data on Google Colab
uploaded = files.upload() # Use to load data on Google Colab
df = pd.read_csv('data.csv')
df.head(7)

#count the number of row and col in data set
df.shape

#count the number of empty value in each col (NaN,NAN.na)
df.isna().sum()

#drop the col with all missing values / empty
df = df.dropna(axis=1)

# get the new count the number of row and col in data set
df.shape

# get the count of number of malignant (M) or benign(B) cells
df['diagnosis'].value_counts()

# now visualize the data of diagnosis
sns.countplot(df['diagnosis'], label='count data')

#look at data type which col need to encoded
df.dtypes

#encode the categorical data values
from sklearn.preprocessing import LabelEncoder
labelencoder_Y = LabelEncoder()
df.iloc[:,1] = labelencoder_Y.fit_transform(df.iloc[:,1].values)

#create a pair plot
sns.pairplot(df.iloc[:,1:5], hue='diagnosis')

#print 1st 5 row of new data
df.head(5)

#get the correlation of the collumns
df.iloc[:,1:12].corr()

#visulize the correlation data
plt.figure(figsize=(10,10))
sns.heatmap(df.iloc[:,1:12].corr(), annot=True, fmt=".0%")

#split the data set into independent (x) and dependent (y) data set
X = df.iloc[:,2:31].values
Y = df.iloc[:,1].values

#split the data set into 75% training and 25 % testing
from sklearn.model_selection import train_test_split
X_train , X_test , Y_train , Y_test = train_test_split( X, Y, test_size = 0.25 , random_state = 0)

# scale the data - feature scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

#create a function for the models
def models(X_train,Y_train):

  #logictic regression
  from sklearn.linear_model import LogisticRegression
  log = LogisticRegression(random_state=0)
  log.fit(X_train,Y_train)

  #decision tree
  from sklearn.tree import DecisionTreeClassifier
  tree = DecisionTreeClassifier(criterion= 'entropy', random_state=0)
  tree.fit(X_train,Y_train)

  #random forest classifier
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)
  forest.fit(X_train,Y_train)

  #print the models accuracy on the traing data
  print('[0]Logistic regression training accuracy:' ,log.score(X_train,Y_train))
  print('[1]Decision tree training accuracy:' ,tree.score(X_train,Y_train))
  print('[2]Forest classifier regression training accuracy:' ,forest.score(X_train,Y_train))

  return log , tree , forest

#getting all of the models
model = models(X_train,Y_train)

#test model accurecy on test data on confusion matrix
from sklearn.metrics import confusion_matrix

for i in range( len(model)):
  print("Model ", i)
  cm = confusion_matrix(Y_test, model[i].predict(X_test))
  TP = cm[0][0]
  TN = cm[1][1]
  FN = cm[1][0]
  FP = cm[0][1]
  print(cm)
  print('Testing accuricy = ',(TP+TN)/(TP+TN+FN+FP))
  print()

#show anaother way to get metrics of the models
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
for i in range( len(model)):
  print("Model ", i)
  print( classification_report(Y_test, model[i].predict(X_test)))
  print( accuracy_score(Y_test, model[i].predict(X_test)))
  print()

#print the prediction of random forest classfier model
pred = model[2].predict(X_test)
print(pred)
print()
print(Y_test)