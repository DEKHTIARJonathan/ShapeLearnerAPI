################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error, Bottle, template
from json import dumps
from sqlalchemy import *
from sqlalchemy.sql import select, column
import STLParser as STL

#################################### WebService Route / #####################################
class API:
	def __init__(self, port, local):
		self._app = Bottle()
		self._route()
		
		self._local = local
		self._port = port
		
		if local:
			self._host = '127.0.0.1'
		else:
			self._host = '0.0.0.0'
			
		self._parser = STL.STLParser()
	
	def start(self):
		self._app.run(server='paste', host=self._host, port=self._port)
		
	def _route(self):
		self._app.hook('before_request')(self._strip_path)
		self._app.error(400)(self._error404)
		self._app.error(500)(self._error500)
		
		self._app.route('/generatePPM', method="POST", callback=self._generatePPM)
		
		self._app.route('/static/<filename:path>', callback=self._getStaticFile)
		self._app.route('/', callback=self._homepage)
	
	def _strip_path(self):
		request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')
	
	def _error404(self):
		return static_file("404.html", root=os.getcwd()+'\\html')
		
	def _error500(self, error):
		return error
		
	def _getStaticFile(self, filename):
		extension = str.lower(os.path.splitext(filename)[1][1:])
		if  extension == 'jpeg'or extension == 'jpg':
			return static_file(filename, root=os.getcwd()+'\\static', mimetype='image/jpg')
		elif extension == 'png':
			return static_file(filename, root=os.getcwd()+'\\static', mimetype='image/png')
		elif extension == 'css':
			return static_file(filename, root=os.getcwd()+'\\static', mimetype='text/css')
		elif extension == 'js':
			return static_file(filename, root=os.getcwd()+'\\static', mimetype='text/javascript')  
	

	def _generatePPM(self):
		#inputs :
		#	{"sourceFile":"../temp/MotoReducteurB.stl", "format": "ppm&png", "precisionLevel" : 4} // "format" = ["ppm", "png", "ppm&png"] && "precisionLevel" : [0,1,2,3,4]
		#outputs :
		# 	{"status": "Success", "outputPPM": ["../temp/####.ppm", "../temp/####.ppm", "../temp/####.ppm"], "outputPNG": ["../temp/####.png", "../temp/####.png", "../temp/####.png"]}
		#	{"status": "Error", "message": "The STL File doesn't exist"}
		
		source = request.json["sourceFile"]
		precisionLevel = request.json["precisionLevel"]
		format = request.json["format"]
		
		rv = ""
		if not os.path.isfile(source) :
			rv = {"status": "Error", "message":"The STL File doesn't exist"}
		else :
			output = self._parser.generatePPMFiles(source, format, precisionLevel)
			rv = {"status": "Success", "outputPPM": output["ppm"], "outputPNG":  output["png"]}
		
		response.content_type = 'application/json'
		return dumps(rv)


	def _homepage(self):
		return static_file("index.html", root=os.getcwd()+'\\html')
