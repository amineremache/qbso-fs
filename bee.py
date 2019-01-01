import random
from rl import QLearning
import numpy as np

class Bee :
    def __init__(self,id,problem,locIterations):
        self.id=id
        self.data=problem
        self.solution=[]
        self.fitness= 0.0
        self.reward = 0.0
        self.locIterations=locIterations
        self.action = []
    
    def localSearch(self):
        best=self.fitness
        #done=False
        lista=[j for j, n in enumerate(self.solution) if n == 1]
        indice =lista[0]
        
        for itr in range(self.locIterations):
            while(True):
                pos=-1
                oldFitness=self.fitness
                for i in range(len(self.solution)):
                    
                    if ((len(lista)==1) and (indice==i)and (i < self.data.nb_attribs-1)):
                        i+=1
                    self.solution[i]= (self.solution[i] + 1) % 2
                    
                    quality = self.data.evaluate(self.solution)
                    if (quality >best):
                        pos = i
                        best=quality
                    self.solution[i]= (self.solution[i]+1) % 2
                    self.fitness = oldFitness 
                if (pos != -1):
                    self.solution[pos]= (self.solution[pos]+1)%2
                    self.fitness = best
                else:
                    break
            for i in range(len(self.solution)):
                oldFitness=self.fitness
                if ((len(lista)==1) and (indice==i) and (i < self.data.nb_attribs-1)):
                    i+=1
                self.solution[i]= (self.solution[i] + 1) % 2
                quality = self.data.evaluate(self.solution)
                if (quality<best):
                    self.solution[i]= (self.solution[i] + 1) % 2
                    self.fitness = oldFitness


    def ql_localSearch(self):
        
        print (self.data.ql.q_table)
        #init_sol = self.solution.copy()
        #for itr in range(self.locIterations):
        for itr in range(6):
            state = self.solution.copy()

            """if not self.data.ql.str_sol(state) in self.data.ql.q_table[self.data.ql.nbrUn(state)]:
                self.data.ql.q_table[self.data.ql.nbrUn(state)][self.data.ql.str_sol(state)] = {self.data.ql.str_sol(state):{}}"""

            next_state, action, self.reward = self.data.ql.step(self.data,state)

            """if (reward > self.fitness):
                self.reward = 100
            elif (reward < self.fitness):
                self.reward = 10
            else: 
                self.reward = 1"""
            
            #self.reward = reward - self.fitness

            self.data.ql.learn(self.data,state,action,self.reward,next_state)
            self.fitness = self.data.ql.get_q_value(self.data,self.solution,action)
            self.solution = next_state.copy()
            

       
    def setSolution(self,solution):
        self.solution=solution
        self.fitness=self.data.evaluate(solution)
    
    def Rand(self,num): 
        res = [] 
        """for j in range(num): 
            res.append(random.randint(start, end))"""
        res = np.random.choice([0,1],size=(num,),p=[3./10,7./10]).tolist()
  
        return res
