import pygame
from pygame.locals import *

pygame.init()
BLACK = (0,0,0)
FONT = pygame.font.SysFont('consolas',25,True)
FONT1 = pygame.font.SysFont('consolas',20,True)

class Chat_panel:

	def __init__(self,screen,coords):

		self.screen = screen
		self.coords = coords
		self.selected = "friends"
		self.chat_img = pygame.transform.scale(pygame.image.load('Media/chat_icon.png'),(50,42))
		self.pwf_img = pygame.transform.scale(pygame.image.load('Media/pwf.png'),(50,42))
		self.spectator_img = pygame.transform.scale(pygame.image.load('Media/spectator.jpg'),(50,37))
		self.leaderboard_img = pygame.transform.scale(pygame.image.load('Media/leaderboard.png'),(150,67))
		self.log_img = pygame.transform.scale(pygame.image.load('Media/log.png'),(47,39))
		
		#get friends here
		self.Friends = [chr(i) for i in range(65,91)]
		self.friends_text = [FONT.render(i,True,(255,255,255)) for i in self.Friends]
		self.friends_text_rects = [i.get_rect() for i in self.friends_text]
		self.first = 0
		self.last = 8
		self.fspec = 0
		self.lspec = 8
		self.invite_buttons_pos = [385+i*50 for i in range(8)]
		self.invite_text = FONT1.render("Invite",True,(0,200,0))
		self.invitations_sent = [False for i in range(len(self.Friends))]
		self.sent_text = FONT1.render("Invitation Sent",True,(255,255,255))
		self.spectators = ["This","Is","The","List","Of","Spectators"]
		self.spectators_text = [FONT1.render(i,True,(255,255,255)) for i in self.spectators]
		self.spectators_text_rects = [i.get_rect() for i in self.spectators_text]
		self.get_lists_pos()

	def get_lists_pos(self):
		x,y= 1115,395
		for i in self.friends_text_rects[self.first:self.last]:
			i.center = (x+i.width/2,y)
			y+=50

		y = 395
		for i in self.spectators_text_rects[self.fspec:self.lspec]:
			i.center = (x+i.width/2,y)
			y+=50

	def mount(self,xstart,ystart):
		pos = pygame.mouse.get_pos()

		pygame.draw.rect(self.screen,BLACK,[xstart+165,ystart,83,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart+247,ystart,86,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart+332,ystart,87,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart,ystart,83,41],2)
		pygame.draw.rect(self.screen,BLACK,[xstart+82,ystart,84,41],2)

		if self.selected == "chat":
			#pygame.draw.line(self.screen,(255,255,255),(xstart+2,ystart+40),(xstart+81,ystart+40),2)
			pygame.draw.rect(self.screen,(23,28,38),[xstart+2,ystart+2,80,40])

		elif self.selected == "friends":
			#pygame.draw.line(self.screen,(255,255,255),(xstart+84,ystart+40),(xstart+164,ystart+40),2)
			pygame.draw.rect(self.screen,(23,28,38),[xstart+84,ystart+2,81,40])

		elif self.selected == "spectators":
			#pygame.draw.line(self.screen,(255,255,255),(xstart+167,ystart+40),(xstart+246,ystart+40),2)
			pygame.draw.rect(self.screen,(23,28,38),[xstart+167,ystart+2,80,40])

		elif self.selected == "leaderboard":
			#pygame.draw.line(self.screen,(255,255,255),(xstart+248,ystart+40),(xstart+331,ystart+40),2)
			pygame.draw.rect(self.screen,(23,28,38),[xstart+249,ystart+2,83,40])

		elif self.selected == "log":
			#pygame.draw.line(self.screen,(255,255,255),(xstart+333,ystart+40),(xstart+417,ystart+40),2)
			pygame.draw.rect(self.screen,(23,28,38),[xstart+334,ystart+2,84,40])

		self.screen.blit(self.chat_img,(xstart+20,ystart+1))
		self.screen.blit(self.pwf_img,(xstart+105,ystart))
		self.screen.blit(self.spectator_img,(xstart+183,ystart+2))
		self.screen.blit(self.leaderboard_img,(xstart+210,ystart-12))
		self.screen.blit(self.log_img,(xstart+355,ystart))
		
		if self.selected == "friends":
			for i in self.friends_text[self.first:self.last]:
				self.screen.blit(i,self.friends_text_rects[self.friends_text.index(i)])
		
			if pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=410 and pos[1]>=385:
				if self.invitations_sent[self.first]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,387,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=460 and pos[1]>=435:
				if self.invitations_sent[self.first+1]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,437,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=510 and pos[1]>=485:
				if self.invitations_sent[self.first+2]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,487,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=560 and pos[1]>=535:
				if self.invitations_sent[self.first+3]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,537,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=610 and pos[1]>=585:
				if self.invitations_sent[self.first+4]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,587,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=660 and pos[1]>=635:
				if self.invitations_sent[self.first+5]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,637,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=710 and pos[1]>=685:
				if self.invitations_sent[self.first+6]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,687,80,25])

			elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=760 and pos[1]>=735:
				if self.invitations_sent[self.first+7]==False:
					pygame.draw.rect(self.screen,(122,122,112),[1423,737,80,25])

			for i in self.invite_buttons_pos:
				if self.invitations_sent[self.first+self.invite_buttons_pos.index(i)]==False:
					pygame.draw.rect(self.screen,(255,255,255),[1421,i,80,25],2)
					self.screen.blit(self.invite_text,(1428,i+4))
				else:
					self.screen.blit(self.sent_text,(1350,i+3))

		elif self.selected == "spectators":
			for i in self.spectators_text[self.fspec:self.lspec]:
				self.screen.blit(i,self.spectators_text_rects[self.spectators_text.index(i)])

