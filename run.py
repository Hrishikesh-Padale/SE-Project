import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
import time
import random
from functions import *
import warnings
from move_functions import Moves_manager, CastleRights
#from login_register import Login_Register
from main_menu import *

#sign_in = Login()
#sign_in.window.mainloop()


warnings.filterwarnings("ignore")

clock = pygame.time.Clock()
# WSIZE = (0,0)
# screen = pygame.display.set_mode((0,0))
width, height = 1536,801

screen = pygame.display.set_mode((width, height))
running = True

icon = pygame.image.load('Media/icon_3.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Chess")

main_menu = Main_menu(screen,clock)
main_menu.update()

Interface = interface(width, height,main_menu.client.sock)
Interface.screen = screen

Interface.generate_board_coordinates()
Interface.generate_settings_panel()
Interface.generate_killed_pieces_box()
Interface.generate_chatbox()
Interface.generate_message_input_box()
Interface.generate_other_functionalities()

# Parameters -> [game grid created earlier,screen,scale for piece images,piece type]
Game = game(Interface, screen, None, 3)
Game.load_pieces()
Game.moves_manager = Moves_manager(Game)
Game.init_my_pieces()
Game.init_opponent_pieces()
Game.get_axes()

#1f1f23 - Dark Grey
#9147ff - Purple
#464649 - Grey

#print(Interface.chatbox_xstart,Interface.chatbox_ystart,
#     Interface.chatbox_width,Interface.chatbox_height)

# main loop of the game
while running:
    Game.moves_manager.whiteToMove = Game.whiteToMove
    screen.fill(WHITE)
    events = pygame.event.get()
    pos = pygame.mouse.get_pos()
    for event in events:
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                col = int((pos[0] - Interface.xstart) // (Interface.boardwidth // 8))
                row = int((pos[1] - Interface.ystart) // (Interface.boardheight // 8))
                #print(row,col,pos)
                if row <= 7 and col <= 7 and row >= 0 and col >= 0:
                    Game.handle_click_event([row, col])

                if pos[0]<=1255 and pos[0]>=1115 and pos[1]<=73 and pos[1]>=20:
                    print("Music")
                elif pos[0]<=1375 and pos[0]>=1275 and pos[1]<=73 and pos[1]>=20:
                    print("Forfeit")
                elif pos[0]<=1505 and pos[0]>=1395 and pos[1]<=73 and pos[1]>=20:
                    print("Leave")

                elif pos[0]<=1184 and pos[0]>=1104 and pos[1]<=357 and pos[1]>=317:
                    Interface.chat_panel.selected = "chat"
                    #print("chat")
                elif pos[0]<=1265 and pos[0]>=1184 and pos[1]<=357 and pos[1]>=317:
                    Interface.chat_panel.selected = "friends"
                    #print("friends")
                elif pos[0]<=1351 and pos[0]>=1271 and pos[1]<=357 and pos[1]>=317:
                    Interface.chat_panel.selected = "spectators"
                    #print("spectators")
                elif pos[0]<=1436 and pos[0]>=1353 and pos[1]<=357 and pos[1]>=317:
                    Interface.chat_panel.selected = "leaderboard"
                    #print("leaderboard")
                elif pos[0]<=1522 and pos[0]>=1438 and pos[1]<=357 and pos[1]>=317:
                    Interface.chat_panel.selected = "log"
                    #print("log")

                if Interface.chat_panel.selected == "friends":

                    #send email request for invitation to server from here

                    if pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=410 and pos[1]>=385:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=460 and pos[1]>=435:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+1]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+1]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=510 and pos[1]>=485:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+2]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+2]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=560 and pos[1]>=535:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+3]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+3]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=610 and pos[1]>=585:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+4]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+4]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=660 and pos[1]>=635:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+5]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+5]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=710 and pos[1]>=685:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+6]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+6]))
                    elif pos[0]<= 1501 and pos[0]>=1421 and pos[1]<=760 and pos[1]>=735:
                        Interface.chat_panel.invitations_sent[Interface.chat_panel.first+7]=True
                        print("Invited {}".format(Interface.chat_panel.Friends[Interface.chat_panel.first+7]))

            elif Interface.chat_panel.selected == "friends":   
                if pos[0]<=1521 and pos[0]>=1102 and pos[1]<=787.5 and pos[1]>=355:
                  if event.button == 4:
                      #scroll up
                      if Interface.chat_panel.first>0:
                          Interface.chat_panel.first-=1
                          Interface.chat_panel.last-=1
                          Interface.chat_panel.get_lists_pos()
                  elif event.button == 5:
                      #scroll down
                      if Interface.chat_panel.last<len(Interface.chat_panel.Friends):
                          Interface.chat_panel.first+=1
                          Interface.chat_panel.last+=1
                          Interface.chat_panel.get_lists_pos()

    # update the screen based on events

    Game.update(pygame.mouse.get_pos())
    Game.highlight_selected_box()
    Game.highlight_legal_moves()
    Game.update_pieces()
    Game.get_captured_pieces_numbers()
    if Interface.chat_panel.selected == "chat":
        Interface.get_chat_input(events)
        Interface.print_messages()

    # collinearity line
    # pygame.draw.line(screen,RED,(10,775),(7+Interface.boardwidth,775),2)
    #screen.blit(cursor,(pos[0]-27,pos[1]-23))
    # pos = pygame.mouse.get_pos()
    # screen.blit(pygame.transform.scale(pygame.image.load('Media/cursor_2.png'),(90,90)),(pos[0]-27,pos[1]-23))

    '''_____________________Moving piece animation test___________________________'''
    # if start[0]>=stop[0] and start[1]>=stop[1]:								
    #	start[0]-=1														
    #	start[1]-=2															
    #	screen.blit(Game.white_pieces_images['Knight'],(start[0],start[1]))		
    # else:																		
    #	screen.blit(Game.white_pieces_images['Knight'],(stop[0],stop[1]))		
    '''___________________________________________________________________________'''
    
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()
