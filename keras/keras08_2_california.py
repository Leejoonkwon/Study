from sklearn.datasets import fetch_california_housing
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

#1. 데이터
datasets = fetch_california_housing()
x = datasets.data
y = datasets.target
x_train, x_test ,y_train, y_test = train_test_split(
          x, y, train_size=0.94,shuffle=True,random_state=12)
# print(x)
# print(y)
# print(x.shape) # (20640, 8)
# print(y.shape) # (20640,)

# print(datasets.feature_names)
# print(datasets.DESCR)

#2. 모델구성
model = Sequential()
model.add(Dense(5, input_dim=8))
model.add(Dense(12))
model.add(Dense(27))
model.add(Dense(38))
model.add(Dense(42))
model.add(Dense(50))
model.add(Dense(32))
model.add(Dense(24))
model.add(Dense(12))
model.add(Dense(8))
model.add(Dense(1))

#3. 컴파일,훈련

model.compile(loss='mse', optimizer='adam')
model.fit(x_train, y_train, epochs=100, batch_size=80)

#4. 평가,예측
loss = model.evaluate(x_test, y_test)
print('loss :', loss)

y_predict = model.predict(x_test)

from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_predict)
print('r2스코어 :', r2)

# [실습 시작!!] #0.54이상
# loss : 0.5898192524909973
# r2스코어 : 0.5617319420274233
