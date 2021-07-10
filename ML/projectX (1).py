#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier



import pickle

filename = 'finalized_model.sav'                           #sav file name path for the model
path = 'C:/Users/User/Documents/project data/dataset.csv'  #dataset path
path_clean = "C:/Users/User/Downloads/clean.csv"           #path to save cleaned csv

data = pd.read_csv(path)


data.head()


#dataset charctersitics
data.describe()


# missing values
data.isna().sum()



#number of disease
len(data['Disease'].unique())


#shape of the dataset(4920 rows and 18 cols)
data.shape


cols = [i for i in data.iloc[:,1:].columns]
cols


tmp = pd.melt(data.reset_index() ,id_vars = ['index'], value_vars = cols )
tmp['add'] = 1
df = pd.pivot_table(tmp, values = 'add',index = 'index', columns = 'value')
df.insert(0,'label',data['Disease'])
df = df.fillna(0)
df.head()


print("shapeof new dataset",df.shape)


# Resplace the disease names with numeric value


disease = {'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}
df.replace({'label':disease},inplace = True)


df.head()


df.columns = df.columns.str[1:]


df.rename(columns = {'tching' : 'itching'}, inplace = True)
df.rename(columns = {'abel' : 'label'}, inplace = True)


df

X = df.drop("label",axis = 1)
y = df['label']


# Random forest

model=RandomForestClassifier(n_estimators=50)

#fold as 5
cv = KFold(n_splits=5, shuffle=False)


print("Accuracy:",)
score = cross_val_score(model, X, y, cv=cv)
print((sum(score)/5)*100)



from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score


#calculating f1 score for all the folds
print("F1 score")
for train_index, test_index in cv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(f1_score(y_test, y_pred, average=None))



#calculating precision score for all the folds
print("precision")
for train_index, test_index in cv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(precision_score(y_test, y_pred, average=None))


#calculating recall score for all the folds
print("recall:")
for train_index, test_index in cv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(recall_score(y_test, y_pred, average=None))



pickle.dump(model, open(filename, 'wb'))



loaded_model = pickle.load(open(filename, 'rb'))



#calculating f1 score for all the folds
print("F1 score")
for train_index, test_index in cv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        model = model.fit(X_train, y_train)
        y_pred = loaded_model.predict(X_test)
        print(f1_score(y_test, y_pred, average=None))




df.to_csv(path_clean)





