import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm_notebook as tqdm

enc = LabelEncoder()
enc.fit(['cowrie.session.connect', 'cowrie.client.version',
       'cowrie.login.success', 'cowrie.session.closed',
       'cowrie.login.failed', 'cowrie.log.closed',
       'cowrie.direct-tcpip.request', 'cowrie.log.open',
       'cowrie.command.input/other', 'cowrie.command.success',
       'cowrie.command.failed', 'cowrie.command.input/delete',
       'cowrie.command.input/dir_sudo', 'cowrie.command.input/write',
       'cowrie.direct-tcpip.data', 'cowrie.client.size',
       'cowrie.session.file_download', 'cowrie.command.input/system',
       'cowrie.session.input'])

def array_to_df(d):
    k = pd.DataFrame(d)
    return k 

def find_inp_type(eventid, inp):
    if eventid != "cowrie.command.input":
        return eventid
    if inp.find("rm")!=-1:
        return "cowrie.command.input/delete"
    if inp.find("nano")!=-1 or inp.find("gedit")!=-1 or inp.find("cp")!=-1 or inp.find("mv")!=-1 or inp.find("mkdir")!=-1:
        return "cowrie.command.input/write"
    if inp.find("sudo")!=-1 or inp.find("cd")!=-1 or inp.find("pwd")!=-1 or inp.find("ls")!=-1:
        return "cowrie.command.input/dir_sudo"
    if inp.find("free")!=-1 or inp.find("uname")!=-1 or inp.find("history")!=-1 or inp.find("df")!=-1 or inp.find("du")!=-1 or inp.find("top")!=-1 or inp.find("lsb_release")!=-1:
        return "cowrie.command.input/system"
    if inp.find("adduser")!=-1 or inp.find("passwd")!=-1:
        return "cowrie.command.input/adduser"
    return "cowrie.command.input/other"

def proc_data(df):
    df['eventid'] = df.apply(lambda x: find_inp_type(x['eventid'], x['input']), axis=1)
    df['eventid'] = enc.transform(df['eventid'])
    df_list = df.groupby('session', as_index=False).agg(lambda x: x.tolist())
    a = df_list[['session', 'eventid']]
    del df_list,df
    seq = []
    for i in tqdm(a.index):
        i_seq = []
        for j in a.loc[i, 'eventid']:
            i_seq.append(j)
        seq.append(i_seq)
    return seq

def predict_seq_probability(mod, seq, length):
    if(len(seq) <= length):
        return mod.likelihood(seq)
    else:
        return mod.likelihood(seq[len(seq)-length:])
    
def predict_next_state(mod, seq, length):
    prob = []
    for i in range(1,19):
        seq.append(i)
        if(len(seq) <= length):
            prob.append(mod.likelihood(seq))
        else:
            prob.append(mod.likelihood(seq[len(seq)-length:]))
        seq = seq[:-1]
    return np.argmax(prob,axis=0) + 1

def mc_predict_seq_probability(mod, seq):
    prob = 1
    for i in range(0, len(seq)-1):
        state = seq[i]
        next_state = seq[i+1]
        prob *= mod.transition[state][next_state]
    return prob

def mc_predict_next_state(mod, seq):
    state = seq[-1]
#     if np.max(mod.transition[state]) == 0:
#         return None
    return np.argmax(mod.transition[state])