# -*- coding: utf-8 -*-
"""data 2014 onwards Open Sample.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kRxDtqQgJOcAzXe1s9Y0yHYlvCAOAa6m
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn as skl
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
data = pd.read_csv('/content/drive/My Drive/Colab Notebooks/aapl.us.txt',sep=',', index_col='Date', parse_dates=['Date'], date_parser=dateparse).fillna(0)
#plot close price
#plt.figure(figsize=(10,6))
# plt.grid(True)
# plt.xlabel('Year')
# plt.ylabel('Close Prices')
# All months data of 2017 for Close price
#data.tail()
#plt.title('All months data of 2017 for Close price')
#plt.plot(data.loc['2017-01-01':'2017-12-31']['Close'])
#plt.figure()
## Difference of close values for each date
#plt.title('Difference of close values for each date')
#plt.plot(np.diff(data.loc['2017-01-01':'2017-12-31']['Close']))
#plt.figure()
## Histogram for values
#plt.title('Histogram for values of Close for each date')
#plt.hist(np.diff(data.loc['2017-01-01':'2017-12-31']['Close']))
## plt.title('Closing Price')
## plt.show()
#plt.figure(figsize=(10,6))
## plt.grid(True)
## plt.xlabel('Year')
## plt.ylabel('Close Prices')
## All close date in file
#plt.title('All Close prices in file')
#plt.plot(data['Close'])
#plt.figure()
## Difference of Close prices
#plt.title('Difference of Close prices in file')
#plt.plot(np.diff(data['Close']))
#plt.figure()
## Histogram for whole data
#plt.title('Histogram for whole Close prices in file')
#plt.hist(np.diff(data['Close']))
#plt.figure()
#df_close = data['Close']
#df_close.plot(style='k.')
#plt.title('Scatter plot of closing price')
#plt.show()
##data.shape
## train, test = train_test_split(data, test_size=0.33)
#data.head()
data = data.loc['2014-01-01':'2017-12-31']
df1=data.reset_index()['Open']
#df1
#plt.plot(df1)
scaler=MinMaxScaler(feature_range=(0,1))
df1=scaler.fit_transform(np.array(df1).reshape(-1,1))
#print(df1)
training_size=int(len(df1)*0.67)
test_size=len(df1)-training_size
train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
training_size,test_size

# convert an array of values into a dataset matrix
def create_dataset(dataset, time_step=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-time_step-1):
		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
		dataX.append(a)
		dataY.append(dataset[i + time_step, 0])
	return np.array(dataX), np.array(dataY)
 
 
# reshape into X=t,t+1,t+2,t+3 and Y=t+4
time_step = 100
X_train, y_train = create_dataset(train_data, time_step)
X_test, ytest = create_dataset(test_data, time_step)
#print(X_train.shape), print(y_train.shape)

# reshape input to be [samples, time steps, features] which is required for LSTM
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

#X_train, X_test

### Create the Stacked LSTM model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.summary()

model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=100,batch_size=64,verbose=1)

import tensorflow as tf
### prediction and check performance metrics
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)

##Transformback to original form
train_predict=scaler.inverse_transform(train_predict)
test_predict=scaler.inverse_transform(test_predict)

import math 
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train,train_predict))

### Test Data RMSE
math.sqrt(mean_squared_error(ytest,test_predict))

### Plotting 
# shift train predictions for plotting
look_back=100
trainPredictPlot = np.empty_like(df1)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[look_back:len(train_predict)+look_back, :] = train_predict
# shift test predictions for plotting
testPredictPlot = np.empty_like(df1)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(train_predict)+(look_back*2)+1:len(df1)-1, :] = test_predict
# plot baseline and predictions
plt.plot(scaler.inverse_transform(df1))
plt.plot(trainPredictPlot)
#plt.figure()
plt.plot(testPredictPlot)
#plt.figure()
plt.show()

len(test_data)

x_input=test_data[(len(test_data) - 100):].reshape(1,-1)
x_input.shape

temp_input=list(x_input)
temp_input=temp_input[0].tolist()

# demonstrate prediction for next 10 days
from numpy import array

lst_output=[]
n_steps=100
i=0
while(i<30):
    
    if(len(temp_input)>100):
        #print(temp_input)
        x_input=np.array(temp_input[1:])
        print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1, n_steps,1))
        yhat = model.predict(x_input, verbose=0)
        print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1
  
print(lst_output)

day_new=np.arange(1,101)
day_pred=np.arange(101,131)

len(df1)

plt.plot(day_new,scaler.inverse_transform(df1[8264:]))
plt.plot(day_pred,scaler.inverse_transform(lst_output))

df3=df1.tolist()
df3.extend(lst_output)
plt.plot(df3[1200:])

df3=scaler.inverse_transform(df3).tolist()

plt.plot(df3)