import numpy as np
import random

class MarkovChain():
    
    def __init__(self, states, transition=None, initial=None):
        self.states = states
        self.n = len(states)
        self.model = {}
        if transition is not None:
            self.transition = transition
        else:
            self.transition = np.zeros((self.n, self.n))
        if initial is not None:
            self.initial = initial
        else:
            self.initial = np.zeros((self.n, 1))
            
    def _train(self, seq):
        for i in range(0, len(seq)-1):
            state = seq[i]
            next_state = seq[i+1]
            if state not in self.model:
                self.model[state] = {}
            if next_state not in self.model[state]:
                self.model[state][next_state] = 0
            self.model[state][next_state] += 1
        self._cal_transition()
    
    def train(self, sequences):
        for seq in sequences:
            for i in range(0, len(seq)-1):
                state = seq[i]
                next_state = seq[i+1]
                if state not in self.model:
                    self.model[state] = {}
                if next_state not in self.model[state]:
                    self.model[state][next_state] = 0
                self.model[state][next_state] += 1
        self._cal_transition()
    
    def _cal_transition(self):
        for i in range(0, self.n):
            total = 0
            for j in range(0, self.n):
                try:
                    total += self.model[i][j]
                except:
                    continue
            for j in range(0, self.n):
                try:
                    self.transition[i][j] = self.model[i][j]/total
                except:
                    self.transition[i][j] = 0
                    
    def retrain(self, sequences):
        self.model = {}
        self.train(sequences)
        
    def get_probability(self, seq):
        prob = 1
        for i in range(0, len(seq)-1):
            state = seq[i]
            next_state = seq[i+1]
            prob *= self.transition[state][next_state]
        return prob
    
    def next_state(self, seq):
        state = seq[-1]
        if np.max(self.transition[state]) == 0:
            return None
        return np.argmax(self.transition[state])
    
    def next_possible_states(self, seq):
        state = seq[-1]
        next_states = []
        state_prob = []
        for i in range(0, self.n):
            if self.transition[state][i] != 0:
                next_states.append(i)
                state_prob.append(self.transition[state][i])
        return next_states, state_prob
    
    def most_probable_sequence(self, start, length=10):
        state = start
        seq = []
        seq.append(state)
        prob = np.max(self.transition[state])
        while prob > 0 and length > 1:
            next_state = np.argmax(self.transition[state])
            seq.append(next_state)
            state = next_state
            prob = np.max(self.transition[state])
            length -= 1
        return seq
            
    def gen_random_seq(self, start, length=10):
        state = start
        seq = []
        while length > 0:
            seq.append(state)
            nnext_states, sp = self.next_possible_states(seq)
            try:
                state = nnext_states[random.randint(0, len(nnext_states)-1)]
            except:
                state = start
            length -= 1
        return seq