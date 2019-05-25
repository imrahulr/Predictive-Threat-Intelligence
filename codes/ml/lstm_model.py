# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 15:17:50 2018

@author: DELL
"""
#train = [0.8800638508054404, 0.8308913162468462, 0.8219439168369428, 0.8082491402602444, 0.7961724407886273, 0.7711620279608957, 0.772112811812399, 0.7514114560731319, 0.7446600184486958, 0.7493572395866271]
#test = [0.8805422049318319, 0.8315030137034097, 0.8230768559789957, 0.8092600507662919, 0.7970569507078495, 0.7730171052746352, 0.7736451418752126, 0.7527803703671397, 0.7461074814860044, 0.7522046701499437]
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import TimeDistributed
from keras.models import load_model
from keras.utils import plot_model
 
def acc(z,j):
    count = 0
    for i in z:
        if (abs(i[j])<.5):
            count+=1
        
    return count/len(z)


def accuracy(x,y):
    a = model.predict(x)*19
    
    a=a-y.reshape(len(y),10)*19
    
    return [acc(a,i) for i in range(10)]


#model = load_model(r'model.h5')

model = Sequential()
 
model.add(LSTM(100, input_shape=(1,100),return_sequences=True,init = 'glorot_normal',activation='sigmoid'))

model.add(LSTM(output_dim=10,input_shape = (1,10),return_sequences=False,init = 'glorot_normal',activation='tanh'))


#model.add(TimeDistributed(Dense(6), input_shape=(1, 10)))

#model.add(LSTM(6,input_shape=(1,6)))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1000, batch_size=256, verbose=1,validation_data=(x_test, y_test))
#model.fit(x, y, epochs=1000, batch_size=256, verbose=1)



train = accuracy(x_train,y_train)
test = accuracy(x_test,y_test)