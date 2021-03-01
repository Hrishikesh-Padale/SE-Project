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
GRAY = (130,130,130)
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

Cursor_image = pygame.image.load('Media/Cursor_type_2.png')
Cursor_image = pygame.transform.scale(Cursor_image,(33,33))


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
        self.server = '65.0.204.13'
        self.port = 12000
        self.username = "Hrishi"
        #self.connect_to_server()
        #self.receive_thread = Thread(target=self.receive_messages)
        #self.receive_thread.start()

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
            #self.send_message(msg)
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


class piece:
	def __init__(self,name,position):
		self.name = name
		self.position = position
		self.image = None

class game:

	def __init__(self,grid):
		self.white_pieces_images = {}
		self.black_pieces_images = {}
		self.grid = grid
		self.mypieces = {}
		self.enemy_pieces = {}

	def load_pieces(self):
		self.white_pieces_images['Rook'] = pygame.image.load('Media/WRook.png')
		self.white_pieces_images['Bishop'] = pygame.image.load('Media/W_Bishop.png')
		self.white_pieces_images['Knight'] = pygame.image.load('Media/WKnight.png')
		self.white_pieces_images['Queen']	= pygame.image.load('Media/WQueen.png')
		self.white_pieces_images['King'] = pygame.image.load('Media/WKing.png')
		self.white_pieces_images['Pawn'] = pygame.image.load('Media/WPawn.png')
		for piece in self.white_pieces_images:
			self.white_pieces_images[piece] = pygame.transform.scale(self.white_pieces_images[piece],(100,100))

		self.black_pieces_images['Rook'] = pygame.image.load('Media/BRook.png')
		self.black_pieces_images['Bishop'] = pygame.image.load('Media/B_Bishop.png')
		self.black_pieces_images['Knight'] = pygame.image.load('Media/BKnight.png')
		self.black_pieces_images['Queen']	= pygame.image.load('Media/BQueen.png')
		self.black_pieces_images['King'] = pygame.image.load('Media/BKing.png')
		self.black_pieces_images['Pawn'] = pygame.image.load('Media/BPawn.png')
		for piece in self.black_pieces_images:
			self.black_pieces_images[piece] = pygame.transform.scale(self.black_pieces_images[piece],(100,100))


	def init_my_pieces(self):
		pawns = [piece('pawn',[6,0]),piece('pawn',[6,1]),piece('pawn',[6,2]),piece('pawn',[6,3]),piece('pawn',[6,4]),piece('pawn',[6,5]),piece('pawn',[6,6]),piece('pawn',[6,7])]
		for pawn in pawns:
			pawn.image = self.white_pieces_images['Pawn']
		self.mypieces['pawns'] = pawns

		rooks = [piece('rook',[7,0]),piece('rook',[7,7])]
		for rook in rooks:
			rook.image = self.white_pieces_images['Rook']
		self.mypieces['rooks'] = rooks

		bishops = [piece('bishop',[7,2]),piece('bisop',[7,5])]
		for bishop in bishops:
			bishop.image = self.white_pieces_images['Bishop']
		self.mypieces['bishops'] = bishops

		knights = [piece('knight',[7,1]),piece('knight',[7,6])]
		for knight in knights:
			knight.image = self.white_pieces_images['Knight']
		self.mypieces['knights'] = knights

		king = piece('king',[7,4])
		king.image = self.white_pieces_images['King']
		self.mypieces['king'] = [king]

		queen = piece('Queen',[7,3])
		queen.image = self.white_pieces_images['Queen']
		self.mypieces['queen'] = [queen]

	def init_opponent_pieces(self):
		pawns = [piece('pawn',[1,0]),piece('pawn',[1,1]),piece('pawn',[1,2]),piece('pawn',[1,3]),piece('pawn',[1,4]),piece('pawn',[1,5]),piece('pawn',[1,6]),piece('pawn',[1,7])]
		for pawn in pawns:
			pawn.image = self.black_pieces_images['Pawn']
		self.enemy_pieces['pawns'] = pawns

		rooks = [piece('rook',[0,0]),piece('rook',[0,7])]
		for rook in rooks:
			rook.image = self.black_pieces_images['Rook']
		self.enemy_pieces['rooks'] = rooks

		bishops = [piece('bishop',[0,2]),piece('bisop',[0,5])]
		for bishop in bishops:
			bishop.image = self.black_pieces_images['Bishop']
		self.enemy_pieces['bishops'] = bishops

		knights = [piece('knight',[0,1]),piece('knight',[0,6])]
		for knight in knights:
			knight.image = self.black_pieces_images['Knight']
		self.enemy_pieces['knights'] = knights

		king = piece('king',[0,4])
		king.image = self.black_pieces_images['King']
		self.enemy_pieces['king'] = [king]

		queen = piece('Queen',[0,3])
		queen.image = self.black_pieces_images['Queen']
		self.enemy_pieces['queen'] = [queen]


	def update_pieces(self,screen):
		for pieces in self.mypieces:
			for piece in self.mypieces[pieces]:
				screen.blit(piece.image,(self.grid[piece.position[0]][piece.position[1]].xstart,self.grid[piece.position[0]][piece.position[1]].ystart))

		for pieces in self.enemy_pieces:
			for piece in self.enemy_pieces[pieces]:
				screen.blit(piece.image,(self.grid[piece.position[0]][piece.position[1]].xstart,self.grid[piece.position[0]][piece.position[1]].ystart))


def update(Interface,screen,events):
	#Board - Border
    pygame.draw.rect(screen,BLACK,[Interface.xstart,Interface.ystart,Interface.boardwidth,Interface.boardheight],3)
    #Settings Panel - Border 
    pygame.draw.rect(screen,BLACK,[Interface.panel_xstart,Interface.panel_ystart,Interface.panelwidth,Interface.panelheight],2)
    #Captured Pieces - Border
    pygame.draw.rect(screen,BLACK,[Interface.killed_xstart,Interface.killed_ystart,Interface.killed_box_width,Interface.killed_box_height],2)
    #Chat box - Border
    pygame.draw.rect(screen,BLACK,[Interface.chatbox_xstart,Interface.chatbox_ystart,Interface.chatbox_width,Interface.chatbox_height],2)	
    #Player 1 - Border
    pygame.draw.rect(screen,BLACK,[Interface.game_info_box1_coords[0],Interface.game_info_box1_coords[1],Interface.game_info_box1_width,Interface.game_info_box1_height],3)
    #Player 2 - Border
    pygame.draw.rect(screen,BLACK,[Interface.game_info_box2_coords[0],Interface.game_info_box2_coords[1],Interface.game_info_box2_width,Interface.game_info_box2_height],3)
    #Board
    Interface.draw_chess_board()
    #Settings Panel
    pygame.draw.rect(screen,LIGHTBLUE,[Interface.panel_xstart+2.5,Interface.panel_ystart+2.5,Interface.panelwidth-2.5,Interface.panelheight-2.5])
    #Captured Pieces
    pygame.draw.rect(screen,GREEN,[Interface.killed_xstart+2.5,Interface.killed_ystart+2.5,Interface.killed_box_width-2.5,Interface.killed_box_height-2.5])
    #Chat box
    pygame.draw.rect(screen,LIGHTGREEN,[Interface.chatbox_xstart+2.5,Interface.chatbox_ystart+2.5,Interface.chatbox_width-2.5,Interface.chatbox_height-2.5])
    #Chat box text bar
    pygame.draw.rect(screen,WHITE,[Interface.messsage_input_xstart+2.5,Interface.messsage_input_ystart+2.5,Interface.messsage_input_width-2.5,Interface.messsage_input_height-2.5])
    #Chat box text bar - Border
    pygame.draw.rect(screen,BLACK,[Interface.messsage_input_xstart,Interface.messsage_input_ystart,Interface.messsage_input_width,Interface.messsage_input_height],2)
    #screen.blit(W_king_image,(300,690))
    if Interface.cursor_blink():
    	pygame.draw.line(screen,BLACK,(Interface.cursor_coord[0][0],Interface.cursor_coord[0][1]),(Interface.cursor_coord[1][0],Interface.cursor_coord[1][1]),2)
    
    Interface.get_chat_input(events)
    Interface.print_messages()

    pos = pygame.mouse.get_pos()
    if pos[0]>1106 and pos[0]<1506 and pos[1]>730 and pos[1]<770:
    	pygame.mouse.set_visible(False)
    	screen.blit(Cursor_image,(pos[0]-15,pos[1]-15))
    else :
    	pygame.mouse.set_visible(True)



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

