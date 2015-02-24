################################# Loading config File ################################
import sys
sys.path.append('../Config/')
from loadConf import loadConf

################################# Import Libraries ################################
import os.path
import urllib2
import time
from sqlalchemy import *
from sqlalchemy.sql import select, column
from bottle import route, run, response, static_file, request, error
from json import dumps

#################################### WebService Route / #####################################

@route('/static/<filename:path>')
def getStaticFile(filename):

	extension = str.lower(os.path.splitext(filename)[1][1:])

	if  extension == 'jpeg'or extension == 'jpg':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\static', mimetype='image/jpg')
	elif extension == 'png':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\static', mimetype='image/png')
	elif extension == 'css':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\static', mimetype='text/css')
	elif extension == 'js':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\static', mimetype='text/javascript') 

@route('/test')
def homepage():
	for i in range (1,5):
		print "processing ..."
		time.sleep(1)
	return "Process Finished"
	
	
@route('/')
def homepage():
    return static_file("index.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\html')
	
@route('<request:path>')
def reroute(request):
	return urllib2.urlopen('http://127.0.0.1:8888'+str(request))

@error(404)
def error404(error):
    return static_file("404.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\ShapeLearnerAPI\\html')
	
@error(500)
def error500(error):
    return error

################################# Server Initialization #####################################
config = loadConf()

run(server='paste', host='0.0.0.0', port=80, debug=True, reloader=True)
