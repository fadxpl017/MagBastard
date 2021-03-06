from resources import ServiceListener
from logging import logger
from ConfigParser import ConfigParser
import socket

# Note: inetsim has the NetBios ports set to 137/138
config = ConfigParser()
config.read("magbastard.cfg")
inetaddr = config.get("inetsim", "inetaddr")
inetNetBiosport = int(config.get("inetsim", "inetNETBIOSport"))

def netbiosHandler(s, server, details):
    request = ServiceListener.getMessage(s)
    logger.updateTimestamp(details[0])
    if request != None: 
        logger.logEvent(details[2], details[3], details[0], details[1], request)
	print request
	honeypot = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	honeypot.connect((inetaddr, inetNetBiosport))
	honeypot.send(request)
	response = honeypot.recv(65535)
	ServiceListener.sendResponse(response)
	logger.logEvent(details[2], details[3], details[0], details[1], response)
    '''
    if request != None and request == '\0\0\0\xa4\xff\x53\x4d\x42\x72\0\0\0\0\x08\x01\x40\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x40\x06\0\0\x01\0\0\x81\0\x02PC NETWORK PROGRAM 1.0\0\x02MICROSOFT NETWORKS 1.03\0\x02MICROSOFT NETWORKS 3.0\0\x02LANMAN1.0\0\x02LM1.2X002\0\x02Samba\0\x02NT LANMAN 1.0\0\x02NT LM 0.12\0':
#		if request != None:
        response = server["Version"]
        ServiceListener.sendResponse(s, response)
        logger.logEvent(details[2], details[3], details[0], details[1], response)
    '''
    s.close()

