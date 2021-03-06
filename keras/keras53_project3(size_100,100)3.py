import numpy as np      
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

# np.save('D:\study_data\_save\_npy\_train_x5.npy',arr=x_train)
# np.save('D:\study_data\_save\_npy\_train_y5.npy',arr=y_train)
# np.save('D:\study_data\_save\_npy\_test_x5.npy',arr=x_test)
# np.save('D:\study_data\_save\_npy\_test_y5.npy',arr=y_test)
###########size 100,100으로 한 파일
 
x_train = np.load('D:\study_data\_save\_npy\_train_x9.npy')
y_train = np.load('D:\study_data\_save\_npy\_train_y9.npy')
x_test = np.load('D:\study_data\_save\_npy\_test_x9.npy')
y_test = np.load('D:\study_data\_save\_npy\_test_y9.npy')
# print(x_train.shape,y_train.shape)  # (27097, 100, 100, 1) (27097, 21)
# print(x_test.shape,y_test.shape) # (6775, 100, 100, 1) (6775, 21)

# import matplotlib.pyplot as plt
# plt.figure(figsize=(100,5))
# for i in range(300):
#     plt.subplot(6,50,i+1)
#     plt.axis('off')
#     plt.imshow(x_train[i])
# plt.show()

#2. 모델 
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D,Flatten,Dense,MaxPool2D,Dropout
# conv_base = VGG16(weights='imagenet',
#                   include_top=False,
#                   input_shape=(100,100,3))
model = Sequential()
model.add(Conv2D(input_shape=(100, 100, 1), kernel_size=(3, 3), filters=32, padding='same', activation='relu'))
model.add(Conv2D(kernel_size=(3, 3), filters=64, padding='same', activation='relu'))
model.add(MaxPool2D((2, 2)))
model.add(Dropout(0.5))

model.add(Conv2D(kernel_size=(3, 3), filters=128, padding='same', activation='relu'))
model.add(Conv2D(kernel_size=(3, 3), filters=256, padding='valid', activation='relu'))
model.add(MaxPool2D((2, 2)))
model.add(Dropout(0.5))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(21,activation='softmax'))
model.summary()

import time
from keras.callbacks import ModelCheckpoint,EarlyStopping

start_time = time.time()
#3. 컴파일,훈련
# filepath = './_test/'
# filename = '{epoch:04d}-{val_loss:.4f}.hdf5'
earlyStopping = EarlyStopping(monitor='val_loss', patience=10, mode='min', 
                              verbose=1,restore_best_weights=True)
# mcp = ModelCheckpoint(monitor='val_loss',mode='auto',verbose=1,
#                       save_best_only=True, 
#                       filepath="".join([filepath,'k24_', date, '_', filename])
#                     )
model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
hist = model.fit(x_train,y_train,epochs=10,verbose=2,
                 validation_split=0.25,
                 callbacks=[earlyStopping])
model.save_weights("D:\study_data\_save\keras53_project2.h5")
# model.save_weights("./_save/keras23_5_save_weights1.h5")

#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)
end_time = time.time()-start_time
print("걸린 시간 :",end_time)
xy = np.load('D:\study_data\_save\_npy\_train_test.npy')
y_predict = model.predict(xy)
y_predict = np.argmax(y_predict,axis=1)

print(y_predict)
# y_predict = np.argmax(y_predict,axis=1)
# y_test = np.argmax(y_test,axis=1)

# print('y_predict :', y_predict.shape) #y_predict : (50,)
# from sklearn.metrics import accuracy_score
# acc = accuracy_score(y_test, y_predict)
# print('acc 스코어 :', acc)




#### 증폭 후 데이터 3만개 일때
# loss : [1.3046691417694092, 0.507749080657959]
# 걸린 시간 : 168.37035512924194
# y_predict : (6775,)
# acc 스코어 : 0.5077490774907749
##########VGG16 적용
# loss : [0.0, 1.0]
# 걸린 시간 : 121.65885210037231
# y_predict : (6000,)
# acc 스코어 : 1.0





