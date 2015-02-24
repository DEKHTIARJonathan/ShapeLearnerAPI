################################# Import Libraries ################################
import os.path
import xml.etree.ElementTree as XML

def loadConf(confPath = '../Config/conf.xml'):
	configurations = XML.parse(confPath).getroot()

	servers = dict()

	for serv in configurations.iter('DBserver'):
	
		serverName = serv.attrib['serverName']
		serverPort = serv.attrib['port']
		serverIP = serv.attrib['ip']
		dbUser = serv.attrib['dbUser']
		dbPass = serv.attrib['dbPass']
		dbName = serv.attrib['dbName']
		
		servers[serverName] = {'ip':serverIP, 'port':serverPort, 'dbUser':dbUser, 'dbPass':dbPass, 'dbName':dbName }
		
	return servers