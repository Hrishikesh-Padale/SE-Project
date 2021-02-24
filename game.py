import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time

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
FONT = pygame.font.SysFont('freesansbold.ttf', 30)
 
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

    def generate_board_coordinates(self):
        self.xstart = self.width-(self.width*99.5)//100
        self.xend = self.width-(self.width*30)//100
        self.boardwidth = 780
        self.ystart = self.xstart
        self.boardheight = 780
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
    	#for i in range(8):
    	#	for j in range(8):
    	#		print(self.grid[i][j].x,self.grid[i][j].y,self.grid[i][j].xstart,self.grid[i][j].ystart)
   		for i in range(8):
   			for j in range(8):
   				if (i+j)%2 == 1:
   					pygame.draw.rect(self.screen,COLOR2,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])
   				else:
   					pygame.draw.rect(self.screen,COLOR1,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])

    def generate_message_input_box(self):
   		self.messsage_input_xstart = self.chatbox_xstart + 15
   		self.messsage_input_ystart = 730
   		self.messsage_input_width = self.chatbox_width - 30
   		self.messsage_input_height = 40
   		self.message_text_xstart = self.messsage_input_xstart+5
   		self.message_text_ystart = self.messsage_input_ystart+5
   		self.cursor_pos=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]

    def cursor_blink(self):
   		self.current_time = pygame.time.get_ticks()
   		if self.current_time >= self.change_time:
   			self.change_time = self.current_time + self.delay
   			self.cursor_visible = not self.cursor_visible
   		return self.cursor_visible

    def get_chat_input(self,events):
   		for event in events:
   			if event.type == pygame.KEYDOWN:
   				if bool(event.unicode):
   					self.message += event.unicode
   					if len(self.message) < 37:
   						self.message_text = FONT.render(self.message,True,BLACK)
   					else :
   						self.message_text = FONT.render(self.message[len(self.message)-33:],True,BLACK)
   					self.message_rect = self.message_text.get_rect()
   					self.message_rect.center = (self.messsage_input_xstart+5+(self.message_rect.width//2),self.messsage_input_ystart+20)
   					#self.message_rect.center = (self.cursor_pos[0][0]+2,self.cursor_pos[0][1]+15)
   					#self.message_dict[self.message_text] = self.message_rect
   					if len(self.message) < 37:
   						self.cursor_pos[0][0] = self.messsage_input_xstart+5+self.message_rect.width
   						self.cursor_pos[1][0] = self.cursor_pos[0][0]
   					else:
   						self.cursor_pos = [[1494, 735], [1494, 765]]
   					#print(len(self.message),self.cursor_pos)

   				#to reset cursor position and save the message
   				if event.key == pygame.K_RETURN and len(self.message)>0:
   					self.last_message_done = False
   					self.message = "Me:"+self.message
   					self.chat_buffer_text.append(self.message)
   					text = FONT.render(self.message,True,RED)
   					rect = text.get_rect()
   					self.chat_buffer_graphic.append([text,rect])
   					self.message = "" 
   					self.cursor_pos=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]
   		try:
   			if len(self.message)>0:
   				self.screen.blit(self.message_text,self.message_rect)
   			#pygame.draw.line(self.screen,RED,(self.messsage_input_xstart+5+self.message_rect.width,self.messsage_input_ystart+5),(self.messsage_input_xstart+5+self.message_rect.width,self.messsage_input_ystart+35))
   		except:
   			pass

   		x = 33
   		j = 1
   		if len(self.chat_buffer_text)>0 and not self.last_message_done:
   			while len(self.chat_buffer_text[-1])>(j*x):
   				self.chat_buffer_text[-1] = self.chat_buffer_text[-1][:(j*x)] + "\n" + self.chat_buffer_text[-1][(j*x):]
   				j += 1
   			self.last_message_done = True
   			#print(self.chat_buffer_text[-1])
  

    def __str__(self):
        return "screen-width:{} screen-height:{}\nboard-width:{} board-height:{}".format(self.width,self.height,self.boardwidth,self.boardheight)


clock = pygame.time.Clock()
Interface = interface(1536,801)
screen = pygame.display.set_mode((Interface.width,Interface.height))
Interface.screen = screen
running = True

Interface.generate_board_coordinates()
Interface.generate_settings_panel()
Interface.generate_killed_pieces_box()
Interface.generate_chatbox()
Interface.generate_message_input_box()

#for i in range(8):
#	for j in range(8):
#		print(Interface.grid[i][j].x,Interface.grid[i][j].y,Interface.grid[i][j].xstart,Interface.grid[i][j].ystart)

W_king_image = pygame.image.load('Media/WKing.png')
W_king_image = pygame.transform.scale(W_king_image,(100,100))

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



while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
    	if event.type == QUIT:
    	    running = False
    	elif event.type == pygame.MOUSEBUTTONDOWN:
    		pos = pygame.mouse.get_pos()
    		col = int((pos[0]-Interface.xstart)//(Interface.boardwidth//8))
    		row = int((pos[1]-Interface.ystart)//(Interface.boardheight//8))
    		print(row,col,pos) 
    pygame.draw.rect(screen,BLACK,[Interface.xstart,Interface.ystart,Interface.boardwidth,Interface.boardheight],3)
    pygame.draw.rect(screen,BLACK,[Interface.panel_xstart,Interface.panel_ystart,Interface.panelwidth,Interface.panelheight],2)
    pygame.draw.rect(screen,BLACK,[Interface.killed_xstart,Interface.killed_ystart,Interface.killed_box_width,Interface.killed_box_height],2)
    pygame.draw.rect(screen,BLACK,[Interface.chatbox_xstart,Interface.chatbox_ystart,Interface.chatbox_width,Interface.chatbox_height],2)	
    Interface.draw_chess_board()
    pygame.draw.rect(screen,LIGHTBLUE,[Interface.panel_xstart+2.5,Interface.panel_ystart+2.5,Interface.panelwidth-2.5,Interface.panelheight-2.5])
    pygame.draw.rect(screen,GREEN,[Interface.killed_xstart+2.5,Interface.killed_ystart+2.5,Interface.killed_box_width-2.5,Interface.killed_box_height-2.5])
    pygame.draw.rect(screen,LIGHTGREEN,[Interface.chatbox_xstart+2.5,Interface.chatbox_ystart+2.5,Interface.chatbox_width-2.5,Interface.chatbox_height-2.5])
    pygame.draw.rect(screen,WHITE,[Interface.messsage_input_xstart+2.5,Interface.messsage_input_ystart+2.5,Interface.messsage_input_width-2.5,Interface.messsage_input_height-2.5])
    pygame.draw.rect(screen,BLACK,[Interface.messsage_input_xstart,Interface.messsage_input_ystart,Interface.messsage_input_width,Interface.messsage_input_height],2)
    screen.blit(W_king_image,(300,690))
    if Interface.cursor_blink():
    	pygame.draw.line(screen,BLACK,(Interface.cursor_pos[0][0],Interface.cursor_pos[0][1]),(Interface.cursor_pos[1][0],Interface.cursor_pos[1][1]),2)
    Interface.get_chat_input(events)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()