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
			#Displays on who you are connected to
			print("Connected to "+recipantUser)
			clientSocket.send(username)
		except:
			print("Error in connecting")
		try:
			 #Checks for public key
			checkPuFile = open(os.path.dirname(__file__)+'/../keys/'+recipantUser+'pub.key','r')
		        publicKey = RSA.importKey(checkPuFile.read())
		        checkPuFile.close()
			print(recipantUser+"'s public key being used")
		except:
			print("Error in obtaining users public key")
	elif command[0] == 'disconnect':
		print("Disconnecting")
	else:
		"Error in selecting commands"

def keyCheck():
	#Try catch block to determine if the keys are there
	try:
		#Checks for private key
	        checkPrFile = open(os.path.dirname(__file__)+'/../keys/'+username+'.key','r')
        	privateKey = RSA.importKey(checkPrFile.read())
	        checkPrFile.close()
	
		#Checks for public key
	        checkPuFile = open(os.path.dirname(__file__)+'/../keys/'+username+'pub.key','r')
	        publicKey = RSA.importKey(checkPuFile.read())
	        checkPuFile.close()
		print("Keys loaded")
	except:
		print("Your keys were not found creating new ones....")
	        #Writing private key to file
		privateKeyFile = open(os.path.dirname(__file__)+"/../keys/"+username+".key",'w')
        	privateKeyFile.write(privateKey.exportKey())
	        privateKeyFile.close()

        	#Writing public key to file
	        publicKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'pub.key','w')
		publicKeyFile.write(publicKey.exportKey())
	        publicKeyFile.close()

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
			display.insert(END, username+":"+msg+"\n")
			cliMsg = clientSocket.recv(1024)
			print(cliMsg)
		except:
			display.insert(END, "Error in sending message\n")
			print("Error in sending message")


#Obtains the necessary info from config files
try:
        username = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',2)
        username = username.split('=',1)[1]
        username = username[:-1]
        print("Username is "+username)

except:
        print("Error in config file!")
        exit(1)

#-----------------------------
#Main running of the code
root = Tk()
root.title("Whisper")

keyCheck()

serverButton = Button(root, text="Send Message",command=sendMessage)
serverButton.grid(row=1, column=1)

input = Entry(root, width=60)
input.grid(row=1,column=0)

display = Text(root, width=60, height=40)
display.grid(row=0, column=0)

root.mainloop()

clientSocket.close()
