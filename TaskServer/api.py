################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

#################################### WebService Route / #####################################
class API:
	def __init__(self, local=False):
		route("/updateTask", method='POST')(self.updateTask)
		run(server='paste', host='0.0.0.0', port=8888)
		
	
	@error(404)
	def error404(error):
		return static_file("404.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\TaskServer\\html')
		
	@error(500)
	def error500(error):
		return error

	@route('/static/<filename:path>')
	def getStaticFile(filename):
		extension = str.lower(os.path.splitext(filename)[1][1:])
		if  extension == 'jpeg'or extension == 'jpg':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\TaskServer\\static', mimetype='image/jpg')
		elif extension == 'png':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\TaskServer\\static', mimetype='image/png')
		elif extension == 'css':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\TaskServer\\static', mimetype='text/css')
		elif extension == 'js':
			return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\TaskServer\\static', mimetype='text/javascript')  

	#@route ('/updateTask', method='POST')
	def updateTask(self):
		print request.json["glossary"]
		print request.json["name"]
		

	@route('/')
	def homepage():
		return static_file("index.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\\TaskServer\\html')
	
	
