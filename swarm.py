from bee import Bee
import random, time
from solution import Solution

class Swarm :
    def __init__(self,problem,flip,maxChance,nbrBees,maxIterations,locIterations):
        self.data=problem
        self.flip=flip
        self.maxChance=maxChance
        self.nbChance=maxChance
        self.nbrBees=nbrBees
        self.maxIterations=maxIterations
        self.locIterations=locIterations
        self.beeList=[]
        self.refSolution = Bee(-1,self.data,self.locIterations,Bee.Rand(self.data.nb_attribs))
        self.bestSolution = self.refSolution
        self.tabou=[]
        Solution.solutions.clear()

    def searchArea(self):    
        i=0
        h=0
        
        self.beeList=[]
        while((i<self.nbrBees) and (i < self.flip) ) :
            #print ("First method to generate")
            
            solution=self.refSolution.solution.get_state()
            k=0
            while((self.flip*k+h) < len(solution)):
                solution[self.flip*k +h] = ((solution[self.flip*k+h]+1) % 2)
                k+=1
            newBee=Bee(i,self.data,self.locIterations,solution)
            self.beeList.append(newBee)
            
            i+=1
            h=h+1
        h=0
        
        while((i<self.nbrBees) and (i< 2*self.flip )):
            #print("Second method to generate")

            solution=self.refSolution.solution.get_state()
            k=0
            while((k<int(len(solution)/self.flip)) and (self.flip*k+h < len(solution))):
                solution[int(self.data.nb_attribs/self.flip)*h+k] = ((solution[int(self.data.nb_attribs/self.flip)*h+k]+1)%2)
                k+=1
            newBee=Bee(i,self.data,self.locIterations,solution)
            self.beeList.append(newBee)
            
            i+=1
            h=h+1
        while (i<self.nbrBees):
            #print("Random method to generate")
            solution= self.refSolution.solution.get_state()
            indice = random.randint(0,len(solution)-1)
            solution[indice]=((solution[indice]+1) % 2)
            newBee=Bee(i,self.data,self.locIterations,solution)
            self.beeList.append(newBee)
            i+=1
        for bee in (self.beeList):
            lista=[j for j, n in enumerate(bee.solution.get_state()) if n == 1]
            if (len(lista)== 0):
                bee.setSolution(Bee.Rand(self.data.nb_attribs))
                
    def selectRefSol(self):
      self.beeList.sort(key=lambda Bee: Bee.fitness, reverse=True)
      bestQuality=self.beeList[0].fitness
      if(bestQuality>self.bestSolution.fitness):
          self.bestSolution=self.beeList[0]
          self.nbChance=self.maxChance
          return self.bestSolution
      else:
          if(  (len(self.tabou)!=0) and  bestQuality > (self.tabou[len(self.tabou)-1].fitness)):
              self.nbChance=self.maxChance
              return self.bestBeeQuality()
          else:
              self.nbChance-=1
              if(self.nbChance > 0): 
                  return self.bestBeeQuality()
              else :
                  return self.bestBeeDiversity()
      
    def distanceTabou(self,bee):
        distanceMin=self.data.nb_attribs
        for i in range(len(self.tabou)):
            cpt=0
            for j in range(self.data.nb_attribs):
                if (bee.solution.state[j] != self.tabou[i].solution.state[j]) :
                      cpt +=1
            if (cpt<=1) :
                return 0
            if (cpt < distanceMin) :
                distanceMin=cpt
        return distanceMin
    
    def bestBeeQuality(self):
        distance = 0
        i=0
        pos=-1
        while(i<self.nbrBees):
            max_val=self.beeList[i].fitness
            nbUn=Solution.nbrUn(self.beeList[i].solution.get_state())
            while((i<self.nbrBees) and (self.beeList[i].solution.get_accuracy(self.beeList[i].solution.get_state()) == max_val)):
                distanceTemp=self.distanceTabou(self.beeList[i])
                nbUnTemp = Solution.nbrUn(self.beeList[i].solution.get_state())
                if(distanceTemp > distance) or ((distanceTemp == distance) and (nbUnTemp < nbUn)):
                    if((distanceTemp==distance) and (nbUnTemp<nbUn)):
                        print("We pick the solution with less features")
                    nbUn=nbUnTemp
                    distance=distanceTemp
                    pos=i
                i+=1
            if(pos!=-1) :
                return self.beeList[pos]
        bee= Bee(-1,self.data,self.locIterations,Bee.Rand(self.data.nb_attribs))
        return bee
            
    def bestBeeDiversity(self):
        max_val=0
        for i in range(len(self.beeList)):
            if (self.distanceTabou(self.beeList[i])> max_val) :
                max_val = self.distanceTabou(self.beeList[i])
        if (max_val==0):
            bee= Bee(-1,self.data,self.locIterations,Bee.Rand(self.data.nb_attribs))
            return bee
        i=0
        while(i<len(self.beeList) and self.distanceTabou(self.beeList[i])!= max_val) :
            i+=1
        return self.beeList[i]
    
    def bso(self,typeOfAlgo,flip):
        i=1
        while(i<=self.maxIterations):
            t1 = time.time()
            print("refSolution is : ", Solution.str_sol(self.refSolution.solution.get_state()))
            self.tabou.append(self.refSolution)
            print("BSO iteration N° : ",i)
            
            self.searchArea()

            # The local search part
            
            for j in range(self.nbrBees):
              if (typeOfAlgo == 0):
                self.beeList[j].localSearch()
              elif (typeOfAlgo == 1):
                for episode in range(self.locIterations):
                  self.beeList[j].ql_localSearch(i,flip)
              print( "Fitness of bee " + str(j) + " is : " + str(self.beeList[j].fitness) + "\n")
            self.refSolution = self.selectRefSol()
            i+=1
            t2 = time.time()
            print("Time of iteration N°{0} : {1:.2f} s".format(i,t2-t1))
            
        print("\n[BSO parameters used]\n")
        print("Type of algo : {0}".format(typeOfAlgo))
        print("Flip : {0}".format(self.flip))
        print("MaxChance : {0}".format(self.maxChance))
        print("Nbr of Bees : {0}".format(self.nbrBees))
        print("Nbr of Max Iterations : {0}".format(self.maxIterations))
        print("Nbr of Loc Iterations : {0}\n".format(self.locIterations))
        print("Best solution found : ",self.bestSolution.solution.get_state())
        print("Accuracy of found sol : {0:.2f} ".format(self.bestSolution.fitness*100))
        print("Number of features used : {0}".format(Solution.nbrUn(self.bestSolution.solution.get_state())))
        print("Size of solutions dict : {0}".format(len(Solution.solutions)))
        print("Average time to evaluate a solution : {0:.3f} s".format(Solution.get_avg_time())) 
        print("Global optimum : {0}, {1:.2f}".format(Solution.get_best_sol()[0],Solution.get_best_sol()[1]*100))
        if (typeOfAlgo == 1):
          print("Return (Q-value) : ",self.bestSolution.rl_return)  
          print("Total sorting time : {0:.2f} s".format(Solution.sorting_time))
        return self.bestSolution.fitness*100, Solution.nbrUn(self.bestSolution.solution.get_state())
