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

shockGraphServerAPI = {'ip':configAPI['shockGraphMatchServer']['ip'], 'port':configAPI['shockGraphMatchServer']['port'], 'local':configAPI['shockGraphMatchServer']['local']}
jobServerAPI = {'ip':configAPI['jobServer']['ip'], 'port':configAPI['jobServer']['port'], 'local':configAPI['jobServer']['local']}

api = api.API(jobServerAPI, shockGraphServerAPI['port'], shockGraphServerAPI['local'])
api.start()