import pygame
import sys
from pygame.locals import *
import pickle
from threading import Timer

pygame.init()
FONT1 = pygame.font.SysFont('calibri',40,True)

class Quickplay:

	def __init__(self,screen,clock,client):

		self.client = client
		self.screen = screen
		self.clock = clock
		self.profile_picture = pygame.transform.scale(pygame.image.load('Media/prof.png'),(240,240))
		self.current_time = pygame.time.get_ticks()
		self.count = 0
		self.loading_text = FONT1.render("MATCHING",True,(255,255,255))
		self.dots = [FONT1.render(".",True,(255,255,255)),FONT1.render("..",True,(255,255,255)),FONT1.render("...",True,(255,255,255))]
		self.notification = None
		self.opponent = None
		self.myname = FONT1.render(self.client.uID,True,(255,255,255))
		self.player1 = FONT1.render("Player 1",True,(255,255,255))
		self.timed_out = False

	def count_down(self):
		message = {'ID':59,'UserID':self.client.uID}
		try:
			if not self.client.room_id:
				self.client.sock.send(pickle.dumps(message))
		except:
			pass
		self.timed_out = True
		self.timer.join()
		print("Auto matching timed out ... Looks like nobody is online ... Try again")

	def loading(self):
		#return pygame.time.get_ticks()-self.current_time
		if pygame.time.get_ticks()-self.current_time >= 500:
			self.current_time = pygame.time.get_ticks()
			self.count += 1
			if self.count <= 3:
				return self.count
			self.count = 0			
			return 0
		return 0

	def get_quickplay_section_messages(self):
		if self.client.quickplay_section_messages:
			self.notification = self.client.quickplay_section_messages.pop()
			if self.notification['ID'] == 56:
				self.opponent = self.notification['FriendID']
				print("opponent found:",self.opponent)
				message = {'ID':58,'UserID':self.client.uID,'FriendID':self.opponent}
				self.client.sock.send(pickle.dumps(message))
				print("58 message sent")

			if self.notification['ID'] == 2200:
				self.client.main_page_messages = []
				self.client.pwf_section_messages = []
				self.client.room_id = self.notification['RoomID']
				self.client.color = self.notification['Turn']


	def update(self):
		self.timer = Timer(20.0,self.count_down)
		self.timer.start()
		while True:
			self.get_quickplay_section_messages()
			self.screen.fill((114,6,6))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

			pygame.draw.rect(self.screen,(140,44,44),[440,100,300,500],border_radius=20)
			pygame.draw.rect(self.screen,(82,0,2),[460,120,260,220],border_radius=20)
			pygame.draw.rect(self.screen,(140,44,44),[796,100,300,500],border_radius=20)
			pygame.draw.rect(self.screen,(82,0,2),[816,120,260,220],border_radius=20)

			pygame.draw.line(self.screen,(0,150,0),(768,70),(768,630),2)

			self.screen.blit(self.player1,(520,360))
			self.screen.blit(self.myname,(500,430))
			self.screen.blit(self.profile_picture,(468,110))
			self.screen.blit(self.profile_picture,(824,110))
			self.screen.blit(self.loading_text,(650,680))
			self.loading()
			if self.count == 1:
				self.screen.blit(self.dots[0],(840,680))
			elif self.count == 2:
				self.screen.blit(self.dots[1],(840,680))
			elif self.count == 3:
				self.screen.blit(self.dots[2],(840,680))

			if self.client.room_id:
				return

			if self.timed_out:
				self.timed_out = False
				return 

			pygame.display.flip()
			self.clock.tick(60)

#width,height = 1536,801
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode((width,height))
#pygame.display.set_caption("Quickplay")
#quickplay = Quickplay(screen,clock)
#quickplay.update()
#pygame.quit()
