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

Game = game(Interface.grid)
Game.load_pieces()
Game.init_my_pieces()
Game.init_opponent_pieces()
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
    		print(row,col,pos) 

    #update the screen based on events
    update(Interface,screen,events)
    Game.update_pieces(screen)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
