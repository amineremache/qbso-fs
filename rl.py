import numpy as np
from collections import defaultdict

class QLearning:
    def __init__(self,nb_atts,actions):
        self.actions = actions
        self.alpha = 0.1 # Facteur d'apprentissage
        self.gamma = 0.85  
        self.epsilon = 0.01
        self.q_table = [ {} for i in range(nb_atts) ] #defaultdict(lambda : [0.0,0.0,0.0,0.0])

    def get_max_value(self,data,state,actions_vals):
        max_val = 0.0
        arg_max = 0
        
        if not self.str_state(state) in self.q_table[self.nbrUn(state)]:
            self.q_table[self.nbrUn(state)][self.str_state(state)] = {self.str_state(state):{}}

        q_s = self.q_table[self.nbrUn(state)][self.str_state(state)]
        for i in actions_vals:

            if not str(i) in q_s:
                q_s[str(i)] = data.evaluate(state)

            if q_s[str(i)] >= max_val:
                max_val = q_s[str(i)]
                arg_max = i
        
        return max_val,arg_max


    def get_q_value(self,state,action):
        return self.q_table[self.nbrUn(state)][self.str_state(state)][str(action)]

    def get_action(self,data,state):
        if np.random.uniform() > self.epsilon :
            #choisir la meilleure action
            action_values = self.actions
            argmax_actions=[] # La meilleure action peut ne pas exister donc on elle est choisie aléatoirement
            for ac in action_values :
                if ac == self.get_max_value(data,state,action_values)[1]:
                    argmax_actions.append(ac)
            next_action = np.random.choice(argmax_actions) 
        else :
             next_action = np.random.choice(self.actions)
        if self.epsilon > 0 :
            self.epsilon -= 0.00001 #Décrementer espsilon pour Arreter l'exploration aléatoire qu'on aura un politique optimale
        if self.epsilon < 0 :
            self.epsilon = 0

        return next_action


    def get_next_state(self,state,action):
        next_state = state.copy()
        next_state[action] = (next_state[action]+1) % 2
        return next_state
    
    def learn(self,data,current_state,current_action,reward,next_state):
        print("current state : " + self.str_state(current_state) + "\ncurrent action : " + str(current_action) + "\nreward : "+ str(reward) + "\nnext state : "+ self.str_state(next_state))
        next_action = self.get_action(data,next_state)
        new_q = reward + self.gamma * self.q_table[self.nbrUn(next_state)][self.str_state(next_state)][str(next_action)]
        self.q_table[self.nbrUn(current_state)][self.str_state(current_state)][str(current_action)] = (1 - self.alpha)*self.q_table[self.nbrUn(current_state)][self.str_state(current_state)][str(current_action)] + self.alpha*new_q

    #@staticmethod
    def str_state(self,mlist):
        result = ''
        for element in mlist:
            result += str(element)
        return result

    def nbrUn(self,solution):
        return len([i for i, n in enumerate(solution) if n == 1])