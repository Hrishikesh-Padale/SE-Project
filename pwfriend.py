import pygame
from pygame.locals import *
import random
from socket import *
import pickle
import time
import threading

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
WHITE = (255,255,255)
FONT = pygame.font.SysFont('freesansbold.ttf', 40)
FONT1 = pygame.font.SysFont('consolas',20,bold=True)
FONT2 = pygame.font.SysFont('freesansbold.ttf', 35)
FONT3 = pygame.font.SysFont('freesansbold.ttf', 30)

class PlayWithFriend:

	def __init__(self,screen,clock,client):

		self.screen = screen
		self.clock = clock
		self.client = client
		self.get_search_bar()
		self.get_friends(client)

		self.Friends_texts = [FONT1.render(i,True,random.choice([RED,GREEN,BLUE])) for i in self.Friends_list]
		self.Friends_texts_rects = [i.get_rect() for i in self.Friends_texts]
		self.first_friend_index = 0
		self.last_friend_index = len(self.Friends_list)
		self.buttons_pos = [146+i*50 for i in range(0,len(self.Friends_list))]
		self.button_texts_pos = [150+i*50 for i in range(0,len(self.Friends_list))]
		self.invite_text = FONT1.render("Invite",True,(0,255,0))
		self.titles = [FONT.render("Invite Friend",True,(255,255,255)),FONT.render("Search",True,(255,255,255))]
		self.search_desc = FONT3.render("Enter username to search",True,(255,255,255))
		self.offline_text = FONT1.render("Offline",True,(255,255,255))
		self.invited_text = FONT1.render("Invite sent",True,(255,255,255))
		self.busy_text = FONT1.render("Busy",True,(248,252,3)) 
		self.add = FONT1.render("ADD",True,(0,255,0))

		self.search_result = ""
		self.search = ""
		self.count_down = 1
		self.get_centers()
		self.goback = FONT.render("Go Back",True,(0,255,0))


	def get_pwf_section_messages(self):
		try:
			msg = self.client.pwf_section_messages.pop()
			#print(msg['ID'])
			if msg['ID']==24:
				#print(msg)
				self.search_result = FONT2.render(msg['Data'][0],True,(66,245,114))
			elif msg['ID']==2200:
				self.client.room_id = msg['RoomID']
				self.client.color = msg['Turn']
			elif msg['ID']==11:
				friend_came_online = msg['FriendID']
				self.status_list[self.Friends_list.index(friend_came_online)] = True
			elif msg['ID']==12:
				friend_went_offline = msg['FriendID']
				self.status_list[self.Friends_list.index(friend_went_offline)] = False
			elif msg['ID']==13:
				friend_became_busy = msg['FriendID']
				self.status_list[self.Friends_list.index(friend_became_busy)] = "busy"
			elif msg['ID']==55:
				print("True")
				self.client.enemy_name = msg['Receiver']
		except:
			#print("exception")
			pass


	def get_friends(self,Flist):
		Flist = self.client.Flist
		self.status_list = []
		self.Friends_list = Flist['Friends']
		online_friends = Flist['Online_Friends']

		for i in self.Friends_list:
			if i in online_friends:
				self.status_list.append(True)
			else:
				self.status_list.append(False)


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
	    	#print(self.input)
	    	message = {'ID':24,'UserID':self.client.uID,'FriendID':self.input}
	    	self.client.sock.send(pickle.dumps(message))
	    	time.sleep(1)
	    	#print(self.client.pwf_section_messages)
	    	#self.get_pwf_section_messages()
	    	

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
		 	
	def set_timer(self,index):
		self.status_list[index]=True

	def update(self):
		while True:
			#events = pygame.event.get()
			self.get_pwf_section_messages()
			pos = pygame.mouse.get_pos()
			self.screen.fill("#1f1f23")
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

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

					elif event.button == 1:

						#invite events
						if len(self.Friends_list)>0:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 171  and pos[1] >= 146:
								if self.status_list[self.first_friend_index] not in ["invited","busy"]:
									self.status_list[self.first_friend_index]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index]))
						
						if len(self.Friends_list)>1:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 221  and pos[1] >= 196:
								print(self.status_list[self.first_friend_index+1])
								if self.status_list[self.first_friend_index+1] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+1]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+1,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+1]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+1]))
						
						if len(self.Friends_list)>2:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 271  and pos[1] >= 246:
								if self.status_list[self.first_friend_index+2] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+2]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+2,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+2]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+2]))
						
						if len(self.Friends_list)>3:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 321 and pos[1] >= 296:
								if self.status_list[self.first_friend_index+3] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+3]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+3,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+3]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+3]))
						
						if len(self.Friends_list)>4:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 371 and pos[1] >= 346:
								if self.status_list[self.first_friend_index+4] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+4]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index,+4))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+4]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+4]))
						
						if len(self.Friends_list)>5:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 421 and pos[1] >= 396:
								if self.status_list[self.first_friend_index+5] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+5]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+5,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+5]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+5]))
						
						if len(self.Friends_list)>6:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 471 and pos[1] >= 446:
								if self.status_list[self.first_friend_index+6] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+6]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+6,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+6]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+6]))
						
						if len(self.Friends_list)>7:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 521 and pos[1] >= 496:
								if self.status_list[self.first_friend_index+7] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+7]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+7,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+7]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+7]))
						
						if len(self.Friends_list)>8:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 571 and pos[1] >= 546:
								if self.status_list[self.first_friend_index+8] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+8]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+8,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+8]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+8]))
						
						if len(self.Friends_list)>9:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 621 and pos[1] >= 596:
								if self.status_list[self.first_friend_index+9] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+9]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+9,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+9]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+9]))
						
						if len(self.Friends_list)>10:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 671 and pos[1] >= 646:
								if self.status_list[self.first_friend_index+10] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+10]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+10,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+10]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+10]))
						
						if len(self.Friends_list)>11:
							if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 721 and pos[1] >= 696:
								if self.status_list[self.first_friend_index+11] not in ["invited","busy"]:
									self.status_list[self.first_friend_index+11]="invited"
									timer = threading.Timer(10.0, self.set_timer,args=(self.first_friend_index+11,))
									timer.start()
									invite_msg = {'ID':20,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+11]}
									self.client.sock.send(pickle.dumps(invite_msg))
									print("Invited {}".format(self.Friends_list[self.first_friend_index+11]))

						if self.search_result:
							if pos[0]<=1350 and pos[0]>=1270 and pos[1]<=235 and pos[1]>=210:
								#print("Friend request sent to {}".format(self.search))
								message = {'ID':25,'UserID':self.client.uID,'FriendID':self.search}
								self.client.sock.send(pickle.dumps(message))
								time.sleep(1)
								print(self.client.pwf_section_messages)

						if pos[0]<=1530 and pos[0]>=1410 and pos[1]<=56 and pos[1]>=6:
							return


			#Two main borders
			pygame.draw.rect(self.screen,(255,255,255),[80,60,640.5,681],2)
			pygame.draw.rect(self.screen,(255,255,255),[740.5,60,640.5,681],2)

			pygame.draw.rect(self.screen,(255,255,255),[1410,6,120,50],2)
			if pos[0]<=1530 and pos[0]>=1410 and pos[1]<=56 and pos[1]>=6:
				pygame.draw.rect(self.screen,(51, 148, 163),[1412,8,118,48])
			self.screen.blit(self.goback,(1415,15))

			#input bar
			pygame.draw.rect(self.screen,(0,255,0),[760.5,146,600.5,50],2)

			#Blinking cursor
			if self.cursor_visible:
				pygame.draw.line(self.screen,(255,255,255),(self.cursor_coords[0][0],self.cursor_coords[0][1]),
								 (self.cursor_coords[1][0],self.cursor_coords[1][1]),2)

			# invite buttons rects
			for i in self.buttons_pos:
				if self.status_list[self.first_friend_index+self.buttons_pos.index(i)]==True:
					pygame.draw.rect(self.screen,(255,255,255),[620,i,80,25],2)


			#invite buttons hover function
			if len(self.Friends_list)>0:
				if self.status_list[self.first_friend_index] and self.status_list[self.first_friend_index] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 171  and pos[1] >= 146:
						pygame.draw.rect(self.screen,(255,255,255),[622,148,80,25])
			if len(self.Friends_list)>1:
				if self.status_list[self.first_friend_index+1] and self.status_list[self.first_friend_index+1] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 221  and pos[1] >= 196:
						pygame.draw.rect(self.screen,(255,255,255),[622,198,80,25])
			if len(self.Friends_list)>2:
				if self.status_list[self.first_friend_index+2] and self.status_list[self.first_friend_index+2] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 271  and pos[1] >= 246:
						pygame.draw.rect(self.screen,(255,255,255),[622,248,80,25])
			if len(self.Friends_list)>3:
				if self.status_list[self.first_friend_index+3] and self.status_list[self.first_friend_index+3] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 321 and pos[1] >= 296:
						pygame.draw.rect(self.screen,(255,255,255),[622,298,80,25])
			if len(self.Friends_list)>4:
				if self.status_list[self.first_friend_index+4] and self.status_list[self.first_friend_index+4] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 371 and pos[1] >= 346:
						pygame.draw.rect(self.screen,(255,255,255),[622,348,80,25])
			if len(self.Friends_list)>5:
				if self.status_list[self.first_friend_index+5] and self.status_list[self.first_friend_index+5] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 421 and pos[1] >= 396:
						pygame.draw.rect(self.screen,(255,255,255),[622,398,80,25])
			if len(self.Friends_list)>6:
				if self.status_list[self.first_friend_index+6] and self.status_list[self.first_friend_index+6] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 471 and pos[1] >= 446:
						pygame.draw.rect(self.screen,(255,255,255),[622,448,80,25])
			if len(self.Friends_list)>7:
				if self.status_list[self.first_friend_index+7] and self.status_list[self.first_friend_index+7] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 521 and pos[1] >= 496:
						pygame.draw.rect(self.screen,(255,255,255),[622,498,80,25])
			if len(self.Friends_list)>8:
				if self.status_list[self.first_friend_index+8] and self.status_list[self.first_friend_index+8] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 571 and pos[1] >= 546:
						pygame.draw.rect(self.screen,(255,255,255),[622,548,80,25])
			if len(self.Friends_list)>9:
				if self.status_list[self.first_friend_index+9] and self.status_list[self.first_friend_index+9] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 621 and pos[1] >= 596:
						pygame.draw.rect(self.screen,(255,255,255),[622,598,80,25])
			if len(self.Friends_list)>10:
				if self.status_list[self.first_friend_index+10] and self.status_list[self.first_friend_index+10] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 671 and pos[1] >= 646:
						pygame.draw.rect(self.screen,(255,255,255),[622,648,80,25])
			if len(self.Friends_list)>11:
				if self.status_list[self.first_friend_index+11] and self.status_list[self.first_friend_index+11] not in ["invited","busy"]:	
					if pos[0] <= 700 and pos[0] >= 620 and pos[1] <= 721 and pos[1] >= 696:
						pygame.draw.rect(self.screen,(255,255,255),[622,698,80,25])

			#add button hover
			if self.search_result:
				if pos[0]<=1350 and pos[0]>=1270 and pos[1]<=325 and pos[1]>=300:
					pygame.draw.rect(self.screen,(255,255,255),[1272,300,80,25])

			for i in self.button_texts_pos:
				#online
				if self.status_list[self.first_friend_index+self.button_texts_pos.index(i)] not in ["invited",False]:
					self.screen.blit(self.invite_text,(627,i))
				#already invited
				elif self.status_list[self.first_friend_index+self.button_texts_pos.index(i)]=="invited":
					self.screen.blit(self.invited_text,(580,i))
				#busy
				elif self.status_list[self.first_friend_index+self.button_texts_pos.index(i)]=="busy":
					self.screen.blit(self.busy_text,(570,i))
				#offline
				else:
					self.screen.blit(self.offline_text,(620,i))

			for friend in self.Friends_texts[self.first_friend_index:self.last_friend_index]:
				self.screen.blit(friend,self.Friends_texts_rects[self.Friends_texts.index(friend)])

			self.screen.blit(self.titles[0],(320,80))
			self.screen.blit(self.titles[1],(1010,80))

			self.screen.blit(self.search_desc,(850,698))

			if self.search_result:
				self.screen.blit(self.search_result,(768,300))
				#searched results add button
				pygame.draw.rect(self.screen,(255,255,255),[1270,300,80,25],2)
				self.screen.blit(self.add,(1295,300))

			if self.client.room_id:
				return
			
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