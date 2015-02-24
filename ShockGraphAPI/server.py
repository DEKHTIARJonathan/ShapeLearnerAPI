################################# Loading config File ################################
import sys
sys.path.append('../Config/')
from loadConf import loadConf

################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

import ctypes
from threading import Thread
import time 
from sqlalchemy import *
from sqlalchemy.sql import select, column

################################# Init Connection #################################

def initConnect(credentials):
	engine = create_engine("postgresql+psycopg2://"+credentials['dbUser']+":"+credentials['dbPass']+"@"+credentials['ip']+":"+credentials['port']+"/"+credentials['dbName'], isolation_level="READ COMMITTED")
	connection = engine.connect()
	return [engine, connection]
	
################################# Threading Classes ###############################
 
class TimingThread(Thread):
 
	def __init__(self, _timer):
		''' Constructor. '''
		Thread.__init__(self)
		self.__timingDLL = ctypes.CDLL('timeTrickDLL.dll')
		self.__timingDLL.changeTime.argtypes = [ctypes.c_uint]
		self.timer = _timer
 
	def run(self):
		self.__timingDLL.changeTime(self.timer)	
		
		
class ShockGrThread(Thread):
 
	def __init__(self, _dll, _img, _class):
		''' Constructor. '''
		Thread.__init__(self)
		self.__dll = _dll
		self.__img = _img
		self.__class = _class
		
	def run(self):
		self.__dll.signBinaryImage(self.__img, self.__class)
		#self.__dll.waitBeforeClosing()

#################################### WebService Route / #####################################

@error(404)
def error404(error):
	return static_file("404.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\ShockGraphAPI\\html')
	
@error(500)
def error500(error):
	return error

@route('/static/<filename:path>')
def getStaticFile(filename):
	extension = str.lower(os.path.splitext(filename)[1][1:])
	if  extension == 'jpeg'or extension == 'jpg':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShockGraphAPI\\static', mimetype='image/jpg')
	elif extension == 'png':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShockGraphAPI\\static', mimetype='image/png')
	elif extension == 'css':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShockGraphAPI\\static', mimetype='text/css')
	elif extension == 'js':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShockGraphAPI\\static', mimetype='text/javascript')  

@route('/prepareLearning')
def prepareLearning():
	v_connect = initConnect(trainServer)
	rslt =  v_connect[1].execute('select * from updateColumnData();')

	return "Training Data Updated"

@route('/')
def homepage():
	global partID
	shockThread = ShockGrThread(dll, lst[partID][0], lst[partID][1])
	shockThread.setName('shockThread1')
	shockThread.start()
	partID = partID + 1
	return static_file("index.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\ShockGraphAPI\\html')
	
################################# Server Initialization #####################################
config = loadConf()

trainServer = {'ip':config['trainDB']['ip'], 'port':config['trainDB']['port'], 'dbUser':config['trainDB']['dbUser'], 'dbPass':config['trainDB']['dbPass'], 'dbName':config['trainDB']['dbName']}
testServer = {'ip':config['prodDB']['ip'], 'port':config['prodDB']['port'], 'dbUser':config['prodDB']['dbUser'], 'dbPass':config['prodDB']['dbPass'], 'dbName':config['prodDB']['dbName']}


timeThread = TimingThread(3)
timeThread.setName('timeThread')

timeThread.start()
time.sleep(1)

dll=ctypes.CDLL('ShapeLearnerDLL.dll')
dll.openDataBase.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p]
dll.signBinaryImage.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
#void openDataBase(char* _dbUser, char* _dbPass, char* _dbName, char* _dbHost, unsigned int _dbPort, char* _dbInit = "")

dll.openDataBase(trainServer['dbUser'], trainServer['dbPass'], trainServer['dbName'], trainServer['ip'], int(trainServer['port']), "structure.sql")

timeThread.join()

lst = [['AmortisseurA00.ppm', 'Amortisseur'],['AmortisseurA10.ppm', 'Amortisseur']]

partID = 0

run(server='paste', host='0.0.0.0', port=8000)