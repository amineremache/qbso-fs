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
        
        print(self.files)
    
    
    def attributs_to_flip(self,dataset):

        return list(range(3))
    
    def run(self):
        
        for filename in self.files:
            if(filename=='.\\Benchmarks\\iris.csv'):
                print(filename)
                df=pd.read_csv(filename,header=None)
                
                #df = df.iloc[:, [j for j, c in enumerate(df.columns) if j != 0]]

                ql = QLearning(len(df.columns),self.attributs_to_flip(df))

                fsd= FsProblem(df,ql)
                swarm= Swarm(fsd,4,4,10,10,10)
                #print(fsd.evaluate([0, 0, 0, 0, 1, 0, 0, 0, 0]))
            
                #swarm.searchArea()
                swarm.bso()
            
                break