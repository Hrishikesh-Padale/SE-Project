import pygame
import sys
from pygame.locals import *
from qplay import *
from pwfriend import *
from player_profile import *
from Settings import *


pygame.init()
FONT1 = pygame.font.SysFont('calibri',35,True)
FONT2 = pygame.font.SysFont('calibri',22,True)
FONT3 = pygame.font.SysFont('calibri',40,True)
FONT4 = pygame.font.SysFont('calibri',25,True)

class Button:
	def __init__(self,name,x,y):
		self.name = name
		self.xstart = x
		self.ystart = y
		self.color = (0,255,0)
		self.text = FONT1.render(self.name,True,self.color)
		self.rect = self.text.get_rect()
		self.rect.center = (x+100,y+50)
		self.xlim = (self.xstart+50,self.xstart+150)
		self.ylim = (self.ystart+25,self.ystart+75)

	def draw(self,screen,pos):
		if (pos[0]>=self.xlim[0] and pos[0]<=self.xlim[1]) and (pos[1]>=self.ylim[0] and pos[1]<= self.ylim[1]):
			pygame.draw.rect(screen,(186,103,35),[self.xstart+51,self.ystart+27,98,48],border_radius=10)
		screen.blit(self.text,self.rect)
		pygame.draw.rect(screen,(255,255,255),[self.xstart+50,self.ystart+25,100,50],2,10)

class Option:
	def __init__(self,name,x,y):
		self.name = name
		self.xstart = x
		self.ystart = y
		self.width = width*(19.53/100)
		self.height = height*(62.42/100)
		self.title = FONT1.render(self.name,True,(255,255,255))
		self.rect = self.title.get_rect()
		self.description = ""
		self.d_rect = None

	

class Main_menu:
	def __init__(self,screen,clock):
		self.screen = screen
		self.clock = clock
		self.background_color = (114,6,6)
		self.options_color = (140,44,44)
		self.icon_background_color = (82,0,2)
		#self.bg = pygame.image.load('Media/bg2.jpg')

		self.quickplay = Option("Quickplay",138,150.5)
		self.quickplay.rect.center = (self.quickplay.xstart+30+(self.quickplay.rect.width/2),self.quickplay.ystart+250)
		self.quickplay.description = [FONT2.render("Automatically match with",True,(255,255,255)),FONT2.render("a random player.",True,(255,255,255))]
		self.quickplay.d_rect = [self.quickplay.description[0].get_rect(),self.quickplay.description[1].get_rect()]
		self.quickplay.d_rect[0].center = (self.quickplay.xstart+30+(self.quickplay.d_rect[0].width/2),self.quickplay.ystart+300)
		self.quickplay.d_rect[1].center = (self.quickplay.xstart+30+(self.quickplay.d_rect[1].width/2),self.quickplay.ystart+325)

		self.play_with_friend = Option("Play With Friend",self.quickplay.xstart+320,150.5)
		self.play_with_friend.rect.center = (self.play_with_friend.xstart+30+(self.play_with_friend.rect.width/2),self.play_with_friend.ystart+250)
		self.play_with_friend.description = [FONT2.render("Invite a friend with",True,(255,255,255)),FONT2.render("game-id/username.",True,(255,255,255))]
		self.play_with_friend.d_rect = [self.play_with_friend.description[0].get_rect(),self.play_with_friend.description[1].get_rect()]
		self.play_with_friend.d_rect[0].center = (self.play_with_friend.xstart+30+(self.play_with_friend.d_rect[0].width/2),self.play_with_friend.ystart+300)
		self.play_with_friend.d_rect[1].center = (self.play_with_friend.xstart+30+(self.play_with_friend.d_rect[1].width/2),self.play_with_friend.ystart+325)

		self.profile = Option("Profile",self.play_with_friend.xstart+320,150.5)
		self.profile.rect.center = (self.profile.xstart+30+(self.profile.rect.width/2),self.profile.ystart+250)
		self.profile.description = [FONT2.render("Edit profile,See statistics,",True,(255,255,255)),FONT2.render("Manage friends.",True,(255,255,255))]
		self.profile.d_rect = [self.profile.description[0].get_rect(),self.profile.description[1].get_rect()]
		self.profile.d_rect[0].center = (self.profile.xstart+30+(self.profile.d_rect[0].width/2),self.profile.ystart+300)
		self.profile.d_rect[1].center = (self.profile.xstart+30+(self.profile.d_rect[1].width/2),self.profile.ystart+325)

		self.settings = Option("Settings",self.profile.xstart+320,150.5)
		self.settings.rect.center = (self.settings.xstart+30+(self.settings.rect.width/2),self.settings.ystart+250)
		self.settings.description = [FONT2.render("Board/Pieces appearance,",True,(255,255,255)),FONT2.render("Adjust volume,theme,",True,(255,255,255)),FONT2.render("Enable/Disable music.",True,(255,255,255))]
		self.settings.d_rect = [self.settings.description[0].get_rect(),self.settings.description[1].get_rect(),self.settings.description[2].get_rect()]
		self.settings.d_rect[0].center = (self.settings.xstart+30+(self.settings.d_rect[0].width/2),self.settings.ystart+300)
		self.settings.d_rect[1].center = (self.settings.xstart+30+(self.settings.d_rect[1].width/2),self.settings.ystart+325)
		self.settings.d_rect[2].center = (self.settings.xstart+30+(self.settings.d_rect[2].width/2),self.settings.ystart+350)

		self.quickplay_image = pygame.image.load('Media/quickplay.png')
		self.quickplay_image = pygame.transform.scale(self.quickplay_image,(250,250))
		self.play_with_friend_image = pygame.image.load('Media/play_with_friend.png')
		self.play_with_friend_image = pygame.transform.scale(self.play_with_friend_image,(160,160))
		self.profile_image = pygame.image.load('Media/profile.png')
		self.profile_image = pygame.transform.scale(self.profile_image,(120,140))
		self.settings_image = pygame.image.load('Media/settings.png')
		self.settings_image = pygame.transform.scale(self.settings_image,(130,130))

		#						Option         original position                         position after adjustment
		self.text_adjust = {'quickplay':[self.quickplay.rect.center,(self.quickplay.rect.center[0]-7.5,self.quickplay.rect.center[1])],
							
							'quickplay info':[self.quickplay.d_rect[0].center,(self.quickplay.d_rect[0].center[0]-7.5,self.quickplay.d_rect[0].center[1])
											 ,self.quickplay.d_rect[1].center,(self.quickplay.d_rect[1].center[0]-7.5,self.quickplay.d_rect[1].center[1])],

							'play with friend':[self.play_with_friend.rect.center,(self.play_with_friend.rect.center[0]+7.5,self.play_with_friend.rect.center[1])
											   ,(self.play_with_friend.rect.center[0]-7.5,self.play_with_friend.rect.center[1])],

							'play with friend info':[self.play_with_friend.d_rect[0].center,(self.play_with_friend.d_rect[0].center[0]+7.5,self.play_with_friend.d_rect[0].center[1])
													,self.play_with_friend.d_rect[1].center,(self.play_with_friend.d_rect[1].center[0]+7.5,self.play_with_friend.d_rect[1].center[1])
													,(self.play_with_friend.d_rect[0].center[0]-7.5,self.play_with_friend.d_rect[0].center[1])
													,(self.play_with_friend.d_rect[1].center[0]-7.5,self.play_with_friend.d_rect[1].center[1])],

							'profile':[self.profile.rect.center,(self.profile.rect.center[0]+7.5,self.profile.rect.center[1])
									  ,(self.profile.rect.center[0]-7.5,self.profile.rect.center[1])],

							'profile info':[self.profile.d_rect[0].center,(self.profile.d_rect[0].center[0]+7.5,self.profile.d_rect[0].center[1])
										   ,self.profile.d_rect[1].center,(self.profile.d_rect[1].center[0]+7.5,self.profile.d_rect[1].center[1])
										   ,(self.profile.d_rect[0].center[0]-7.5,self.profile.d_rect[0].center[1])
										   ,(self.profile.d_rect[1].center[0]-7.5,self.profile.d_rect[1].center[1])],

							'settings':[self.settings.rect.center,(self.settings.rect.center[0]+7.5,self.settings.rect.center[1])],

							'settings info':[self.settings.d_rect[0].center,(self.settings.d_rect[0].center[0]+7.5,self.settings.d_rect[0].center[1])
											,self.settings.d_rect[1].center,(self.settings.d_rect[1].center[0]+7.5,self.settings.d_rect[1].center[1])
											,self.settings.d_rect[2].center,(self.settings.d_rect[2].center[0]+7.5,self.settings.d_rect[2].center[1])]
							}

		self.quit_button = Button('Quit',1350,0)


		self.qp_object = Quickplay(self.screen,self.clock)
		self.pwf_object = PlayWithFriend(self.screen,self.clock)
		self.prof_object = Profile(self.screen,self.clock)
		self.settings_object = Settings(self.screen,self.clock)

	def update(self):
		while True:
			pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if (pos[0]>=self.quit_button.xlim[0] and pos[0]<=self.quit_button.xlim[1]) and (pos[1]>=self.quit_button.ylim[0] and pos[1]<= self.quit_button.ylim[1]):
							return
						elif pos[0]>=138 and pos[0]<=438 and pos[1]>=150.5 and pos[1]<=650.5:
							self.qp_object.update()
						elif pos[0]>=478 and pos[0]<=758 and pos[1]>=150.5 and pos[1]<=650.5:
							self.pwf_object.update()
						elif pos[0]>=778 and pos[0]<=1078 and pos[1]>=150.5 and pos[1]<=650.5:
							self.prof_object.update()
						elif pos[0]>=1098 and pos[0]<=1398 and pos[1]>=150.5 and pos[1]<=650.5:
							self.settings_object.update()

			self.screen.fill(self.background_color)
			#self.screen.blit(self.bg,(0,0))

			#mouse pointer on quickplay
			if pos[0]>=138 and pos[0]<=438 and pos[1]>=150.5 and pos[1]<=650.5:
				pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart-12.5,self.quickplay.ystart-40,self.quickplay.width+25,self.quickplay.height+80],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart+7.5,self.play_with_friend.ystart,self.play_with_friend.width,self.play_with_friend.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart+7.5,self.profile.ystart,self.profile.width,self.profile.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart+7.5,self.settings.ystart,self.settings.width,self.settings.height],border_radius=20)
				
				pygame.draw.rect(self.screen,self.icon_background_color,[self.quickplay.xstart+7.5,self.quickplay.ystart-20,self.quickplay.width-15,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.play_with_friend.xstart+27.5,self.play_with_friend.ystart+20,self.play_with_friend.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.profile.xstart+27.5,self.profile.ystart+20,self.profile.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.settings.xstart+27.5,self.settings.ystart+20,self.settings.width-40,200],border_radius=20)
				
				self.screen.blit(self.quickplay_image,(self.quickplay.xstart+25,self.quickplay.ystart-40))
				self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+82.5,self.play_with_friend.ystart+40))
				self.screen.blit(self.profile_image,(self.profile.xstart+92.5,self.profile.ystart+50))
				self.screen.blit(self.settings_image,(self.settings.xstart+92.5,self.settings.ystart+55))

				self.quickplay.title = FONT3.render(self.quickplay.name,True,(255,255,255))
				self.quickplay.rect = self.quickplay.title.get_rect()
				self.quickplay.rect.center = (self.quickplay.xstart+20+(self.quickplay.rect.width/2),self.quickplay.ystart+250)
				self.quickplay.description = [FONT4.render("Automatically match with",True,(255,255,255)),FONT4.render("a random player.",True,(255,255,255))]
				self.quickplay.d_rect = [self.quickplay.description[0].get_rect(),self.quickplay.description[1].get_rect()]
				self.quickplay.d_rect[0].center = (self.quickplay.xstart+20+(self.quickplay.d_rect[0].width/2),self.quickplay.ystart+300)
				self.quickplay.d_rect[1].center = (self.quickplay.xstart+20+(self.quickplay.d_rect[1].width/2),self.quickplay.ystart+325)

				self.play_with_friend.rect.center = self.text_adjust['play with friend'][1]
				self.play_with_friend.d_rect[0].center = self.text_adjust['play with friend info'][1]
				self.play_with_friend.d_rect[1].center = self.text_adjust['play with friend info'][3]
				
				self.profile.rect.center = self.text_adjust['profile'][1]
				self.profile.d_rect[0].center = self.text_adjust['profile info'][1]
				self.profile.d_rect[1].center = self.text_adjust['profile info'][3]

				self.settings.rect.center = self.text_adjust['settings'][1]
				self.settings.d_rect[0].center = self.text_adjust['settings info'][1]
				self.settings.d_rect[1].center = self.text_adjust['settings info'][3]
				self.settings.d_rect[2].center = self.text_adjust['settings info'][5]

			
			#mouse pointer on play_with_friend
			elif pos[0]>=478 and pos[0]<=758 and pos[1]>=150.5 and pos[1]<=650.5:
				pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart-7.5,self.quickplay.ystart,self.quickplay.width,self.quickplay.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart-12.5,self.play_with_friend.ystart-40,self.play_with_friend.width+25,self.play_with_friend.height+80],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart+7.5,self.profile.ystart,self.profile.width,self.profile.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart+7.5,self.settings.ystart,self.settings.width,self.settings.height],border_radius=20)					
				
				pygame.draw.rect(self.screen,self.icon_background_color,[self.quickplay.xstart+12.5,self.quickplay.ystart+20,self.quickplay.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.play_with_friend.xstart+7.5,self.play_with_friend.ystart-20,self.play_with_friend.width-15,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.profile.xstart+27.5,self.profile.ystart+20,self.profile.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.settings.xstart+27.5,self.settings.ystart+20,self.settings.width-40,200],border_radius=20)
				
				self.screen.blit(self.quickplay_image,(self.quickplay.xstart+17.5,self.quickplay.ystart))
				self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+75,self.play_with_friend.ystart))
				self.screen.blit(self.profile_image,(self.profile.xstart+92.5,self.profile.ystart+50))
				self.screen.blit(self.settings_image,(self.settings.xstart+92.5,self.settings.ystart+55))

				self.play_with_friend.title = FONT3.render(self.play_with_friend.name,True,(255,255,255))
				self.play_with_friend.rect = self.play_with_friend.title.get_rect()
				self.play_with_friend.rect.center = (self.play_with_friend.xstart+20+(self.play_with_friend.rect.width/2),self.play_with_friend.ystart+250)
				self.play_with_friend.description = [FONT4.render("Invite a friend with",True,(255,255,255)),FONT4.render("game-id/username.",True,(255,255,255))]
				self.play_with_friend.d_rect = [self.play_with_friend.description[0].get_rect(),self.play_with_friend.description[1].get_rect()]
				self.play_with_friend.d_rect[0].center = (self.play_with_friend.xstart+20+(self.play_with_friend.d_rect[0].width/2),self.play_with_friend.ystart+300)
				self.play_with_friend.d_rect[1].center = (self.play_with_friend.xstart+20+(self.play_with_friend.d_rect[1].width/2),self.play_with_friend.ystart+325)

				self.quickplay.rect.center = self.text_adjust['quickplay'][1]
				self.quickplay.d_rect[0].center = self.text_adjust['quickplay info'][1]
				self.quickplay.d_rect[1].center = self.text_adjust['quickplay info'][3]

				self.profile.rect.center = self.text_adjust['profile'][1]
				self.profile.d_rect[0].center = self.text_adjust['profile info'][1]
				self.profile.d_rect[1].center = self.text_adjust['profile info'][3]

				self.settings.rect.center = self.text_adjust['settings'][1]
				self.settings.d_rect[0].center = self.text_adjust['settings info'][1]
				self.settings.d_rect[1].center = self.text_adjust['settings info'][3]
				self.settings.d_rect[2].center = self.text_adjust['settings info'][5]

			#mouse pointer on profile
			elif pos[0]>=778 and pos[0]<=1078 and pos[1]>=150.5 and pos[1]<=650.5:
				pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart-7.5,self.quickplay.ystart,self.quickplay.width,self.quickplay.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart-7.5,self.play_with_friend.ystart,self.play_with_friend.width,self.play_with_friend.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart-12.5,self.profile.ystart-40,self.profile.width+25,self.profile.height+80],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart+7.5,self.settings.ystart,self.settings.width,self.settings.height],border_radius=20)

				pygame.draw.rect(self.screen,self.icon_background_color,[self.quickplay.xstart+12.5,self.quickplay.ystart+20,self.quickplay.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.play_with_friend.xstart+12.5,self.play_with_friend.ystart+20,self.play_with_friend.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.profile.xstart+7.5,self.profile.ystart-20,self.profile.width-15,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.settings.xstart+27.5,self.settings.ystart+20,self.settings.width-40,200],border_radius=20)

				self.screen.blit(self.quickplay_image,(self.quickplay.xstart+17.5,self.quickplay.ystart))
				self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+67.5,self.play_with_friend.ystart+40))
				self.screen.blit(self.profile_image,(self.profile.xstart+90,self.profile.ystart+10))
				self.screen.blit(self.settings_image,(self.settings.xstart+92.5,self.settings.ystart+55))

				self.profile.title = FONT3.render(self.profile.name,True,(255,255,255))
				self.profile.rect = self.profile.title.get_rect()
				self.profile.rect.center = (self.profile.xstart+20+(self.profile.rect.width/2),self.profile.ystart+250)
				self.profile.description = [FONT4.render("Edit profile,See statistics,",True,(255,255,255)),FONT4.render("Manage friends.",True,(255,255,255))]
				self.profile.d_rect = [self.profile.description[0].get_rect(),self.profile.description[1].get_rect()]
				self.profile.d_rect[0].center = (self.profile.xstart+20+(self.profile.d_rect[0].width/2),self.profile.ystart+300)
				self.profile.d_rect[1].center = (self.profile.xstart+20+(self.profile.d_rect[1].width/2),self.profile.ystart+325)

				self.quickplay.rect.center = self.text_adjust['quickplay'][1]
				self.quickplay.d_rect[0].center = self.text_adjust['quickplay info'][1]
				self.quickplay.d_rect[1].center = self.text_adjust['quickplay info'][3]

				self.play_with_friend.rect.center = self.text_adjust['play with friend'][2]
				self.play_with_friend.d_rect[0].center = self.text_adjust['play with friend info'][4]
				self.play_with_friend.d_rect[1].center = self.text_adjust['play with friend info'][5]

				self.settings.rect.center = self.text_adjust['settings'][1]
				self.settings.d_rect[0].center = self.text_adjust['settings info'][1]
				self.settings.d_rect[1].center = self.text_adjust['settings info'][3]
				self.settings.d_rect[2].center = self.text_adjust['settings info'][5]

			#mouse pointer on settings
			elif pos[0]>=1098 and pos[0]<=1398 and pos[1]>=150.5 and pos[1]<=650.5:
				pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart-7.5,self.quickplay.ystart,self.quickplay.width,self.quickplay.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart-7.5,self.play_with_friend.ystart,self.play_with_friend.width,self.play_with_friend.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart-7.5,self.profile.ystart,self.profile.width,self.profile.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart-12.5,self.settings.ystart-40,self.settings.width+25,self.settings.height+80],border_radius=20)

				pygame.draw.rect(self.screen,self.icon_background_color,[self.quickplay.xstart+12.5,self.quickplay.ystart+20,self.quickplay.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.play_with_friend.xstart+12.5,self.play_with_friend.ystart+20,self.play_with_friend.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.profile.xstart+12.5,self.profile.ystart+20,self.profile.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.settings.xstart+7.5,self.settings.ystart-20,self.settings.width-15,200],border_radius=20)

				self.screen.blit(self.quickplay_image,(self.quickplay.xstart+17.5,self.quickplay.ystart))
				self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+67.5,self.play_with_friend.ystart+40))
				self.screen.blit(self.profile_image,(self.profile.xstart+78.5,self.profile.ystart+50))
				self.screen.blit(self.settings_image,(self.settings.xstart+85,self.settings.ystart+15))

				self.settings.title = FONT3.render(self.settings.name,True,(255,255,255))
				self.settings.rect = self.settings.title.get_rect()
				self.settings.rect.center = (self.settings.xstart+20+(self.settings.rect.width/2),self.settings.ystart+250)
				self.settings.description = [FONT4.render("Board/Pieces appearance,",True,(255,255,255)),FONT4.render("Adjust volume,theme,",True,(255,255,255)),FONT4.render("Enable/Disable music.",True,(255,255,255))]
				self.settings.d_rect = [self.settings.description[0].get_rect(),self.settings.description[1].get_rect(),self.settings.description[2].get_rect()]
				self.settings.d_rect[0].center = (self.settings.xstart+20+(self.settings.d_rect[0].width/2),self.settings.ystart+300)
				self.settings.d_rect[1].center = (self.settings.xstart+20+(self.settings.d_rect[1].width/2),self.settings.ystart+325)
				self.settings.d_rect[2].center = (self.settings.xstart+20+(self.settings.d_rect[2].width/2),self.settings.ystart+350)

				self.quickplay.rect.center = self.text_adjust['quickplay'][1]
				self.quickplay.d_rect[0].center = self.text_adjust['quickplay info'][1]
				self.quickplay.d_rect[1].center = self.text_adjust['quickplay info'][3]

				self.play_with_friend.rect.center = self.text_adjust['play with friend'][2]
				self.play_with_friend.d_rect[0].center = self.text_adjust['play with friend info'][4]
				self.play_with_friend.d_rect[1].center = self.text_adjust['play with friend info'][5]

				self.profile.rect.center = self.text_adjust['profile'][2]
				self.profile.d_rect[0].center = self.text_adjust['profile info'][4]
				self.profile.d_rect[1].center = self.text_adjust['profile info'][5]

			else:
				pygame.draw.rect(self.screen,self.options_color,[self.quickplay.xstart,self.quickplay.ystart,self.quickplay.width,self.quickplay.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.play_with_friend.xstart,self.play_with_friend.ystart,self.play_with_friend.width,self.play_with_friend.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.profile.xstart,self.profile.ystart,self.profile.width,self.profile.height],border_radius=20)
				pygame.draw.rect(self.screen,self.options_color,[self.settings.xstart,self.settings.ystart,self.settings.width,self.settings.height],border_radius=20)					
				
				pygame.draw.rect(self.screen,self.icon_background_color,[self.quickplay.xstart+20,self.quickplay.ystart+20,self.quickplay.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.play_with_friend.xstart+20,self.play_with_friend.ystart+20,self.play_with_friend.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.profile.xstart+20,self.profile.ystart+20,self.profile.width-40,200],border_radius=20)
				pygame.draw.rect(self.screen,self.icon_background_color,[self.settings.xstart+20,self.settings.ystart+20,self.settings.width-40,200],border_radius=20)
				
				self.screen.blit(self.quickplay_image,(self.quickplay.xstart+25,self.quickplay.ystart))
				self.screen.blit(self.play_with_friend_image,(self.play_with_friend.xstart+75,self.play_with_friend.ystart+40))
				self.screen.blit(self.profile_image,(self.profile.xstart+85,self.profile.ystart+50))
				self.screen.blit(self.settings_image,(self.settings.xstart+85,self.settings.ystart+55))

				self.quickplay.title = FONT1.render(self.quickplay.name,True,(255,255,255))
				self.quickplay.rect = self.quickplay.title.get_rect()
				self.quickplay.description = [FONT2.render("Automatically match with",True,(255,255,255)),FONT2.render("a random player.",True,(255,255,255))]
				self.quickplay.d_rect = [self.quickplay.description[0].get_rect(),self.quickplay.description[1].get_rect()]
				
				self.play_with_friend.title = FONT1.render(self.play_with_friend.name,True,(255,255,255))
				self.play_with_friend.rect = self.play_with_friend.title.get_rect()
				self.play_with_friend.description = [FONT2.render("Invite a friend with",True,(255,255,255)),FONT2.render("game-id/username.",True,(255,255,255))]
				self.play_with_friend.d_rect = [self.play_with_friend.description[0].get_rect(),self.play_with_friend.description[1].get_rect()]
				
				self.profile.title = FONT1.render(self.profile.name,True,(255,255,255))
				self.profile.rect = self.profile.title.get_rect()
				self.profile.description = [FONT2.render("Edit profile,See statistics,",True,(255,255,255)),FONT2.render("Manage friends.",True,(255,255,255))]
				self.profile.d_rect = [self.profile.description[0].get_rect(),self.profile.description[1].get_rect()]

				self.settings.title = FONT1.render(self.settings.name,True,(255,255,255))
				self.settings.rect = self.settings.title.get_rect()
				self.settings.description = [FONT2.render("Board/Pieces appearance,",True,(255,255,255)),FONT2.render("Adjust volume,theme,",True,(255,255,255)),FONT2.render("Enable/Disable music.",True,(255,255,255))]
				self.settings.d_rect = [self.settings.description[0].get_rect(),self.settings.description[1].get_rect(),self.settings.description[2].get_rect()]

				self.quickplay.rect.center = self.text_adjust['quickplay'][0]
				self.quickplay.d_rect[0].center = self.text_adjust['quickplay info'][0]
				self.quickplay.d_rect[1].center = self.text_adjust['quickplay info'][2]

				self.play_with_friend.rect.center = self.text_adjust['play with friend'][0]
				self.play_with_friend.d_rect[0].center = self.text_adjust['play with friend info'][0]
				self.play_with_friend.d_rect[1].center = self.text_adjust['play with friend info'][2]

				self.profile.rect.center = self.text_adjust['profile'][0]
				self.profile.d_rect[0].center = self.text_adjust['profile info'][0]
				self.profile.d_rect[1].center = self.text_adjust['profile info'][2]

				self.settings.rect.center = self.text_adjust['settings'][0]
				self.settings.d_rect[0].center = self.text_adjust['settings info'][0]
				self.settings.d_rect[1].center = self.text_adjust['settings info'][2]
				self.settings.d_rect[2].center = self.text_adjust['settings info'][4]


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
			self.screen.blit(self.settings.description[0],self.settings.d_rect[0])
			self.screen.blit(self.settings.description[1],self.settings.d_rect[1])
			self.screen.blit(self.settings.description[2],self.settings.d_rect[2])
			
			self.quit_button.draw(self.screen,pygame.mouse.get_pos())
			pygame.display.flip()
			self.clock.tick(60)


width,height = 1536,801
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
Main_menu = Main_menu(screen,clock)
Main_menu.update()
pygame.quit()