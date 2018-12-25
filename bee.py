import random
from rl import QLearning

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
        
          for itr in range(self.locIterations):
            state = self.solution
            self.fitness = self.data.evaluate(state)

            if not self.data.ql.str_sol(state) in self.data.ql.q_table[self.data.ql.nbrUn(state)]:
                self.data.ql.q_table[self.data.ql.nbrUn(state)][self.data.ql.str_sol(state)] = {self.data.ql.str_sol(state):{}}

            action = self.data.ql.step(self.data,state)
            next_state = self.data.ql.get_next_state(state,action)
            accur_ns = self.data.evaluate(next_state)

            """if (accur_ns > self.fitness):
                self.reward = 100
            elif (accur_ns < self.fitness):
                self.reward = 10
            else: 
                self.reward = 1"""
            
            #self.reward = accur_ns - self.fitness

            self.data.ql.learn(self.data,state,action,self.fitness,next_state)
            self.solution = next_state.copy()

       
    def setSolution(self,solution):
        self.solution=solution
        self.fitness=self.data.evaluate(solution)
    
    def Rand(self,start, end, num): 
        res = [] 
  
        for j in range(num): 
            res.append(random.randint(start, end)) 
  
        return res
