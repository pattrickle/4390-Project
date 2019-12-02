#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Server Code

import socket
import sys
import os
#alt+r

class Server:
	#assign values
	LOCAL_IP = "10.0.0.1" #local
	R_IP = "10.0.0.2"
	C_IP = "10.0.0.3"

	C = (C_IP,5000) #tuple object
	R = (R_IP,5000)
	S = (LOCAL_IP,5000)

	serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, udp
    print("Server: Server socket created.")
	type = ""
	code = ""
	inPayload = ["",""]
	outPayload = ""
	selectFile = None
	switchVar = 4 #escape
	lineCount = 0
	totalLines = 0
	filePath = "desktop/projectfiles"
	disconnect = False

	def __init__(self):
    	self.serverSock.bind(self.S)


	def listenCommand(self, socket):
    	serverSock = socket
    	rawPacket = serverSock.recvfrom(64) #length of bytes, listen for amount of bytes
    	if rawPacket: #only parse once received
        	packet = rawPacket.split(" ",2) #differentiate between t
        	self.type = packet[0] #first is type
        	self.code = packet[1] #second is code
        	if self.type == "STREAM" and self.code == "NULL": #OPTIONAL
            	self.inPayload = packet[2].split(" ",1) #will be split if type and code are stream and null make sure to just split once
        	else:
            	self.inPayload[0] = packet[2]

	def sendCommand(self, HOST, STATUS): #work on
    	print("Send Command")
    	localPacket = STATUS + self.outPayload
    	if HOST == "R":
        	self.serverSock.sendto(localPacket,self.R) #host and port
    	if HOST == "C":
        	self.serverSock.sendto(localPacket,self.C)

	#switch statement
	def case0(self): #CONNECT
    	self.outPayload = ""
    	print("Case 0:CONNECT")
    	arr = os.listdir(self.filePath) #directory of files
    	print(arr) #temp check
    	for x in arr: #goes through file
        	if os.path.isFile(x):
            	self.outPayload += x + ' ' #names of files
    	self.switchVar = 4

	def case1(self): #STREAM
    	print("Case 1:STREAM")
    	arr = os.listdir(self.filePath) #directory of files
    	print(arr) #temp check
    	for x in arr: #goes through file, then opens
        	if os.path.isFile(x):
            	if path.exists(self.filePath + "/" + self.inPayload[0]): #adding to full file path
                	self.selectFile = open(self.filePath + "/" + self.inPayload[0],'r')
    	#opened file
    	if self.selectFile != None: #FIX
        	line = self.selectFile.readline() #first line
        	while line:
            	print(line) #dont have to, # TEMP
            	self.lineCount += 1 #increment total totalLines
            	line = self.selectFile.readline()

        	self.outPayload = self.lineCount
        	self.sendCommand("R", "STATUS READY ")
    	else:
        	self.sendCommand("R", "STATUS FNF ")
    	self.lineCount = 0
    	self.selectFile.seek(0) #restart file pointer
    	self.switchVar = 4

	def case2(self): #PLAY/NULL
    	print("Case 2:PLAY/NULL")
    	line = self.selectFile.readline()
    	if line:
        	self.outPayload = string(self.lineCount)
        	self.outPayload = self.outPayload + " "
        	self.outPayload = self.outPayload + line
        	self.sendCommand("R","STREAM NULL ")
        	self.lineCount += 1
        	time.sleep(.1) #delay of 1/10s
    	else:
        	self.sendCommand("R","STATUS END ")
        	self.switchVar = 4

	def case3(self): #PLAY/LINE
    	print("Case 3:PLAY/LINE")
    	self.selectFile.seek(0)
    	x = 0
    	while x < self.inPayload[0]:
        	line = self.selectFile.readline() #store current line indexed by # x
        	x += 1
    	self.lineCount = self.inPayload[0]
    	self.switchVar = 2


	def case4(self): #PAUSE, DEFAULT
    	print("Case 4:PAUSE")

	def case5(self): #DISCONNECT
    	print("Case 5: DISCONNECT")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.sendCommand("C","DISCONNECT ACK ")
    	self.disconnect = True


s = Server()
while True:
	#do stuff
	s.listenCommand(s.serverSock)

	if s.type == "CONNECT":
    	s.switchVar = 0
	if s.type == "STREAM":
    	s.switchVar = 1
	if s.type == "PLAY" and s.code == "NULL":
    	s.switchVar = 2
	if s.type == "PLAY" and s.code == "LINE":
    	s.switchVar = 3
	if s.type == "PAUSE":
    	s.switchVar = 4
	if s.type == "DISCONNECT":
    	s.switchVar = 5

	#switchThing(switchVar)
	if s.switchVar == 0:
        print("Server: CONNECT")
    	s.case0()
	elif s.switchVar == 1:
        print("Server: STREAM")
    	s.case1()
	elif s.switchVar == 2:
        print("Server: PLAY/NULL")
    	s.case2()
	elif s.switchVar == 3:
        print("Server:PLAY/LINE")
    	s.case3()
	elif s.switchVar == 4:
        print("Server: PAUSE")
    	s.case4()
	elif s.switchVar == 5:
        print("Server: DISCONNECT")
    	s.case5()

	if s.disconnect == True:
    	break
