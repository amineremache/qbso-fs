from swarm import Swarm
from fs_problem import FsProblem
import pandas as pd
import os, glob
from rl import QLearning

class FSData():

    def __init__(self):
        #url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        path = ".\\Benchmarks"
        self.files = glob.glob(os.path.join(path, "*.csv"))
        self.filename = path +'\\glass.csv'
        self.df = pd.read_csv(self.filename,header=None)
        self.ql = QLearning(len(self.df.columns),self.attributs_to_flip(self.df))
        self.fsd = FsProblem(self.df,self.ql)
    
    
    def attributs_to_flip(self,dataset):

        return list(range(8))
    
    def run(self):

            swarm = Swarm(self.fsd,4,4,10,10,10)
            swarm.bso()