import deploy_functions as dpf
import hmm as hmm
import os
import numpy as np

class PredictHMM:
    
	def __init__(self):

	def predict(self, seq):
		
		N = 25
	    M = 19
	    T = len(seq)
		temp = [i for i in seq]
		
		trms = np.load('resources/models/hmm_model/'+str(T)+'_a.npy')
	    emis = np.load('resources/models/hmm_model/'+str(T)+'_b.npy')
	    pri = np.load('resources/models/hmm_model/'+str(T)+'_pi.npy')
	    model = hmm.HMM(N, M, T, transmission=trms, emission=emis, prior=pri)

		res = dpf.predict_next_state(model, temp, T)         

		return  res

