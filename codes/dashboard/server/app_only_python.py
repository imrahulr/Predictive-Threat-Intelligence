import pickle   
import copy 
import os, sys, time, json
import numpy as np
import py.hmm as hmm
from py.markovchain import MarkovChain
import py.deploy_functions as dpf

#from keras.models import load_model
#model = load_model('model.h5')


def load_pickle(name):
    with open(name, 'rb') as file:
        k = pickle.load(file)
    return k


def predict(vector):
   data_arr = copy.deepcopy(vector)
   predmc = dpf.mc_predict_next_state(mcmod,data_arr)
   predhmm = dpf.predict_next_state(mod,data_arr,T)
   #data_arr = copy.deepcopy(vector)
   #data_arr = np.array(data_arr).reshape(1,1,100)   
   #res = model.predict(data_arr)*18
   #res_out = pickle.dumps([res, predmc, predhmm])
   print (predmc)
   print(predhmm)
   sys.stdout.flush()


if __name__ == '__main__':

    f= open("py/log/log.txt", "w+")
    f.write(" Start ")

    states = ['cowrie.client.size', 'cowrie.client.version', 'cowrie.command.failed', 
    'cowrie.command.input/delete', 'cowrie.command.input/dir_sudo', 'cowrie.command.input/other', 
    'cowrie.command.input/system', 'cowrie.command.input/write', 'cowrie.command.success', 
    'cowrie.direct-tcpip.data', 'cowrie.direct-tcpip.request', 'cowrie.log.closed', 
    'cowrie.log.open', 'cowrie.login.failed', 'cowrie.login.success', 'cowrie.session.closed', 
    'cowrie.session.connect', 'cowrie.session.file_download', 'cowrie.session.input']

    
    sessId = sys.argv[1]
    sess = load_pickle('py/data/seq_session.txt')
    f.write(" Sequence Session.txt ")    
    indx = sess.index(sessId)
    f.write(" Seq found ")
    
    del sess


    tr = np.load('py/weights/mc_transition.npy')
    init = np.load('py/weights/mc_initial.npy')
    mcmod = MarkovChain(transition=tr,initial=init,states=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
    f.write(" Loaded Markov Chain ")

    # f.write(index)
    k = load_pickle('py/data/seq_events.txt')
    seq = k[indx]
    
    pred1 = []
    pred1.append(seq[0])
    pred2 = []
    pred2.append(seq[0])
    
    N = 25
    M = 19
    T = len(seq)
    
    trms = np.load('py/weights/hmm/'+str(T)+'_a.npy')
    emis = np.load('py/weights/hmm/'+str(T)+'_b.npy')
    pri = np.load('py/weights/hmm/'+str(T)+'_pi.npy')
    mod = hmm.HMM(N,M,T,transmission=trms,emission=emis,prior=pri)
    f.write(" Loaded HMM ")
    
    response = []
    response.append({
        'event': states[seq[0]],
        'timestamp': '25 Aug 2018',
        'mc': states[pred1[0]],
        'hmm': states[pred2[0]],
        'valid1': 'true',
        'valid2': 'true'
    })
    f.write(" Initialized variables ")
    
    if len(seq) >= 4:
        for ind in range(1, len(seq)):
            s = seq[:ind]
            nxt1 = mcmod.next_state(s)
            nxt2 = dpf.predict_next_state(mod, s, T)
            pred1.append(nxt1)
            pred2.append(nxt2)
            
            response.append({
                'event': states[seq[ind]],
                'timestamp': '25 Aug 2018',
                'mc': states[pred1[ind]],
                'hmm': states[pred2[ind]],
                'valid1': 'false',
                'valid2': 'false'
            })
            if nxt1 == seq[ind]:
                response[ind]['valid1'] = 'true'
            if nxt2 == seq[ind]:
                response[ind]['valid2'] = 'true'

    
    f.write(" Completed predictions.. printing ")
    print (response)
    sys.stdout.flush()

    f.write(" Output Done!!! ")
    f.close()
