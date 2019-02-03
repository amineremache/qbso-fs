from swarm import Swarm
from fs_problem import FsProblem
import pandas as pd
import os, glob, re, time, sys
from rl import QLearning
import xlsxwriter

class FSData():

    def __init__(self,typeOfAlgo,location,nbr_exec):
        
        self.typeOfAlgo = typeOfAlgo
        self.location = location
        self.nb_exec = nbr_exec
        self.dataset_name = re.search('[A-Za-z\-]*.csv',self.location)[0].split('.')[0]
        self.df = pd.read_csv(self.location,header=None)
        self.ql = QLearning(len(self.df.columns),self.attributs_to_flip(len(self.df.columns)-1))
        self.fsd = FsProblem(self.typeOfAlgo,self.df,self.ql)
        
        self.classifier_name = str(type(self.fsd.classifier)).strip('< > \' class ').split('.')[3]
        path = './results/'+ self.dataset_name
        self.instance_name = str(time.strftime("%d-%m-%Y_%H-%M_", time.localtime()) + self.dataset_name + '_' + self.classifier_name)
        log_filename = str(path + '/logs/'+ self.instance_name)
        
        log_file = open(log_filename + '.txt','w+')
        sys.stdout = log_file
        
        print("[START] Dataset" + self.dataset_name + "description \n")
        print("Shape : " + str(self.df.shape) + "\n")
        print(self.df.describe())
        print("\n[END] Dataset" + self.dataset_name + "description\n")
        print("[START] Ressources specifications\n")
        os.system('cat /proc/cpuinfo') # Think of changing this when using Windows
        print("[END] Ressources specifications\n")

        
        sheet_filename = str(path + '/sheets/'+ self.instance_name )
        self.workbook = xlsxwriter.Workbook(sheet_filename + '.xlsx')
        
        self.worksheet = self.workbook.add_worksheet(self.classifier_name)
        self.worksheet.write(0,0,'Iteration')
        self.worksheet.write(0,1,'Accuracy')
        self.worksheet.write(0,2,'N_Features')
        self.worksheet.write(0,3,'Time')
    
    
    def attributs_to_flip(self,dataset):

        return list(range(9))
    
    def run(self,flip,maxChance,nbrBees,maxIterations,locIterations):
        t_init = time.time()
        
        for itr in range(1,self.nb_exec+1):
          print ("Execution {0}".format(str(itr)))
          self.ql = QLearning(len(self.df.columns),self.attributs_to_flip(len(self.df.columns)-1))
          self.fsd = FsProblem(self.typeOfAlgo,self.df,self.ql)
          swarm = Swarm(self.fsd,flip,maxChance,nbrBees,maxIterations,locIterations)
          t1 = time.time()
          best = swarm.bso(self.typeOfAlgo)
          t2 = time.time()
          print("Time elapsed for execution {0} : {1:.2f} s\n".format(itr,t2-t1))
          self.worksheet.write(itr, 0, itr)
          self.worksheet.write(itr, 1, "{0:.2f}".format(best[0]))
          self.worksheet.write(itr, 2, best[1])
          self.worksheet.write(itr, 3, "{0:.3f}".format(t2-t1))
          
        t_end = time.time()
        print ("Total execution time for dataset {0} is {1:.2f} s".format(self.dataset_name,t_end-t_init))
        self.workbook.close()