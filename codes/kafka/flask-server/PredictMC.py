import deploy_functions as dpf
from markovchain import MarkovChain
import os
import numpy as np

class PredictMC:
    
	def __init__(self):

		path_ini = os.getcwd()+'/resources/models/mc_model/mc_initial.npy'
		path_trans = os.getcwd()+'/resources/models/mc_model/mc_transition.npy'

		trans = np.load(path_trans)
		pi = np.load(path_ini)

		self.model = MarkovChain(transition=trans, initial=pi, states=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])

	def predict(self, seq):
		temp = [i for i in seq]
		res = dpf.mc_predict_next_state(self.model, temp)         

		return  res

