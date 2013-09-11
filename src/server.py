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
from Crypto.PublicKey import RSA

privateKey = None
username = "default"
port = 12345
#Obtains the necessary info from config files
try:
        username = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',2)
        username = username.split('=',1)[1]
	username = username[:-1]
        port = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg', 3)
	port = port.split('=',1)[1]
	print("Username is "+username)
	print("Listening on port "+port)	
	
except:
        print("Error in config file!")
        exit(1)

#Creates the sockets and waits for connections to show up
serverSocket = socket.socket()
host = socket.gethostname()
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((host,int(port)))
serverSocket.listen(5)
c,addr = serverSocket.accept()
print("Server started")

print("Got connection from ",addr)

#Sends and recieves messages from the client
c.send(username)
senderUsername=c.recv(1024)
while True:
	clientMess=c.recv(1024)	
	if not clientMess:
		break
	else:
		try:
			global privateKey
			filepath = os.path.dirname(__file__)+"/../keys/"+username+".key"
			print(filepath)
			privateKeyFile = open(filepath,"r")
			privateKey = RSA.importKey(privateKeyFile.read())
			clientMess=privateKey.decrypt(clientMess)
			print(senderUsername+":"+clientMess)

		except Exception as e:
        		print("Error in obtaining key"+str(e))
			break
serverSocket.close()
