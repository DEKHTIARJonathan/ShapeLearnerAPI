################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

import ctypes
import threading
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

#######################################################################################
#######################################################################################
#######################################################################################

################################# Init Connection #################################

def initConnect(credentials):
	engine = create_engine("postgresql+psycopg2://"+credentials['dbUser']+":"+credentials['dbPass']+"@"+credentials['ip']+":"+credentials['port']+"/"+credentials['dbName'], isolation_level="READ COMMITTED")
	connection = engine.connect()
	return [engine, connection]
	
################################# Threading Classes ###############################
 

config = loadConf()
jobServer = {'ip':config['jobDB']['ip'], 'port':config['jobDB']['port'], 'dbUser':config['jobDB']['dbUser'], 'dbPass':config['jobDB']['dbPass'], 'dbName':config['jobDB']['dbName']}

v_connect = initConnect(jobServer)

api = api.API(v_connect)
api.start()



'''
UPDATE table SET field='C', field2='Z' WHERE id=3;
INSERT INTO table (id, field, field2)
       SELECT 3, 'C', 'Z'
       WHERE NOT EXISTS (SELECT 1 FROM table WHERE id=3);
	   '''