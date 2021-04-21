from socket import *
from threading import Thread
import sys
from pygame.locals import *
import pygame
import random

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (102, 204, 0)
LIGHTBLUE = (51, 153, 255)
COLOR1 = (48,128,42)
COLOR2 = (118,196,112)
LIGHTGREEN = (102,255,102)
LIGHTNAVY = (153,153,255)
RED = (255,0,0)
FONT = pygame.font.SysFont('freesansbold.ttf', 25) 

class Network:
	def __init__(self,server_ip,port_no):
		self.server = server_ip
		self.port = port_no
		self.username = "Hrishi"

	def connect_to_server(self):
		try:  
		    self.sock = socket(AF_INET,SOCK_STREAM)  
		    print ("Socket successfully created") 
		except error as err:  
		    print ("socket creation failed with error %s" %(err))
	
		self.sock.connect((self.server,self.port))
		self.sock.send(self.username.encode())
	
	def get_username_and_message(self,message):
	    username = ""
	    msg = ""
	    for i in message:
	        if i != ":":
	            username += i
	        else:
	        	break
	    msg = message[len(username)+1:]
	    return username,msg
	
	def receive_messages(self,msg_buffer,msg_graphical_buffer,last_msg,first_msg):
		while True:
			try:
				message = self.sock.recv(1024).decode()
				username,message = self.get_username_and_message(message)
				print(username,message,"message:",message)
				msg_buffer.append(message)
				username = FONT.render(username+":",True,random.choice([RED,GREEN,LIGHTBLUE,LIGHTNAVY]))
				uname_rect = username.get_rect()
				message = FONT.render(message,True,BLACK)
				message_rect = message.get_rect()
				msg_graphical_buffer.append(([username,uname_rect],[message,message_rect]))
				last_msg += 1
				if last_msg>=12:
					first_msg +=1
			except:
				print("Error receiving!!")
				self.sock.close()
				break
	
	def send_message(self,message):
		try:
			self.sock.send(message.encode())
		except:
			print("Error sending message!!")
			self.sock.close()


