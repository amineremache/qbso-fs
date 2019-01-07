from bee import Bee
import random, copy


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
        self.refSolution = Bee(-1,self.data,self.locIterations)
        self.refSolution.setSolution(self.refSolution.Rand(self.data.nb_attribs))
        self.bestSolution = self.refSolution
        self.tabou=[]

    def searchArea(self):    
        i=0
        h=0
        
        self.beeList=[]
        while((i<self.nbrBees) and (i < self.flip) ) :
            #print ("First method to generate")
            
            solution=self.refSolution.solution
            k=0
            while((self.flip*k+h) < len(solution)):
                solution[self.flip*k +h] = ((solution[self.flip*k+h]+1) % 2)
                k+=1
            newBee=Bee(i,self.data,self.locIterations)
            newBee.solution = copy.deepcopy(solution)
            self.beeList.append(newBee)
            
            i+=1
            h=h+1
        h=0
        
        while((i<self.nbrBees) and (i< 2*self.flip )):
            #print("Second method to generate")

            solution=self.refSolution.solution
            k=0
            while((k<int(len(solution)/self.flip)) and (self.flip*k+h < len(solution))):
                solution[int(self.data.nb_attribs/self.flip)*h+k] = ((solution[int(self.data.nb_attribs/self.flip)*h+k]+1)%2)
                k+=1
            newBee=Bee(i,self.data,self.locIterations)
            newBee.solution = copy.deepcopy(solution)
            self.beeList.append(newBee)
            
            i+=1
            h=h+1
        while (i<self.nbrBees):
            #print("Random method to generate")
            solution= self.refSolution.solution
            indice = random.randint(0,len(solution)-1)
            solution[indice]=((solution[indice]+1) % 2)
            newBee=Bee(i,self.data,self.locIterations)
            newBee.solution = copy.deepcopy(solution)
            self.beeList.append(newBee)
            i+=1
        for bee in (self.beeList):
            lista=[j for j, n in enumerate(bee.solution) if n == 1]
            if (len(lista)== 0):
                bee.setSolution(bee.Rand(self.data.nb_attribs))
                
    def selectRefSol(self):
        self.beeList.sort(key=lambda Bee: Bee.reward, reverse=True)
        bestQuality=self.beeList[0].reward
        if(bestQuality>self.bestSolution.reward):
            self.bestSolution=self.beeList[0]
            self.nbChance=self.maxChance
            return self.bestSolution
        else:
            if(  (len(self.tabou)!=0) and  bestQuality > (self.tabou[len(self.tabou)-1].reward)  ):
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
                if (bee.solution[j] != self.tabou[i].solution[j]) :
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
            max=self.beeList[i].reward
            nbUn=self.data.nbrUn(self.beeList[i].solution)
            while((i<self.nbrBees) and (self.data.evaluate(self.beeList[i].solution)==max)):
                distanceTemp=self.distanceTabou(self.beeList[i])
                nbUnTemp= self.data.nbrUn(self.beeList[i].solution)
                if(distanceTemp >   distance) or ((distanceTemp==distance) and (nbUnTemp<nbUn)):
                    if((distanceTemp==distance) and (nbUnTemp<nbUn)):
                        print("On choisi la meilleure solution avec moins d'attributs")
                    nbUn=nbUnTemp
                    distance=distanceTemp
                    pos=i
                i+=1
            if(pos!=-1) :
                return self.beeList[pos]
        bee= Bee(-1,self.data,self.locIterations)
        bee.setSolution(bee.Rand(self.data.nb_attribs))
        return bee
            
    def bestBeeDiversity(self):
        max=0
        for i in range(len(self.beeList)):
            if (self.distanceTabou(self.beeList[i])> max) :
                max = self.distanceTabou(self.beeList[i])
        if (max==0):
            bee= Bee(-1,self.data,self.locIterations)
            bee.setSolution(bee.Rand(self.data.nb_attribs))
            return bee
        i=0
        while(i<len(self.beeList) and self.distanceTabou(self.beeList[i])!= max) :
            i+=1
        return self.beeList[i]
    
    def bso(self):
        i=0
        while(i<self.maxIterations):
            #print("La solution de référence est : ",self.refSolution.solution)
            #print(self.refSolution.solution)
            self.tabou.append(self.refSolution)
            #print("Iteration N° : ",i)
            
            self.searchArea()
            """print("********************************************************")
            print("La zone de recherche est :")
            for k in range (self.nbrBees): 
                print(self.beeList[k].id)
                print(self.beeList[k].solution)
            print("*******************************************************")"""
            #La recherche locale
            
            for j in range(self.nbrBees):
                #self.beeList[j].localSearch()
                for episode in range(5):
                    self.beeList[j].ql_localSearch()
                #print( "Fitness of bee " + str(j) + " " + str(self.beeList[j].fitness) )
            self.refSolution=self.selectRefSol()
            i+=1
        
        print("La meilleure solution trouvé est : ",self.bestSolution.solution)
        print("Sa récompense est : ",self.bestSolution.reward)
        print("Sa fitness est : ",self.bestSolution.fitness)

    
    def str_sol(self,mlist):
        result = ''
        for element in mlist:
            result += str(element)
        return result
