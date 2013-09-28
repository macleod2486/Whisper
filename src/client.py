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

import socket
import os.path
import os
import linecache
from Tkinter import *
import threading
from Crypto.PublicKey import RSA
import Crypto.PublicKey.RSA

#Obtaining the key
privateKey = None
publicKey = None
username = "default"
recipantUser = " "
connected = False
unlocked = False

#Creates the socket
clientSocket = None
serverSocket = None
host = socket.gethostname()
port = 3333
servMd5 = None

#Function that will take in commands 
def Commands (arguments):
	global unlocked

	command = arguments.split(' ')

	#Displays help menu when prompted
	if command[0]=="help":
		print("\nCommands available\n/connect ip/hostname portNo\n/disconnect\n/clear")
		display.config(state="normal")
		display.insert(END,"\nCommands available\n/connect ip/hostname portNo\n/disconnect\n/clear\n/quit\n/keygen password password\n/unlock password\n")
		display.config(state="disabled")

	#Attempts to connect to the server and obtain the username for their public key to be used
	elif (command[0]=="connect") and unlocked:
		try:
			global recipantUser, clientSocket, servMd5
			host = command[1]
			port = command[2]
			clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		
			clientSocket.connect((host,int(port)))
			recipantUser=clientSocket.recv(1024)
			
			
			#Displays on who you are connected to
			display.config(state="normal")
			display.insert(END,"Connected to "+recipantUser+"\n")
			display.config(state="disabled")

			#Sends the server your username
			clientSocket.send(username)

			#Recieves the checksum of the public key the server has
			servMd5=clientSocket.recv(1024)
			
			#Checks to see if the key is currently stored		
			md5=KeyCheckSum()
			if md5.CurrentAuthorized(servMd5):
				display.config(state="normal")
				display.insert(END,"Host valid\n")
				display.config(state="disabled")
			else:
				confim = AuthorizedHosts(root)
				root.wait_window(confirm.top)

			connected = True
		except IndexError:
			display.config(state="normal")
			display.config(END,"Error: format for command is\n/connect hostname/ip port\n")
			display.config(state="disabled")
		except Exception as e:
			display.config(state="normal")
			display.insert(END,"Error in connecting\n")
			display.config(state="disabled")
			print("Error in connecting")
			connected = 0
			print(e)
		#Then checks to see if the users public key exists
                try:
	                #Checks for public key
                        global publicKey
                        checkPuFile = open(os.path.dirname(__file__)+'/../keys/'+recipantUser+'pub.key','r')
                        publicKey = RSA.importKey(checkPuFile.read())
                        checkPuFile.close()
			display.config(state="normal")
			display.insert(END,'\n'+recipantUser+"'s public key being used\n")
			display.config(state="disabled")
                except Exception as e:
                        print("Error in obtaining users public key")
			display.insert(END,"Error in obtaining"+recipantUser+"'s public key\n")
                        print(e)

	#Will disconnect from server when prompted		
	elif command[0] == 'disconnect':
		try:
			clientSocket.shutdown(2)
			clientSocket.close()
			print("Disconnected")
			display.config(state="normal")
			display.insert(END,"Disconnected\n")
			display.config(state="disabled")
		except:
			print("No connection")
			display.config(state="normal")
			display.insert(END,"No connection")
			display.config(state="disabled")
	#Generates the keys with the password specified
	elif command[0] == 'keygen':
		try:
			if command[1] == command[2]:
				keyCreate(command[1])
			else:
				display.config(state="normal")
				display.insert(END,"Error: passwords do not match\n")
				display.config(state="disabled")
		except IndexError:
			display.config(state="normal")
			display.insert(END,"Error: Missing password or blank password\nFormat: /keygen <password> <password>\n")
			display.config(state="disabled")
	#Unlock keys
	elif command[0] == 'unlock':
		keyUnlock(command[1])

	#Clears the text displayed in the chat window
	elif command[0] == 'clear':
		display.config(state="normal")
		display.delete('1.0',END)
		display.config(state="disabled")
	else:
		display.config(state="normal")
		display.insert(END,"Error "+command[0]+" either does not exist or you need to unlock your private key\n")
		display.config(state="disabled")

#Checks and/or creates keys
def keyCreate(password):
	global privateKey
	try:
		privateKey = RSA.generate(1024)
		publicKey = privateKey.publickey()
		#Checks for private key
	        privateKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'.key','w')
		privateKeyFile.write(privateKey.exportKey('PEM',password,pkcs=1))
	        privateKeyFile.close()

		#Checks for public key
	        publicKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'pub.key','w')
		publicKeyFile.write(publicKey.exportKey())
	        publicKeyFile.close()
		print("Keys create")
		display.config(state="normal")
		display.insert(END,"Keys created\n")
		display.config(state="disabled")
	except Exception as e:
		print("Error creating keys")
		print(e)

#Attempts to unlock the keys
def keyUnlock(password):
		try:
			global privateKey, unlocked
			privateKeyFile = open(os.path.dirname(__file__)+'/../keys/'+username+'.key','r')
			privateKey = RSA.importKey(privateKeyFile.read(),password)
			privateKeyFile.close()
			display.config(state="normal")
			display.insert(END,"Keys unlocked\n")
			display.config(state="disabled")
			unlocked = True
		except Exception as e:
			print(str(e))
			display.config(state="normal")
			display.insert(END,"Error in unlocking key\nBad passphrase or file does not exist\nError"+str(e)+'\n')
			display.config(state="disabled")

class AuthorizedHosts:
	def __init__(self,parent):
		top = self.top = Toplevel(parent)
		Label(top, text="Willing to add host to authorized file?").pack()
		yesButton = Button(top, text="Yes", command = self.yes)
		yesButton.pack()
		noButton = Button(top, text="No", command = self.no)
		noButton.pack()
	def yes(self):
		print("Yes selected!")
		md5 = KeyCheckSum()
		md5.WriteAuthorized(servMd5, username)
		self.top.destroy()
	def no(self):
		print("No selected!")
		clientSocket.shutdown(1)
		self.top.destroy()


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
		global serverSocket
		serverSocket = socket.socket()
		serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serverSocket.bind((host,int(port)))

		display.config(state="normal")
		display.insert(END,"Server started\n")
		display.config(state="disabled")
		
		serverSocket.listen(1)
		c,addr = serverSocket.accept()
		
		print("Server started")
		print("Got connection from ",addr)
		
		#Sends and recieves messages from the client
		c.send(username)
		senderUsername=c.recv(1024)
		
		#Gets and sends the md5sum of the public file
		md5 = KeyCheckSum()
		md5Pub=md5.Sum(recipantUser)
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
					display.config(state="normal")
					display.insert(END,senderUsername+":"+clientMess+'\n')
					display.config(state="disabled")
		                except Exception as e:
		                        display.config(state="normal")
					display.insert(END,"Error: Either your private key is not unlocked or socket busy\n")
					display.config(state="disabled")
		                        break
		serverSocket.close()
		print ("Server closed")

#Server function
def singleServer():
	server = Server()
	server.start()

#Stops both the server and client
def stopServer():
	try:
		serverSocket.shutdown(2)
		serverSocket.close()
		print("Server stopped")
	except:
		print("Server already stopped")
def stopClient():
	try:
		clientSocket.shutdown(2)
                clientSocket.close()
                print("Disconnected")
        except:
                print("No connection")
                
#Takes in user commands and messages
def sendMessage():
	
	msg = input.get()
	cliMsg = msg
	input.delete(0,END)
	
	if len(cliMsg) != 0:
	
		#Quits the system and exits
		if msg=="/quit":
			Commands("disconnect")
			stopServer()
			exit(1)
		#If a command is issued then it will shoot it to the command method
		elif msg[0]=='/':
			Commands(msg[1:])
		#Attempts to send the message to the server
		else:
			try:
				global clientSocket
				msg=publicKey.encrypt(msg,2)
				clientSocket.send(msg[0])
				display.config(state="normal")
				display.insert(END, username+":"+cliMsg+"\n")
				display.config(state="disabled")
				print(cliMsg)
			except Exception as e:
				display.config(state="normal")
				display.insert(END, "Error in sending message\n")
				display.config(state="disabled")
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
display.configure(state="disabled")
display.grid(row=0, column=0)

startServer = Button(root, text = "Start Server", command=singleServer)
startServer.grid(row=1, column=2)

root.mainloop()

#Cleans up connections when GUI is closed
stopClient()
stopServer()
