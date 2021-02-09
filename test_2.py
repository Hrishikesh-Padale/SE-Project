import pygame
from pygame.locals import *
from time import *
import sys

pygame.init()
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (102, 204, 0)
LIGHTBLUE = (51, 153, 255)
BROWN = (153,77,0)
LIGHTBROWN = (255,155,51)
LIGHTGREEN = (102,255,102)
LIGHTNAVY = (153,153,255)
RED = (255,0,0)
 
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
   					pygame.draw.rect(self.screen,LIGHTBROWN,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])
   				else:
   					pygame.draw.rect(self.screen,BROWN,[self.grid[i][j].xstart,self.grid[i][j].ystart,self.boxwidth,self.boxheight])


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

for i in range(8):
	for j in range(8):
		print(Interface.grid[i][j].x,Interface.grid[i][j].y,Interface.grid[i][j].xstart,Interface.grid[i][j].ystart)

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
    pygame.event.pump()
    event = pygame.event.wait()
    if event.type == QUIT:
        running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
    	pos = pygame.mouse.get_pos()
    	col = int((pos[0]-Interface.xstart)//(Interface.boardwidth//8))
    	row = int((pos[1]-Interface.ystart)//(Interface.boardheight//8))
    	print(row,col) 

    pygame.draw.rect(screen,BLACK,[Interface.xstart,Interface.ystart,Interface.boardwidth,Interface.boardheight],3)
    pygame.draw.rect(screen,BLACK,[Interface.panel_xstart,Interface.panel_ystart,Interface.panelwidth,Interface.panelheight],2)
    pygame.draw.rect(screen,BLACK,[Interface.killed_xstart,Interface.killed_ystart,Interface.killed_box_width,Interface.killed_box_height],2)
    pygame.draw.rect(screen,BLACK,[Interface.chatbox_xstart,Interface.chatbox_ystart,Interface.chatbox_width,Interface.chatbox_height],2)
    Interface.draw_chess_board()
    pygame.draw.rect(screen,LIGHTBLUE,[Interface.panel_xstart+2.5,Interface.panel_ystart+2.5,Interface.panelwidth-2.5,Interface.panelheight-2.5])
    pygame.draw.rect(screen,GREEN,[Interface.killed_xstart+2.5,Interface.killed_ystart+2.5,Interface.killed_box_width-2.5,Interface.killed_box_height-2.5])
    pygame.draw.rect(screen,LIGHTGREEN,[Interface.chatbox_xstart+2.5,Interface.chatbox_ystart+2.5,Interface.chatbox_width-2.5,Interface.chatbox_height-2.5])
    screen.blit(W_king_image,(300,690))
    clock.tick(60)
    pygame.display.flip()

pygame.quit()