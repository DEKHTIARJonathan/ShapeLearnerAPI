################################ Import Libraries ################################
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

trainDBServer = {'ip':configDB['trainDB']['ip'], 'port':configDB['trainDB']['port'], 'dbUser':configDB['trainDB']['dbUser'], 'dbPass':configDB['trainDB']['dbPass'], 'dbName':configDB['trainDB']['dbName']}

shockGraphServerAPI = {'ip':configAPI['shockGraphTrainServer']['ip'], 'port':configAPI['shockGraphTrainServer']['port'], 'local':configAPI['shockGraphTrainServer']['local']}
jobServerAPI = {'ip':configAPI['jobServer']['ip'], 'port':configAPI['jobServer']['port'], 'local':configAPI['jobServer']['local']}

api = api.API(jobServerAPI, shockGraphServerAPI['port'], shockGraphServerAPI['local'], trainDBServer)
api.start()