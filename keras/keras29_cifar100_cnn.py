#칼라 
#분류 100
# 32
# 컴불루션 3개 이상 
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D,Dropout
from keras.datasets import mnist,cifar10,cifar100
import pandas as pd
import numpy as np


#1. 데이터 전처리

(x_train, y_train), (x_test, y_test) = cifar100.load_data()

print(x_train.shape,y_train.shape) #(50000, 32, 32, 3) (50000, 1)
print(x_test.shape,y_test.shape) #(10000, 32, 32, 3) (10000, 1)

x_train = x_train.reshape(50000, 32*32* 3)
x_test = x_test.reshape(10000, 32*32*3)
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, QuantileTransformer, PowerTransformer
scaler = StandardScaler()
scaler.fit(x_train) #여기까지는 스케일링 작업을 했다.
scaler.transform(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)
x_train = x_train.reshape(50000, 32,32, 3)
x_test = x_test.reshape(10000, 32,32,3)
print(x_train.shape) #(50000, 32, 32, 3, 1)
print(x_test.shape) #(10000, 32, 32, 3, 1)
print(np.unique(y_train,return_counts=True))

# (array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
#        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
#        34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
#        51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
#        68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
#        85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]), array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500,
#        500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=int64))
print(y_train.shape) #(50000, 100)
print(y_test.shape) #(10000, 10)
from tensorflow.keras.utils import to_categorical 
y_train = to_categorical(y_train) 
y_test = to_categorical(y_test) 

# y_train = pd.get_dummies((y_train)) 
# y_test = pd.get_dummies((y_test))
print(y_train.shape) #(50000, 100)
print(y_test.shape) #(10000, 100)


#2. 모델 구성
model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(5, 5),   # 출력(4,4,10)                                       # 자르는 사이즈 (행,렬 규격.) 10= 다음레이어에 주는 데이터
                 padding='same',
                 input_shape=(32, 32, 3)))    #(batch_size, row, column, channels)       # N(장수) 이미지 5,5 짜리 1 흑백 3 칼라 
                                                                                           # kernel_size(2*2) * 바이어스(3) + 10(output)
model.add(MaxPooling2D())

 #    (kernel_size * channls) * filters = summary Param 개수(CNN모델)  
model.add(Conv2D(32, (2,2), 
                 padding = 'valid',         # 디폴트값(안준것과 같다.) 
                 activation= 'relu'))    # 출력(3,3,7)                                                     
model.add(MaxPooling2D())                                              
model.add(Flatten()) # (N, 63)
model.add(Dense(1000,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(1000,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(1000,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(1000,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(1000, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(100, activation='softmax'))
model.summary()

#3. 컴파일 훈련
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint
earlyStopping = EarlyStopping(monitor='loss', patience=150, mode='min', 
                              verbose=1,restore_best_weights=True)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=10000, batch_size=5000, 
                callbacks = [earlyStopping],
                verbose=2
                )
model.save_weights("./_save/keras23_5_cifar10_2.h5")
#4. 평가 예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)
y_predict = model.predict(x_test)
from sklearn.metrics import r2_score,accuracy_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 :', r2)
y_test = np.argmax(y_test,axis=1)
print(y_test)

y_predict = np.argmax(y_predict,axis=1)
# y_test와 y_predict의  shape가 일치해야한다.
print(y_predict)


acc = accuracy_score(y_test, y_predict)
print('acc 스코어 :', acc)

# loss : [3.8618671894073486, 0.45080000162124634]
# r2스코어 : 0.1313088401031084
# acc 스코어 : 0.4508

