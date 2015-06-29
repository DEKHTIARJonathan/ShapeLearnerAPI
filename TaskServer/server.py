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
taskServer = {'ip':config['taskDB']['ip'], 'port':config['taskDB']['port'], 'dbUser':config['taskDB']['dbUser'], 'dbPass':config['taskDB']['dbPass'], 'dbName':config['taskDB']['dbName']}

api = api.API()