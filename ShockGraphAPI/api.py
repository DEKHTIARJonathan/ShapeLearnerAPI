################################# Import Libraries ################################
import os.path
from bottle import route, run, response, static_file, request, error
from json import dumps

#################################### WebService Route / #####################################
class API:
	def __init__(self, local=False):
		run(server='paste', host='0.0.0.0', port=8000)
	
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
	
	
