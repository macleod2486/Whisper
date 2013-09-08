#!/usr/bin/env python2

#    This file is part of the Whisper project
#    Copyright (C) 2013  Manuel Gonzales Jr.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket
import os.path
import linecache
from Tkinter import *
from Crypto.PublicKey import RSA

#Obtaining the key
privateKey = RSA.generate(1024)
publicKey = privateKey.publickey()
username = "default"

recipantUser = " "
#Creates the socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 3333


#Function that will take in commands 
def Commands (arguments):
	command = arguments.split(' ')
	if command[0]=="help":
		print("Help list")
	elif command[0]=="connect":
		try:
			host = command[1]
			port = command[2]
			clientSocket.connect((host,int(port)))
			recipantUser=clientSocket.recv(1024)
			#recipantUser = recipantUser[:-1]
			
			#Displays on who you are connected to
			print("Connected to "+recipantUser)
			clientSocket.send(username)
		except Exception as e:
			print("Error in connecting")
			print(e)
		try:
			 #Checks for public key
			checkPuFile = open(os.path.dirname(__file__)+'/../keys/'+recipantUser+'pub.key','r')
		        publicKey = RSA.importKey(checkPuFile.read())
		        checkPuFile.close()
			print(recipantUser+"'s public key being used")
		except Exception as e:
			print("Error in obtaining users public key")
			print(e)
	elif command[0] == 'disconnect':
		print("Disconnecting")
	else:
		display.insert(END,"Error in selecting commands\n")

#Checks and/or creates keys
def keyCreate():

	try:
		#Checks for private key
	        privateKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'.key','w')
		privateKeyFile.write(privateKey.exportKey())
	        privateKeyFile.close()

		#Checks for public key
	        publicKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'pub.key','w')
		publicKeyFile.write(publicKey.exportKey())
	        publicKeyFile.close()
		print("Keys create")
	except Exception as e:
		print("Error creating keys")
		print(e)

#Server function
def server():
	#Obtains the necessary info from config files
	try:
        	username = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',2)
	        username = username.split('=',1)[1]
		username = username[:-1]
	        port = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg', 3)
		port = port.split('=',1)[1]
		print("Username is "+username)
	
	except:
        	print("Error in config file!")
	        exit(1)

	#Creates the sockets and waits for connections to show up
	serverSocket = socket.socket()
	host = socket.gethostbyname(socket.gethostname())
	serverSocket.bind((host,int(port)))

	print("Listening on "+host+"Port "+port)

	serverSocket.listen(5)
	c,addr = serverSocket.accept()

	#Once the socket is created it will notifify you
	print("Server started")
	print("Got connection from ",addr)

	#Sends and recieves messages from the client
	c.send(username)
	senderUsername=c.recv(1024)

	#Then continues to recieve messages and decrypt them with your private key
	while True:
		clientMess=c.recv(1024)	
		try:
			filepath = "../keys/"+username+".key"
			print(filepath)
			privateKeyFile = open(filepath,"r")
			privateKey = RSA.importKey(privateKeyFile.read())
			clientMess=privateKey.decrypt(clientMess)
	       		print(senderUsername+":"+clientMess)
			c.send(str(clientMess))

		except:
        		print("Error in obtaining key")
			break
		serverSocket.close()

#Takes in user commands and messages
def sendMessage():
	msg = input.get()
	input.delete(0,END)
	if msg=="/quit":
		exit(1)
	elif msg[0]=='/':
		Commands(msg[1:])
	else:
		try:
			msg=publicKey.encrypt(msg,2)
			clientSocket.send(msg[0])
			display.insert(END, username+":"+msg[0]+"\n")
			cliMsg = clientSocket.recv(1024)
			display.insert(END, username+":"+cliMsg+"\n")
			print(cliMsg)
		except Exception as e:
			display.insert(END, "Error in sending message\n")
			display.insert(END, e+"\n")
			print("Error in sending message")


#Obtains the necessary info from config files
try:
        username = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',2)
        username = username.split('=',1)[1]
        username = username[:-1]
        print("Username is "+username)

except Exception as e:
        print("Error in config file!")
	print(e)
        exit(1)

#--------------------------------------------------------------------------
#Main running of the code
root = Tk()
root.title("Whisper")

sendButton = Button(root, text="Send Message",command=sendMessage)
sendButton.grid(row=1, column=1)

input = Entry(root, width=60)
input.grid(row=1,column=0)

display = Text(root, width=60, height=40)
display.grid(row=0, column=0)

generateKeys = Button(root, text="Generate keys", command=keyCreate)
generateKeys.grid(row=2, column=1)

startServer = Button(root, text = "Start Server", command=server)
startServer.grid(row=2, column=2)

stopServer = Button(root, text="Stop Server", command=server)
stopServer.grid(row=1, column=2)

root.mainloop()

clientSocket.close()
