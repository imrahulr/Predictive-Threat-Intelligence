import numpy as np
import pandas as pd
from math import log
from tqdm import tqdm_notebook as tqdm
import pickle
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import hmm

import networkx as nx
from nxpd import draw

lab = ['cowrie.client.size', 'cowrie.client.version', 'cowrie.command.failed', 'cowrie.command.input',
       'cowrie.command.input/delete', 'cowrie.command.input/dir_sudo', 'cowrie.command.input/system', 
       'cowrie.command.input/write', 'cowrie.command.success', 'cowrie.direct-tcpip.data', 'cowrie.direct-tcpip.request', 
       'cowrie.log.closed', 'cowrie.log.open', 'cowrie.login.failed', 'cowrie.login.success', 'cowrie.session.closed', 
       'cowrie.session.connect', 'cowrie.session.file_download', 'cowrie.session.input']


def load_pickle(name):
    with open(name,'rb') as file:
        k = pickle.load(file)
    print('pickle loading complete')
    return k

def vis(data1,data2,data3):
    cow = pd.concat([data1,data2,data3],axis=0)
    print ('Data Shape : '+str(cow.shape))
    display(cow.head())
    display(cow['eventid'].value_counts().plot(kind='bar', figsize=(15, 5)))
    plt.show()
    display(cow['src_ip'].value_counts()[:10].plot(kind='barh', figsize=(18, 6)))
    plt.show()
    display(cow['username'].value_counts()[:10].plot(kind='bar', figsize=(10, 5)))
    plt.show()
    display(cow['password'].value_counts()[:20].plot(kind='bar', figsize=(18, 8)))
    plt.show()
    display(cow['system'].value_counts()[:20].plot(kind='bar', figsize=(18, 7)))
    plt.show()

def process_data(data1,data2,data3):
    df = pd.concat([data1,data2,data3],axis=0)
    le = LabelEncoder()
    df['eventid'] = le.fit_transform(df['eventid'].astype('str').values)
    data_agg = df.groupby('session',as_index=False).agg(lambda x: x.tolist())
    agg = pd.DataFrame()
    agg['eventid'] = data_agg['eventid'].values
    print('processed data samples: \n')
    print(agg.head())
    with open("input/data.txt", "wb") as fp:   
        pickle.dump(agg['eventid'].values, fp)
    seqs = load_pickle('input/data.txt')
    return seqs, le

def desired_seq(df,length):
    data = []
    for i in tqdm(range(0,len(df))):
        if len(df[i]) == length:
            data.append(df[i])
    data = np.array(data)
    print('total samples found: ' + str(len(data)) + '\n')
    print('few samples of data of sequence length ' + str(length))
    print(data[:5])
    return data

def calculate_probablity(mod,df):
    prob = []
    seq = []
    for i in tqdm(range(0,len(df))):
        seq.append(df[i])
        prob.append(mod.full_prob(mod.forward(df[i])))
    data = pd.DataFrame()
    data['seq'] = seq
    data['prob'] = prob
    print('result samples: \n')
    print(data.head())
    print('\n Further analysis of results:  \n')
    print(data.describe())
    print('\n Max probablity sequence: \n')
    print(data.loc[data['prob'].idxmax(),:])
    return data
    
def sample_per_seq(df, n):
    samples = pd.DataFrame()
    for index in range(0,n):
        samples.loc[index, 'length'] = index
        samples.loc[index, 'no of samples'] = 0
    for i in range(0, len(df)):
        length = len(df[i])
        samples.loc[length, 'no of samples'] += 1    
    samples = samples.sort_values('no of samples',ascending = False)
    samples = samples.reset_index(drop=True)
    print('Top maximum number of sequence length: \n')
    print(samples.head(20))
    
def plot_seq(seq, dpi=80):
    nodes = []
    for i in range(0, len(seq)-1):
        nodes.append(str(i)+" - "+lab[seq[i]])
    edges = []
    for i in range(0, len(seq)-1):
        edges.append(((str(i)+" - "+lab[seq[i]]), (str(i+1)+" - "+lab[seq[i+1]])))
    G = nx.DiGraph()
    G.graph['dpi'] = dpi
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

def next_highprob_action(mod,seq,n_class,le):
    df = pd.DataFrame()
    df['seq'] = 0
    df['seq'] = df['seq'].astype(str)
    df['prob'] = 0
    for i in range(0,n_class):
        k = seq.copy()
        k.append(i)
        y = mod.likelihood(k)
        df.loc[i,'seq'] = str(k)
        df.loc[i,'prob'] = y
    if df['prob'].sum() == 0:
        print('The given seq itself is highly unlikely')
        display(df)
    else:
        maxlast = df.loc[df['prob'].idxmax(),:]['seq'][-2]
        maxtextlast = le.inverse_transform(int(maxlast))
        minlast = df.loc[df['prob'].idxmin(),:]['seq'][-2]
        mintextlast = le.inverse_transform(int(minlast))
        print('\n Next highly probable action taken by hacker will be ' + str(maxlast) + ' i.e ' + maxtextlast)
        print('\n')
        print(df.loc[df['prob'].idxmax(),:])
        print('\n Next least probable action taken by hacker will be ' + str(minlast) + ' i.e ' + mintextlast)
        print('\n')
        print(df.loc[df['prob'].idxmax(),:])
        print('\n')
        display(df)
