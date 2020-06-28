"""이미 트레이닝을 거친 모델의 가중치를 불러와서 오랜 시간을 기다리지 않고 테스트 하는 코드 (미완성)"""
import random
from keras.preprocessing import image
import os, re, glob
import cv2
import numpy as np
import shutil
from numpy import argmax
from keras.models import load_model
 
categories = ['Onepiece','Outer','Pants','Skirt','Top']
 
def Dataization(img_path):
    image_w = 220
    image_h = 220
    img = cv2.imread(img_path)
    img = cv2.resize(img, None, fx=image_w/img.shape[1], fy=image_h/img.shape[0])
    return (img/256)
 
src = []
name = []
test = []
image_dir = 'D:/dataset1/Testset/Test/'

for file in os.listdir(image_dir):
    if (file.find('.png') is not -1):      
        src.append(image_dir + file)
        name.append(file)
        test.append(Dataization(image_dir + file))
 
test = np.array(test)
model = load_model('JH_nonFine.h5')
predict = model.predict_classes(test)
 
for i in range(len(test)):
    print(name[i] + " : , Predict : "+ str(categories[predict[i]]))
    
    if predict == 0:
        print('Onepiece')
    elif predict == 1:
        print('Outer')
    elif predict == 2:
        print('Pants')
    elif predict == 3:
        print('Skirt')
    else:
        print('Top')
