import numpy as np  
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense

#1. 데이터
x = np.array([[1,2,3,4,5,6,7,8,9,10],
              [1, 1, 1, 1, 2, 1.3, 1.4, 1.5, 1.6, 1.4],
              [9,8,7,6,5,4,3,2,1,0]]
             )
y = np.array([11,12,13,14,15,16,17,18,19,20])

print(x.shape) # (3, 10)
print(y.shape) # (10,)

# x = x.T
# x = x.transtpose(10,3)
x = x.T
print(x)
print(x.shape) #(10,3)


# [숙제] 모델을 완성하시오
# 예측 : [[10, 1.4, 0]]

#2. 모델구성
model = Sequential()
model.add(Dense(5,input_dim=3))
model.add(Dense(4))
model.add(Dense(3))
model.add(Dense(3))
model.add(Dense(3))
model.add(Dense(4))
model.add(Dense(1))

#3. 컴파일,훈련
model.compile(loss='mse', optimizer='adam')
model.fit(x, y , epochs=250, batch_size=1)

#4. 평가,예측
loss = model.evaluate(x,y)
print('loss :',loss)
result = model.predict([[10, 1.4, 0]])
print('[10,1.4]의 예측값 :',result)

#loss : 2.1824778741574846e-05
#[10,1.4]의 예측값 : [[20.003965]]




