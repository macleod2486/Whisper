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

#Obtaining the key
privateKey = RSA.generate(1024)
publicKey = privateKey.publickey()
username = "default"

recipantUser = " "
#Obtains the necessary info from config files
try:
	username = linecache.getline(os.path.dirname(__file__)+'/etc/whisper.cfg',2)
	username = username.split('=',1)[1]
	username = username[:-1]
	print("Username is "+username)

except:
	print("Error in config file!")
	exit(1)

#Try catch block to determine if the keys are there
try:
	#Checks for private key
        checkPrFile = open(os.path.dirname(__file__)+'/keys/'+username+'.key','r')
        privateKey = RSA.importKey(checkPrFile.read())
        checkPrFile.close()
	
	#Checks for public key
        checkPuFile = open(os.path.dirname(__file__)+'/keys/'+username+'pub.key','r')
        publicKey = RSA.importKey(checkPuFile.read())
        checkPuFile.close()
except:
        #Writing private key to file
	privateKeyFile = open(os.path.dirname(__file__)+"/../keys/"+username+".key",'w')
        privateKeyFile.write(privateKey.exportKey())
        privateKeyFile.close()

        #Writing public key to file
        publicKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'pub.key','w')
	publicKeyFile.write(publicKey.exportKey())
        publicKeyFile.close()

#Creates the socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 3333
clientSocket.connect((host, int(port)))


#Proceeds to then send and recieve messages from the server
clientSocket.send(username)
while True:
	msg = raw_input(":")
	msg=publicKey.encrypt(msg,2)
	clientSocket.send(msg[0])
	cliMsg = clientSocket.recv(1024)
	print(cliMsg)
clientSocket.close()
