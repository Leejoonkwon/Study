from keras.datasets import mnist #tensorflow 안 써야 자동완성이 된다.
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator 

import numpy as np
import pandas as pd

#1 .데이터
(x_train, y_train), (x_test, y_test) = mnist.load_data()
train_datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    # vertical_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1,
    rotation_range=5,
    zoom_range=0.1,
    # shear_range=0.7,
    fill_mode='nearest'
)
test_datagen = ImageDataGenerator(
    rescale=1./255,)
    

augument_size = 4000

randidx = np.random.randint(x_train.shape[0],size=augument_size)

x_augumented = x_train[randidx].copy()
y_augumented = y_train[randidx].copy()


print(x_augumented.shape)  #(400, 28, 28)
print(y_augumented.shape) #(400,)
x_train = x_train.reshape(60000,28,28,1)
x_augumented = x_augumented.reshape(x_augumented.shape[0],
                                    x_augumented.shape[1],
                                    x_augumented.shape[2], 1)


x_test = x_test.reshape(x_test.shape[0],x_test.shape[1],x_test.shape[2],1)

xy_df2 = train_datagen.flow(x_train,y_train,
                                  batch_size=augument_size,shuffle=False)
x_df = np.concatenate((x_train,x_augumented))
y_df = np.concatenate((y_train,y_augumented))
# print(x_df.shape) #(64000, 28, 28, 1)

xy_df3 = test_datagen.flow(x_df,y_df,
                       batch_size=augument_size,shuffle=False)

x_train,x_test,y_train,y_test =train_test_split(xy_df3[0][0],xy_df3[0][1],train_size=0.75,shuffle=False)
np.save('D:/study_data/_save/_npy/keras49_2_train_x.npy',arr=x_train)
np.save('D:/study_data/_save/_npy/keras49_2_train_y.npy',arr=y_train)
np.save('D:/study_data/_save/_npy/keras49_2_test_x.npy',arr=x_test)
np.save('D:/study_data/_save/_npy/keras49_2_test_y.npy',arr=y_test)