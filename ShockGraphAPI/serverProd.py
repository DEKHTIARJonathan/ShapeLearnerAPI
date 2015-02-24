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

prodDBServer = {'ip':configDB['prodDB']['ip'], 'port':configDB['prodDB']['port'], 'dbUser':configDB['prodDB']['dbUser'], 'dbPass':configDB['prodDB']['dbPass'], 'dbName':configDB['prodDB']['dbName']}

shockGraphServerAPI = {'ip':configAPI['shockGraphProdServer']['ip'], 'port':configAPI['shockGraphProdServer']['port'], 'local':configAPI['shockGraphProdServer']['local']}
jobServerAPI = {'ip':configAPI['jobServer']['ip'], 'port':configAPI['jobServer']['port'], 'local':configAPI['jobServer']['local']}

api = api.API(jobServerAPI, shockGraphServerAPI['port'], shockGraphServerAPI['local'], prodDBServer)
api.start()