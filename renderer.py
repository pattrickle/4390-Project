#4390 Semester Project
#Patrick Le, Trevor, Duncan, Logan Dennison
#Renderer Code

import socket
import sys
import os

class Renderer:
	C_IP = "10.0.0.3"
	LOCAL_IP = "10.0.0.2"
	S_IP = "10.0.0.1"

	C = (C_IP,5000) #tuple object
	R = (LOCAL_IP,5000)
	S = (S_IP,5000)

	rendererSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #internet, udp

	outPayload = ""
	inPayload = []
	type = ""
	code = ""
	switchVar = -1
	lineCount = 0
	totalLines = 0
	disconnect = False

	def __init__(self):
    	self.rendererSock.bind(self.R)

	def listenCommand(self):
    	rawPacket = self.rendererSock.recv(64) #length of bytes, listen for amount of bytes
    	if rawPacket: #only parse once received
        	self.packet = rawPacket.split(" ",2) #differentiate between t
        	self.type = self.packet[0] #first is type
        	self.code = self.packet[1] #second is code
        	if self.type == "STREAM" and self.code == "NULL": #OPTIONAL
            	self.inPayload = self.packet[2].split(" ",1) #will be split if type and code are stream and null make sure to just split once
        	else:
            	self.inPayload[0] = self.packet[2]

	def sendCommand(self, HOST, STATUS):
    	print("Send Command")
    	self.localPacket = STATUS + self.outPayload
    	if HOST == "S":
        	self.rendererSock.sendto(self.localPacket,self.S) #host and port
    	if HOST == "C":
        	self.rendererSock.sendto(self.localPacket,self.C)

	def case0(self):
    	self.outPayload = self.inPayload[0]
    	self.sendCommand(S, "STREAM FILE ")
    	self.outPayload = ""
    	self.sendCommand(C, "STREAM ACK ")
    	self.switchVar = -1

	def case1(self):
    	self.totalLines = int(self.inPayload[0])
    	self.outPayload = ""
    	self.sendCommand(self.C, "STATUS READY ")
    	self.switchVar = -1

	def case2(self):
    	self.outPayload = ""
    	self.sendCommand(self.C, "STATUS FNF ")
    	self.switchVar = -1

	def case3(self):
    	tempLine = int(self.inPayload[0])
    	line = self.inPayload[1]
    	if tempLine != self.currentLine :
        	self.outPayload = str(self.currentLine)
        	self.sendCommand(self.S, "PLAY LINE ")
    	else:
        	if line != "":
            	print(line)
        	else:
            	print("No Text Found")
        	self.currentLine += 1
    	self.switchVar = -1

	def case4(self):
    	print("case 4")

	def case5(self):
    	if self.currentLine == self.totalLines :
        	self.outPayload = ""
        	self.sendCommand(self.C, "STATUS END ")
    	else :
        	self.outPayload = str(self.currentLine)
        	self.sendCommand(self.S, "PLAY LINE ")
    	self.switchVar = -1

	def case6(self):
    	self.outPayload = ""
    	self.sendCommand(self.C, "DISCONNECT ACK ")
    	self.disconnect = True


	#create Frame
renderer = Renderer()

while not renderer.disconnect:
	renderer.listenCommand()
	if renderer.type == "STREAM":
    	if renderer.code == "FILE":
        	renderer.switchVar = 0
    	else:
        	renderer.switchVar = 3
	if renderer.type == "STATUS":
    	if renderer.code == "READY":
        	renderer.switchVar = 1
    	if renderer.code == "FNF":
        	renderer.switchVar = 2
    	if renderer.code == "END":
        	renderer.switchVar = 5
	if renderer.type == "PLAY":
    	renderer.switchVar = 4
	if renderer.type == "DISCONNECT":
    	renderer.switchVar = 6

	if renderer.switchVar == 0:
    	renderer.case0()
	elif renderer.switchVar == 1:
    	renderer.case1()
	elif renderer.switchVar == 2:
    	renderer.case2()
	elif renderer.switchVar == 3:
    	renderer.case3()
	elif renderer.switchVar == 4:
    	renderer.case4()
	elif renderer.switchVar == 5:
    	renderer.case5()
	elif renderer.switchVar == 6:
    	renderer.case6()
