#  과제
# activation : sigmoid,relu,linear
# metrics 추가
# EarlyStopping  넣고
# 성능비교
# 감상문 2줄이상!
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.callbacks import EarlyStopping
matplotlib.rcParams['font.family']='Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus']=False


#1. 데이터
path = './_data/kaggle_bike/' # ".은 현재 폴더"
train_set = pd.read_csv(path + 'train.csv',
                        index_col=0)
print(train_set)

print(train_set.shape) #(10886, 11)

test_set = pd.read_csv(path + 'test.csv', #예측에서 쓸거야!!
                       index_col=0)

sampleSubmission = pd.read_csv(path + 'sampleSubmission.csv',#예측에서 쓸거야!!
                       index_col=0)
            
print(test_set)
print(test_set.shape) #(6493, 8) #train_set과 열 값이 '1'차이 나는 건 count를 제외했기 때문이다.예측 단계에서 값을 대입

print(train_set.columns)
print(train_set.info()) #null은 누락된 값이라고 하고 "결측치"라고도 한다.
print(train_set.describe()) 


###### 결측치 처리 1.제거##### dropna 사용
print(train_set.isnull().sum()) #각 컬럼당 결측치의 합계
print(train_set.shape) #(10886,11)


x = train_set.drop([ 'casual', 'registered','count'],axis=1) #axis는 컬럼 


print(x.columns)
print(x.shape) #(10886, 8)

y = train_set['count']
x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size = 0.949, shuffle = True, random_state = 100
 )
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
print(test_set)
# print(y)
# print(y.shape) # (10886,)


#2. 모델구성
model = Sequential()
model.add(Dense(100,input_dim=8))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1))
model.summary()
# Total params: 21,201
# Trainable params: 21,201
# Non-trainable params: 0
import time
start_time = time.time()
#3. 컴파일,훈련
earlyStopping = EarlyStopping(monitor='loss', patience=100, mode='min', 
                              verbose=1,restore_best_weights=True)
model.compile(loss='mae', optimizer='adam')

hist = model.fit(x_train, y_train, epochs=1010, batch_size=2500, 
                validation_split=0.3,
                callbacks = [earlyStopping],
                verbose=2)

#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)
y_predict = model.predict(x_test)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 :', r2)
end_time = time.time()-start_time
print("걸린시간 :",end_time)
# print("============")
# print(hist) #<tensorflow.python.keras.callbacks.History object at 0x000001B6B522F0A0>
# print("============")
# # print(hist.history) #(지정된 변수,history)를 통해 딕셔너리 형태의 데이터 확인 가능 
# print("============")
# print(hist.history['loss'])
# print("============")
# print(hist.history['val_loss'])
# # y_predict = model.predict(x_test)
# plt.figure(figsize=(9,6))
# plt.plot(hist.history['loss'],marker='.',c='red',label='loss') #순차적으로 출력이므로  y값 지정 필요 x
# plt.plot(hist.history['val_loss'],marker='.',c='blue',label='val_loss')
# plt.grid()
# plt.title('이결바보') #맥플러립 한글 깨짐 현상 알아서 해결해라 
# plt.ylabel('loss')
# plt.xlabel('epochs')
# # plt.legend(loc='upper right')
# plt.legend()
# plt.show()

# loss : 356.1080
# RMSE :  50.77395531000674
###################
# activation 및 EarlyStopping 으로 적용 후
# loss : 97.43128967285156
# r2스코어 : 0.3425327427467255

#####################################
# EarlyStopping  적용 및 활성화 함수
# loss : 30.648914337158203
# r2스코어 : 0.7276545891537277
##################
#1. 스케일러 하기전
# loss : 97.43128967285156
# r2스코어 : 0.3425327427467255
##################
#2. MinMaxScaler
# loss : 94.7766342163086
# r2스코어 : 0.3555606095041368
# 걸린시간 : 36.777430057525635
##################
#3. StandardScaler
# loss : 94.6276626586914
# r2스코어 : 0.3632466637287737
# 걸린시간 : 38.000826358795166
##################
#4. MaxAbsScaler
# loss : 96.97545623779297
# r2스코어 : 0.3390128944655548
# 걸린시간 : 37.0623733997345
##################
#5. RobustScaler
# loss : 95.10087585449219
# r2스코어 : 0.3657807949740439
# 걸린시간 : 37.770310163497925