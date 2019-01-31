from fs_data import FSData
from packages.stream import stream_tee
import sys, time

if __name__=="__main__":

    # Prepare the dataset

    dataset = "Glass"
    #data_loc_path = "https://raw.githubusercontent.com/Neofly4023/bso-fs/master/datasets/"
    data_loc_path = "./datasets/"
    location = data_loc_path + dataset + ".csv"

    # Params init

    typeOfAlgo = 1
    nbr_exec = 1
    flip = 5
    maxChance = 3
    nbrBees = 10
    maxIterations = 2
    locIterations = 4

    instance = FSData(location,nbr_exec)
    instance.run(typeOfAlgo,flip,maxChance,nbrBees,maxIterations,locIterations)