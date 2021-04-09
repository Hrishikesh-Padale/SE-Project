import pygame
from pygame.locals import *

pygame.init()

FONT = pygame.font.SysFont('calibri',25,True)

width,height = 1536,801
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))

class Profile:

	def __init__(self,screen,clock):
		self.profile_picture = pygame.transform.scale(pygame.image.load('Media/prof.png'),(280,280))
		self.screen = screen
		self.clock = clock
		#self.get_fields()

	def get_fields(self):

		self.data = {"username":"Hrishikesh#12345",
					 "email":"padalehrishi07@gmail.com",
					 "gameid":"OCS#987432",
					 "total_hours_played":20,
					 "points":25000}

		self.username = "Username                {}".format(self.data["username"])
		self.email = "Email                        {}".format(self.data["email"])
		self.gameid = "Game ID                  {}".format(self.data["gameid"])
		self.total_hours_played = "Hours played           {}".format(self.data["total_hours_played"])
		self.points = "Points                       {}".format(self.data["points"])
		self.edit = "Edit"

		self.username = FONT.render(self.username,True,(255,255,255))
		self.username_rect = self.username.get_rect()
		self.username_rect.center = (500+(self.username_rect.width/2),(120+self.username_rect.height/2))

		self.email = FONT.render(self.email,True,(255,255,255))
		self.email_rect = self.email.get_rect()
		self.email_rect.center = (500+(self.email_rect.width/2),(35+self.username_rect.center[1]+self.email_rect.height/2))

		self.gameid = FONT.render(self.gameid,True,(255,255,255))
		self.gameid_rect = self.gameid.get_rect()
		self.gameid_rect.center = (500+(self.gameid_rect.width/2),(35+self.email_rect.center[1]+self.gameid_rect.height/2))

		self.total_hours_played = FONT.render(self.total_hours_played,True,(255,255,255))
		self.total_hours_played_rect = self.total_hours_played.get_rect()
		self.total_hours_played_rect.center = (500+(self.total_hours_played_rect.width/2),
										  (35+self.gameid_rect.center[1]+self.total_hours_played_rect.height/2))

		self.points = FONT.render(self.points,True,(255,255,255))
		self.points_rect = self.points.get_rect()
		self.points_rect.center = (500+(self.points_rect.width/2),(35+self.total_hours_played_rect.center[1]+self.points_rect.height/2))

		self.edit = FONT.render(self.edit,True,(0,0,0))
		self.edit_rect = self.edit.get_rect()
		self.edit_rect.center = (1055-self.edit_rect.width/2,335-self.edit_rect.height/2)


		self.fields = {}
		self.fields[self.username] = self.username_rect
		self.fields[self.email] = self.email_rect
		self.fields[self.gameid] = self.gameid_rect
		self.fields[self.total_hours_played] = self.total_hours_played_rect
		self.fields[self.points] = self.points_rect
		self.fields[self.edit] = self.edit_rect

		self.edit_hover = (209,209,209)
		

	def update(self):
		while True:
			self.screen.fill((4,76,84))
			pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

			self.screen.blit(self.profile_picture,(85,85))

			#profile picture border
			pygame.draw.rect(self.screen,(0,0,0),[100,100,250,250],3)
			#Info border
			pygame.draw.rect(self.screen,(0,0,0),[480,100,600,250],3)

			#edit button
			if pos[0]<=1070 and pos[0]>=1000 and pos[1]<=345 and pos[1]>=305:
				pygame.draw.rect(self.screen,self.edit_hover,[1000,300,70,40])
			else:
				pygame.draw.rect(self.screen,(0,255,0),[1000,300,70,40])

			for field in self.fields:
				self.screen.blit(field,self.fields[field])
			pygame.display.flip()
			clock.tick(60)


profile = Profile(screen,clock)
profile.get_fields()
profile.update()
pygame.quit()