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
#from Crypto.PublicKey import RSA
import Crypto.PublicKey.RSA

#Obtaining the key
privateKey = None
publicKey = None
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
			global recipantUser
			host = command[1]
			port = command[2]
			clientSocket.connect((host,int(port)))
			recipantUser=clientSocket.recv(1024)
			
			#Displays on who you are connected to
			print("Connected to "+recipantUser)
			display.insert(END,recipantUser+"\n")
			clientSocket.send(username)
		except Exception as e:
			print("Error in connecting")
			print(e)
		#Then checks to see if the users public key exists
                try:
                #Checks for public key
                        global publicKey
                        checkPuFile = open(os.path.dirname(__file__)+'/../keys/'+recipantUser+'pub.key','r')
                        publicKey = Crypto.PublicKey.RSA.importKey(checkPuFile.read())
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
	privateKey = RSA.generate(1024)
	publicKey = privateKey.publicKey()

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
	print("Server started")
#Takes in user commands and messages
def sendMessage():
	
	msg = input.get()
	cliMsg = msg
	input.delete(0,END)
	if msg=="/quit":
		exit(1)
	elif msg[0]=='/':
		Commands(msg[1:])
	else:
		try:
			msg=publicKey.encrypt(msg,2)
			clientSocket.send(msg[0])
	#		cliMsg = clientSocket.recv(1024)
			display.insert(END, username+":"+cliMsg+"\n")
			print(cliMsg)
		except Exception as e:
			#display.insert(END, "Error in sending message\n")
			display.insert(END, str(e)+"\n")
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
