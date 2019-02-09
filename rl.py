import numpy as np
from solution import Solution

class QLearning:
    def __init__(self,nb_atts,actions):
        self.actions = actions
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.q_table = [ {} for i in range(nb_atts) ] 

    def get_max_q_value(self,solution,actions_vals):
        max_val = 0.0
        arg_max = 0

        for i in actions_vals: # Basic itirative max search from a list of possible actions
            state_i = self.get_next_state(solution,i)
            state_i_acc = solution.get_accuracy(state_i)
            if state_i_acc > max_val: 
                max_val = self.get_q_value(solution,i) + state_i_acc
                arg_max = i

        return max_val, arg_max # We return the max q_value and the action that led to it from that state


    def get_q_value(self,solution,action):
        
        state = solution.get_state()
        if not Solution.str_sol(state) in self.q_table[Solution.nbrUn(state)]: 
            self.q_table[Solution.nbrUn(state)][Solution.str_sol(state)] = {}

        if not str(action) in self.q_table[Solution.nbrUn(state)][Solution.str_sol(state)]:
            # We initilize the q_table with 0
            self.q_table[Solution.nbrUn(state)][Solution.str_sol(state)][str(action)] = 0
            
        return self.q_table[Solution.nbrUn(state)][Solution.str_sol(state)][str(action)]

    
    def set_q_value(self,solution,action,val):
        state = solution.get_state()
        self.q_table[Solution.nbrUn(state)][Solution.str_sol(state)][str(action)] = val

    
    def step(self,solution,actions,flip):
        
        if len(actions) != 0:
          if len(actions) > flip:
            self.actions = [actions[i] for i in sorted(random.sample(range(len(actions)), flip))]
          else:
            self.actions = [actions[i] for i in sorted(random.sample(range(len(actions)), 1))]
        
        if np.random.uniform() > self.epsilon :
            
            #action_values = [self.actions[i] for i in sorted(random.sample(range(len(self.actions)), sample_size))]
            action_values = self.actions
            max_val = self.get_max_q_value(solution,action_values)[0] # getting the max next q_value
            argmax_actions=[self.get_max_q_value(solution,action_values)[1]] # saving the action that maxmizes the reward

            # There may be actions that has the same reward, so we add them to the argmax_avtions
            for ac in action_values : 
              ac_state = self.get_next_state(solution,ac)
              ac_state_q_val = self.get_q_value(solution,ac) + solution.get_accuracy(ac_state)
              
              if ( ac_state_q_val >= max_val ):
                  argmax_actions.append(ac) 
                  # We could make the condition "equal", because theorically there won't be any bigger q_value
            next_action = np.random.choice(argmax_actions) # We choose a random action from eqaul reward actions
            next_state = self.get_next_state(solution,next_action)

        else : # This is the exploration condition
            next_action = np.random.choice(self.actions)
            next_state = self.get_next_state(solution,next_action)

        if self.epsilon > 0 :
            self.epsilon -= 0.0001 
        if self.epsilon < 0 :
            self.epsilon = 0

        return next_state, next_action 

    def get_next_state(self,solution,action):
        next_state = solution.get_state()
        next_state[action] = (next_state[action]+1) % 2
        if (Solution.nbrUn(next_state) != 0):
          return next_state
        else:
          return solution.get_state()
    
    def learn(self,current_sol,current_action,reward,next_sol):
        next_action = self.get_max_q_value(next_sol,self.actions)[1] # Get the action with the max reward
        new_q = reward + self.gamma * self.get_q_value(next_sol,next_action)  #This part will be multiplied by alpha
        self.set_q_value(current_sol,current_action,(1 - self.alpha)*self.get_q_value(current_sol,current_action) + self.alpha*new_q) # This is the basic Q-learning formula