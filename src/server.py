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
import netifaces
import linecache
import os
import os.path

#Server class
class Server():

	serverSocket = None
	host = None

	def startServer(self):
		serverPort = None
		interface = None

		#Obtains the necessary info from config files
		try:
		        serverPort = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg', 3)
			serverPort = serverPort.split('=',1)[1]
			serverPort = serverPort[:-1]

			interface = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg',4)
			interface = interface.split('=',1)[1]
			interface = interface[:-1]
        
		except Exception as e:
		        print("Error in config file!"+str(e))

		#Creates the sockets and waits for connections to show up
		print(interface)
		self.host = netifaces.ifaddresses(interface)[2][0]['addr']

		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSocket.bind((self.host, int(serverPort)))
		
		print("Listening on port "+serverPort) 

	def stopServer(self):
		print("Socket closed")
		self.serverSocket.close()
