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
        
        #print (self.data.ql.q_table)
        #init_sol = self.solution.copy()
        for itr in range(self.locIterations):
        #for step in range(5):
            #print ("Q-Table : \n",self.data.ql.q_table)
            state = self.solution.copy()

            """if not self.data.ql.str_sol(state) in self.data.ql.q_table[self.data.ql.nbrUn(state)]:
                self.data.ql.q_table[self.data.ql.nbrUn(state)][self.data.ql.str_sol(state)] = {self.data.ql.str_sol(state):{}}"""

            next_state, action = self.data.ql.step(self.data,state)
            acc_state = self.data.evaluate(state)
            acc_new_state = self.data.evaluate(next_state)

            if (acc_state < acc_new_state):
                self.reward = acc_new_state
            elif (acc_state > acc_new_state):
                self.reward = acc_new_state - acc_state
            else :
                if (self.data.nbrUn(state) > self.data.nbrUn(next_state) ):
                    self.reward = 0.5 * acc_new_state
                else :
                    self.reward = -0.5 * acc_new_state

            """if (reward > self.fitness):
                self.reward = 100
            elif (reward < self.fitness):
                self.reward = 10
            else: 
                self.reward = 1"""
            
            #self.reward = reward - self.fitness
            #self.fitness = self.data.ql.get_q_value(self.data,self.solution,action)[1] - self.data.evaluate(state) 
            self.fitness = self.data.ql.get_q_value(self.data,state,action)
            self.data.ql.learn(self.data,state,action,self.reward,next_state)
            self.solution = next_state.copy()
        
       
    def setSolution(self,solution):
        self.solution=solution
        self.fitness=self.data.evaluate(solution)
    
    def Rand(self,num): 
        res = [] 
        """for j in range(num): 
            res.append(random.randint(start, end))"""
        res = np.random.choice([0,1],size=(num,),p=[2./10,8./10]).tolist()
  
        return res
