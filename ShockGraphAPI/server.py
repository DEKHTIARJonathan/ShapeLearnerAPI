################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

import ctypes
import threading
import time 
import threadPool as TP
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
 
jobs = []
threadList = []

for file in files :
	partID = partID + 1 
	if (file.endswith('.ppm') or file.endswith('.PPM')) and file[0] != "." :
		classname = ""
		
		try:
			if int(file[-7:-4]) >= 100: #FileNumber is equal or greater than 100
				classname = file[:-8]
		except Exception :
				classname = file[:-7]
		jobs.append(["data/" + file, classname, 'shockThread' + str(partID)])

locker = threading.Lock() 
	
for j in jobs:
	locker.acquire()
	activeThread = trainEngine.getActiveThread()
	
	if activeThread > 60 and len(threadList) > 0:
		th = threadList[0]
		del threadList[0]
		
	elif activeThread > 60 and len(threadList) <= 0 :
		time.sleep(1)
		
	else :
		print "Launched : " + j[0] + " // " + j[1] + " && Thread number = " + str(activeThread)
		threadList.append(threading.Thread(target = trainEngine.signBinaryImage, name=j[2],args=(j[0], j[1])))	
		threadList[-1].daemon=True
		threadList[-1].start()
		
	locker.release()

for t in threadList:	
	t.join(1)
	
print "Operation Finished"