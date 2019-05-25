# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 07:43:38 2018

@author: DELL
"""
import numpy as np
import pandas as pd
import chardet
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

#df = pd.DataFrame()
#df = pd.read_csv('seq_events.txt')
#with open('seq_events.txt', 'rb') as f:
#    result =  chardet.detect(f.read())


with open('seq_events.txt','rb') as p:
      a = pickle.load(p) 
      
for i in range (len(a)):
    for j in range(len(a[i])):

        a[i][j] +=1

   
enc = OneHotEncoder()
enc.fit([[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18]])
def createDataset(a,bucketSize=10,opSize=6):
    
    x = []
    y = []
    print('initiating')    
    for i in a:
        temp = []
        temp1 = []
        
        if len(i)> bucketSize:
            for j in range(len(i)-1):
                #if j < bucketSize-1:
                #temp.append(i[j])
                #    continue
                temp.append(i[j])
                x.append(temp.copy())
                y.append(i[j+1:])
        else:
            for j in range(len(i)-1):
                temp.append(i[j])
                x.append(temp.copy())
                y.append(i[j+1:])
            
    print('truncating')
    for i in range(len(x)):
        if len(x[i])>bucketSize:
            x[i] = x[i][len(x[i])-bucketSize:]
        if len(y[i])> opSize:
            y[i] = y[i][:opSize] 
            
    print('padding')
    for i in range(len(x)):
        if len(x[i])<bucketSize:
            n =bucketSize- len(x[i])
            for j in range(n):
                x[i] = [0]+x[i]
        if len(y[i])<opSize:
            n =opSize- len(y[i])
            for j in range(n):
                y[i].append(0)
    print('finializing')
    for i in range(len(x)):
        x[i] = np.array(x[i])
    for i in range(len(y)):
        y[i] = np.array(y[i])
    x = np.array(x)
    y = np.array(y)
    #x = x.reshape(len(x),1,bucketSize)
    y = y.reshape(len(y),opSize)
    return x,y

x,y = createDataset(a,100,10)
y=y/19
#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
 