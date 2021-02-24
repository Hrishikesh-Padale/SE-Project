import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time
import warnings

pygame.init()
warnings.filterwarnings("ignore")

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
        self.max_message_length = 30
        self.old_messages = []
        self.first_msg = 0
        self.last_msg = 0

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
   				if len(self.message)<=35 and bool(event.unicode) and event.key != pygame.K_RETURN:
   					self.message = self.message[:self.cursor_position] + event.unicode + self.message[self.cursor_position:]
   					self.cursor_position += 1
   					self.message_text = FONT.render(self.message,True,BLACK)
   					self.message_rect = self.message_text.get_rect()
   					self.message_rect.center = (self.messsage_input_xstart+5+(self.message_rect.width//2),self.messsage_input_ystart+20)
   					text = FONT.render(self.message[self.cursor_position:],True,BLACK)
   					rect = text.get_rect()
   					self.cursor_coord[0][0] = self.messsage_input_xstart+5+self.message_rect.width-rect.width
   					self.cursor_coord[1][0] = self.cursor_coord[0][0]

   				#to reset cursor position and save the message
   				elif event.key == pygame.K_RETURN and len(self.message)>0:
   					self.last_message_done = False
   					self.message = "Me:"+self.message
   					self.chat_buffer_text.append(self.message)
   					text = FONT.render(self.message,True,BLACK)
   					rect = text.get_rect()
   					self.chat_buffer_graphic.append([text,rect])
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
   					#print(self.chat_buffer_text)

   		try:
   			if len(self.message)>0:
   				self.screen.blit(self.message_text,self.message_rect)
   		except:
   			pass

   		#x = 33
   		#j = 1
   		#if len(self.chat_buffer_text)>0 and not self.last_message_done:
   		#	while len(self.chat_buffer_text[-1])>(j*x):
   		#		self.chat_buffer_text[-1] = self.chat_buffer_text[-1][:(j*x)] + "\n" + self.chat_buffer_text[-1][(j*x):]
   		#		j += 1
   		#	self.last_message_done = True
   		
   		if len(self.message) == 0:
   			self.cursor_coord=[[self.messsage_input_xstart+5,self.messsage_input_ystart+5],[self.messsage_input_xstart+5,self.messsage_input_ystart+35]]

    def print_messages(self):
    	free_space_start = [self.messsage_input_xstart,self.messsage_input_ystart-30]
    	for i in reversed(self.chat_buffer_graphic[self.first_msg:self.last_msg]):
    		i[1].center = (free_space_start[0]+i[1].width//2,free_space_start[1])
    		self.screen.blit(i[0],i[1])
    		free_space_start[1] -= 30


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


W_king_image = pygame.image.load('Media/WKing.png')
W_king_image = pygame.transform.scale(W_king_image,(100,100))
Cursor_image = pygame.image.load('Media/Cursor_type_2.png')
Cursor_image = pygame.transform.scale(Cursor_image,(33,33))

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
    	pygame.draw.line(screen,BLACK,(Interface.cursor_coord[0][0],Interface.cursor_coord[0][1]),(Interface.cursor_coord[1][0],Interface.cursor_coord[1][1]),2)
    Interface.get_chat_input(events)
    Interface.print_messages()
    pos = pygame.mouse.get_pos()
    if pos[0]>1106 and pos[0]<1506 and pos[1]>730 and pos[1]<770:
    	pygame.mouse.set_visible(False)
    	screen.blit(Cursor_image,(pos[0]-15,pos[1]-15))
    else :
    	pygame.mouse.set_visible(True)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
