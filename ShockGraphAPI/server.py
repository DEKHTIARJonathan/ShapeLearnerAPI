################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

import ctypes
from threading import Thread
import time 
from sqlalchemy import *
from sqlalchemy.sql import select, column

################################# Loading config File ################################
import sys
sys.path.append('../Config/')
dllsPath = os.path.dirname(os.path.realpath(__file__))+'\dlls'
os.environ['PATH'] = dllsPath + ';' + os.environ['PATH']
from loadConf import loadConf

import api
import shapeLearner as SL

#######################################################################################
#######################################################################################
#######################################################################################

################################# Init Connection #################################

def initConnect(credentials):
	engine = create_engine("postgresql+psycopg2://"+credentials['dbUser']+":"+credentials['dbPass']+"@"+credentials['ip']+":"+credentials['port']+"/"+credentials['dbName'], isolation_level="READ COMMITTED")
	connection = engine.connect()
	return [engine, connection]
	
################################# Threading Classes ###############################
 
'''
api = api.API()
'''

config = loadConf()
trainServer = {'ip':config['trainDB']['ip'], 'port':config['trainDB']['port'], 'dbUser':config['trainDB']['dbUser'], 'dbPass':config['trainDB']['dbPass'], 'dbName':config['trainDB']['dbName']}
testServer = {'ip':config['prodDB']['ip'], 'port':config['prodDB']['port'], 'dbUser':config['prodDB']['dbUser'], 'dbPass':config['prodDB']['dbPass'], 'dbName':config['prodDB']['dbName']}

trainEngine = SL.ShapeLearner(trainServer['dbUser'], trainServer['dbPass'], trainServer['dbName'], trainServer['ip'], int(trainServer['port']), "structure.sql")

################################### LAUNCH EXEC ######################################################

def getFiles(path) : 
	files = []
	listing = os.listdir(path)
	for f in listing:
		if os.path.isfile(path + "/" + f):
			files.append(f)
	return files
	
inputDir = "data"

partID = 0
files = getFiles(inputDir + "/")

for file in files :
	partID = partID + 1 
	if (file.endswith('.ppm') or file.endswith('.PPM')) and file[0] != "." :
		classname = ""
		
		try:
			if int(file[-7:-4]) >= 100: #FileNumber is equal or greater than 100
				classname = file[:-8]
		except Exception :
				classname = file[:-7]
		
		shockThread = SL.ShockGrThread(trainEngine, "data/" + file, classname)
		shockThread.setName('shockThread' + str(partID))
		shockThread.start()
		print "Launched : " + file