import pygame
from pygame.locals import *
import random

pygame.init()

FONT1 = pygame.font.SysFont('calibri',25,True)
FONT2 = pygame.font.SysFont('calibri',30,True)

width,height = 1536,801
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))

class Profile:

	def __init__(self,screen,clock):
		self.profile_picture = pygame.transform.scale(pygame.image.load('Media/prof.png'),(280,280))
		self.screen = screen
		self.clock = clock
		self.get_fields()
		self.get_friends()

	def get_friends(self):
		self.Friends_list = [chr(character) for character in range(65,91)]
		#print(self.Friends_list)
		self.Friends_texts = [FONT1.render(i,True,(random.randrange(1,256),random.randrange(1,256),random.randrange(1,256))) for i in self.Friends_list]
		#self.Friends_texts = [FONT1.render(i,True,(255,255,255)) for i in self.Friends_list]
		self.Friends_texts_rects = [i.get_rect() for i in self.Friends_texts]
		self.first_friend_index = 0
		self.last_friend_index = 12
		self.get_centers()

	def get_centers(self):
		x,y = 1140,180
		for i in self.Friends_texts_rects[self.first_friend_index:self.last_friend_index]:
			i.center = (x+i.width/2,y)
			y += 50

	def get_fields(self):

		self.data = {"username":"Hrishikesh#12345",
					 "email":"padalehrishi07@gmail.com",
					 "gameid":"OCS#987432",
					 "total_hours_played":20,
					 "points":24150}

		self.username = "Username                {}".format(self.data["username"])
		self.email = "Email                        {}".format(self.data["email"])
		self.gameid = "Game ID                  {}".format(self.data["gameid"])
		self.total_hours_played = "Hours played          {}".format(self.data["total_hours_played"])
		self.points = "Points                      {}".format(self.data["points"])
		self.edit = "Edit"
		self.friends = "Friends"

		self.username = FONT1.render(self.username,True,(255,255,255))
		self.username_rect = self.username.get_rect()
		self.username_rect.center = (415+(self.username_rect.width/2),(120+self.username_rect.height/2))

		self.email = FONT1.render(self.email,True,(255,255,255))
		self.email_rect = self.email.get_rect()
		self.email_rect.center = (415+(self.email_rect.width/2),(35+self.username_rect.center[1]+self.email_rect.height/2))

		self.gameid = FONT1.render(self.gameid,True,(255,255,255))
		self.gameid_rect = self.gameid.get_rect()
		self.gameid_rect.center = (415+(self.gameid_rect.width/2),(35+self.email_rect.center[1]+self.gameid_rect.height/2))

		self.total_hours_played = FONT1.render(self.total_hours_played,True,(255,255,255))
		self.total_hours_played_rect = self.total_hours_played.get_rect()
		self.total_hours_played_rect.center = (415+(self.total_hours_played_rect.width/2),
										  (35+self.gameid_rect.center[1]+self.total_hours_played_rect.height/2))

		self.points = FONT1.render(self.points,True,(255,255,255))
		self.points_rect = self.points.get_rect()
		self.points_rect.center = (415+(self.points_rect.width/2),(35+self.total_hours_played_rect.center[1]+self.points_rect.height/2))

		self.edit = FONT1.render(self.edit,True,(0,0,0))
		self.edit_rect = self.edit.get_rect()
		self.edit_rect.center = (1025-self.edit_rect.width/2,335-self.edit_rect.height/2)

		self.friends = FONT2.render(self.friends,True,(0,255,0))
		self.friends_rect = self.friends.get_rect()
		self.friends_rect.center = (1287.5,100+self.friends_rect.height)


		self.fields = {}
		self.fields[self.username] = self.username_rect
		self.fields[self.email] = self.email_rect
		self.fields[self.gameid] = self.gameid_rect
		self.fields[self.total_hours_played] = self.total_hours_played_rect
		self.fields[self.points] = self.points_rect
		self.fields[self.edit] = self.edit_rect
		self.fields[self.friends] = self.friends_rect

		self.edit_hover = (209,209,209)
		

	def update(self):
		while True:
			self.screen.fill((4,76,84))
			pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 4:
						#print("Scroll Up")
						if pos[0]<1450 and pos[0]>1125 and pos[1]<750 and pos[1] >153:
							if self.first_friend_index > 0:
								self.first_friend_index -= 1
								self.last_friend_index -= 1
								self.get_centers()

					if event.button == 5:
						#print("Scroll Down")
						if pos[0]<1450 and pos[0]>1125 and pos[1]<750 and pos[1] >153:
							if self.last_friend_index < len(self.Friends_list):
								self.first_friend_index += 1
								self.last_friend_index += 1
								self.get_centers()

			self.screen.blit(self.profile_picture,(55,85))

			#profile picture border
			pygame.draw.rect(self.screen,(0,0,0),[70,100,250,250],3)
			#Info border
			pygame.draw.rect(self.screen,(0,0,0),[395,100,655,250],3)

			#edit button
			if pos[0]<=1040 and pos[0]>=970 and pos[1]<=340 and pos[1]>=300:
				pygame.draw.rect(self.screen,self.edit_hover,[970,300,70,40])
			else:
				pygame.draw.rect(self.screen,(0,255,0),[970,300,70,40])

			for field in self.fields:
				self.screen.blit(field,self.fields[field])

			for friend in self.Friends_texts[self.first_friend_index:self.last_friend_index]:
				self.screen.blit(friend,self.Friends_texts_rects[self.Friends_texts.index(friend)])

			#graph
			pygame.draw.rect(self.screen,(255,255,255),[70,400,980,350])
			#friends box border
			pygame.draw.rect(self.screen,(0,0,0),[1125,100,325,650],3)
			#pygame.draw.rect(self.screen,(255,255,255),[1128,103,319,50])
			pygame.draw.line(self.screen,(0,0,0),(1125,153),(1450,153),3)

			pygame.display.flip()
			clock.tick(60)


profile = Profile(screen,clock)
profile.update()
pygame.quit()