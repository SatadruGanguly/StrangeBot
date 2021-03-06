# -*- coding: utf-8 -*-
"""Red Eye Recognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zvFEMrMGk_ExVku59KVu52UVexxMdFWu
"""

# pip install fer

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib
import cv2 
import glob
# from skimage import io
# from tensorflow import keras
# from keras.preprocessing.image import ImageDataGenerator
# from google.colab import files
# from google.colab.patches import cv2_imshow
# from keras.preprocessing import image
import fer

import os
from MedBotProject.settings import BASE_DIR

def Eye_Evaluation(eyeImg):
    new_mod = tf.keras.models.load_model(os.path.join(BASE_DIR, 'DL', 'EyesModel.h5'))
    eyeCascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'DL', 'haarcascade_eye.xml'))
    the_eyes = eyeCascade.detectMultiScale(eyeImg,
                                       scaleFactor = 1.05,
                                       minNeighbors = 3,
                                       minSize = (100 , 80),
                                       maxSize = (150 , 130),
                                       flags = cv2.CASCADE_SCALE_IMAGE)
    
    for x,y,w,h in the_eyes:
        cv2.rectangle(eyeImg , (x , y-20) , (x+10+w,y+h+20) , (0,255,0) , 2)
        
    flag =1
    for x , y , w , h in the_eyes:
        if y-20>=0 and x-10>=0:
            image = cv2.resize(eyeImg[y-20:y+h+20 , x:x+w+10], (400 , 400))
            X = tf.keras.preprocessing.image.img_to_array(image)
            X = np.expand_dims(X , axis = 0)
            imagery = np.vstack([X])
            pred = new_mod.predict(imagery)
            classes = new_mod.predict_classes(imagery)
            print(pred , classes)
            if classes[0]==0:
                cv2.putText(eyeImg , 'Infected' , (x-35 , y-35) , cv2.FONT_HERSHEY_DUPLEX , 0.8 , (0,0,255) , 2)

            elif classes[0]==1:
                cv2.putText(eyeImg , 'Normal' , (x-35 , y-35) , cv2.FONT_HERSHEY_DUPLEX , 0.8 , (0,0,255) , 2)

        else:
            flag = 0
            break

    if flag==0:
        return eyeImg, 0, 'Could not detect eyes properly, please take the picture again'

    else:
        return eyeImg , 1, 'Evaluation Successful'


def detect_Expression(img):
    detector = fer.FER()
    emotions = detector.detect_emotions(img)
    max = 0
    max_emotion = ''
    if len(emotions)!=0:
        for params in emotions:
            for j,k in params.items():
                if j=='emotions':
                    for emo , score in k.items():
                        if max<score:
                            max = score
                            max_emotion = emo

        return max_emotion 

    else:
        return 'Face undetected , please click the picture again!'

