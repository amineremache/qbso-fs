from fs_data import FSData
from packages.stream import stream_tee
import sys, time

if __name__=="__main__":

    instance = FSData()
    classifier_name = str(type(instance.fsd.classifier)).strip('< > \' class ').split('.')[3]
    dataset_name = instance.filename.split('\\')[2].split('.')[0]
    log_file = open('.\\logs\\'+ time.strftime("%d-%m-%Y_%H-%M_", time.localtime()) + dataset_name + '_' + classifier_name +'.txt','w+')
    sys.stdout = stream_tee(sys.stdout, log_file)
    instance.run()