import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time
import random
from functions import *
import warnings
from move_functions import *
#from main_menu import *

warnings.filterwarnings("ignore")

clock = pygame.time.Clock()
#WSIZE = (0,0)
#screen = pygame.display.set_mode((0,0))
width,height = 1536,801

screen = pygame.display.set_mode((width,height))
Interface = interface(width,height)
Interface.screen = screen
running = True

icon = pygame.image.load('Media/icon_3.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Chess")

#Main_menu = Main_menu(screen)
#Main_menu.update(clock)  

Interface.generate_board_coordinates()
Interface.generate_settings_panel()
Interface.generate_killed_pieces_box()
Interface.generate_chatbox()
Interface.generate_message_input_box()
Interface.generate_other_functionalities()

#Parameters -> [game grid created earlier,screen,scale for piece images,piece type]
Game = game(Interface,screen,None,3)
Game.load_pieces()
Game.moves_manager = Moves_manager()
Game.init_my_pieces()
Game.init_opponent_pieces()
Game.get_axes()

#start = [Game.grid[7][6].xstart+Game.position_adjustment['type3']['WKnight'][0],Game.grid[7][6].ystart+Game.position_adjustment['type3']['WKnight'][1]] 
#stop = [Game.grid[5][5].xstart+Game.position_adjustment['type3']['WKnight'][0],Game.grid[5][5].ystart+Game.position_adjustment['type3']['WKnight'][1]]
#print(start,stop)

#main loop of the game
while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
    	if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            running = False
    	elif event.type == pygame.MOUSEBUTTONDOWN:
    		pos = pygame.mouse.get_pos()
    		col = int((pos[0]-Interface.xstart)//(Interface.boardwidth//8))
    		row = int((pos[1]-Interface.ystart)//(Interface.boardheight//8))
    		#print(row,col,pos)
    		if row <= 7 and col <= 7 and row >= 0 and col >= 0:
    			Game.handle_click_event([row,col])

    #update the screen based on events
    Game.update()
    Game.highlight_selected_box()
    Game.highlight_legal_moves()
    Game.update_pieces()
    if Interface.chat_panel.selected == "chat":
    	Interface.get_chat_input(events)
    	Interface.print_messages()

    #collinearity line
    #pygame.draw.line(screen,RED,(10,775),(7+Interface.boardwidth,775),2)

    #pos = pygame.mouse.get_pos()
    #screen.blit(pygame.transform.scale(pygame.image.load('Media/cursor_2.png'),(90,90)),(pos[0]-27,pos[1]-23))

    '''_____________________Moving piece animation test___________________________'''
    #if start[0]>=stop[0] and start[1]>=stop[1]:								
    #	start[0]-=1														
    #	start[1]-=2															
    #	screen.blit(Game.white_pieces_images['Knight'],(start[0],start[1]))		
    #else:																		
    #	screen.blit(Game.white_pieces_images['Knight'],(stop[0],stop[1]))		
    '''___________________________________________________________________________'''

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
