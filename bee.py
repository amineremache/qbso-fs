import random
import numpy as np
from solution import Solution

class Bee :
    def __init__(self,id,problem,locIterations,state):
        self.id=id
        self.data=problem
        self.solution = Solution(self.data,state=state)
        self.fitness= 0.0
        self.rl_return = 0.0
        self.locIterations=locIterations
        self.action = []
    
    def localSearch(self):
        best=self.fitness
        #done=False
        lista=[j for j, n in enumerate(self.solution.get_state()) if n == 1]
        indice =lista[0]
        
        for itr in range(self.locIterations):
            while(True):
                pos = -1
                oldFitness = self.fitness
                for i in range(len(self.solution.get_state())):
                    
                    if ((len(lista)==1) and (indice==i) and (i < self.data.nb_attribs-1)):
                        i+=1
                    self.solution.state[i]= (self.solution.state[i] + 1) % 2
                    quality = self.solution.get_accuracy(self.solution.get_state())
                    
                    if (quality > best):
                        pos = i
                        best = quality
                    self.solution.state[i]= (self.solution.state[i]+1) % 2
                    self.fitness = oldFitness 
                if (pos != -1):
                    self.solution.state[pos]= (self.solution.state[pos]+1)%2
                    self.fitness = best
                else:
                    break
            for i in range(len(self.solution.get_state())):
                oldFitness=self.fitness
                if ((len(lista)==1) and (indice==i) and (i < self.data.nb_attribs-1)):
                    i+=1
                self.solution.state[i]= (self.solution.state[i] + 1) % 2
                quality = self.solution.get_accuracy(self.solution.get_state())
                if (quality<best):
                    self.solution.state[i]= (self.solution.state[i] + 1) % 2
                    self.fitness = oldFitness


    def ql_localSearch(self,maxIterIndex,flip):
      
        """The reason why we do this is to 
        explore at the beginning and 
        eploit at the end to converge to the optimal solution"""
        iterations = int(maxIterIndex/self.locIterations)+1 if int(maxIterIndex/self.locIterations)+1 <= self.locIterations else self.locIterations
        for itr in range(iterations):
       
          state = self.solution.get_state()
          # We get the best solution to be calculated yet
          best_state = Solution.get_best_sol()
          # We xor ( logic xor ) it with the actual state we're in to define the actions that could be done
          if best_state[1] != 0:
            xor_states = Solution.xor(state,best_state[0])
          else:
            xor_states = Solution.xor(state,[0 for i in range(len(state))])

          # We get the indexes of the actions to do and pass them to the step() function to pick the next state  
          actions = Solution.get_indexes(xor_states)

          #next_state, action = self.data.ql.step(self.solution,self.data.nb_attribs)
          # Ths first +1, is not to devide by 0, the 2nd one, is not to get an empty list in case iterations > nb_atts
          #next_state, action = self.data.ql.step(self.solution,int(self.data.nb_attribs/(iterations+1))+1)

          next_state, action = self.data.ql.step(self.solution,actions,flip)
          next_sol = Solution(self.data,state=next_state)
          acc_state = self.solution.get_accuracy(state)
          acc_new_state = self.solution.get_accuracy(next_state)

          if (acc_state < acc_new_state):
              reward = acc_new_state
          elif (acc_state > acc_new_state):
              reward = acc_new_state - acc_state
          else :
              if (Solution.nbrUn(state) > Solution.nbrUn(next_state) ):
                  reward = 1/2 * acc_new_state
              else :
                  reward = -1/2 * acc_new_state

          self.data.ql.learn(self.solution,action,reward,next_sol)
          self.rl_return = self.data.ql.get_q_value(self.solution,action)
          self.fitness = acc_new_state
          self.solution = next_sol
          #print("Next state's acc : ",acc_new_state)
          #print("This is acc choosed : {0}".format(acc_new_state))
            
    def setSolution(self,solution):
        self.solution.set_state(solution)
        self.fitness = self.solution.get_accuracy(solution)
    
    @classmethod
    def Rand(self, num, start=None, end=None): 
        res = [] 
        if (not start) or (not end): 
          """We used 20%/80% (Pareto's law) to initilize the solution"""
          res = np.random.choice([0,1],size=(num,),p=[8./10,2./10]).tolist()
        else: 
          for j in range(num): 
              res.append(random.randint(start, end))
        return res 