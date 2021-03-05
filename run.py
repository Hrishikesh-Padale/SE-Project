import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time
import random
from functions import *
import warnings

warnings.filterwarnings("ignore")

clock = pygame.time.Clock()

#fullscreen = int(input("Run in fullscreen?(1/0):"))
#if fullscreen:
#    WSIZE = (0,0)
#    screen = pygame.display.set_mode((0,0))
#    width,height = screen.get_size()
#else:
#    width,height = 1536,801
#    screen = pygame.display.set_mode((width,height))

width,height = 1536,801
screen = pygame.display.set_mode((width,height))
Interface = interface(width,height)
Interface.screen = screen
running = True

icon = pygame.image.load('Media/icon_5.png')
pygame.display.set_icon(icon)
#pygame.display.set_caption("Chess",'Media/icon_5.png')


Interface.generate_board_coordinates()
Interface.generate_settings_panel()
Interface.generate_killed_pieces_box()
Interface.generate_chatbox()
Interface.generate_message_input_box()
Interface.generate_other_functionalities()

Game = game(Interface.grid,screen)
Game.load_pieces()
Game.init_my_pieces()
Game.init_opponent_pieces()


#start = [495,689]
#stop = [204,398]

#main loop of the game
while running:
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
    	if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
            running = False
    	elif event.type == pygame.MOUSEBUTTONDOWN:
    		pos = pygame.mouse.get_pos()
    		col = int((pos[0]-Interface.xstart)//(Interface.boardwidth//8))
    		row = int((pos[1]-Interface.ystart)//(Interface.boardheight//8))
    		#print(row,col,pos)
    		if row <= 7 and col <= 7:
    			Game.handle_click_event((row,col))

    #update the screen based on events
    update(Interface,screen,events)
    screen.blit(Game.white_pieces_images['Bishop'],(495,689))
    Game.highlight_selected_box()
    Game.update_pieces(screen)

    '''_____________________Moving piece animation test___________________________'''
    #if start[0]>=stop[0] and start[1]>=stop[1]:								
    #	start[0]-=3																
    #	start[1]-=3																
    #	screen.blit(Game.white_pieces_images['Bishop'],(start[0],start[1]))		
    #else:																		
    #	screen.blit(Game.white_pieces_images['Bishop'],(stop[0],stop[1]))		
    '''___________________________________________________________________________'''

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
