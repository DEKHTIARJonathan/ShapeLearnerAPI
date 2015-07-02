################################# Import Libraries ################################
import os.path
import sys

sys.path.append('../Config/')
dllsPath = os.path.dirname(os.path.realpath(__file__))+'\dlls'
os.environ['PATH'] = dllsPath + ';' + os.environ['PATH']
from loadConf import loadDBConf, loadAPIConf

import api

#######################################################################################
#######################################################################################
#######################################################################################
 
configAPI = loadAPIConf()

STL2PPMServerAPI = {'ip':configAPI['STL2PPMServer']['ip'], 'port':configAPI['STL2PPMServer']['port'], 'local':configAPI['STL2PPMServer']['local']}

api = api.API(STL2PPMServerAPI['port'], STL2PPMServerAPI['local'])
api.start()