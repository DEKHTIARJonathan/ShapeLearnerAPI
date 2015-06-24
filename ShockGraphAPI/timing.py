################################# Import Libraries ################################
import ctypes
from threading import Thread
import time 

class TimingThread(Thread):
	def __init__(self, _timer):
		''' Constructor. '''
		Thread.__init__(self)
		self.__timingDLL = ctypes.CDLL('dlls/timeTrickDLL.dll')
		self.__timingDLL.changeTime.argtypes = [ctypes.c_uint]
		self.timer = _timer
 
	def run(self):
		self.__timingDLL.changeTime(self.timer)	
