################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error, Bottle, template
from json import dumps, loads
import uuid
import urllib2

#################################### WebService Route / #####################################
class API:
	def __init__(self, stl2ppmServer, jobServer, shockGraphProdServer, shockGraphTrainServer, shockGraphMatchServer, port, local):
		self._app = Bottle()
		self._route()
		
		self._stl2ppmServer = 'http://' + stl2ppmServer['ip'] + ':' + stl2ppmServer['port'] + '/generatePPM'
		self._jobServer = 'http://' + jobServer['ip'] + ':' + jobServer['port'] + '/getJobStatus'
		self._shockGraphProdServer = 'http://' + shockGraphProdServer['ip'] + ':' + shockGraphProdServer['port'] + '/launchComputation'
		self._shockGraphTrainServer = 'http://' + shockGraphTrainServer['ip'] + ':' + shockGraphTrainServer['port'] + '/launchComputation'
		self._shockGraphMatchServer = 'http://' + shockGraphMatchServer['ip'] + ':' + shockGraphMatchServer['port'] + '/launchComputation'
		
		self._local = local
		self._port = port
		
		if local:
			self._host = '127.0.0.1'
		else:
			self._host = '0.0.0.0'
	
	def start(self):
		self._app.run(server='paste', host=self._host, port=self._port)
		
	def _generateFilename (self):
		return str(uuid.uuid4().hex)
		
	def _sendPostRequest(self, url, params):
		
		req = 	urllib2.Request(
					url,
					headers = {
						"Content-Type": "application/json",
						"Accept": "*/*",   
						"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36",
						"DNT": '1',
						'Accept-Encoding': 'gzip, deflate',
						'Accept-Language': 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4',
					}, 
					data = dumps(params)
				)				
		
		f = urllib2.urlopen(req)
		
		return loads(f.read())
		
	def _route(self):
		self._app.hook('before_request')(self._strip_path)
		self._app.error(400)(self._error404)
		self._app.error(500)(self._error500)
		self._app.route('/static/<filename:path>', callback=self._getStaticFile)
		self._app.route('/', callback=self._homepage)
		
		self._app.route('/upload', method="POST", callback=self._upload)
		self._app.route('/signInContext', method="POST", callback=self._signInContext)
		self._app.route('/getJobStatus', method="POST", callback=self._getJobStatus)
		
	
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

	def _homepage(self):
		return static_file("index.html", root=os.getcwd()+'\\html')
	
	def _upload(self):
		classname   = request.forms.get('classname')
		upload     = request.files.get('upload')
		
		name, ext = os.path.splitext(upload.filename.lower())
		
		rv = ""
		if ext not in ('.ppm','.stl'):
			rv = {"status": "Error", "message": 'File extension not allowed.'}
		else:
			save_path = "../temp/"
			savingName = self._generateFilename() + ext
			fullpath = save_path + savingName
			upload.save(fullpath) # appends upload.filename automatically
			
			rv = {"status": "Success", "filePath": fullpath}
			
		response.content_type = 'application/json'
		return dumps(rv)
	
	def _signInContext(self):
		classname	= request.forms.get('classname')
		upload		= request.files.get('upload')
		
		shockServer = ""
		if classname.lower() == "production":
			shockServer = self._shockGraphProdServer
		else :
			shockServer = self._shockGraphTrainServer
		
		name, ext = os.path.splitext(upload.filename.lower())
		
		rv = ""
		if ext not in ('.ppm','.stl', '.zip'):
			rv = {"status": "Error", "message": 'File extension not allowed.'}
		else:
			save_path = "../temp/"
			savingName = self._generateFilename() + ext
			fullpath = save_path + savingName
			upload.save(fullpath) # appends upload.filename automatically
			
			if ext ==  ".zip":
				rv = {"status": "Success", "filepath": fullpath, "classname": classname}
			elif ext == ".ppm":
			
				dataShock = {"filename":fullpath, "classname":classname}
				tmp = self._sendPostRequest(shockServer, dataShock)
				if tmp['status'] != 'Error':
					rv = {"status": "Success", "jobID": tmp['jobID'], "classname": classname}
					
			else: # == ".stl"				
								
				params = {"sourceFile":fullpath, "format": "ppm", "precisionLevel" : 4}
				outputSTL = self._sendPostRequest(self._stl2ppmServer, params)
				os.remove(fullpath) #Removing the file after using
				
				jobIDs = []
				for file in outputSTL['outputPPM']:
					dataShock = {"filename":file, "classname":classname}
					tmp = self._sendPostRequest(shockServer, dataShock)
					if tmp['status'] != 'Error':
						jobIDs.append(tmp['jobID'])
					
				rv = {"status": "Success", "jobIDs": jobIDs, "classname": classname}
		
		response.content_type = 'application/json'
		return dumps(rv)
	
	def _getJobStatus(self):
		
		idJob = request.json["idJob"]
		
		jobData = {"idJob":idJob}
		tmp = self._sendPostRequest(self._jobServer, jobData)
		
		response.content_type = 'application/json'
		return dumps(tmp)
