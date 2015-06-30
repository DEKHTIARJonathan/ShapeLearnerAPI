################################# Import Libraries ################################
import os.path
import sys
import ctypes
import threading
import time
from timing import TimingThread
import threadPool as TP

dllsPath = os.path.dirname(os.path.realpath(__file__))+'\dlls'
os.environ['PATH'] = dllsPath + ';' + os.environ['PATH']

class ShapeLearner():
	def __init__(self, _dbUser, _dbPass, _dbName, _ip, _port, _dbInitFile = ""):
		
		timeThread = TimingThread(3)
		timeThread.setName('timeThread')
		
		timeThread.start()
		time.sleep(1)
		
		self.__dll = ctypes.CDLL('dlls/ShapeLearnerDLL.dll')
		#void openDataBase(char* _dbUser, char* _dbPass, char* _dbName, char* _dbHost, unsigned int _dbPort, char* _dbInit = "")
		self.__dll.openDataBase.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_char_p]
		self.__dll.signBinaryImage.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
	
		self.__dll.openDataBase(_dbUser, _dbPass, _dbName, _ip, int(_port), _dbInitFile)
		timeThread.join()
	
	
	def signBinaryImage(self, _img, _class):
		self.__dll.signBinaryImage(_img, _class, 1)
		return "OK"
		
	
	def getActiveThread(self):
		return int(self.__dll.getActiveThread())