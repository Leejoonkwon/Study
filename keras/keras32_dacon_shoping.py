#  과제
# activation : sigmoid,relu,linear
# metrics 추가
# EarlyStopping  넣고
# 성능비교
# 감상문 2줄이상!
from tensorflow.python.keras.models import Sequential,load_model
from tensorflow.python.keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import EarlyStopping,ModelCheckpoint
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
import matplotlib
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus']=False
import pandas as pd

#1. 데이터
path = './_data/kaggle_shopping/' # ".은 현재 폴더"
train_set = pd.read_csv(path + 'train.csv',
                        index_col=0)
print(train_set)

print(train_set.shape) #(6255, 12)

test_set = pd.read_csv(path + 'test.csv', #예측에서 쓸거야!!
                       index_col=0)
submission = pd.read_csv(path + 'sample_submission.csv',#예측에서 쓸거야!!
                       index_col=0)
                       
print(test_set)
print(test_set.shape) #(180,11) #train_set과 열 값이 '1'차이 나는 건 count를 제외했기 때문이다.예측 단계에서 값을 대입

print(train_set.columns)
# 'Store', 'Date', 'Temperature', 'Fuel_Price', 'Promotion1',
#        'Promotion2', 'Promotion3', 'Promotion4', 'Promotion5', 'Unemployment',
#        'IsHoliday', 'Weekly_Sales'
# print(train_set.info()) #null은 누락된 값이라고 하고 "결측치"라고도 한다.
# print(train_set.describe()) 
print(test_set.columns)
# 'Store', 'Date', 'Temperature', 'Fuel_Price', 'Promotion1',
#        'Promotion2', 'Promotion3', 'Promotion4', 'Promotion5', 'Unemployment',
#        'IsHoliday'

###### 결측치 처리 1.제거##### dropna 사용
print(train_set.isnull().sum()) #각 컬럼당 결측치의 합계
# Store              0
# Date               0
# Temperature        0
# Fuel_Price         0
# Promotion1      4153 
# Promotion2      4663
# Promotion3      4370
# Promotion4      4436
# Promotion5      4140
# Unemployment       0
# IsHoliday          0
# Weekly_Sales       0
print(test_set.isnull().sum()) #각 컬럼당 결측치의 합계
# Store             0
# Date              0
# Temperature       0
# Fuel_Price        0
# Promotion1        2
# Promotion2      135
# Promotion3       19
# Promotion4       34
# Promotion5        0
# Unemployment      0
# IsHoliday         0
cols = ['IsHoliday']
for col in cols:
    le = LabelEncoder()
    train_set[col]=le.fit_transform(train_set[col])
    test_set[col]=le.fit_transform(test_set[col])
train_set = train_set.fillna(train_set.mean())
print(train_set.isnull().sum())
print(train_set.shape)
test_set = train_set.fillna(test_set.mean())
print(test_set.isnull().sum())
# train_set = pd.get_dummies((train_set['IsHoliday'])) 
# test_set = pd.get_dummies((test_set['IsHoliday']))
x = train_set.drop(['Weekly_Sales','Date'], axis=1) #axis는 컬럼 


print(x.shape) #(6255, 11)
print(train_set)


y = train_set['Weekly_Sales']
print(y.shape) 

x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size = 0.919, shuffle = True, random_state = 100)
from sklearn.preprocessing import MaxAbsScaler,RobustScaler 
from sklearn.preprocessing import MinMaxScaler,StandardScaler
# scaler = MinMaxScaler()
scaler = StandardScaler()
# scaler = MaxAbsScaler()
# scaler = RobustScaler()
scaler.fit(x_train) #여기까지는 스케일링 작업을 했다.
scaler.transform(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

#2. 모델구성
model = Sequential()
model.add(Dense(100,input_dim=10))
model.add(Dense(60,input_shape=(784,),activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(60,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(60,activation='swish'))
model.add(Dropout(0.3))
model.add(Dense(60, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(60, activation='relu'))
model.add(Dropout(0.3))
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
                      filepath="".join([filepath,'k25_', date, '_kaggle_shopping', filename])
                    )
model.compile(loss='mae', optimizer='adam')

hist = model.fit(x_train, y_train, epochs=550, batch_size=20, 
                validation_split=0.3,
                callbacks = [earlyStopping,mcp],
                verbose=2
                )

#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)
y_predict = model.predict(x_test)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 :', r2)

import matplotlib
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus']=False
import time
# y_predict = model.predict(x_test)
plt.figure(figsize=(9,6))
plt.plot(hist.history['loss'],marker='.',c='red',label='loss') #순차적으로 출력이므로  y값 지정 필요 x
plt.plot(hist.history['val_loss'],marker='.',c='blue',label='val_loss')
plt.grid()
plt.title('영어싫어') #맥플러립 한글 깨짐 현상 알아서 해결해라 
plt.ylabel('loss')
plt.xlabel('epochs')
# plt.legend(loc='upper right')
plt.legend()
plt.show()
