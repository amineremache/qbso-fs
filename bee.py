import random
import numpy as np
from solution import Solution

class Bee :
    def __init__(self,id,problem,locIterations,state):
        self.id=id
        self.data=problem
        self.solution = Solution(self.data,state=state)
        self.fitness= 0.0
        self.reward = 0.0
        self.locIterations=locIterations
        self.action = []
    
    def localSearch(self):
        best=self.fitness
        #done=False
        lista=[j for j, n in enumerate(self.solution.state) if n == 1]
        indice =lista[0]
        
        for itr in range(self.locIterations):
            while(True):
                pos=-1
                oldFitness=self.fitness
                for i in range(len(self.solution.state)):
                    
                    if ((len(lista)==1) and (indice==i) and (i < self.data.nb_attribs-1)):
                        i+=1
                    self.solution.state[i]= (self.solution.state[i] + 1) % 2
                    
                    quality = self.solution.get_accuracy(self.solution.get_state())
                    if (quality >best):
                        pos = i
                        best=quality
                    self.solution.state[i]= (self.solution.state[i]+1) % 2
                    self.fitness = oldFitness 
                if (pos != -1):
                    self.solution.state[pos]= (self.solution.state[pos]+1)%2
                    self.fitness = best
                else:
                    break
            for i in range(len(self.solution.state)):
                oldFitness=self.fitness
                if ((len(lista)==1) and (indice==i) and (i < self.data.nb_attribs-1)):
                    i+=1
                self.solution.state[i]= (self.solution.state[i] + 1) % 2
                quality = self.solution.get_accuracy(self.solution.get_state())
                if (quality<best):
                    self.solution.state[i]= (self.solution.state[i] + 1) % 2
                    self.fitness = oldFitness


    def ql_localSearch(self,maxIterIndex):
        
        iterations = int(self.locIterations/maxIterIndex) if self.locIterations >= maxIterIndex else 1
        for itr in range(iterations):
       
            state = self.solution.get_state()

            next_state, action = self.data.ql.step(self.data,self.solution)
            next_sol = Solution(self.data,state=next_state)
            acc_state = self.solution.get_accuracy(state)
            acc_new_state = self.solution.get_accuracy(next_state)

            if (acc_state < acc_new_state):
                reward = acc_new_state
            elif (acc_state > acc_new_state):
                reward = acc_new_state - acc_state
            else :
                if (self.data.nbrUn(state) > self.data.nbrUn(next_state) ):
                    reward = 0.5 * acc_new_state
                else :
                    reward = -0.5 * acc_new_state

            self.fitness = self.data.ql.get_q_value(self.data,self.solution,action)
            self.reward = self.solution.get_accuracy(next_state)
            self.data.ql.learn(self.data,self.solution,action,reward,next_sol)
            self.solution = next_sol
        
       
    def setSolution(self,solution):
        self.solution.set_state(solution)
        if (self.data.typeOfAlgo == 0) :
            self.fitness = self.solution.get_accuracy(solution)
        elif (self.data.typeOfAlgo == 1):
            self.reward = self.solution.get_accuracy(solution)
    
    @classmethod
    def Rand(self,num): 
        res = [] 
        res = np.random.choice([0,1],size=(num,),p=[2./10,8./10]).tolist()
        return res