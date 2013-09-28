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

import hashlib
import os.path

class KeyCheckSum(object):
	#Takes in the username and does a md5 checksum of the public key
	def Sum(self,username):
		md5sumValue=hashlib.md5(open(os.path.dirname(__file__)+"/../keys/"+username+"pub.key").read()).hexdigest()
		return md5sumValue

	#Gets the current md5sum
	def CurrentAuthorized(self,md5sum):
		exists = False
		try:
			authorizedFile = open(os.path.dirname(__file__)+"/../etc/authorized_keys",'r')
			for line in authorizedFile:
				line = line.split(':')
				sum = line[1]
				sum = sum[:-1]
				if sum==md5sum:
					exists = True
			
			authorizedFile.close()
			print("Authorized")
		except Exception as e:
			exists = False
			print("Unable to open file\n"+str(e))
		return exists
	#Writes the sum into the authorized file
	def WriteAuthorized(self,md5Sum,username):
		authorizedFile = open(os.path.dirname(__file__)+"/../etc/authorized_keys",'a')
		authorizedFile.write(username+":"+md5Sum+'\n')
		authorizedFile.close()
