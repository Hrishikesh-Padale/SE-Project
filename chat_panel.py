import pygame
from pygame.locals import *

pygame.init()
BLACK = (0,0,0)

class Chat_panel:

	def __init__(self,screen,coords):

		self.screen = screen
		self.coords = coords
		self.selected = "chat"
		self.chat_img = pygame.transform.scale(pygame.image.load('Media/chat_icon.png'),(50,42))
		self.pwf_img = pygame.transform.scale(pygame.image.load('Media/pwf.png'),(50,42))
		self.spectator_img = pygame.transform.scale(pygame.image.load('Media/spectator.png'),(50,42))
		self.leaderboard_img = pygame.transform.scale(pygame.image.load('Media/leaderboard.png'),(150,67))
		self.log_img = pygame.transform.scale(pygame.image.load('Media/log.png'),(47,39))

	def mount(self,xstart,ystart):

		self.screen.blit(self.chat_img,(xstart+20,ystart+1))
		self.screen.blit(self.pwf_img,(xstart+105,ystart))
		self.screen.blit(self.spectator_img,(xstart+183,ystart))
		self.screen.blit(self.leaderboard_img,(xstart+210,ystart-12))
		self.screen.blit(self.log_img,(xstart+355,ystart))

		if self.selected != "chat":
			pygame.draw.rect(self.screen,BLACK,[xstart,ystart,83,41],2)

		if self.selected != "online friends":
			pygame.draw.rect(self.screen,BLACK,[xstart+83,ystart,83,41],2)
		

		pygame.draw.rect(self.screen,BLACK,[xstart+165,ystart,83,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart+247,ystart,86,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart+332,ystart,87,41],2)

