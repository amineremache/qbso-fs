from bee import Bee

class Swarm():


    def __init__(self,flip=0,maxChance=0,nbrBees=0,nbrItLocSrch=0,maxIters=0):

        self.flip = flip
        self.maxChance = maxChance
        self.nbrBees = nbrBees
        self.nbrItLocSrch = nbrItLocSrch
        self.maxIters = maxIters
        self.beeList = []
        self.initBee = None

        pass


    def bso(self, beeInit):
        
        tabo = set()
        dance = list()
        nbChances = self.maxChance
        refSol = beeInit.sol
        bestSol = refSol
        i=0
        while  ( i<self.maxIters and not(refSol.problem.isOptimal(bestSol)) ) :

            tabo.add(refSol) # Add reSol to the taboo list
            dance = self.getSearchPoints(refSol, self.nbrBees) # Determine the SearchArea & assign a solution to each bee

            for bee in self.beeList:
                bee.localSearch()
                dance.sort()

            lastRefSol = refSol
            refSol = self.selectNextRefSol(refSol)
        pass

    
    def getSearchPoints(self, refSol, nbrBees):
        neighbors = list()
        n = len(refSol)
        k = n/self.flip
        for i in range(0,self.flip):
            break
        return neighbors

    def localSearch(self):
        pass

    def selectNextRefSol(self,refSol):
        nextSol = None
        return nextSol