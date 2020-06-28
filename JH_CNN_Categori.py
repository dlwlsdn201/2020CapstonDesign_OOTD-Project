"""CNN 모델 구현중일 때 설계한 트레이닝 모델(트레이닝 시간이 너무 오래걸림)"""
import keras
from keras.layers import Dense, Input, Activation
from keras.models import Model
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
# 모듈 선언
img_width, img_height = 220, 220   # 이미지 사이즈 조절
batch_size=32
epochs=50
input=Input(shape=(img_width,img_height,3))
model = keras.applications.InceptionV3(input_tensor=input, include_top=False, weights='imagenet', pooling='max')
x = model.output
x = Dense(512, kernel_initializer='uniform')(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dense(5, activation='softmax', name='softmax')(x)
model = Model(model.input, x)
model.summary()

train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
        'D:/dataset1/Trainset', \
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')  #타겟사이즈,라벨링
model.compile(loss='categorical_crossentropy',optimizer=optimizers.adam())
history = model.fit_generator(train_generator,epochs=epochs,)
model.save('JH_Top_Model')


