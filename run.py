import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread,Timer
import time
import random
from functions import *
import warnings
from move_functions import Moves_manager, CastleRights
from login_register import Login_Register
from main_menu import *
from configure import *
import os

FONT = pygame.font.SysFont('Arial Bold',80,True)
FONT1 = pygame.font.SysFont('Arial Bold',40,True)

warnings.filterwarnings("ignore")

#1f1f23 - Dark Grey
#9147ff - Purple
#464649 - Grey

class run:
    def __init__(self):
        self.sign_in = Login_Register()
        self.sign_in.window.mainloop()
        try:
            temp = open("Temp","r")
            password = temp.read()
            temp.close()
            os.remove("Temp")
        except:
            pass
        
        self.clock = pygame.time.Clock()
        self.WSIZE = (0,0)
        self.screen = pygame.display.set_mode(self.WSIZE)

        self.width, self.height = 1536,801  
        #self.screen = pygame.display.set_mode((self.width, self.height))

        self.running = True 
        self.icon = pygame.image.load('Media/icon_3.png')
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Chess")

        try:
            self.main_menu = Main_menu(self.screen,self.clock,password)
        except:
            sys.exit()

        # Parameters -> [game grid created earlier,screen,scale for piece images,piece type]
        self.settings = read_settings()

        if self.settings:
            self.ptype = int(self.settings['Piece Appearance'])
            self.ctype = int(self.settings['Board Theme'])

        else:
            update_settings()
            self.settings = read_settings()
            self.ptype = int(self.settings['Piece Appearance'])
            self.ctype = int(self.settings['Board Theme'])

    def init_game(self):
        self.Interface = interface(self.width,self.height,self.main_menu.client,self.ctype)
        self.Interface.screen = self.screen
        self.Interface.generate_board_coordinates()
        self.Interface.generate_settings_panel()
        self.Interface.generate_killed_pieces_box()
        self.Interface.generate_chatbox()
        self.Interface.generate_message_input_box()
        self.Interface.generate_other_functionalities()

        #self.Promoted_Queen = piece('queen', [-1, -1], 'white')

        self.Game = game(self.Interface,self.screen,100 if self.ptype == 1 else None,self.ptype,self.main_menu.client.color)
        self.Game.load_pieces()
        self.Game.moves_manager = Moves_manager(self.Game)
        self.Game.init_my_pieces()
        self.Game.init_opponent_pieces()
        self.Game.get_axes()
        self.Game.main_menu = self.main_menu

        self.checkmate_text = FONT.render("You Lost",True,(255,0,0))
        self.win_text = FONT.render("You won",True,(0,255,0))
        self.game_end = False

        self.I_won = False

        if self.Game.my_piece_color == "White":
            self.Game.myprofimg = pygame.image.load('Media/Whiteplayer.png')
            self.Game.myprofimg = pygame.transform.scale(self.Game.myprofimg,(260,330))
            self.Game.enemyprofimg = pygame.image.load('Media/Blackplayer.png')
            self.Game.enemyprofimg = pygame.transform.scale(self.Game.enemyprofimg,(260,330))
        else:
            self.Game.myprofimg = pygame.image.load('Media/Blackplayer.png')
            self.Game.enemyprofimg = pygame.image.load('Media/Whiteplayer.png')
            self.Game.myprofimg = pygame.transform.scale(self.Game.myprofimg,(260,330))
            self.Game.enemyprofimg = pygame.transform.scale(self.Game.enemyprofimg,(260,330))

        self.Game.myname = FONT1.render(self.main_menu.client.uID,True,(0,0,0))
        self.Game.enemyname = FONT1.render(self.main_menu.client.enemy_name,True,(0,0,0))

    def timer(self):
        self.game_end = True


    def start(self):
        # main loop of the game
        while self.running:
            self.Game.moves_manager.whiteToMove = self.Game.whiteToMove
            self.screen.fill(WHITE)
            events = pygame.event.get()
            pos = pygame.mouse.get_pos()
            for event in events:
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        col = int((pos[0] - self.Interface.xstart) // (self.Interface.boardwidth // 8))
                        row = int((pos[1] - self.Interface.ystart) // (self.Interface.boardheight // 8))
                        print(row,col,pos)
                        if row <= 7 and col <= 7 and row >= 0 and col >= 0 and self.Game.my_turn:
                            self.Game.handle_click_event([row, col])
        
                        if pos[0]<=1255 and pos[0]>=1115 and pos[1]<=73 and pos[1]>=20:
                            self.main_menu.settings_object.music = not self.main_menu.settings_object.music
                            if not self.main_menu.settings_object.music:
                                self.main_menu.settings_object.stop_music()
                            else:
                                self.main_menu.settings_object.play_music()
                            #print("Music")
                        elif pos[0]<=1375 and pos[0]>=1275 and pos[1]<=73 and pos[1]>=20:
                            print("Forfeit")
                            message = {'ID': 60, 'UserID':self.main_menu.client.uID, 'RoomID':None,'Start':None,'Stop':None, 'MoveNo':None,'Turn':None,'Checkmate':True,'Forfeit':True,'Stalemate':False,'Left':False}
                            self.main_menu.client.sock.send(pickle.dumps(message))
                            self.I_won = False
                            self.running = False


                        elif pos[0]<=1505 and pos[0]>=1395 and pos[1]<=73 and pos[1]>=20:
                        	message = {'ID': 60, 'UserID':self.main_menu.client.uID, 'RoomID':None,'Start':None,'Stop':None, 'MoveNo':None,'Turn':None,'Checkmate':True,'Forfeit':True,'Stalemate':False,'Left':True}
                        	self.main_menu.client.sock.send(pickle.dumps(message))
                        	self.I_won = False
                        	self.running = False
        
            # update the screen based on events
            self.Game.update(pygame.mouse.get_pos())

            self.Game.highlight_selected_box()
            self.Game.highlight_legal_moves()
            self.Game.update_pieces()
            self.Game.get_captured_pieces_numbers()

            #if self.Interface.chat_panel.selected == "chat":
            self.Interface.get_chat_input(events)
            self.Interface.print_messages()


            if self.Game.opponent_turn and self.Game.opponent_click and not self.Game.opponent_checkmate and not self.Game.opponent_forfeited and not self.Game.opponent_left and not self.Game.moves_manager.stalemate:
                self.Game.handle_click_event(self.Game.opponent_click)
                self.Game.handle_click_event(self.Game.opponent_coords)
                self.Game.opponent_click = []
                self.Game.opponent_coords = []
                self.Game.opponentclick = []


            # If I get checkmated
            if self.Game.moves_manager.checkmate:
                message = {'ID': 60, 'UserID':self.main_menu.client.uID, 'RoomID':None,'Start':None,'Stop':None, 'MoveNo':None,'Turn':None,'Checkmate':True,'Forfeit':None,'Stalemate':False,'Left':False}
                self.main_menu.client.sock.send(pickle.dumps(message))
                self.I_won = False
                self.running = False

            # If opponent forfeits
            if self.Game.opponent_forfeited:
            	self.I_won = True
            	self.running = False

            # If opponent leaves
            if self.Game.opponent_left:
            	self.I_won = True
            	self.running = False

            # If opponent gets checkmated
            if self.Game.opponent_checkmate:
                self.I_won = True
                self.running = False

            self.clock.tick(60)
            pygame.display.flip()

        win_thread = Timer(5.0,self.timer)
        win_thread.start()
        while not self.game_end:
            self.Game.update(pygame.mouse.get_pos())
            self.Game.update_pieces()
            self.Interface.print_messages()
            if self.main_menu.settings_object.music:
                self.screen.blit(self.Game.music_on_button, (1125, 35))
            else:
                self.screen.blit(self.Game.music_off_button,(1120,35))
            self.screen.blit(self.Game.forfeit_button, (1285, 35))
            self.screen.blit(self.Game.leave_button, (1415, 35))
            if self.I_won:
                self.screen.blit(self.win_text,(530,350))
            else:
                self.screen.blit(self.checkmate_text,(530,350))
            pygame.display.flip()
            self.clock.tick(60)


    def run_game(self):

        while True: 
            return_val = self.main_menu.update()
            if return_val == "game started":
                self.running = True
                self.init_game()
                self.start()
                self.main_menu.client.room_id = None
                self.main_menu.client.color = None
                #self.Interface.receive_thread.join()
                #self.Game.receive_messages.join()
                #del self.Interface
                #del self.Game
            elif return_val == "exit to desktop":
                break
        return
    
Run = run()
Run.run_game()
pygame.quit()

