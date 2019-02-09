from fs_data import FSData

if __name__=="__main__":

    # Prepare the dataset

    dataset = "Glass"
    #data_loc_path = "https://raw.githubusercontent.com/Neofly4023/bso-fs/master/datasets/"
    data_loc_path = "./datasets/"
    location = data_loc_path + dataset + ".csv"

    # Params init

    typeOfAlgo = 0
    nbr_exec = 1
    flip = 5
    maxChance = 3
    nbrBees = 10
    maxIterations = 4
    locIterations = 2

    instance = FSData(typeOfAlgo,location,nbr_exec)
    instance.run(flip,maxChance,nbrBees,maxIterations,locIterations)