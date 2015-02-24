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
 

configDB = loadDBConf()
configAPI = loadAPIConf()

shapeLearnerAPI = {'ip':configAPI['shapeLearnerAPI']['ip'], 'port':configAPI['shapeLearnerAPI']['port'], 'local':configAPI['shapeLearnerAPI']['local']}
stl2ppmServer =  {'ip':configAPI['STL2PPMServer']['ip'], 'port':configAPI['STL2PPMServer']['port'], 'local':configAPI['STL2PPMServer']['local']}
shockGraphProdServer =  {'ip':configAPI['shockGraphProdServer']['ip'], 'port':configAPI['shockGraphProdServer']['port'], 'local':configAPI['shockGraphProdServer']['local']}
shockGraphTrainServer =  {'ip':configAPI['shockGraphTrainServer']['ip'], 'port':configAPI['shockGraphTrainServer']['port'], 'local':configAPI['shockGraphTrainServer']['local']}
shockGraphMatchServer =  {'ip':configAPI['shockGraphMatchServer']['ip'], 'port':configAPI['shockGraphMatchServer']['port'], 'local':configAPI['shockGraphMatchServer']['local']}

api = api.API(stl2ppmServer, shockGraphProdServer, shockGraphTrainServer, shockGraphMatchServer, shapeLearnerAPI['port'], shapeLearnerAPI['local'])
api.start()