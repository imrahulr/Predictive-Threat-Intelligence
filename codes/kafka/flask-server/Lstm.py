# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 15:06:35 2019

@author: DELL
"""
from keras.models import load_model
import numpy as np
import os

class Lstm:
    
    def __init__(self):
        
        path = os.getcwd()+'/resources/models/lstm_model/model.h5'
        self.model = load_model(path)

        
    def predict(self,seq,lenseq=100):
    
    
        temp = [i+1 for i in seq]
         
        
        if len(temp)> lenseq:
            temp = temp[len(temp)-lenseq:]
        if len(seq) < lenseq:
            while len(temp) is not lenseq:
                temp = [0] + temp            
        res = self.model.predict(np.array(temp).reshape(1,1,lenseq))*18     
        res = [round(i-1) for i in res[0]]
        return  res