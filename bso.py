from bee import Bee

class BSO():


    def __init__(self,maxNumIters,numBees,numLocalSearchIters,flipParameter,maxNumChanges):

        self.maxNumIters = maxNumIters
        self.numBees = numBees
        self.numLocalSearchIters = numLocalSearchIters
        self.flipParameter = flipParameter
        self.maxNumChanges = maxNumChanges

        pass


    def bso(self, beeInit):
        
        tabo = set()
        dance = list()
        nbChanges = self.maxNumChanges
        sref = beeInit.sol
        bestSol = sref
        i=0
        while  ( i<self.maxNumIters and not(sref.problem.isOptimal(bestSol)) ) :

            tabo.add(sref)
            dance = sref.getSearchPoints(self.numBees)
            

        pass