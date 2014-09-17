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

#Server class
class Server(threading.Thread):
	def run(self):
		serverPort = None
		#Obtains the necessary info from config files
		try:
		        serverPort = linecache.getline(os.path.dirname(__file__)+'/../etc/whisper.cfg', 3)
			serverPort.split('=',1)[1]
		        print("Listening on port "+serverPort)        
        
		except Exception as e:
		        print("Error in config file!"+str(e))

		#Creates the sockets and waits for connections to show up
		global serverSocket, serverStarted
		serverSocket = socket.socket()
		serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serverSocket.bind((host,int(port)))

		serverStarted = True	
		serverSocket.listen(1)
		c,addr = serverSocket.accept()
		
		print("Server started")
		print("Got connection from ",addr)
		
		#Sends and recieves messages from the client
		c.send(username)
		senderUsername=c.recv(1024)
		
		#Gets and sends the md5sum of the public file
		md5 = KeyCheckSum()
		md5Pub = md5.Sum(recipantUser)
		c.send(md5Pub)
		while True:
	        	clientMess=c.recv(1024) 
		        if not clientMess:
        		        print(str(clientMess))
				break
		        else:
	        	        try:
					global privateKey
		                        clientMess=privateKey.decrypt(clientMess)
		                        print(senderUsername+":"+clientMess)
		                except Exception as e:
		                        break
		serverSocket.close()
		serverStarted = False
		print ("Server closed")


