import random

class Bee :
    def __init__(self,id,data,locIterations):
        self.id=id
        self.data=data
        self.solution=[]
        self.fitness=0.0
        self.locIterations=locIterations
    
    def localSearch(self):
        best=self.fitness
        done=False
        lista=[j for j, n in enumerate(self.solution) if n == 1]
        indice =lista[0]
        
        for itr in range(self.locIterations):
            while(True):
                pos=-1
                oldFitness=self.fitness
                for i in range(len(self.solution)):
                    
                    if ((len(lista)==1) and (indice==i)and (i < self.data.nbrAttributs-1)):
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
                if ((len(lista)==1) and (indice==i) and (i < self.data.nbrAttributs-1)):
                    i+=1
                self.solution[i]= (self.solution[i] + 1) % 2
                quality = self.data.evaluate(self.solution)
                if (quality<best):
                    self.solution[i]= (self.solution[i] + 1) % 2
                    self.fitness = oldFitness
        
        
    def setSolution(self,solution):
        self.solution=solution
        self.fitness=self.data.evaluate(solution)
    
    def Rand(self,start, end, num): 
        res = [] 
  
        for j in range(num): 
            res.append(random.randint(start, end)) 
  
        return res