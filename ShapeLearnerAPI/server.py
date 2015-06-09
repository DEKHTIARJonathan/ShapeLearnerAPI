################################# Loading config File ################################
import sys
sys.path.append('../Config/')
from loadConf import loadConf

################################# Import Libraries ################################
import os.path
from sqlalchemy import *
from sqlalchemy.sql import select, column
from bottle import route, run, response, static_file, request, error
from json import dumps

#################################### WebService Route / #####################################
@error(404)
def error404(error):
    return static_file("404.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\PredictionAPI\\')
	
@error(500)
def error500(error):
    return error
	
@route('/images/<filename:path>')
def getImages(filename):
	extension = str.lower(os.path.splitext(filename)[1][1:])
	if  extension == 'jpeg'or extension == 'jpg':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\PredictionAPI\\images', mimetype='image/jpg')
	elif extension == 'png':
		return static_file(filename, root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\PredictionAPI\\images', mimetype='image/png')
     
	
@route('/')
def homepage():
    return static_file("index.html", root='C:\\Users\\Administrator\\Desktop\\ShapeLearnerPackage\\PredictionAPI\\')

################################# Server Initialization #####################################
config = loadConf()

run(server='paste', host='0.0.0.0', port=8080, debug=True, reloader=True)
