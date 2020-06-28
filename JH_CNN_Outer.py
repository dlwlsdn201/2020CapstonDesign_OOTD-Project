"""상위 카테고리에서 나눠지는 여러개의 하위 카테고리에 대한 Test를 거치고 싶을 때"""

import numpy as np
import random
from keras.preprocessing import image
import os
from keras.preprocessing.image import ImageDataGenerator
from keras import models
from keras import layers
from keras import optimizers
import keras

base_dir = 'D:/dataset/'
train_dir = os.path.join(base_dir, 'Trainset')

test='D:/dataset/Testset/Outer/'
test_Outer_Blouson_dir=os.path.join(test,'Outer_Blouson')
test_Outer_Bluejean_jacket_dir=os.path.join(test,'Outer_Bluejean_jacket')
test_Outer_Cardigan_dir=os.path.join(test,'Outer_Cardigan')
test_Outer_Nylon_Jacket_dir=os.path.join(test,'Outer_Nylon_Jacket')
test_Outer_Padding_dir=os.path.join(test,'Outer_Padding')
test_Outer_Suit_jacket_dir=os.path.join(test,'Outer_Suit_jacket')
test_Outer_ThinCoat_dir=os.path.join(test,'Outer_ThinCoat')
test_Outer_WinterCoat_dir=os.path.join(test,'Outer_WinterCoat')

epochs = 3
img_width, img_height = 220, 220
train_size = 800
conv_base = keras.applications.InceptionV3(weights='imagenet',include_top = False,input_shape=(img_width, img_height, 3))
conv=conv_base.output.shape

conv_base.summary()
datagen = ImageDataGenerator(rescale=1. / 255)
batch_size = 16


def extract_features(directory, sample_count):  #라벨링
    features = np.zeros(shape=(sample_count, conv[1], conv[2], conv[3]))
    labels = np.zeros(shape=(sample_count,3))
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
model.add(layers.Dense(3, activation='softmax'))
model.summary()
model.compile(optimizer=optimizers.Adam(0.001),loss='categorical_crossentropy',)
history = model.fit(train_features, train_labels,batch_size=batch_size,epochs=epochs)
model.save('JH_nonFine.h5')
# 빌드 모델



def visualize_predictions(classifier, n_cases): #
    for i in range(0,n_cases):
        path = random.choice([test_Outer_Blouson_dir,test_Outer_Bluejean_jacket_dir,test_Outer_Cardigan_dir,test_Outer_Nylon_Jacket_dir,test_Outer_Padding_dir,test_Outer_Suit_jacket_dir,test_Outer_ThinCoat_dir,test_Outer_WinterCoat_dir]) #테스트데이터 경로 랜덤으로 선택
        random_img = random.choice(os.listdir(path))
        img_path = os.path.join(path, random_img)# 테스트 이미지 랜덤으로 선택
        img = image.load_img(img_path, target_size=(img_width, img_height)) #랜덤으로 가져온 데이터 전처리
        img_tensor = image.img_to_array(img)
        img_tensor /= 255. #데이터 0~1사이값으로 전처리
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
        
                
visualize_predictions(model, 10)