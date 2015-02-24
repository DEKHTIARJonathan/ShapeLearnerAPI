# coding: utf-8

################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error, Bottle, template
from json import dumps
import shapeLearner as SL

#################################### WebService Route / #####################################
'''
@route('/prepareLearning')
def prepareLearning():
	v_connect = initConnect(trainServer)
	rslt =  v_connect[1].execute('select * from updateColumnData();')

	return "Training Data Updated"
'''
#################################### WebService Route / #####################################
class API:
	def __init__(self, jobServerAPI, port, local, credentials = ""):
		
		self._matchServer = False
		if credentials == "":
			self._matchServer = True
		
		self._app = Bottle()
		self._route()
		
		self._engine = ""
		if self._matchServer != "":
			self._engine =  SL.ShapeLearner(credentials['dbUser'], credentials['dbPass'], credentials['dbName'], credentials['ip'], int(credentials['port']))
		else:
			self._engine =  SL.ShapeLearner()
		
		self._jobServer = jobServerAPI
		
		self._local = local
		self._port = port
		
		if local:
			self._host = '127.0.0.1'
		else:
			self._host = '0.0.0.0'
	
	def start(self):
		self._app.run(server='paste', host=self._host, port=self._port)
		
	def _route(self):
		self._app.hook('before_request')(self._strip_path)
		self._app.error(400)(self._error404)
		self._app.error(500)(self._error500)
		
		if not self._matchServer :
			self._app.route('/launchComputation', method="POST", callback=self._launchComputation)
			self._app.route('/batchProcess', method="POST", callback=self._batchProcess)	
		else:
			self._app.route('/compareSignatures', method="POST", callback=self._compareSignatures)		
		
		self._app.route('/getActiveThreads', callback=self._getActiveThreads)		
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
			
	def _launchComputation(self):
	#inputs : 
	#	Production : {"folder": "../temp", "filename":"AmortisseurA00.ppm", "classname":"production"}
	#	Training : {"folder": "../temp", "filename":"AmortisseurA00.ppm", "classname":"Bielle"}
	#outputs :
	#	Success : {"status": "JobStarted", "jobID": 38}
	#	Error : {"status": "Error", "message": "The file requested doesn't exist"}
	#	Error : {"status": "Error", "message": "The folder requested doesn't exist"}
	#	Error : {"status": "Error", "message": "The File's extension is not the correct one (*.ppm required)"}
	
	
		inputDir = request.json["folder"]
		filename = request.json["filename"]
		classname = request.json["classname"]
		
		file = inputDir + "/" + filename
		rv = ""
		
		if not os.path.isdir(inputDir):
			rv = {"status" : "Error", "message" : "The folder requested doesn't exist"}
			
		else:
			if not os.path.isfile(file) :
				rv = {"status" : "Error", "message" : "The file requested doesn't exist"}
				
			elif not ( (file.endswith('.ppm') or file.endswith('.PPM')) and file[0] != "." ):
				rv = {"status" : "Error", "message" : "The File's extension is not the correct one (*.ppm required)"}
				
			else :
				jobID = self._engine.signBinaryImage(file, classname)
				rv = {"status" : "JobStarted", "jobID": jobID}
		
		response.content_type = 'application/json'
		return dumps(rv)

	def _batchProcess(self):
	#inputs : 
	#	Production && Training : {"folder": "../temp"} // Attention, le nom des fichiers doit correspondre au formalisme : Nomdeclasse{compteurAlphabetiqueEn1Lettre}{CompteurNumériqueMax3Chiffres}.ppm, exemple : BielleA120.ppm
	#outputs :
	#	Success : {"status": "Batch Process launched", "jobInfos": [{"jobFile": "AmortisseurA00.ppm", "jobID": 45}, {"jobFile": "AmortisseurA10.ppm", "jobID": 46}]}
	#	Error : {"status": "Error", "message": "The folder requested doesn't exist"}
		
		inputDir = request.json["folder"]
		rv = ""
		
		if not os.path.isdir(inputDir):
			rv = {"status" : "Error", "message" : "The folder requested doesn't exist"}
		else :
		
			files = self._getFiles(inputDir + "/")
			jobs = []

			for file in files :
				if (file.endswith('.ppm') or file.endswith('.PPM')) and file[0] != "." :
					classname = ""
					
					try:
						if int(file[-7:-4]) >= 100: #FileNumber is equal or greater than 100
							classname = file[:-8]
					except Exception :
							classname = file[:-7]

					jobs.append([inputDir + "/" + file, classname, file])
			
			rslt = []
			for j in jobs:
				rslt.append({"jobID":self._engine.signBinaryImage(j[0], j[1]), "jobFile" : j[2]})
			
			rv = {"status": "Batch Process launched", "jobInfos": rslt}
		
		response.content_type = 'application/json'
		return dumps(rv)
		
	def _compareSignatures(self): #NOT WORKING FOR THE MOMENT !
	#inputs:
	#	{"mainSignature": "<DAG>...</DAG>","candidates": [{"classname" : "test","signature" : "<Dag ...."},{"classname" : "test","signature" : "<DAG>...</DAG>"},{"classname" : "test","signature" : "<DAG>...</DAG>"}]}
	#	Valider le JSON d'entrée sur : http://jsonlint.com/
	#outputs :
	#	{"mainSignature": "<DAG>...</DAG>", "candidates": [{"classname": "test", "signature": "<Dag ...."}, {"classname": "test", "signature": "<DAG>...</DAG>"}, {"classname": "test", "signature": "<DAG>...</DAG>"}]}
	#	{"resultat": "bielle"}
	
		mainSignature = request.json["mainSignature"]
		
		candidates = request.json["candidates"]
		
		rv = {"resultat": "bielle"}
		response.content_type = 'application/json'
		
		return dumps(rv)

	def _getActiveThreads(self):
		rv = {"activeThreads": self._engine.getActiveThread()}
		
		response.content_type = 'application/json'
		return dumps(rv)
		
	def _homepage(self):
		return static_file("index.html", root=os.getcwd()+'\\html')
		
	######################## Tool Methods ############################
	
	def _getFiles(self, path) : 
		files = []
		listing = os.listdir(path)
		for f in listing:
			if os.path.isfile(path + "/" + f):
				files.append(f)
		return files
		
	def _escapeXML(self, signature) :
		import re
		signature.replace('"','\"')
		signature = re.sub(r'\s*[\n\t\r]\s*', '', signature)
		return signature
		
		"""<DAG class="ShockGraph" nodeCount="2">
		<objectName>data/AmortisseurA</objectName>
		<viewNumber>52</viewNumber>
		<node parentCount="1" childCount="0" index="1" label="1" level="1" mass="1">
		<type>4</type>
		<pointCount>4</pointCount>
		<point xcoord="149" ycoord="148" radius="26.9998"/>
		<point xcoord="149" ycoord="149" radius="27.8888"/>
		<point xcoord="149" ycoord="150" radius="27.8888"/>
		<point xcoord="149" ycoord="151" radius="26.9998"/>
		</node>
		<node parentCount="0" childCount="1" index="0" label="#" level="0" mass="3">
		<type>5</type>
		<pointCount>0</pointCount>
		</node>
		<edge source="0" target="1">
		<weight>1</weight>
		</edge>
		</DAG>
		"""
		
	
