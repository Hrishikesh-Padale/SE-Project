import pygame
from pygame.locals import *

pygame.init()
BLACK = (0,0,0)

class Chat_panel:

	def __init__(self,screen,coords):

		self.screen = screen
		self.coords = coords
		self.selected = "chat"

	def mount(self):
		if self.selected != "chat":
			pygame.draw.rect(self.screen,BLACK,[1085,365,89,41],2)

		if self.selected != "online friends":
			pygame.draw.rect(self.screen,BLACK,[1173,365,89,41],2)
		

		pygame.draw.rect(self.screen,BLACK,[1261,365,89,41],2)
		pygame.draw.rect(self.screen,BLACK,[1349,365,86,41],2)
		pygame.draw.rect(self.screen,BLACK,[1434,365,86,41],2)

		self.screen.blit(pygame.transform.scale(pygame.image.load('Media/chat_icon.png'),(50,42)),(1105,365))
		self.screen.blit(pygame.transform.scale(pygame.image.load('Media/pwf.png'),(50,42)),(1193,365))

		#if self.selected == "chat":
		#	pygame.draw.rect(self.screen,(255,255,255),[1087,367,86,40])
		#elif self.selected == "online_friends":
		#	pygame.draw.rect(self.screen,(255,255,255),[1175,367,86,40])