from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import Input
from vectorBuilder import createVectors
from vectorBuilder import getLastVector
from matplotlib import pyplot
import os

time = "quaterly"
predictTime = 4
numYear = 4
path = ".//data//quaterlyRequest//incomeS"
dir_list = os.listdir(path)
stockList = dir_list

xVal = getLastVector(stockList, numYear=numYear, time=time)

xTrain, yTrain, xTest, yTest = createVectors(stockList, numYear=numYear, trainPercentage=0.7, time=time, predictTime=predictTime)

print(xTrain.shape)
print(yTrain.shape)
print(xTest.shape)
print(yTest.shape)

model = Sequential()
model.add(LSTM(100, return_sequences=True, input_shape=(xTrain.shape[1], xTrain.shape[2])))
model.add(Dropout(0.2))
model.add(LSTM(units=100,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(20))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')

history = model.fit(xTrain, yTrain, epochs=70, verbose=2, validation_data=(xTest, yTest), shuffle=False, batch_size=32)

pyplot.plot(history.history['loss'], label='train')
pyplot.plot(history.history['val_loss'], label='test')
pyplot.legend()
# pyplot.show()

yhat = model.predict(xVal)
tuples = []
for s, y in zip(stockList, yhat):
    tuples.append([s, y])

sortedTuples = sorted(tuples, key=lambda tup: tup[1])
for i in sortedTuples:
    print(i)