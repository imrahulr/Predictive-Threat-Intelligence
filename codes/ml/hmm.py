import numpy as np
from math import log


class HMM:
    
    
    def __init__(self, N, M, T, transmission=None, emission=None, prior=None):
        """
        N = number of hidden states
        M = number of visible states
        T = length of sequences
        """
        
        self.N = N
        self.M = M
        self.T = T
        if transmission is None:
            self.a = self._get_transmission()
        else:
            self.a = transmission
        if emission is None:
            self.b = self._get_emission()
        else:
            self.b = emission
        if prior is None:
            self.pi = self._get_prior()
        else:
            self.pi = prior
        self.hmm = (self.pi, self.a, self.b, self.N, self.M, self.T)
            
      
    def _get_transmission(self):
        a = np.random.random((self.N, self.N))
        a /= np.array([a.sum(axis=-1)]).T
        return a
    
    def _get_emission(self):
        b = np.random.random((self.N, self.M))
        b /= np.array([b.sum(axis=0)])
        return b
    
    def _get_prior(self):
        pi = np.random.random(self.N)
        pi /= pi.sum()
        return pi
       
        
    def forward(self, O):
        fwd = np.zeros((self.T, self.N))
        #initialization
        fwd[0] = (self.pi)*(self.b[:, O[0]])
        #induction:
        for t in range(self.T-1):
            fwd[t+1] = np.dot(fwd[t], self.a)*self.b[:, O[t+1]]
        return fwd
    
    
    def full_prob(self, fwd):
        return fwd[-1].sum()

    
    def viterbi(self, O):
        d = np.zeros((self.T, self.N))
        ph = np.zeros((self.T, self.N),dtype=np.int)

        #initialization
        d[0] = self.pi*self.b[:,O[0]]
        ph[0]=0
        #recursion
        for t in range(1, self.T):
            m = d[t-1]*self.a.T        
            ph[t] = m.argmax(axis=1)
            d[t] = m[np.arange(self.N),ph[t]]*self.b[:,O[t]]    

        #termination
        Q = np.zeros(self.T, dtype=np.int)
        Q[self.T-1] = np.argmax(d[self.T-1])
        Pv = d[self.T-1, Q[self.T-1]]

        #path back-tracking
        for t in reversed(range(self.T-1)):
            Q[t] = ph[t+1,Q[t+1]]

        return Q

    
    def backward(self, O):
        bk = np.zeros((self.T, self.N))
        #initialization
        bk[self.T-1] = 1
        #induction:
        for t in reversed(range(self.T-1)):
            bk[t]=np.dot(bk[t+1]*self.b[:, O[t+1]], self.a.T)
        return bk
    
 
    def _gamma_fn(self, fwd, bk, fp):
        self.gamma = (fwd*bk)/fp
        return (fwd*bk)/fp
    
    
    def _xi(self, fwd, bk, fp, O):
        return fwd[:-1].reshape((self.T-1, self.N, 1))*self.a.reshape((1, self.N, self.N))*self.b[:,O[1:]].T.reshape((self.T-1, 1, self.N))*bk[1:].reshape((self.T-1, 1, self.N))/fp
    
    
    def _exp_pi(self, gamma):
        return self.gamma[0]
    
    
    def _exp_a(self, gamma, xi, smoothing=0):            
        return (xi[:].sum(axis=0)+smoothing)/(gamma[:-1].sum(axis=0).reshape(self.N, 1)+self.N*smoothing)
    
    
    def _exp_b(self, gamma, O, smoothing=0):
        e_b = np.zeros((self.N, self.M))
        for j in range(self.N):
            for k in range(self.M):        
                e_b[j,k] = (np.sum(gamma[O==k, j]+smoothing))/(np.sum(gamma[:, j])+self.N*smoothing)
        return e_b
        # return np.array(map(lambda k: np.sum(gamma[O==k],axis=0)/np.sum(gamma, axis=0), np.arange(self.M))).T
    
    def _train(self, O, epochs=15, smoothing=0):
        
        hmm_new = self.hmm
        for i in range(epochs):
            fw = self.forward(O)
            bk = self.backward(O)
            fp = self.full_prob(fw)
            
            g = self._gamma_fn(fw, bk, fp)
            x = self._xi(fw, bk, fp, O)

            self.pi = self._exp_pi(g)
            self.a = self._exp_a(g, x, smoothing)
            self.b = self._exp_b(g, O, smoothing)
            
            err = np.concatenate(((self.pi-hmm_new[0]).ravel(),(self.a-hmm_new[1]).ravel(),(self.b-hmm_new[2]).ravel()))    
            hmm_new = self.hmm
            
            print ('Update #{} Probability: {} -- Mean Error:{}'.format(i+1, self.full_prob(self.forward(O)), np.mean(err**2)))

            
    def train(self, sequences, epochs=15, delta = 0.0001, smoothing=0):
        
        hmm_new = self.hmm
        length = len(sequences)
        
        old_likelihood = 0
        for O in sequences:
            old_likelihood += np.log(self.full_prob(self.forward(O)))
        old_likelihood /= length
        
        for i in range(epochs):
            new_likelihood = 0
            total_prob = 0
            
            for O in sequences:
                fw = self.forward(O)
                bk = self.backward(O)
                fp = self.full_prob(fw)
                
                if fp == 0:
                    continue
                
                g = self._gamma_fn(fw, bk, fp)
                x = self._xi(fw, bk, fp, O)

                self.pi = self._exp_pi(g)
                self.a = self._exp_a(g, x, smoothing)
                self.b = self._exp_b(g, O, smoothing)

                self.hmm = (self.pi, self.a, self.b, self.N, self.M, self.T)
                err = np.concatenate(((self.pi-hmm_new[0]).ravel(),(self.a-hmm_new[1]).ravel(),(self.b-hmm_new[2]).ravel()))    
                hmm_new = self.hmm
                new_likelihood += np.log(self.full_prob(self.forward(O)))
                total_prob += self.full_prob(self.forward(O))
            
         
            new_likelihood /= length
            total_prob /= length
            
            print ('Update #{} Log Probability: {} -- Mean Error {}'.format(i+1, new_likelihood, np.mean(err**2)))
            print ('Update #{} Probability: {}'.format(i+1, total_prob))
            
            if abs(new_likelihood - old_likelihood) < delta:
                break;
                
            old_likelihood = new_likelihood
                
            
    def likelihood(self, new_observations):
        T = len(new_observations)
        new_hmm = HMM(self.N, self.M, T, self.a, self.b, self.pi)
        forward = new_hmm.forward(new_observations)
        return new_hmm.full_prob(forward)
    