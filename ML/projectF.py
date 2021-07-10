# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 19:31:04 2021

@author: User
"""
import pandas as pd
import pickle
import os
from MedBotProject.settings import BASE_DIR

filename = os.path.join(BASE_DIR, 'ML', 'finalized_model_x.sav')      #use the path from projectX
path_clean = os.path.join(BASE_DIR, 'ML', 'clean_x.csv')              #path from projectX
path_prec = os.path.join(BASE_DIR, 'ML', 'symptom_precaution.csv') #path of the precation csv

model = pickle.load(open(filename, 'rb'))

data = pd.read_csv(path_clean)

data = data.drop('label', axis=1)
data = data.drop('index', axis=1)



import sys

n = len(sys.argv)

if n>1:    
    for i in (1,n-1):
        
        print(sys.argv[i])



disease = {'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}
revdisease = {value : key for (key, value) in disease.items()}





    
#print("You are probably have : "+dis)

prec = pd.read_csv(path_prec)



#print("Your recomended precautions are :")

        #print(show.iloc[0,i])

def pred(simp):
    check = pd.DataFrame(columns=data.columns)
    check.loc['a']=0
    for i in simp:
        check[i].replace({0:1},inplace=True)
    p = model.predict(check)
    ret = []
    for i in p:
        dis = revdisease[i]
    show = prec[prec['Disease']==dis]
    show.fillna(1)
    for i in range(4):
        if(show.iloc[0,i] != 1):
            ret.append(show.iloc[0,i])
    return ret


# pp = pred(['itching','skin_rash'])
# print(pp)    