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
        
        for i in actions_vals:
            if self.get_q_value(data,state,i)[1] >= max_val:
                max_val = self.get_q_value(data,state,i)[1]
                arg_max = i
        
        if max_val == 0:
            arg_max = np.random.choice(actions_vals)

        return max_val,arg_max


    def get_q_value(self,data,state,action):
        
        if not self.str_sol(state) in self.q_table[self.nbrUn(state)]:
            self.q_table[self.nbrUn(state)][self.str_sol(state)] = {}

        if not str(action) in self.q_table[self.nbrUn(state)][self.str_sol(state)]:
            #self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)] = data.evaluate(self.get_next_state(state,action))
            self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)] = [0,data.evaluate(self.get_next_state(state,action))]
            
        return self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)]

    def set_q_value(self,state,action,val):
        self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)][0] = val

    def step(self,data,state):
        if np.random.uniform() > self.epsilon :
            #choisir la meilleure action
            action_values = self.actions
            argmax_actions=[] # La meilleure action peut ne pas exister donc on elle est choisie aléatoirement
            for ac in action_values :
                """if ac == self.get_max_value(state,action_values)[1]:
                    print("This action is to append : ", ac)
                    argmax_actions.append(ac)"""

                """if self.get_q_value(state,ac) == self.get_max_value(state,action_values)[1]:
                    print("This action is to append : ", ac)
                    argmax_actions.append(ac)"""

                #ac_state = self.get_next_state(state,ac)
                """print("Q-value for action :" + str(ac) + " is " + str(self.get_q_value(state,ac)))
                argmax_actions.append(ac)"""  


                ac_state_q_val = self.get_q_value(data,state,ac)[1]
                if ( ac_state_q_val == self.get_max_value(data,state,action_values)[0] ):
                    #print("Q-value for action :" + str(ac) + " is " + str(ac_state_q_val))
                    argmax_actions.append(ac)

            #print("This is argmax list : ",argmax_actions)
            next_action = np.random.choice(argmax_actions) 
            next_state = self.get_next_state(state,next_action)
            #print("The next state is :",next_state)
            reward = self.get_q_value(data,state,next_action)[1]
        else :
            next_action = np.random.choice(self.actions)
            next_state = self.get_next_state(state,next_action)
            reward = self.get_q_value(data,state,next_action)[1]
        if self.epsilon > 0 :
            self.epsilon -= 0.00001 #Décrementer espsilon pour Arreter l'exploration aléatoire qu'on aura un politique optimale
        if self.epsilon < 0 :
            self.epsilon = 0

        return next_state, next_action, reward


    def get_next_state(self,state,action):
        next_state = state.copy()
        next_state[action] = (next_state[action]+1) % 2
        return next_state
    
    def learn(self,data,current_state,current_action,reward,next_state):
        print("current state : " + self.str_sol(current_state) + "| current action : " + str(current_action) + "| reward : "+ str(reward) + "| next state : "+ self.str_sol(next_state))
        
        next_action = self.step(data,next_state)[1]
        new_q = reward + self.gamma * self.get_q_value(data,next_state,next_action)[0]
        self.set_q_value(current_state,current_action,(1 - self.alpha)*self.get_q_value(data,current_state,current_action)[0] + self.alpha*new_q)  

    #@staticmethod
    def str_sol(self,mlist):
        result = ''
        for element in mlist:
            result += str(element)
        return result

    def nbrUn(self,solution):
        return len([i for i, n in enumerate(solution) if n == 1])