"""트레이닝셋을 통해 이미지 트레이닝 후 테스트셋으로 이미지 분류 테스트를 하는 CNN 알고리즘"""

import numpy as np
import random
from keras.preprocessing import image
import os
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers
from keras import optimizers
import keras
# 모듈 import

base_dir = 'D:/dataset1/'
train_dir = os.path.join(base_dir, 'Trainset')
# 경로 지정

test='D:/dataset1/Testset/'
test_OnePiece_dir=os.path.join(test,'Onepiece')
test_Outer_dir=os.path.join(test,'Outer')
test_Pants_dir=os.path.join(test,'Pants')
test_Skirt_dir=os.path.join(test,'Skirt')
test_Top_dir=os.path.join(test,'Top')
# test할 data가 있는 폴더 지정

epochs = 50 
img_width, img_height = 220, 220 
train_size = 992 
conv_base = keras.applications.InceptionV3(weights='imagenet',include_top = False,input_shape=(img_width, img_height, 3))
conv=conv_base.output.shape
conv_base.summary()
datagen = ImageDataGenerator(rescale=1. / 255)
batch_size = 16
# epoch(전체 데이터 셋에 대해 학습할 횟수), img_size, train_size, batch_size(epoch을 나누어 실행하는 횟수) 등 지정

def extract_features(directory, sample_count):  # 라벨링 작업
    features = np.zeros(shape=(sample_count, conv[1], conv[2], conv[3]))
    labels = np.zeros(shape=(sample_count,5))
    generator = datagen.flow_from_directory(directory,
                                            target_size=(img_width, img_height),
                                            batch_size=batch_size,
                                            class_mode='categorical')
    i = 0
    for inputs_batch, labels_batch in generator:
        print(inputs_batch.shape,i)
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size : (i + 1) * batch_size] = features_batch
        labels[i * batch_size: (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:
            break
    return features, labels

train_features, train_labels = extract_features(train_dir, train_size)

model = models.Sequential()
model.add(layers.Flatten(input_shape=train_features.shape[1:]))
model.add(layers.Dense(256, activation='relu', input_dim=(train_features.shape[1]*train_features.shape[2]*train_features.shape[3])))
model.add(layers.Dropout(0.25))
model.add(layers.Dense(5, activation='softmax'))
model.summary()
model.compile(optimizer=optimizers.Adam(0.001),loss='categorical_crossentropy',)
history = model.fit(train_features, train_labels,batch_size=batch_size,epochs=epochs)
model.save('JH_nonFine.h5')
# 모델 빌드 (층 쌓기)

def visualize_predictions(classifier, n_cases): # 예측 모델
    for i in range(0,n_cases):
        path = random.choice([test_OnePiece_dir,test_Outer_dir,test_Pants_dir,test_Skirt_dir,test_Top_dir]) #테스트데이터 경로 랜덤으로 선택
        random_img = random.choice(os.listdir(path))
        img_path = os.path.join(path, random_img)# 테스트 이미지 랜덤으로 선택
        img = image.load_img(img_path, target_size=(img_width, img_height)) # 랜덤으로 가져온 데이터 전처리
        img_tensor = image.img_to_array(img)
        img_tensor /= 255. # 데이터 0~1사이값으로 전처리
        features = conv_base.predict(img_tensor.reshape(1,img_width, img_height, 3))
        try:
            prediction = classifier.predict_classes(features)
        except:
            prediction = classifier.predict_classes(features.reshape(1, train_features.shape[1]*train_features.shape[2]*train_features.shape[3]))

        print(img_path)
        print(prediction)
        
        if prediction == 0:
            print('Onepiece')
        elif prediction == 1:
            print('Outer')
        elif prediction == 2:
            print('Pants')
        elif prediction == 3:
            print('Skirt')
        else:
            print('Top')
        # if문을 통해 output을 쉽게 비교하기
        
visualize_predictions(model, 1000)
# 1000번의 테스트 예측
