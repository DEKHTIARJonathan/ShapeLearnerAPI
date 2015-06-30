################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error, Bottle, template
from json import dumps

#################################### WebService Route / #####################################
class API:
	def __init__(self, connectArr, local=False):
		self._app = Bottle()
		self._route()
		
		self._engine = connectArr[0]
		self._connection = connectArr[1]
		self._local = local
	
	def start(self):
		if self._local:
			self._app.run(server='paste', host='127.0.0.1', port=8888)
		else:
			self._app.run(server='paste', host='0.0.0.0', port=8888)
		
	def _route(self):
		self._app.route('/updateJob', method="POST", callback=self._updateJob)
		self._app.route('/initdb/', callback=self._initDB)
		self._app.route('/initdb', callback=self._initDB)
		self._app.route('/static/<filename:path>', callback=self._getStaticFile)
		self._app.route('/', callback=self._homepage)
		self._app.error(400)(self._error404)
		self._app.error(500)(self._error500)
		
	def _error404(self):
		return static_file("404.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\JobServer\\html')
		
	def _error500(self, error):
		return error
		
	def _getStaticFile(self, filename):
		extension = str.lower(os.path.splitext(filename)[1][1:])
		if  extension == 'jpeg'or extension == 'jpg':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\JobServer\\static', mimetype='image/jpg')
		elif extension == 'png':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\JobServer\\static', mimetype='image/png')
		elif extension == 'css':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\JobServer\\static', mimetype='text/css')
		elif extension == 'js':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\JobServer\\static', mimetype='text/javascript')  

	def _updateJob(self):
		print request.json["jobID"]
		print request.json["jobStatus"]
		print request.json["partID"]
		print request.json["partName"]
		print request.json["serverIP"]
		print request.json["serverPort"]
		print request.json["message"]
		return "ok"
	
	def _initDB(self):
		f = open('structure.sql', 'r')
		result = ""
		try:
			sql = str(f.read())
			result = self._engine.execute(sql)
		finally:
			f.close()
			return "ok"

	def _homepage(self):
		return static_file("index.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\JobServer\\html')
