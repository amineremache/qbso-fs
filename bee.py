from fs_solution import FSSolution
from fs_data import FSData

class Bee():  
    def __init__(self, sol, id, numLocSrchIters, quality, fsData):
        self.sol = sol
        self.id = id
        self.numLocSrchIters = numLocSrchIters
        self.quality = quality
        self.fsData = fsData
        pass
