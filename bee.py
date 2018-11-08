from fs_solution import FSSolution
from fs_data import FSData

class Bee():

    def __init__(self,id):
        self.id = id
        self.sol = []
        self.numLocSrchIters = 0
        self.fitness = 0
        self.fsData = None
        pass
