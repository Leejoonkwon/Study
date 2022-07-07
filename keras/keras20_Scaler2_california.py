#  과제
# activation : sigmoid,relu,linear
# metrics 추가
# EarlyStopping  넣고
# 성능비교
# 감상문 2줄이상!
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint
import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus']=False
import time

#1. 데이터
datasets = fetch_california_housing()
x = datasets.data #데이터를 리스트 형태로 불러올 때 함
y = datasets.target
x_train, x_test ,y_train, y_test = train_test_split(
          x, y, train_size=0.8,shuffle=True,random_state=100)
from sklearn.preprocessing import MaxAbsScaler,RobustScaler 
from sklearn.preprocessing import MinMaxScaler,StandardScaler
# scaler = MinMaxScaler()
# scaler = StandardScaler()
# scaler = MaxAbsScaler()
scaler = RobustScaler()

scaler.fit(x_train) #여기까지는 스케일링 작업을 했다.
scaler.transform(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)
# print(x.shape, y.shape) #(506, 13)-> 13개의 피쳐 (506,) 

# print(datasets.feature_names)
# print(datasets.DESCR)


#2. 모델구성
model = Sequential()
model.add(Dense(100,input_dim=8))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))
import datetime
date = datetime.datetime.now()
print(date)

date = date.strftime("%m%d_%H%M") # 0707_1723
print(date)


# #3. 컴파일,훈련
filepath = './_ModelCheckPoint/K24/'
filename = '{epoch:04d}-{val_loss:.4f}.hdf5'
#04d :                  4f : 
earlyStopping = EarlyStopping(monitor='loss', patience=10, mode='min', 
                              verbose=1,restore_best_weights=True)
mcp = ModelCheckpoint(monitor='val_loss',mode='auto',verbose=1,
                      save_best_only=True, 
                      filepath="".join([filepath,'k25_', date, '_', filename])
                    )
model.compile(loss='mae', optimizer='adam')

start_time = time.time()
print(start_time)
hist = model.fit(x_train, y_train, epochs=150, batch_size=150, 
                validation_split=0.3,
                callbacks = [earlyStopping],
                verbose=2
                )

end_time = time.time() - start_time

#verbose = 0으로 할 시 출력해야할 데이터가 없어 속도가 빨라진다.강제 지연 발생을 막는다.



#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)
y_predict = model.predict(x_test)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 :', r2)
print("걸린 시간 :",end_time)

# print("============")
# print(hist) #<tensorflow.python.keras.callbacks.History object at 0x000001B6B522F0A0>
# print("============")
# # print(hist.history) #(지정된 변수,history)를 통해 딕셔너리 형태의 데이터 확인 가능 
# print("============")
# print(hist.history['loss'])
# print("============")
# print(hist.history['val_loss'])
# print("걸린시간 :",end_time)
# # y_predict = model.predict(x_test)
# plt.figure(figsize=(9,6))
# plt.plot(hist.history['loss'],marker='.',c='red',label='loss') #순차적으로 출력이므로  y값 지정 필요 x
# plt.plot(hist.history['val_loss'],marker='.',c='blue',label='val_loss')
# plt.grid()
# plt.title('영어싫어') #맥플러립 한글 깨짐 현상 알아서 해결해라 
# plt.ylabel('loss')
# plt.xlabel('epochs')
# # plt.legend(loc='upper right')
# plt.legend()
# plt.show()
# validation 적용 전
# [실습 시작!!] #0.54이상
# loss : 0.5898192524909973
# r2스코어 : 0.5617319420274233
#################
# validation 적용 후
# loss : 0.5187357664108276
# r2스코어 : 0.606785090759131
##################
# EarlyStopping 적용 및 활성화 함수 적용
# loss : 0.5606501698493958
# r2스코어 : 0.5248489028606996
##################
#1. 스케일러 하기전
# loss : 3.1941933631896973
# r2스코어 : 0.8146167932510104
##################
#2. 민맥스
# loss : 0.3700266182422638
# r2스코어 : 0.7486719942735911
##################
#3. 스탠다드
# loss : 0.3460002839565277
# r2스코어 : 0.8088948945752725
#4. 절댓값
# loss : 0.4312553405761719
# r2스코어 : 0.686649003612051
# 걸린 시간 : 36.01555895805359
#5. RobustScaler
# loss : 0.3402252495288849
# r2스코어 : 0.7961290757181281
# 걸린 시간 : 34.902045249938965

