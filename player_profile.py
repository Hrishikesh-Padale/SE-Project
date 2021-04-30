import pygame
from pygame.locals import *
import random
import pickle
import matplotlib.pyplot as plt
import numpy as np



pygame.init()
FONT = pygame.font.SysFont('freesansbold.ttf', 40)
FONT1 = pygame.font.SysFont('calibri',25,True)
FONT2 = pygame.font.SysFont('calibri',30,True)
FONT3 = pygame.font.SysFont('calibri',20,True)

class Profile:

	def __init__(self,screen,clock,client):
		self.profile_picture = pygame.transform.scale(pygame.image.load('Media/prof.png'),(280,280))
		self.screen = screen
		self.clock = clock
		self.client = client

		self.data = {}
		self.fields = {}
		message = {'ID':40,'UserID':self.client.uID}
		self.client.sock.send(pickle.dumps(message))
		
		self.get_friends()
		self.get_buttons()
		self.goback = FONT.render("Go Back",True,(0,255,0))
		

	def get_buttons(self):
		self.remove_friend_buttons_pos = [166+i*50 for i in range(12)]
		self.rem = FONT3.render("Remove",True,(255,0,0))
		self.accept_reject_buttons_pos = [464+i*50 for i in range(6)]
		self.add = FONT2.render("+",True,(0,255,0))
		self.rej = FONT2.render("-",True,(255,0,0))
		#print([i+25 for i in self.accept_reject_buttons_pos])

	def get_friends(self):
		self.Friends_list = self.client.Flist['Friends']
		#print(self.Friends_list)
		self.Friends_texts = [FONT1.render(i,True,(random.randrange(1,256),random.randrange(1,256),random.randrange(1,256))) for i in self.Friends_list]
		#self.Friends_texts = [FONT1.render(i,True,(255,255,255)) for i in self.Friends_list]
		self.Friends_texts_rects = [i.get_rect() for i in self.Friends_texts]
		self.first_friend_index = 0
		self.last_friend_index = len(self.Friends_list)
		self.p_req_text = FONT2.render("Pending Requests",True,(0,255,0))
		self.pending_requests = self.client.Flist['Friend_Requests']
		self.p_reqs = [FONT1.render(i,True,(random.randrange(1,256),random.randrange(1,256),random.randrange(1,256))) for i in self.pending_requests]
		self.p_reqs_rects = [i.get_rect() for i in self.p_reqs]
		self.first_pending_req = 0
		self.last_pending_req = len(self.pending_requests)
		self.get_centers()
	

	def get_centers(self):
		x,y = 1140,180
		for i in self.Friends_texts_rects[self.first_friend_index:self.last_friend_index]:
			i.center = (x+i.width/2,y)
			y += 50

		j,k = 710,480
		for i in self.p_reqs_rects[self.first_pending_req:self.last_pending_req]:
			i.center = (j+i.width/2,k)
			k += 50


	def get_fields(self):

		self.email = "Email                        {}".format(self.data["email"])
		self.gameid = "Game ID                  {}".format(self.data["gameid"])
		self.total_matches_played = "Matches played      {}".format(self.data["total_matches_played"])
		self.points = "Points                      {}".format(self.data["points"])
		self.total_matches_won = "Total wins               {}".format(self.data["Wins"])
		self.friends = "Friends({})".format(len(self.Friends_list))

		self.g_figure = plt.figure()
		self.graph = np.array([self.data["Wins"],self.data["total_matches_played"]-self.data["Wins"]])
		self.graph_labels = ["Win rate","Loss rate"]
		plt.pie(self.graph,labels=self.graph_labels)
		self.g_figure.savefig('./Media/stats.png')

		self.email = FONT1.render(self.email,True,(255,255,255))
		self.email_rect = self.email.get_rect()
		self.email_rect.center = (415+(self.email_rect.width/2),(110+self.email_rect.center[1]+self.email_rect.height/2))

		self.gameid = FONT1.render(self.gameid,True,(255,255,255))
		self.gameid_rect = self.gameid.get_rect()
		self.gameid_rect.center = (415+(self.gameid_rect.width/2),(35+self.email_rect.center[1]+self.gameid_rect.height/2))

		self.total_matches_played = FONT1.render(self.total_matches_played,True,(255,255,255))
		self.total_matches_played_rect = self.total_matches_played.get_rect()
		self.total_matches_played_rect.center = (415+(self.total_matches_played_rect.width/2),
										  (35+self.gameid_rect.center[1]+self.total_matches_played_rect.height/2))

		self.points = FONT1.render(self.points,True,(255,255,255))
		self.points_rect = self.points.get_rect()
		self.points_rect.center = (415+(self.points_rect.width/2),(35+self.total_matches_played_rect.center[1]+self.points_rect.height/2))

		self.total_matches_won = FONT1.render(self.total_matches_won,True,(255,255,255))
		self.total_matches_won_rect = self.total_matches_won.get_rect()
		self.total_matches_won_rect.center = (415+(self.total_matches_won_rect.width/2),(35+self.points_rect.center[1]+self.total_matches_won_rect.height/2))
		
		self.friends = FONT2.render(self.friends,True,(0,255,0))
		self.friends_rect = self.friends.get_rect()
		self.friends_rect.center = (1287.5,100+self.friends_rect.height)

		self.fields[self.email] = self.email_rect
		self.fields[self.gameid] = self.gameid_rect
		self.fields[self.total_matches_played] = self.total_matches_played_rect
		self.fields[self.points] = self.points_rect
		self.fields[self.total_matches_won] = self.total_matches_won_rect
		self.fields[self.friends] = self.friends_rect


	def get_profile_section_messages(self):
		try:
			message = self.client.profile_section_messages.pop()
			if message['ID'] == 27:
				self.pending_requests.append(message['FriendID'])
				p_req_text = FONT1.render(message['FriendID'],True,random.choice([(0,255,0),(0,0,255)]))
				self.last_pending_req += 1

			elif message['ID'] == 28:
				print("Removed {} from friend list successfully ...".format(message['FriendID']))

			elif message['ID'] == 40:
				self.data["email"] = message['Email']
				self.data["gameid"] = message['UserID']
				self.data["total_matches_played"] = message['Matches_Played']
				self.data["points"] = message['Points']
				self.data["Wins"] = message['Matches_Won']
				self.get_fields()
				self.pie_chart = pygame.transform.scale(pygame.image.load('Media/stats.png'),(595,345))

		except:
			pass

	def update(self):
		while True:
			self.get_profile_section_messages()
			self.screen.fill("#17252A")
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
						if pos[0]<=1050 and pos[0]>=700 and pos[1]<=750 and pos[1]>=400:
							if self.first_pending_req > 0:
								self.first_pending_req -= 1
								self.last_pending_req -= 1
								self.get_centers()


					if event.button == 5:
						#print("Scroll Down")
						if pos[0]<1450 and pos[0]>1125 and pos[1]<750 and pos[1] >153:
							if self.last_friend_index < len(self.Friends_list):
								self.first_friend_index += 1
								self.last_friend_index += 1
								self.get_centers()

						if pos[0]<=1050 and pos[0]>=700 and pos[1]<=750 and pos[1]>=400:
							if self.last_pending_req < len(self.pending_requests):
								self.first_pending_req += 1
								self.last_pending_req += 1
								self.get_centers()

					if event.button == 1:
						#print(pos)
						#remove buttons
						if len(self.Friends_list)>0:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=191 and pos[1]>= 166:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index]))
						if len(self.Friends_list)>1:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=241 and pos[1]>= 216:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+1]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+1])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+1])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+1]))
						if len(self.Friends_list)>2:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=291 and pos[1]>= 266:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+2]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+2])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+2])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+2]))
						if len(self.Friends_list)>3:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=341 and pos[1]>= 316:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+3]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+3])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+3])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+3]))
						if len(self.Friends_list)>4:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=391 and pos[1]>= 366:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+4]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+4])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+4])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+4]))
						if len(self.Friends_list)>5:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=441 and pos[1]>= 416:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+5]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+5])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+5])
								self.friends = "Friends({})".format(len(self.Friends_list))		
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+5]))
						if len(self.Friends_list)>6:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=491 and pos[1]>= 466:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+6]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+6])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+6])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+6]))
						if len(self.Friends_list)>7:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=541 and pos[1]>= 516:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+7]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+7])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+7])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+7]))
						
						if len(self.Friends_list)>8:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=591 and pos[1]>= 566:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+8]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+8])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+8])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+8]))
						if len(self.Friends_list)>9:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=641 and pos[1]>= 616:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+9]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+9])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+9])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+9]))
						if len(self.Friends_list)>10:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=691 and pos[1]>= 666:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+10]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+10])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+10])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+10]))
						if len(self.Friends_list)>11:
							if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=741 and pos[1]>= 716:
								message = {'ID':28,'UserID':self.client.uID,'FriendID':self.Friends_list[self.first_friend_index+11]}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.remove(self.Friends_list[self.first_friend_index+11])
								self.Friends_texts.remove(self.Friends_texts[self.first_friend_index+11])
								self.friends = "Friends({})".format(len(self.Friends_list))
								#print("Removed {}".format(self.Friends_list[self.first_friend_index+11]))

						#accept buttons
						if len(self.pending_requests)>0:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=489 and pos[1]>=464:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index])

								print("Accepted {}".format(self.pending_requests[self.first_pending_req]))
						if len(self.pending_requests)>1:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=539 and pos[1]>=514:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req+1])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req+1],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+1])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+1])
								print("Accepted {}".format(self.pending_requests[self.first_pending_req+1]))
						if len(self.pending_requests)>2:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=589 and pos[1]>=564:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req+2])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req+2],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+2])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+2])
								print("Accepted {}".format(self.pending_requests[self.first_pending_req+2]))
						if len(self.pending_requests)>3:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=639 and pos[1]>=614:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req+3])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req+3],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+3])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+3])
								print("Accepted {}".format(self.pending_requests[self.first_pending_req+3]))
						if len(self.pending_requests)>4:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=689 and pos[1]>=664:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req+4])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req+4],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+4])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+4])
								print("Accepted {}".format(self.pending_requests[self.first_pending_req+4]))
						if len(self.pending_requests)>5:
							if pos[0]<=985 and pos[0]>=960 and pos[1]<=739 and pos[1]>=714:
								message = {'ID':26,'Status':'Accepted'}
								self.client.sock.send(pickle.dumps(message))
								self.Friends_list.append(self.pending_requests[self.first_pending_req+5])
								self.Friends_texts.append(self.pending_requests[self.first_pending_req+5],True,(255,255,255))
								self.get_centers()
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+5])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+5])
								print("Accepted {}".format(self.pending_requests[self.first_pending_req+5]))


						if len(self.pending_requests)>0:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=489 and pos[1]>=464:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req]))
						if len(self.pending_requests)>1:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=539 and pos[1]>=514:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+1])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+1])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req+1]))
						if len(self.pending_requests)>2:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=589 and pos[1]>=564:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+2])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+2])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req+2]))
						if len(self.pending_requests)>3:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=639 and pos[1]>=614:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+3])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+3])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req+3]))
						if len(self.pending_requests)>4:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=689 and pos[1]>=664:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+4])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+4])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req+4]))
						if len(self.pending_requests)>5:
							if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=739 and pos[1]>=714:
								message = {'ID':26,'Status':'Rejected'}
								self.client.sock.send(pickle.dumps(message))
								self.pending_requests.remove(self.pending_requests[self.first_pending_req+5])
								self.p_reqs.remove(self.p_reqs[self.first_friend_index+5])
								print("Rejected {}".format(self.pending_requests[self.first_pending_req+5]))

						if pos[0]<=1530 and pos[0]>=1410 and pos[1]<=56 and pos[1]>=6:
							return


			self.screen.blit(self.profile_picture,(55,85))

			#profile picture border
			pygame.draw.rect(self.screen,(0,0,0),[70,100,250,250],3)
			#Info border
			pygame.draw.rect(self.screen,(0,0,0),[395,100,655,250],3)

			pygame.draw.rect(self.screen,(255,255,255),[1410,6,120,50],2)
			if pos[0]<=1530 and pos[0]>=1410 and pos[1]<=56 and pos[1]>=6:
				pygame.draw.rect(self.screen,(51, 148, 163),[1412,8,118,48])
			self.screen.blit(self.goback,(1415,15))


			for field in self.fields:
				self.screen.blit(field,self.fields[field])

			for friend in self.Friends_texts[self.first_friend_index:self.last_friend_index]:
				self.screen.blit(friend,self.Friends_texts_rects[self.Friends_texts.index(friend)])

			for req in self.p_reqs[self.first_pending_req:self.last_pending_req]:
				self.screen.blit(req,self.p_reqs_rects[self.p_reqs.index(req)])

			#graph
			pygame.draw.rect(self.screen,(0,0,0),[70,400,600,350],3)
			try:
				self.screen.blit(self.pie_chart,(72,402))
			except:
				pass
			#pending requests border
			pygame.draw.rect(self.screen,(0,0,0),[700,400,350,350],3)


			#accept buttons focus
			if len(self.pending_requests)>0:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=489 and pos[1]>=464:
					pygame.draw.rect(self.screen,(255,255,255),[960,464,25,25])
			if len(self.pending_requests)>1:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=539 and pos[1]>=514:
					pygame.draw.rect(self.screen,(255,255,255),[960,514,25,25])
			if len(self.pending_requests)>2:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=589 and pos[1]>=564:
					pygame.draw.rect(self.screen,(255,255,255),[960,564,25,25])
			if len(self.pending_requests)>3:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=639 and pos[1]>=614:
					pygame.draw.rect(self.screen,(255,255,255),[960,614,25,25])
			if len(self.pending_requests)>4:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=689 and pos[1]>=664:
					pygame.draw.rect(self.screen,(255,255,255),[960,664,25,25])
			if len(self.pending_requests)>5:
				if pos[0]<=985 and pos[0]>=960 and pos[1]<=739 and pos[1]>=714:
					pygame.draw.rect(self.screen,(255,255,255),[960,714,25,25])

			#reject button focus
			if len(self.pending_requests)>0:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=489 and pos[1]>=464:
					pygame.draw.rect(self.screen,(255,255,255),[1000,464,25,25])
			if len(self.pending_requests)>1:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=539 and pos[1]>=514:
					pygame.draw.rect(self.screen,(255,255,255),[1000,514,25,25])
			if len(self.pending_requests)>2:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=589 and pos[1]>=564:
					pygame.draw.rect(self.screen,(255,255,255),[1000,564,25,25])
			if len(self.pending_requests)>3:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=639 and pos[1]>=614:
					pygame.draw.rect(self.screen,(255,255,255),[1000,614,25,25])
			if len(self.pending_requests)>4:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=689 and pos[1]>=664:
					pygame.draw.rect(self.screen,(255,255,255),[1000,664,25,25])
			if len(self.pending_requests)>5:
				if pos[0]<=1025 and pos[0]>=1000 and pos[1]<=739 and pos[1]>=714:
					pygame.draw.rect(self.screen,(255,255,255),[1000,714,25,25])

			#accept/reject buttons
			for i in self.accept_reject_buttons_pos:
				if len(self.pending_requests)>self.accept_reject_buttons_pos.index(i):
					pygame.draw.rect(self.screen,(255,255,255),[960,i,25,25],2)
					pygame.draw.rect(self.screen,(255,255,255),[1000,i,25,25],2)
					self.screen.blit(self.add,(965,i-2))
					self.screen.blit(self.rej,(1009,i-1))

			#friends box border
			pygame.draw.rect(self.screen,(0,0,0),[1125,100,325,650],3)
			#pygame.draw.rect(self.screen,(255,255,255),[1128,103,319,50])
			pygame.draw.line(self.screen,(0,0,0),(1125,153),(1450,153),3)
			pygame.draw.line(self.screen,(0,0,0),(700,450),(1050,450),3)

			#remove buttons rects
			for i in self.remove_friend_buttons_pos:
				if len(self.Friends_list)>self.remove_friend_buttons_pos.index(i):
					pygame.draw.rect(self.screen,(255,255,255),[1350,i,80,25],2)
			self.screen.blit(self.p_req_text,(765,410))

			#remove buttons focus
			if len(self.Friends_list)>0:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=191 and pos[1]>= 166:
					pygame.draw.rect(self.screen,(255,255,255),[1352,168,80,25])
			if len(self.Friends_list)>1:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=241 and pos[1]>= 216:
					pygame.draw.rect(self.screen,(255,255,255),[1352,218,80,25])
			if len(self.Friends_list)>2:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=291 and pos[1]>= 266:
					pygame.draw.rect(self.screen,(255,255,255),[1352,268,80,25])
			if len(self.Friends_list)>3:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=341 and pos[1]>= 316:
					pygame.draw.rect(self.screen,(255,255,255),[1352,318,80,25])
			if len(self.Friends_list)>4:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=391 and pos[1]>= 366:
					pygame.draw.rect(self.screen,(255,255,255),[1352,368,80,25])
			if len(self.Friends_list)>5:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=441 and pos[1]>= 416:
					pygame.draw.rect(self.screen,(255,255,255),[1352,418,80,25])
			if len(self.Friends_list)>6:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=491 and pos[1]>= 466:
					pygame.draw.rect(self.screen,(255,255,255),[1352,468,80,25])
			if len(self.Friends_list)>7:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=541 and pos[1]>= 516:
					pygame.draw.rect(self.screen,(255,255,255),[1352,518,80,25])
			if len(self.Friends_list)>8:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=591 and pos[1]>= 566:
					pygame.draw.rect(self.screen,(255,255,255),[1352,568,80,25])
			if len(self.Friends_list)>9:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=641 and pos[1]>= 616:
					pygame.draw.rect(self.screen,(255,255,255),[1352,618,80,25])
			if len(self.Friends_list)>10:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=691 and pos[1]>= 666:
					pygame.draw.rect(self.screen,(255,255,255),[1352,668,80,25])
			if len(self.Friends_list)>11:
				if pos[0]<=1430 and pos[0]>=1350 and pos[1]<=741 and pos[1]>= 716:
					pygame.draw.rect(self.screen,(255,255,255),[1352,718,80,25])

			for i in range(len(self.Friends_list)):
				self.screen.blit(self.rem,(1357,170+i*50))

			pygame.display.flip()
			self.clock.tick(60)


#width,height = 1536,801
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode((width,height))
#profile = Profile(screen,clock)
#profile.update()
#pygame.quit()