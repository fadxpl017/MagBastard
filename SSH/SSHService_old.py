import time, uuid, sys, re
import socket
import urlparse

# Constants
sendRate = 1000
listenAddress = "localhost"

if len(sys.argv) > 1:
    def randint(a, b):
        return int(sys.argv[1])
else:
    from random import randint

def selectServer():
    # Read list of supported servers from file
    file = open("SSHservers.config", "r")
    servers = eval(file.read())
    file.close()

    # Choose the server version
    return servers[randint(0, len(servers) - 1)]

def createListenerSocket(host, port):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind((host, port))
    listener.listen(10)
    return listener


def getMessage(skt):
    skt.setblocking(1)
    try:
        message = skt.recv(1)
    
        if (len(message) < 1):
            return None
        skt.setblocking(0)
        while True:
            try:
                message += skt.recv(100)
            except socket.error:
                break;
        skt.setblocking(1)
        return message
    except:
        return None

def sendResponse(skt, msg, flags=0):
    try: 
    	skt.send(msg)
    except:
	print("Connection reset!")

def __main__():
    server = selectServer()
    print("Chose SSH server %s" % server["Name"])
    listener = createListenerSocket(listenAddress, 22)
    while 1 == 1:
        (s, details) = listener.accept()
        print("Got a connection!")
        response = server["Response"]
        sendResponse(s, response)
        s.close()

__main__()
