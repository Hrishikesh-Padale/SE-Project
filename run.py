import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time
import random
from functions import *
from network_client import *

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
Interface.generate_other_functionalities()

W_king_image = pygame.image.load('Media/WKing.png')
W_king_image = pygame.transform.scale(W_king_image,(100,100))
Cursor_image = pygame.image.load('Media/Cursor_type_2.png')
Cursor_image = pygame.transform.scale(Cursor_image,(33,33))


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