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

from checksum import KeyCheckSum
from Crypto.PublicKey import RSA
from getpass import getpass
from keys import KeyManager
from server import Server

import platform
import socket
import os.path
import os
import linecache
import netifaces
import threading
import Crypto.PublicKey.RSA

serverInstance = None

#Obtaining the key
keymanage = None
privateKey = None
publicKey = None
username = "default"
recipantUser = " "

#Used to monitor statuses
connected = False
unlocked = False
serverStarted = False

#Socket information
clientSocket = None
serverSocket = None
interface = None
host = None
clienthost = None
port = 3333
servMd5 = None

#Function that will take in commands 
def Commands (arguments):

	global unlocked

	command = arguments.split(' ')

	#Displays help menu when prompted
	if command[0] == "help":
		print("\nCommands available\nconnect ip hostname portNo\ndisconnect\nkeygen password password\nunlock password\nclear\nstartserver\nstopserver")

	#Generates the keys with the password specified
	elif command[0] == 'keygen':
		try:
			keymanage.keyCreate()
		except IndexError:
			print("Error in creating keys")

	#Unlock keys
	elif command[0] == 'unlock':
		unlocked = keymanage.keyUnlock()
		if unlocked:
			privateKey = keymanage.getKey()

	elif command[0] == 'clear':
		if platform.system() == 'Linux':
			os.system('clear')

		elif platform.system() == 'OSX':
			os.system('clear')

		elif platform.system() == 'Windows':
			os.system('cls')

	elif command[0] == 'startserver':
		startServer()

	elif command[0] == 'stopserver':
		stopServer()

	else:
		print("Command not found")
		print("\nCommands available\nconnect ip hostname portNo\ndisconnect\nkeygen password password\nunlock password\nclear\nstartserver\nstopserver")

#Server function
def startServer():
	serverInstance.startServer()
	print("Server started")

#Stops both the server and client
def stopServer():
	serverInstance.stopServer()

#Takes in user commands and messages
def sendMessage():
	print("Message sent")

#--------------------------------------------------------------------------

#Main running of the code


#Obtains the necessary info from config files
try:
        username = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',2)
        username = username.split('=',1)[1]
        username = username[:-1]

        print("Username is "+username)

	interface = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',4)
	interface = interface.split('=',1)[1]
	interface = interface[:-1]

	print("Interface "+interface)

	host = netifaces.ifaddresses(interface)[2][0]['addr']

	print(host)

	keymanage = KeyManager(username)

	print("\nFinished loading information from config file")
except Exception as e:
        print("Error in config file!")
	print(e)
        exit(1)

print ("\n******************************")
print ("Welcome to the Whisper program")
print ("Type in help for the help menu")

serverInstance = Server()

while(1):
	command = raw_input("> ")
	if command == "exit":
		break
	else:
		Commands(command)

print ("*******************************\n")

#Cleans up connections 
stopServer()
