import pygame
from pygame.locals import *
pygame.init()
FONT1 = pygame.font.SysFont('arial.ttf',40,True)
FONT2 = pygame.font.SysFont('arial.ttf',30)

class Option:
	def __init__(self,name,x,y):
		self.name = name
		self.xstart = x
		self.ystart = y
		self.width = 300
		self.height = 500
		self.title = FONT1.render(self.name,True,(255,255,255))
		self.rect = self.title.get_rect()
		self.description = ""
		self.d_rect = None

class Main_menu:
	def __init__(self,screen):
		self.screen = screen
		self.background_color = (114,6,6)
		self.options_color = (140,44,44)

		self.quickplay = Option("Quickplay",138,150.5)
		self.quickplay.title = FONT1.render(self.quickplay.name,True,(255,255,255))
		self.quickplay.rect = self.quickplay.title.get_rect()
		self.quickplay.rect.center = (self.quickplay.xstart+10+(self.quickplay.rect.width/2),self.quickplay.ystart+250)
		self.quickplay.description = [FONT2.render("Automatically match with",True,(255,255,255)),FONT2.render("a random player.",True,(255,255,255))]
		self.quickplay.d_rect = [self.quickplay.description[0].get_rect(),self.quickplay.description[1].get_rect()]
		self.quickplay.d_rect[0].center = (self.quickplay.xstart+10+(self.quickplay.d_rect[0].width/2),self.quickplay.ystart+300)
		self.quickplay.d_rect[1].center = (self.quickplay.xstart+10+(self.quickplay.d_rect[1].width/2),self.quickplay.ystart+325)

		self.play_with_friend = Option("Play With Friend",self.quickplay.xstart+320,150.5)
		self.play_with_friend.title = FONT1.render(self.play_with_friend.name,True,(255,255,255))
		self.play_with_friend.rect = self.play_with_friend.title.get_rect()
		self.play_with_friend.rect.center = (self.play_with_friend.xstart+10+(self.play_with_friend.rect.width/2),self.play_with_friend.ystart+250)
		self.play_with_friend.description = [FONT2.render("Invite a friend with game-id/",True,(255,255,255)),FONT2.render("username.",True,(255,255,255))]
		self.play_with_friend.d_rect = [self.play_with_friend.description[0].get_rect(),self.play_with_friend.description[1].get_rect()]
		self.play_with_friend.d_rect[0].center = (self.play_with_friend.xstart+10+(self.play_with_friend.d_rect[0].width/2),self.play_with_friend.ystart+300)
		self.play_with_friend.d_rect[1].center = (self.play_with_friend.xstart+10+(self.play_with_friend.d_rect[1].width/2),self.play_with_friend.ystart+325)

		self.profile = Option("Profile",self.play_with_friend.xstart+320,150.5)
		self.profile.title = FONT1.render(self.profile.name,True,(255,255,255))
		self.profile.rect = self.profile.title.get_rect()
		self.profile.rect.center = (self.profile.xstart+10+(self.profile.rect.width/2),self.profile.ystart+250)
		self.profile.description = [FONT2.render("Edit profile,see statistics,",True,(255,255,255)),FONT2.render("manage friends.",True,(255,255,255))]
		self.profile.d_rect = [self.profile.description[0].get_rect(),self.profile.description[1].get_rect()]
		self.profile.d_rect[0].center = (self.profile.xstart+10+(self.profile.d_rect[0].width/2),self.profile.ystart+300)
		self.profile.d_rect[1].center = (self.profile.xstart+10+(self.profile.d_rect[1].width/2),self.profile.ystart+325)

		self.settings = Option("Settings",self.profile.xstart+320,150.5)
		self.settings.title = FONT1.render(self.settings.name,True,(255,255,255))
		self.settings.rect = self.settings.title.get_rect()
		self.settings.rect.center = (self.settings.xstart+10+(self.settings.rect.width/2),self.settings.ystart+250)
		#self.settings.description = [FONT2.render("Adjust volume,theme,enable/disable music.")]


		self.quickplay_image = pygame.image.load('Media/quickplay.png')
		self.quickplay_image = pygame.transform.scale(self.quickplay_image,(250,250))
		self.play_with_friend_image = pygame.image.load('Media/play_with_friend.png')
		self.play_with_friend_image = pygame.transform.scale(self.play_with_friend_image,(160,160))
		self.profile_image = pygame.image.load('Media/profile.png')
		self.profile_image = pygame.transform.scale(self.profile_image,(120,140))
		self.settings_image = pygame.image.load('Media/settings.png')
		self.settings_image = pygame.transform.scale(self.settings_image,(130,130))


	def update(self,clock):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print(pygame.mouse.get_pos())
					return
			self.screen.fill(self.background_color)
			pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart,self.quickplay.ystart,self.quickplay.width,self.quickplay.height],border_radius=20)
			pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart,self.play_with_friend.ystart,self.play_with_friend.width,self.play_with_friend.height],border_radius=20)
			pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart,self.profile.ystart,self.profile.width,self.profile.height],border_radius=20)
			pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart,self.settings.ystart,self.settings.width,self.settings.height],border_radius=20)			
			pygame.draw.rect(self.screen,(82,0,2),[self.quickplay.xstart+20,self.quickplay.ystart+20,self.quickplay.width-40,200],border_radius=20)
			pygame.draw.rect(self.screen,(82,0,2),[self.play_with_friend.xstart+20,self.play_with_friend.ystart+20,self.play_with_friend.width-40,200],border_radius=20)
			pygame.draw.rect(self.screen,(82,0,2),[self.profile.xstart+20,self.profile.ystart+20,self.profile.width-40,200],border_radius=20)
			pygame.draw.rect(self.screen,(82,0,2),[self.settings.xstart+20,self.settings.ystart+20,self.settings.width-40,200],border_radius=20)

			self.screen.blit(self.quickplay_image,(self.quickplay.xstart+25,self.quickplay.ystart))
			self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+75,self.play_with_friend.ystart+40))
			self.screen.blit(self.profile_image,(self.profile.xstart+85,self.profile.ystart+50))
			self.screen.blit(self.settings_image,(self.settings.xstart+85,self.settings.ystart+55))

			self.screen.blit(self.quickplay.title,self.quickplay.rect)
			self.screen.blit(self.play_with_friend.title,self.play_with_friend.rect)
			self.screen.blit(self.profile.title,self.profile.rect)
			self.screen.blit(self.settings.title,self.settings.rect)

			self.screen.blit(self.quickplay.description[0],self.quickplay.d_rect[0])
			self.screen.blit(self.quickplay.description[1],self.quickplay.d_rect[1])
			self.screen.blit(self.play_with_friend.description[0],self.play_with_friend.d_rect[0])
			self.screen.blit(self.play_with_friend.description[1],self.play_with_friend.d_rect[1])
			self.screen.blit(self.profile.description[0],self.profile.d_rect[0])
			self.screen.blit(self.profile.description[1],self.profile.d_rect[1])

			pygame.display.flip()
			clock.tick(60)

width,height = 1536,801
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
Main_menu = Main_menu(screen)
Main_menu.update(clock)