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

from getpass import getpass
from Crypto.PublicKey import RSA
import os

class KeyManager:
	
	username = None
	privateKey = None
	unlocked = None

	def __init__(self,username):

		self.username = username
		print ("Keymanager loaded")

	def keyCreate(self):

		password = getpass("Enter password ")
		reEnteredPassword = getpass("Re-enter password ")

		if(password == reEnteredPassword):
			try:
				privateKey = RSA.generate(1024)
				publicKey = privateKey.publickey()

				#Checks for private key
				privateKeyFile = open(os.path.dirname(__file__)+'/../keys/'+self.username+'.key','w')
				privateKeyFile.write(privateKey.exportKey('PEM',password,pkcs=1))
				privateKeyFile.close()

				#Checks for public key
				publicKeyFile = open(os.path.dirname(__file__)+'/../keys/'+self.username+'pub.key','w')
				publicKeyFile.write(publicKey.exportKey())
				publicKeyFile.close()
				print("Keys create")
				
				#Reset the key values
				privateKey = None
				publicKey = None
			except Exception as e:
				print("Error in creating keys")
				print(e)
		else:
			print("Passwords do not match")
	
	#Attempts to unlock the keys
	def keyUnlock(self):
		try:
			global privateKey, unlocked
			password = getpass("Enter password: ")
			privateKeyFile = open(os.path.dirname(__file__)+'/../keys/'+self.username+'.key','r')
			privateKey = RSA.importKey(privateKeyFile.read(),password)
			privateKeyFile.close()
			self.unlocked = True
			return True
			print("Private key loaded")
		except Exception as e:
			print("Error in unlocking key")
			print(str(e))
			return False

	#Gets the privatekey
	def getPrivateKey(self):
		print("Private key recieved")
		return privateKey

	#Gets the public key
	def getPublicKey(self,username):
		publicKey = None

		#Attempts to obtain the public key for the user
		try:
			with open('../etc/users.cfg','r') as userList:
				for user in userList:
					if user.startswith(username):
						keyfilename = user.split(':')[2]
						publicKey = open('../keys/'+keyfilename,'r').read()
						return publicKey
		except Exception as e:
			print("Error in getting public key check for key or configuration")
			print(e)

		return None

	def isUnlocked():
		return self.unlocked
