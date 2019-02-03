import numpy as np
from collections import defaultdict

class QLearning:
    def __init__(self,nb_atts,actions):
        self.actions = actions
        self.alpha = 0.1 # Facteur d'apprentissage
        self.gamma = 0.9
        self.epsilon = 0.1
        self.q_table = [ {} for i in range(nb_atts) ] #defaultdict(lambda : [0.0,0.0,0.0,0.0])

    def get_max_value(self,data,solution,actions_vals):
        max_val = 0.0
        arg_max = 0
        for i in actions_vals:
            if self.get_q_value(data,solution,i) >= max_val:
                max_val = self.get_q_value(data,solution,i)
                arg_max = i
        if max_val == 0:
            arg_max = np.random.choice(actions_vals)
        return max_val,arg_max


    def get_q_value(self,data,solution,action):
        
        state = solution.get_state()
        if not self.str_sol(state) in self.q_table[self.nbrUn(state)]:
            self.q_table[self.nbrUn(state)][self.str_sol(state)] = {}

        if not str(action) in self.q_table[self.nbrUn(state)][self.str_sol(state)]:
            self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)] = solution.get_accuracy(self.get_next_state(solution,action))
            
        return self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)]

    def set_q_value(self,solution,action,val):
        state = solution.get_state()
        self.q_table[self.nbrUn(state)][self.str_sol(state)][str(action)] = val

    def step(self,data,solution):
        if np.random.uniform() > self.epsilon :
            action_values = self.actions
            argmax_actions=[] 
            for ac in action_values :

                ac_state_q_val = self.get_q_value(data,solution,ac)
                if ( ac_state_q_val >= self.get_max_value(data,solution,action_values)[0] ):
                    #print("Q-value for action :" + str(ac) + " is " + str(ac_state_q_val))
                    argmax_actions.append(ac)

            #print("This is argmax list : ",argmax_actions)
            if len(argmax_actions) != 0:
              next_action = np.random.choice(argmax_actions) 
            else:
              next_action = np.random.choice(action_values) 
            next_state = self.get_next_state(solution,next_action)
            #print("The next state is :",next_state)
            
            #reward = data.evaluate(next_state)
        else :
            next_action = np.random.choice(self.actions)
            next_state = self.get_next_state(solution,next_action)
            
            #reward = reward = data.evaluate(next_state)
            
        if self.epsilon > 0 :
            self.epsilon -= 0.0001 
        if self.epsilon < 0 :
            self.epsilon = 0

        return next_state, next_action #, reward


    def get_next_state(self,solution,action):
        next_state = solution.get_state()
        next_state[action] = (next_state[action]+1) % 2
        if (self.nbrUn(next_state) != 0):
          return next_state
        else:
          return solution.get_state()
    
    def learn(self,data,current_sol,current_action,reward,next_sol):
        #print("current state : " + self.str_sol(current_state) + "| current action : " + str(current_action) + "| reward : "+ str(reward) + "| next state : "+ self.str_sol(next_state))
        
        next_action = self.step(data,next_sol)[1] # step returns 3 values : next_state, next_action, and the reward
        new_q = reward + self.gamma * self.get_q_value(data,next_sol,next_action)  #[0] is to pick q-value instead of [1] which is the accuracy of the new state 
        self.set_q_value(current_sol,current_action,(1 - self.alpha)*self.get_q_value(data,current_sol,current_action) + self.alpha*new_q)  

    #@staticmethod
    def str_sol(self,mlist):
        result = ''
        for element in mlist:
            result += str(element)
        return result

    def nbrUn(self,state):
        return len([i for i, n in enumerate(state) if n == 1])