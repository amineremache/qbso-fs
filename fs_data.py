from swarm import Swarm
from fs_problem import FsProblem
import pandas as pd
import os, glob
from rl import QLearning
import time

class FSData():

    def __init__(self):
        #url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        path = ".\\Benchmarks"
        self.files = glob.glob(os.path.join(path, "*.csv"))
        self.filename = path +'\\glass.csv'
        print("[START] Dataset reading")
        self.df = pd.read_csv(self.filename,header=None)
        print("Shape : " + str(self.df.shape) + "\nDescription : \n")
        #self.df.describe()
        print("[END] Dataset reading")
        self.ql = QLearning(len(self.df.columns),self.attributs_to_flip(self.df))
        self.fsd = FsProblem(self.df,self.ql)
    
    
    def attributs_to_flip(self,dataset):

        return list(range(9))
    
    def run(self):

            swarm = Swarm(self.fsd,4,4,10,5,5)
            t1 = time.time()
            swarm.bso()
            t2 = time.time()
            print("Execusion time : {0:.2f} s".format(t2-t1))