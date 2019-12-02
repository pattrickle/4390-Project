#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Controller Code
import socket
import sys
import os

class Controller:
	LOCAL_IP = "10.0.0.3"
	R_IP = "10.0.0.2"
	S_IP = "10.0.0.1"

	C = (LOCAL_IP,5000)
	R = (LOCAL_IP,5000)
	S = (LOCAL_IP,5000)
	controllerSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	COMMANDPROMPT = ("Enter the number corresponding to the desired command:\n[0] Play\n[1] Pause\n[2] Restart\n[3] Disconnect")
	FILEPROMPT = ("Enter the number corresponding to the desired file:")

	type = ""
	code = ""
	inPayload = ["",""]
	outPayload = ""
	disconnect = False
	streaming = False

	def __init__(self):
    	self.controllerSock.bind(self.C)
    	self.disconnect = False

	def isConnected(self):
    	if self.disconnect:
        	return False
    	else:
        	return True

	def listenCommand(self):
    	rawPacket = self.controllerSock.recv(64)
    	if rawPacket:
        	packet = rawPacket.split(" ",3)
        	self.type = packet[0] #first is type
        	self.code = packet[1] #second is type
        	if type == "STREAM" and code == "NULL":
            	self.inPayload = packet[2].split(" ",1) #will be split if type and code are stream and NULL
        	else:
            	self.inPayload[0] = packet[2]
	def sendCommand(self, HOST, STATUS):

    	self.outPayload = ""
    	print("Send Command")
    	self.localPacket = STATUS + self.outPayload
    	if HOST == "S":
        	self.controllerSock.sendto(self.localPacket,self.S)
        	if HOST == "R":
            	self.controllerSock.sendto(self.localPacket,self.R)

	def play(self):
    	sendCommand("S", "PLAY LINE ")
	def pause(self):
    	sendCommand("S", "PAUSE NULL ")
	def restart(self):
    	sendCommand("S", "RESTART NULL ")
	def disconnect(self):
    	sendCommand("S", "DISCONNECT NULL ")

controller = Controller()

if controller.isConnected():
	print "True"
else:
	print "False"

while controller.isConnected():
	#create initial frame
	controller.sendCommand("S", "CONNECT NULL ")
	prompt = ""
	controller.controllerSock.setblocking(1)
	controller.listenCommand()
	controller.controllerSock.setblocking(0)
	files = controller.inPayload[0].split(" ")
	print controller.FILEPROMPT
	index = 0
	for f in files:
    	prompt += "[" + str(index) + "]" + " " + f + "\n"
    	index += 1
	index = int(raw_input(prompt))
	controller.outPayload = controller.inPayload[index]
	controller.sendCommand("R", "STREAM FILE ")

	#populate list frame
	#wait for selection of file by user
	while controller.isConnected():
    	try:
        	controller.listenCommand()
    	except socket_error:
        	print("NO ACK")
        	continue #include try and catch in a loop
    	else:
        	if controller.code == "FNF" or controller.code == "ACK":
            	break
        	else:
            	continue
    	if controller.code == "FNF":
        	continue
    	controllerSock.setblocking(1)
    	while controller.code != "READY":
        	controller.listenCommand()

    	controller.sendCommand("S", "PLAY NULL ")
    	controllerSock.setblocking(0)
    	while controller.isConnected():

        	buttonPress = int(raw_input(controller.COMMANDPROMPT))

        	if buttonPress == 0:
            	controller.play()
        	elif buttonPress == 1:
            	controller.pause()
        	elif buttonPress == 2:
            	controller.restart()
        	elif buttonPress == 3:
            	controller.disconnect()
            	controller.disconnect = True
        	controller.listenCommand()
        	if(controller.type == "END"):
            	controller.disconnect = True
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
    	controller.sendCommand("S", "DISCONNECT NULL ")
    	controller.sendCommand("R", "DISCONNECT NULL ")
