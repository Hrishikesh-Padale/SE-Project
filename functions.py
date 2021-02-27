import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
from socket import *
import time
import random


pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (102, 204, 0)
LIGHTBLUE = (51, 153, 255)
COLOR1 = (48,128,42)
COLOR2 = (118,196,112)
LIGHTGREEN = (102,255,102)
LIGHTNAVY = (153,153,255)
RED = (255,0,0)
FONT = pygame.font.SysFont('freesansbold.ttf', 25)
 
class box:
	def __init__(self,x,y,xstart,ystart):
		self.x = x
		self.y = y
		self.xstart = xstart
		self.ystart = ystart


class interface:
    
    def __init__(self,width,height,screen=None):
        self.width = width
        self.height = height
        self.screen = screen  
        self.grid = []
        self.delay = 500
        self.current_time = pygame.time.get_ticks()
        self.change_time = self.current_time + self.delay
        self.cursor_visible = True
        self.message = "" 
        self.chat_buffer_text = []
        self.chat_buffer_graphic = []
        self.last_message_done = True
        self.cursor_position = 0
        self.max_message_length = 25
        self.old_messages = []
        self.first_msg = 0
        self.last_msg = 0
        self.server = '127.0.0.1'
        self.port = 13000
        self.username = "Hrishi"
        self.connect_to_server()
        self.receive_thread = Thread(target=self.receive_messages)
        self.receive_thread.start()

    def generate_board_coordinates(self):
        self.xstart = self.width-(self.width*99.5)//100
        self.xend = self.width-(self.width*30)//100
        self.ystart = self.xstart
        self.boardheight = self.height-2*self.ystart-5
        self.boardwidth = self.boardheight
        self.boxwidth = self.boardwidth//8
        self.boxheight = self.boardheight//8
        for row in range(8):
        	self.grid.append([])
        	for column in range(8):
        		self.grid[row].append(box(row,column,int(self.xstart+2+(column*self.boxwidth)),self.ystart+2+(row*self.boxheight)))

    def generate_settings_panel(self):
    	self.panel_xstart = self.xend + 15
    	self.panel_ystart = self.ystart
    	self.panelwidth = (self.width-15) - self.panel_xstart
    	self.panelheight = 80

    def generate_killed_pieces_box(self):
    	self.killed_xstart = self.xend + 15
    	self.killed_ystart = self.panel_ystart + self.panelheight + 15
    	self.killed_box_width = self.panelwidth
    	self.killed_box_height = 250

    def generate_chatbox(self):
    	self.chatbox_xstart = self.xend + 15
    	self.chatbox_ystart = self.killed_ystart + self.killed_box_height + 15
    	self.chatbox_width = self.panelwidth
    	self.chatbox_height = self.boardheight + self.ystart - self.chatbox_ystart

    def draw_chess_board(self):
   		for i in range(8):
   			for j in range(8):
   				if (i+j)%2 == 1:
   					pygame.draw.rect(self.screen,COLOR1,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])
   				else:
   					pygame.draw.rect(self.screen,COLOR2,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])

    def generate_message_input_box(self):
   		self.messsage_input_xstart = self.chatbox_xstart + 15
   		self.messsage_input_ystart = self.chatbox_ystart+self.chatbox_height-50
   		self.messsage_input_width = self.chatbox_width - 30
   		self.messsage_input_height = 40
   		self.message_text_xstart = self.messsage_input_xstart+5
   		self.message_text_ystart = self.messsage_input_ystart+5
   		self.cursor_coord=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]

    def cursor_blink(self):
   		self.current_time = pygame.time.get_ticks()
   		if self.current_time >= self.change_time:
   			self.change_time = self.current_time + self.delay
   			self.cursor_visible = not self.cursor_visible
   		return self.cursor_visible

    def get_chat_input(self,events):
      for event in events:
        if event.type == pygame.KEYDOWN:
          if bool(event.unicode) and len(self.message)<self.max_message_length and event.key!=pygame.K_RETURN:
            self.message = self.message[:self.cursor_position] + event.unicode + self.message[self.cursor_position:]
            self.cursor_position += 1
            self.message_text = FONT.render(self.message,True,BLACK)
            self.message_rect = self.message_text.get_rect()
            self.message_rect.center = (self.messsage_input_xstart+5+(self.message_rect.width//2),self.messsage_input_ystart+20)
            text = FONT.render(self.message[self.cursor_position:],True,BLACK)
            rect = text.get_rect()
            self.cursor_coord[0][0] = self.messsage_input_xstart+5+self.message_rect.width-rect.width
            self.cursor_coord[1][0] = self.cursor_coord[0][0]
            if self.cursor_coord[0][0] >= self.messsage_input_xstart+self.messsage_input_width-5:
              self.cursor_coord[0][0] = self.messsage_input_xstart+self.messsage_input_width-5
              self.cursor_coord[1][0] = self.cursor_coord[0][0]

          elif event.key == pygame.K_RETURN and len(self.message)>0:
            self.last_message_done = False
            self.chat_buffer_text.append("Me:"+self.message)
            msg = self.username+":"+self.message
            self.send_message(msg)
            text = FONT.render(self.message,True,BLACK)
            rect = text.get_rect()
            username = FONT.render("Me:",True,random.choice([RED,GREEN,LIGHTBLUE,LIGHTNAVY]))
            uname_rect = username.get_rect()
            self.chat_buffer_graphic.append(([username,uname_rect],[text,rect]))
            self.message = ""
            self.cursor_position = 0
            self.cursor_coord=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]
            self.last_msg += 1
            if self.last_msg>=12:
              self.first_msg +=1

          elif event.key == pygame.K_LEFT and self.cursor_position > 0:
            self.cursor_position -= 1
            string_right_to_cursor = self.message[self.cursor_position:]
            text = FONT.render(string_right_to_cursor,True,BLACK)
            rect = text.get_rect()
            #change cursor coordinates 
            self.cursor_coord[0][0] = self.messsage_input_xstart+5+self.message_rect.width-rect.width
            self.cursor_coord[1][0] = self.cursor_coord[0][0]

   				
          elif event.key == pygame.K_RIGHT and self.cursor_position < len(self.message):
            self.cursor_position += 1
            string_left_to_cursor = self.message[:self.cursor_position]
            text = FONT.render(string_left_to_cursor,True,BLACK)
            rect = text.get_rect()
            self.cursor_coord[0][0] = self.messsage_input_xstart+5+rect.width
            self.cursor_coord[1][0] = self.cursor_coord[0][0]

          elif event.key == pygame.K_BACKSPACE and self.cursor_position>0:
            self.cursor_position -= 1
            deleted_letter = self.message[self.cursor_position]
            temp = ""
            for i in range(len(self.message)):
              if i != self.cursor_position:
                temp += self.message[i]
            self.message = temp
            self.message_text = FONT.render(self.message,True,BLACK)
            self.message_rect = self.message_text.get_rect()
            self.message_rect.center = (self.messsage_input_xstart+5+(self.message_rect.width//2),self.messsage_input_ystart+20)
            deleted_letter = FONT.render(deleted_letter,True,BLACK)
            rect = deleted_letter.get_rect()
            self.cursor_coord[0][0] -= rect.width
            self.cursor_coord[1][0] = self.cursor_coord[0][0]
      
      if len(self.message)>0:
        self.screen.blit(self.message_text,self.message_rect)

      if len(self.message) == 0:
        self.cursor_coord=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]

    def print_messages(self):
    	free_space_start = [self.messsage_input_xstart,self.messsage_input_ystart-30]
    	for i in reversed(self.chat_buffer_graphic[self.first_msg:self.last_msg]):
    		i[0][1].center = (free_space_start[0]+i[0][1].width//2,free_space_start[1])
    		i[1][1].center = (free_space_start[0]+i[0][1].width+(i[1][1].width//2)+3,free_space_start[1])
    		self.screen.blit(i[0][0],i[0][1])
    		self.screen.blit(i[1][0],i[1][1])
    		free_space_start[1] -= 30

    def generate_other_functionalities(self):
    	self.game_info_box1_coords = (self.xstart+self.boardwidth+10,self.ystart)
    	self.game_info_box1_width = (self.panel_xstart-10)-self.game_info_box1_coords[0]
    	self.game_info_box1_height = (self.boardheight//2)-10

    	self.game_info_box2_coords = (self.xstart+self.boardwidth+10,self.ystart+self.game_info_box1_height+10)
    	self.game_info_box2_width = self.game_info_box1_width
    	self.game_info_box2_height = (self.boardheight//2)



    #Networking part
    def connect_to_server(self):
      try:  
        self.sock = socket(AF_INET,SOCK_STREAM)  
        print ("Socket successfully created") 
      except error as err:  
        print ("socket creation failed with error %s" %(err))
      self.sock.connect((self.server,self.port))
      self.sock.send(self.username.encode())

    def get_username_and_message(self,message):
      username = ""
      msg = ""
      if ":" not in message:
        return None,message
      for i in message:
          if i != ":":
              username += i
          else:
            break
      msg = message[len(username)+1:]
      return username,msg

    def receive_messages(self):
      while True:
        try:
          message = self.sock.recv(1024).decode()
          if message:
            username,message = self.get_username_and_message(message)
            if message and username:
              self.chat_buffer_text.append(message)
              username = FONT.render(username+":",True,random.choice([RED,GREEN,LIGHTBLUE,LIGHTNAVY]))
              uname_rect = username.get_rect()
              message = FONT.render(message,True,BLACK)
              message_rect = message.get_rect()
              self.chat_buffer_graphic.append(([username,uname_rect],[message,message_rect]))
              self.last_msg += 1
              if self.last_msg>=12:
                self.first_msg +=1
            else:
              self.chat_buffer_text.append(message)
              text1 = message.split(" ")[0]
              text2 = message[len(text1):]
              text1 = FONT.render(text1,True,BLACK)
              text2 = FONT.render(text2,True,BLACK)
              text1_rect = text1.get_rect()
              text2_rect = text2.get_rect()
              self.chat_buffer_graphic.append(([text1,text1_rect],[text2,text2_rect]))
              self.last_msg += 1
              if self.last_msg>=12:
                self.first_msg +=1
        except:
          self.sock.close()
          break

    def send_message(self,message):
      try:
        self.sock.send(message.encode())
      except:
        print("Error sending message!!")
        self.sock.close()

    def __str__(self):
        return "screen-width:{} screen-height:{}\nboard-width:{} board-height:{}".format(self.width,self.height,self.boardwidth,self.boardheight)




#font = pygame.font.SysFont('freesansbold.ttf', 100)
#start_text = font.render("PRESS ANY KEY",True,(255,0,0))
#text_rect = start_text.get_rect()
#text_rect.center = (Interface.width//2,Interface.height//2)
#
#while True:
#	screen.fill(LIGHTGREEN)
#	screen.blit(start_text,text_rect)
#	pygame.draw.rect(screen,RED,[50,50,1425,680],5)
#	pygame.display.flip()
#	pygame.event.pump()
#	event = pygame.event.wait()
#	if event.type == pygame.MOUSEBUTTONDOWN:
#		break
#	elif event.type == pygame.KEYDOWN:
#		break
#	elif event.type == QUIT:
#		sys.exit()

#print(Interface.messsage_input_xstart,Interface.messsage_input_ystart,Interface.messsage_input_xstart+Interface.messsage_input_width,Interface.messsage_input_ystart+Interface.messsage_input_height)

