import pygame
from pygame.locals import *
import random

pygame.init()
WHITE = (255,255,255)
FONT = pygame.font.SysFont('freesansbold.ttf', 40)
FONT1 = pygame.font.SysFont('freesansbold.ttf',30,bold=False)

class PlayWithFriend:

	def __init__(self,screen,clock):

		self.screen = screen
		self.clock = clock
		self.get_search_bar()
		self.done = False
		self.Friends_list = [chr(character) for character in range(65,91)]
		#print(self.Friends_list)
		self.Friends_texts = [FONT1.render(i,True,(random.randrange(1,256),random.randrange(1,256),random.randrange(1,256))) for i in self.Friends_list]
		#self.Friends_texts = [FONT1.render(i,True,(255,255,255)) for i in self.Friends_list]
		self.Friends_texts_rects = [i.get_rect() for i in self.Friends_texts]
		self.first_friend_index = 0
		self.last_friend_index = 12

		self.buttons_pos = [146+i*50 for i in range(0,12)]

		#print([i for i in self.buttons_pos])

		self.button_texts_pos = [150+i*50 for i in range(0,12)]

		self.invite_text = FONT1.render("Invite",True,(0,255,0))

		self.titles = [FONT.render("Invite Friend",True,(255,255,255)),FONT.render("Search",True,(255,255,255))]

		self.search_desc = FONT1.render("Enter username or room id to search",True,(255,255,255))

		#self.spec_text = FONT1.render("Spec",True,(0,255,0))
		#self.spec_text_rect = self.spec_text.get_rect()
		#self.spec_text_rect.center = (660,160)
		self.get_centers()

	def get_centers(self):
		x,y = 100,160
		for i in self.Friends_texts_rects[self.first_friend_index:self.last_friend_index]:
			i.center = (x+i.width/2,y)
			y += 50

	def get_search_bar(self):
		self.delay = 500
		self.current_time = pygame.time.get_ticks()
		self.change_time = self.current_time + self.delay
		self.cursor_visible = True
		self.input = ""
		self.cursor_position = 0
		self.max_input_length = 25
		self.cursor_coords = [[770.5,156],[770.5,186]]

	def cursor_blink(self):
		self.current_time = pygame.time.get_ticks()
		if self.current_time >= self.change_time:
		    self.change_time = self.current_time + self.delay
		    self.cursor_visible = not self.cursor_visible
		    return self.cursor_visible

	def get_input_pwf(self,event):

	    if bool(event.unicode) and len(self.input) < self.max_input_length and event.key != pygame.K_RETURN:
	        self.input = self.input[:self.cursor_position] + event.unicode + self.input[self.cursor_position:]
	        self.cursor_position += 1
	        self.input_text = FONT.render(self.input, True, WHITE)
	        self.input_rect = self.input_text.get_rect()
	        self.input_rect.center = (770.5 + (self.input_rect.width // 2),
	        						  160 + self.input_rect.height//2)
	        text = FONT.render(self.input[self.cursor_position:], True, WHITE)
	        rect = text.get_rect()
	        self.cursor_coords[0][0] = 770.5 + self.input_rect.width - rect.width
	        self.cursor_coords[1][0] = self.cursor_coords[0][0]

	    elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(self.input) > 0:       
	    	print(self.input)

	    elif event.key == pygame.K_LEFT and self.cursor_position > 0:
	    	self.cursor_position -= 1
	    	text = FONT.render(self.input[:self.cursor_position],True,WHITE)
	    	rect = text.get_rect()
	    	self.cursor_coords[0][0] = 770.5+rect.width
	    	self.cursor_coords[1][0] = 770.5+rect.width 

	    elif event.key == pygame.K_RIGHT and self.cursor_position < len(self.input):
	    	self.cursor_position += 1
	    	text = FONT.render(self.input[:self.cursor_position],True,WHITE)
	    	rect = text.get_rect()
	    	self.cursor_coords[0][0] = 770.5+rect.width
	    	self.cursor_coords[1][0] = 770.5+rect.width

	    elif event.key == pygame.K_BACKSPACE and self.cursor_position > 0:
	    	self.cursor_position -= 1
	    	text = FONT.render(self.input[self.cursor_position],True,WHITE)
	    	rect = text.get_rect()
	    	self.cursor_coords[0][0] = self.cursor_coords[0][0]-rect.width
	    	self.cursor_coords[1][0] = self.cursor_coords[0][0]
	    	temp = ""
	    	for i in range(len(self.input)):
	    	    if i != self.cursor_position:
	    	        temp += self.input[i]
	    	self.input = temp
	    	self.input_text = FONT.render(self.input, True, WHITE)
	    	self.input_rect = self.input_text.get_rect()
	    	self.input_rect.center = (770.5 + (self.input_rect.width // 2),160 + self.input_rect.height//2)


	def print_input(self):
		if len(self.input) > 0 :
			self.screen.blit(self.input_text,self.input_rect)
		 	


	def update(self):
		while not self.done:
			#events = pygame.event.get()
			pos = pygame.mouse.get_pos()
			self.screen.fill("#1f1f23")
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.done = True

				elif event.type == pygame.KEYDOWN:
					self.get_input_pwf(event)

				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 4:
						if pos[0]<= 720.5 and pos[0]>=80 and pos[1]<=741 and pos[1] >=60:
							if self.first_friend_index > 0:
								self.first_friend_index -= 1
								self.last_friend_index -= 1
								self.get_centers()

					elif event.button == 5:
						if pos[0]<= 720.5 and pos[0]>=80 and pos[1]<=741 and pos[1] >=60:
							if self.last_friend_index < len(self.Friends_list):
								self.first_friend_index += 1
								self.last_friend_index += 1
								self.get_centers()

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 171  and pos[1] >= 146:
						print("Invited {}".format(self.Friends_list[self.first_friend_index]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 221  and pos[1] >= 196:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+1]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 271  and pos[1] >= 246:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+2]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 321 and pos[1] >= 296:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+3]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 371 and pos[1] >= 346:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+4]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 421 and pos[1] >= 396:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+5]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 471 and pos[1] >= 446:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+6]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 521 and pos[1] >= 496:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+7]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 571 and pos[1] >= 546:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+8]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 621 and pos[1] >= 596:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+9]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 671 and pos[1] >= 646:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+10]))

					elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 721 and pos[1] >= 696:
						print("Invited {}".format(self.Friends_list[self.first_friend_index+11]))

			#Two main borders
			pygame.draw.rect(self.screen,(255,255,255),[80,60,640.5,681],2)
			pygame.draw.rect(self.screen,(255,255,255),[740.5,60,640.5,681],2)

			#input bar
			pygame.draw.rect(self.screen,(0,255,0),[760.5,146,600.5,50],2)


			if self.cursor_visible:
				pygame.draw.line(self.screen,(255,255,255),(self.cursor_coords[0][0],self.cursor_coords[0][1]),
								 (self.cursor_coords[1][0],self.cursor_coords[1][1]),2)

			for i in self.buttons_pos:
				pygame.draw.rect(self.screen,(255,255,255),[620,i,80,25],2)

				
			if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 171  and pos[1] >= 146:
				pygame.draw.rect(self.screen,(255,255,255),[622,148,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 221  and pos[1] >= 196:
				pygame.draw.rect(self.screen,(255,255,255),[622,198,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 271  and pos[1] >= 246:
				pygame.draw.rect(self.screen,(255,255,255),[622,248,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 321 and pos[1] >= 296:
				pygame.draw.rect(self.screen,(255,255,255),[622,298,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 371 and pos[1] >= 346:
				pygame.draw.rect(self.screen,(255,255,255),[622,348,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 421 and pos[1] >= 396:
				pygame.draw.rect(self.screen,(255,255,255),[622,398,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 471 and pos[1] >= 446:
				pygame.draw.rect(self.screen,(255,255,255),[622,448,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 521 and pos[1] >= 496:
				pygame.draw.rect(self.screen,(255,255,255),[622,498,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 571 and pos[1] >= 546:
				pygame.draw.rect(self.screen,(255,255,255),[622,548,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 621 and pos[1] >= 596:
				pygame.draw.rect(self.screen,(255,255,255),[622,598,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 671 and pos[1] >= 646:
				pygame.draw.rect(self.screen,(255,255,255),[622,648,80,25])
			elif pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 721 and pos[1] >= 696:
				pygame.draw.rect(self.screen,(255,255,255),[622,698,80,25])

			for i in self.button_texts_pos:
				self.screen.blit(self.invite_text,(635,i))
				#self.screen.blit(self.spec_text,(640,i))

			for friend in self.Friends_texts[self.first_friend_index:self.last_friend_index]:
				self.screen.blit(friend,self.Friends_texts_rects[self.Friends_texts.index(friend)])

			self.screen.blit(self.titles[0],(320,80))
			self.screen.blit(self.titles[1],(1010,80))

			self.screen.blit(self.search_desc,(880,698))
			
			self.cursor_blink()
			self.print_input()
			pygame.display.flip()
			self.clock.tick(60)


#width,height = 1536,801
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode((width,height))
#pygame.display.set_caption("Play With Friend")
#play_with_friend = PlayWithFriend(screen,clock)
#play_with_friend.update()
#pygame.quit()