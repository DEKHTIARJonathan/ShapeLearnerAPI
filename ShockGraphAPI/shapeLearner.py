################################# Import Libraries ################################
import os.path
import sys
import ctypes
from threading import Thread
import time
from timing import TimingThread

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
		self.__dll.signBinaryImage.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
	
		self.__dll.openDataBase(_dbUser, _dbPass, _dbName, _ip, int(_port), _dbInitFile)
		timeThread.join()
	
	def signBinaryImage(self, _img, _class):
		self.__dll.signBinaryImage(_img, _class)


class ShockGrThread(Thread):
 
	def __init__(self, _app, _img, _class):
		''' Constructor. '''
		Thread.__init__(self)
		self.__app = _app
		self.__img = _img
		self.__class = _class
		
	def run(self):
		self.__app.signBinaryImage(self.__img, self.__class)