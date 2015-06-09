################################# Import Libraries ################################
import os.path
import xml.etree.ElementTree as XML

def loadConf(confPath = '../Config/conf.xml'):
	configurations = XML.parse(confPath).getroot()

	servers = dict()

	for serv in configurations.iter('DBserver'):
		serverName = serv.attrib['name']
		serverPort = serv.attrib['port']
		serverIP = serv.attrib['ip']
		servers[serverName] = [serverIP, serverPort]
		
	return servers