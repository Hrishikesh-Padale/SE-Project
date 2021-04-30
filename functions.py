import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
from socket import *
import time
import random
#from chat_panel import *
from move_functions import Moves_manager, CastleRights
import pickle

captured_piece = None
moved_piece = None

pygame.init()
BLACK = (0, 0, 0)
GRAY = (130, 130, 130)
WHITE = (255, 255, 255)
GREEN = (0, 102, 0)
LIGHTBLUE = (51, 153, 255)
COLOR1 = (48, 128, 42)
COLOR2 = (118, 196, 112)

COLOR3 = (153, 77, 0)
COLOR4 = (255, 155, 51)

COLOR5 = (71, 144, 192)
COLOR6 = (185, 214, 232)

COLOR7 = (105, 105, 105)
COLOR8 = (166, 166, 166)

LIGHTGREEN = (153, 255, 153)
LIGHTNAVY = (153, 153, 255)
RED = (255, 0, 0)

FONT = pygame.font.SysFont('freesansbold.ttf', 25)
FONT1 = pygame.font.SysFont('freesansbold.ttf', 35)
AXIS_COORD_FONT = pygame.font.SysFont('consolas', 25, True)


class box:
    def __init__(self, x, y, xstart, ystart, width, height):
        self.x = x
        self.y = y
        self.xstart = xstart
        self.ystart = ystart
        self.is_empty = True
        self.width = width
        self.height = height
        self.piece = None


class interface:

    def __init__(self, width, height, client, ctype):
        self.width = width
        self.height = height
        self.ctype = ctype

        if self.ctype == 1:
            self.board_colors = (COLOR1, COLOR2)
        elif self.ctype == 2:
            self.board_colors = (COLOR3, COLOR4)
        elif self.ctype == 3:
            self.board_colors = (COLOR5, COLOR6)
        elif self.ctype == 4:
            self.board_colors = (COLOR7, COLOR8)

        self.screen = None
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
        # self.server = '65.0.204.13'
        self.port = 12000

        self.client = client
        self.username = self.client.uID
        # self.connect_to_server()
        self.receive_thread = Thread(target=self.decode_messages)
        self.receive_thread.start()

    def generate_board_coordinates(self):
        self.xstart = self.width * (20 / 100)
        self.ystart = self.height * (0.998 / 100)
        self.boardheight = 780
        self.boardwidth = self.boardheight
        self.xend = self.xstart + self.boardwidth
        self.boxwidth = self.boardwidth // 8
        self.boxheight = self.boardheight // 8
        for row in range(8):
            self.grid.append([])
            for column in range(8):
                self.grid[row].append(box(row, column, int(self.xstart + 2 + (column * self.boxwidth)),
                                          self.ystart + 2 + (row * self.boxheight), self.boxwidth, self.boxheight))

    def generate_settings_panel(self):
        self.panel_xstart = self.xend + self.width * (0.97 / 100)
        self.panel_ystart = self.ystart
        self.panelwidth = (self.width - self.width * (0.97 / 100)) - self.panel_xstart
        self.panelheight = self.height * (9.9 / 100)

    def generate_killed_pieces_box(self):
        self.killed_xstart = self.xend + self.width * (0.97 / 100)
        self.killed_ystart = self.panel_ystart + self.panelheight + self.width * (0.97 / 100)
        self.killed_box_width = self.panelwidth
        self.killed_box_height = self.height * (31 / 100) - 50

    def generate_chatbox(self):
        self.chatbox_xstart = self.xend + self.width * (0.97 / 100)
        self.chatbox_ystart = self.killed_ystart + self.killed_box_height + self.width * (0.97 / 100)
        self.chatbox_width = self.panelwidth
        self.chatbox_height = self.boardheight + self.ystart - self.chatbox_ystart

    def draw_chess_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pygame.draw.rect(self.screen, self.board_colors[0],
                                     [self.grid[i][j].xstart, self.grid[i][j].ystart, self.boxwidth, self.boxheight])
                else:
                    pygame.draw.rect(self.screen, self.board_colors[1],
                                     [self.grid[i][j].xstart, self.grid[i][j].ystart, self.boxwidth, self.boxheight])

    def generate_message_input_box(self):
        self.messsage_input_xstart = self.chatbox_xstart + self.width * (0.97 / 100)
        self.messsage_input_ystart = self.chatbox_ystart + self.chatbox_height - (self.height * (6 / 100))
        self.messsage_input_width = self.chatbox_width - self.width * (1.9 / 100)
        self.messsage_input_height = self.width * (2.6 / 100)
        self.message_text_xstart = self.messsage_input_xstart + self.width * (0.3 / 100)
        self.message_text_ystart = self.messsage_input_ystart + self.height * (0.6 / 100)
        self.cursor_coord = [[self.messsage_input_xstart + self.width * (0.3 / 100),
                              self.messsage_input_ystart + self.height * (0.6 / 100)],
                             [self.messsage_input_xstart + self.width * (0.3 / 100),
                              self.messsage_input_ystart + self.height * (4.4 / 100)]]

    def cursor_blink(self):
        self.current_time = pygame.time.get_ticks()
        if self.current_time >= self.change_time:
            self.change_time = self.current_time + self.delay
            self.cursor_visible = not self.cursor_visible
        return self.cursor_visible

    def get_chat_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if bool(event.unicode) and len(self.message) < self.max_message_length and event.key != pygame.K_RETURN:
                    self.message = self.message[:self.cursor_position] + event.unicode + self.message[
                                                                                         self.cursor_position:]
                    self.cursor_position += 1
                    self.message_text = FONT.render(self.message, True, WHITE)
                    self.message_rect = self.message_text.get_rect()
                    self.message_rect.center = (
                        self.messsage_input_xstart + self.width * (0.3 / 100) + (self.message_rect.width // 2),
                        self.messsage_input_ystart + self.height * (2 / 100))
                    text = FONT.render(self.message[self.cursor_position:], True, BLACK)
                    rect = text.get_rect()
                    self.cursor_coord[0][0] = self.messsage_input_xstart + self.width * (
                            0.3 / 100) + self.message_rect.width - rect.width
                    self.cursor_coord[1][0] = self.cursor_coord[0][0]
                    if self.cursor_coord[0][
                        0] >= self.messsage_input_xstart + self.messsage_input_width - self.width * (0.3 / 100):
                        self.cursor_coord[0][
                            0] = self.messsage_input_xstart + self.messsage_input_width - self.width * (0.3 / 100)
                        self.cursor_coord[1][0] = self.cursor_coord[0][0]

                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(self.message) > 0:
                    self.last_message_done = False
                    self.chat_buffer_text.append("Me:" + self.message)
                    msg = self.message
                    msg = {'ID': 30, 'UserID': self.username, 'Data': msg, 'RoomID': self.client.room_id}
                    # send the text message on socket
                    self.client.sock.send(pickle.dumps(msg))

                    text = FONT.render(self.message, True, WHITE)
                    rect = text.get_rect()
                    username = FONT.render(self.username + ":", True, (0, 255, 0))
                    uname_rect = username.get_rect()
                    self.chat_buffer_graphic.append(([username, uname_rect], [text, rect]))
                    self.message = ""
                    self.cursor_position = 0
                    self.cursor_coord = [[self.messsage_input_xstart + self.width * (0.3 / 100),
                                          self.messsage_input_ystart + self.height * (0.6 / 100)],
                                         [self.messsage_input_xstart + self.width * (0.3 / 100),
                                          self.messsage_input_ystart + self.height * (4.4 / 100)]]
                    self.last_msg += 1
                    if self.last_msg >= 13:
                        self.first_msg += 1

                elif event.key == pygame.K_LEFT and self.cursor_position > 0:
                    self.cursor_position -= 1
                    string_right_to_cursor = self.message[self.cursor_position:]
                    text = FONT.render(string_right_to_cursor, True, BLACK)
                    rect = text.get_rect()
                    # change cursor coordinates
                    self.cursor_coord[0][0] = self.messsage_input_xstart + self.width * (
                            0.3 / 100) + self.message_rect.width - rect.width
                    self.cursor_coord[1][0] = self.cursor_coord[0][0]


                elif event.key == pygame.K_RIGHT and self.cursor_position < len(self.message):
                    self.cursor_position += 1
                    string_left_to_cursor = self.message[:self.cursor_position]
                    text = FONT.render(string_left_to_cursor, True, BLACK)
                    rect = text.get_rect()
                    self.cursor_coord[0][0] = self.messsage_input_xstart + self.width * (0.3 / 100) + rect.width
                    self.cursor_coord[1][0] = self.cursor_coord[0][0]

                elif event.key == pygame.K_BACKSPACE and self.cursor_position > 0:
                    self.cursor_position -= 1
                    deleted_letter = self.message[self.cursor_position]
                    temp = ""
                    for i in range(len(self.message)):
                        if i != self.cursor_position:
                            temp += self.message[i]
                    self.message = temp
                    self.message_text = FONT.render(self.message, True, WHITE)
                    self.message_rect = self.message_text.get_rect()
                    self.message_rect.center = (
                        self.messsage_input_xstart + self.width * (0.3 / 100) + (self.message_rect.width // 2),
                        self.messsage_input_ystart + self.height * (2 / 100))
                    deleted_letter = FONT.render(deleted_letter, True, BLACK)
                    rect = deleted_letter.get_rect()
                    self.cursor_coord[0][0] -= rect.width
                    self.cursor_coord[1][0] = self.cursor_coord[0][0]

        if len(self.message) > 0:
            self.screen.blit(self.message_text, self.message_rect)

        if len(self.message) == 0:
            self.cursor_coord = [[self.messsage_input_xstart + self.width * (0.3 / 100),
                                  self.messsage_input_ystart + self.height * (0.6 / 100)],
                                 [self.messsage_input_xstart + self.width * (0.3 / 100),
                                  self.messsage_input_ystart + self.height * (4.4 / 100)]]

    def print_messages(self):
        free_space_start = [self.messsage_input_xstart, self.messsage_input_ystart - self.height * (3.7 / 100)]
        for i in reversed(self.chat_buffer_graphic[self.first_msg:self.last_msg]):
            i[0][1].center = (free_space_start[0] + i[0][1].width // 2, free_space_start[1])
            i[1][1].center = (free_space_start[0] + i[0][1].width + (i[1][1].width // 2) + 3, free_space_start[1])
            self.screen.blit(i[0][0], i[0][1])
            self.screen.blit(i[1][0], i[1][1])
            free_space_start[1] -= self.height * (3.7 / 100)

    def generate_other_functionalities(self):
        self.game_info_box1_coords = (self.width * (0.65 / 100), self.ystart)
        self.game_info_box1_width = (self.height * (33.7 / 100)) + 10
        self.game_info_box1_height = (self.boardheight // 2) - (self.height * (1.2 / 100))

        self.game_info_box2_coords = (
            self.width * (0.65 / 100), self.ystart + self.game_info_box1_height + (self.height * (1.2 / 100)))
        self.game_info_box2_width = self.game_info_box1_width
        self.game_info_box2_height = (self.boardheight // 2)


    def decode_messages(self):
        while True:
            try:
                # message = self.sock.recv(1024).decode()
                message = self.client.chat_messages.pop()
                if message['ID'] == 30:
                    username, message = message['UserID'], message['Data']
                    if message and username:
                        self.chat_buffer_text.append(message)
                        username = FONT.render(username + ":", True, RED)
                        uname_rect = username.get_rect()
                        message = FONT.render(message, True, WHITE)
                        message_rect = message.get_rect()
                        self.chat_buffer_graphic.append(([username, uname_rect], [message, message_rect]))
                        self.last_msg += 1
                        if self.last_msg >= 10:
                            self.first_msg += 1
                    else:
                        self.chat_buffer_text.append(message)
                        text1 = message.split(" ")[0]
                        text2 = message[len(text1):]
                        text1 = FONT.render(text1, True, BLACK)
                        text2 = FONT.render(text2, True, BLACK)
                        text1_rect = text1.get_rect()
                        text2_rect = text2.get_rect()
                        self.chat_buffer_graphic.append(([text1, text1_rect], [text2, text2_rect]))
                        self.last_msg += 1
                        if self.last_msg >= 10:
                            self.first_msg += 1
            except:
                pass

    def __del__(self):
        print("Interface object deleted")


class Piece(object):
    def __init__(self, name, position, color):
        self.name = name
        self.position = position
        self.image = None
        self.color = color
        self.pos_adjustment = None
        self.is_alive = True
        self.is_at_start = True
        self.locked = True

    def __str__(self):
        return "Name:{}\nPosition:{}\nColor:{}\nAlive:{}".format(self.name, self.position, self.color, self.is_alive)


class game(object):

    def __init__(self, Interface=None, screen=None, sfac=None, piece_type=None, my_piece_color=None):

        self.main_menu = None
        self.my_piece_color = my_piece_color
        self.my_turn = True if self.my_piece_color == 'White' else False
        self.opponent_turn = not self.my_turn
        if self.my_piece_color == "White":
            self.enemy_piece_color = "Black"
        else:
            self.enemy_piece_color = "White"

        self.white_pieces_images = {}
        self.black_pieces_images = {}
        self.captured_pieces = {'wpawn': 0, 'wrook': 0, 'wknight': 0, 'wbishop': 0, 'wqueen': 0,
                                'bpawn': 0, 'brook': 0, 'bknight': 0, 'bbishop': 0, 'bqueen': 0}
        self.captured_pieces_count = {}
        self.piece_type = piece_type
        self.grid = Interface.grid
        self.Interface = Interface
        self.moves_manager = None
        #self.moved_piece = None
        self.myprofimg = None
        self.enemyprofimg = None
        self.myname = None
        self.enemyname = None

        self.selected_square = list()
        self.playerclick = list()
        self.opponentclick = list()

        self.whiteToMove = True #if self.my_piece_color == "White" else False  # modify after pawn work properly

        self.opponent_coords = []
        self.opponent_click = []

        self.currentCastleRights = CastleRights(True, True, True, True)
        self.enemy_pieces = {}
        self.selected_box = None
        self.screen = screen
        self.pieces_scaling_factor = sfac
        self.selected_piece = None
        self.get_captured_pieces_numbers()
        self.get_buttons()
        self.position_adjustment = {
            'type1': {'WPawn': (0, 0), 'WRook': (0, 0),
                      'WKnight': (0, 0), 'WBishop': (0, 0),
                      'WQueen': (0, 0), 'WKing': (0, 0),
                      'BPawn': (0, 0), 'BRook': (0, 0),
                      'BKnight': (0, 0), 'BBishop': (0, 0),
                      'BQueen': (0, 0), 'BKing': (0, 0)},

            'type2': {'WPawn': (Interface.width * (0.19 / 100), 0),
                      'WRook': (Interface.width * (0.4 / 100), Interface.height * (0.62 / 100)),
                      'WKnight': (Interface.width * (0.97 / 100), Interface.height * (0.4 / 100)),
                      'WBishop': (Interface.width * (0.5 / 100), Interface.height * (0.5 / 100)),
                      'WQueen': (Interface.width * (1.1 / 100), -Interface.height * (0.4 / 100)),
                      'WKing': (Interface.width * (0.97 / 100), Interface.height * (0.4 / 100)),
                      'BPawn': (0, 0), 'BRook': (Interface.width * (0.4 / 100), Interface.height * (0.4 / 100)),
                      'BKnight': (Interface.width * (1 / 100), Interface.height * (0.12 / 100)),
                      'BBishop': (Interface.width * (0.65 / 100), Interface.height * (1.1 / 100)),
                      'BQueen': (Interface.width * (1.1 / 100), 0),
                      'BKing': (Interface.width * (0.97 / 100), Interface.height * (0.4 / 100))},

            'type3': {'WPawn': (Interface.width * (1 / 100), Interface.height * (0.62 / 100)),
                      'WRook': (Interface.width * (0.97 / 100), Interface.height * (0.9 / 100)),
                      'WKnight': (Interface.width * (0.97 / 100), Interface.height * (0.5 / 100)),
                      'WBishop': (Interface.width * (0.97 / 100), Interface.height * (0.7 / 100)),
                      'WQueen': (Interface.width * (0.32 / 100), Interface.height * (0.7 / 100)),
                      'WKing': (Interface.width * (0.8 / 100), Interface.height * (0.9 / 100)),
                      'BPawn': (Interface.width * (0.97 / 100), Interface.height * (0.6 / 100)),
                      'BRook': (Interface.width * (0.97 / 100), Interface.height * (0.6 / 100)),
                      'BKnight': (Interface.width * (1 / 100), Interface.height * (0.24 / 100)),
                      'BBishop': (Interface.width * (1 / 100), Interface.height * (0.12 / 100)),
                      'BQueen': (Interface.width * (0.32 / 100), 0),
                      'BKing': (Interface.width * (0.84 / 100), Interface.height * (0.5 / 100))},
        }

        self.opponent_checkmate = False
        self.opponent_forfeited = False
        self.opponent_left = False

        self.receive_messages = Thread(target=self.decode_messages)
        self.receive_messages.start()

    def get_buttons(self):
        self.music_on_button = FONT1.render("Music:ON", True, (0, 180, 0))
        self.music_off_button = FONT1.render("Music:OFF", True, (0, 180, 0))
        self.forfeit_button = FONT1.render("Forfeit", True, (0, 0, 0))
        self.leave_button = FONT1.render("Leave", True, (0, 0, 0))

    def load_pieces(self):
        piece = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Pawn']
        for i in piece:
            self.white_pieces_images[i] = pygame.image.load(f'Media/pieces type {self.piece_type}/W{i}.png')

        if self.pieces_scaling_factor:
            for piece in self.white_pieces_images:
                self.white_pieces_images[piece] = pygame.transform.scale(self.white_pieces_images[piece],
                                                                         (self.pieces_scaling_factor,
                                                                          self.pieces_scaling_factor))

        for i in piece:
            self.black_pieces_images[i] = pygame.image.load(f'Media/pieces type {self.piece_type}/B{i}.png')

        if self.pieces_scaling_factor:
            for piece in self.black_pieces_images:
                self.black_pieces_images[piece] = pygame.transform.scale(self.black_pieces_images[piece],
                                                                         (self.pieces_scaling_factor,
                                                                          self.pieces_scaling_factor))

    def init_my_pieces(self):
        pawns = [Piece('pawn', [6, 0], self.my_piece_color.lower()), Piece('pawn', [6, 1], self.my_piece_color.lower()),
                 Piece('pawn', [6, 2], self.my_piece_color.lower()),
                 Piece('pawn', [6, 3], self.my_piece_color.lower()), Piece('pawn', [6, 4], self.my_piece_color.lower()),
                 Piece('pawn', [6, 5], self.my_piece_color.lower()),
                 Piece('pawn', [6, 6], self.my_piece_color.lower()), Piece('pawn', [6, 7], self.my_piece_color.lower())]

        for pawn in pawns:
            if self.my_piece_color == "White":
                pawn.image = self.white_pieces_images['Pawn']
            else:
                pawn.image = self.black_pieces_images['Pawn']
            pawn.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Pawn'.format(self.my_piece_color[0].upper())]

        self.moves_manager.pieces['pawn'] = pawns
        for i in range(8):
            self.grid[6][i].piece = pawns[i]

        rooks = [Piece('rook', [7, 0], "{}".format(self.my_piece_color.lower())),
                 Piece('rook', [7, 7], self.my_piece_color.lower())]

        for rook in rooks:
            if self.my_piece_color == "White":
                rook.image = self.white_pieces_images['Rook']
            else:
                rook.image = self.black_pieces_images['Rook']

            rook.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Rook'.format(self.my_piece_color[0].upper())]

        self.moves_manager.pieces['rook'] = rooks
        self.grid[7][0].piece = rooks[0]
        self.grid[7][7].piece = rooks[1]

        bishops = [Piece('bishop', [7, 2], self.my_piece_color.lower()),
                   Piece('bishop', [7, 5], self.my_piece_color.lower())]
        for bishop in bishops:
            if self.my_piece_color == "White":
                bishop.image = self.white_pieces_images['Bishop']
            else:
                bishop.image = self.black_pieces_images['Bishop']

            bishop.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Bishop'.format(self.my_piece_color[0].upper())]
        self.moves_manager.pieces['bishop'] = bishops
        self.grid[7][2].piece = bishops[0]
        self.grid[7][5].piece = bishops[1]

        knights = [Piece('knight', [7, 1], self.my_piece_color.lower()),
                   Piece('knight', [7, 6], self.my_piece_color.lower())]
        for knight in knights:
            if self.my_piece_color == "White":
                knight.image = self.white_pieces_images['Knight']
            else:
                knight.image = self.black_pieces_images['Knight']
            knight.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Knight'.format(self.my_piece_color[0].upper())]
        self.moves_manager.pieces['knight'] = knights
        self.grid[7][1].piece = knights[0]
        self.grid[7][6].piece = knights[1]

        if self.my_piece_color == "White":
            king = Piece('king', [7, 4], self.my_piece_color.lower())
            king.image = self.white_pieces_images['King']
            self.grid[7][4].piece = king
        else:
            king = Piece('king', [7, 3], self.my_piece_color.lower())
            king.image = self.black_pieces_images['King']
            self.grid[7][3].piece = king

        king.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
            '{}King'.format(self.my_piece_color[0].upper())]
        self.moves_manager.pieces['king'] = [king]

        if self.my_piece_color == "White":
            queen = Piece('queen', [7, 3], self.my_piece_color.lower())
            queen.image = self.white_pieces_images['Queen']
            self.grid[7][3].piece = queen
        else:
            queen = Piece('queen', [7, 4], self.my_piece_color.lower())
            queen.image = self.black_pieces_images['Queen']
            self.grid[7][4].piece = queen

        queen.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
            '{}Queen'.format(self.my_piece_color[0].upper())]
        self.moves_manager.pieces['queen'] = [queen]

        for i in range(6, 8):
            for j in range(0, 8):
                self.grid[i][j].is_empty = False

        for i in range(2, 6):
            for j in range(0, 8):
                self.grid[i][j].is_empty = True

    def init_opponent_pieces(self):
        pawns = [Piece('pawn', [1, 0], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 1], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 2], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 3], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 4], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 5], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 6], self.enemy_piece_color.lower()),
                 Piece('pawn', [1, 7], self.enemy_piece_color.lower())]
        for pawn in pawns:
            if self.enemy_piece_color == "Black":
                pawn.image = self.black_pieces_images['Pawn']
            else:
                pawn.image = self.white_pieces_images['Pawn']

            pawn.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Pawn'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['pawn'] = pawns
        for i in range(8):
            self.grid[1][i].piece = pawns[i]

        rooks = [Piece('rook', [0, 0], self.enemy_piece_color.lower()),
                 Piece('rook', [0, 7], self.enemy_piece_color.lower())]
        for rook in rooks:
            if self.enemy_piece_color == "Black":
                rook.image = self.black_pieces_images['Rook']
            else:
                rook.image = self.white_pieces_images['Rook']
            rook.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Rook'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['rook'] = rooks
        self.grid[0][0].piece = rooks[0]
        self.grid[0][7].piece = rooks[1]

        bishops = [Piece('bishop', [0, 2], self.enemy_piece_color.lower()),
                   Piece('bishop', [0, 5], self.enemy_piece_color.lower())]
        for bishop in bishops:
            if self.enemy_piece_color == "Black":
                bishop.image = self.black_pieces_images['Bishop']
            else:
                bishop.image = self.white_pieces_images['Bishop']
            bishop.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Bishop'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['bishop'] = bishops
        self.grid[0][2].piece = bishops[0]
        self.grid[0][5].piece = bishops[1]

        knights = [Piece('knight', [0, 1], self.enemy_piece_color.lower()),
                   Piece('knight', [0, 6], self.enemy_piece_color.lower())]

        for knight in knights:
            if self.enemy_piece_color == "Black":
                knight.image = self.black_pieces_images['Knight']
            else:
                knight.image = self.white_pieces_images['Knight']

            knight.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                '{}Knight'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['knight'] = knights
        self.grid[0][1].piece = knights[0]
        self.grid[0][6].piece = knights[1]

        if self.enemy_piece_color == "Black":
            king = Piece('king', [0, 4], self.enemy_piece_color.lower())
            king.image = self.black_pieces_images['King']
            self.grid[0][4].piece = king
        else:
            king = Piece('king', [0, 3], self.enemy_piece_color.lower())
            king.image = self.white_pieces_images['King']
            self.grid[0][3].piece = king

        king.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
            '{}King'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['king'] = [king]

        if self.enemy_piece_color == "White":
            queen = Piece('queen', [0, 4], self.enemy_piece_color.lower())
            queen.image = self.white_pieces_images['Queen']
            self.grid[0][4].piece = queen
        else:
            queen = Piece('queen', [0, 3], self.enemy_piece_color.lower())
            queen.image = self.black_pieces_images['Queen']
            self.grid[0][3].piece = queen

        queen.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
            '{}Queen'.format(self.enemy_piece_color[0].upper())]
        self.moves_manager.enemy_pieces['queen'] = [queen]

        for i in range(0, 2):
            for j in range(0, 8):
                self.grid[i][j].is_empty = False

    def update_pieces(self):
        for pieces in self.moves_manager.pieces:
            for piece in self.moves_manager.pieces[pieces]:
                if piece.locked and piece.is_alive:
                    self.screen.blit(piece.image, (
                        self.grid[piece.position[0]][piece.position[1]].xstart + piece.pos_adjustment[0],
                        self.grid[piece.position[0]][piece.position[1]].ystart + piece.pos_adjustment[1]))

        for pieces in self.moves_manager.enemy_pieces:
            for piece in self.moves_manager.enemy_pieces[pieces]:
                if piece.locked and piece.is_alive:
                    self.screen.blit(piece.image, (
                        self.grid[piece.position[0]][piece.position[1]].xstart + piece.pos_adjustment[0],
                        self.grid[piece.position[0]][piece.position[1]].ystart + piece.pos_adjustment[1]))

    # as of now, both white and black pieces can move as per some basic rules.

    def handle_click_event(self,coords):
        # print(self.whiteToMove, self.my_turn)
        # print(self.moves_manager.currentCastleRights.bks, self.moves_manager.currentCastleRights.bqs)
        self.selected_box = self.grid[coords[0]][coords[1]]
        my_color = self.my_piece_color.lower()
        '''
        if self.whiteToMove and self.my_piece_color == 'White':
            my_color = "white"
            enemy_color = "black"
        elif not self.whiteToMove and self.my_piece_color == 'Black':
            my_color = "black"
            enemy_color = "white"
        '''
        # print(self.my_turn, end = " - self.my_turn\n")
        # print(self.whiteToMove)
        # print(self.selected_box.piece)

        # if self.my_turn and .....
        if self.my_turn and len(self.playerclick) == 0:  # player clicks on first square
            if self.grid[coords[0]][coords[1]].is_empty == False:  # if the square selected is not empty
                if self.grid[coords[0]][coords[1]].piece.color == my_color:  # player selects his piece
                    self.selected_square = coords
                    self.playerclick.append(self.selected_square)
                    # print(self.playerclick)
                    # print('1')
                    self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                elif (self.grid[coords[0]][
                          coords[1]].piece.color != my_color):  # player selects empty square or opposite piece
                    self.selected_box = None
                    self.playerclick = list()
                    self.selected_square = list()
                    # print('2')
            else:  # if square selected is empty
                self.selected_box = None
                self.playerclick = list()
                self.selected_square = list()
                # print('3')

        # if self.my_turn and .....
        elif self.my_turn and len(self.playerclick) == 1:  # player clicks on second square
            if self.grid[coords[0]][coords[1]].is_empty == False:  # if selected square is not empty
                if self.grid[coords[0]][
                    coords[1]].piece.color == my_color:  # if selected square contains player's piece
                    # print("Hellllo")
                    if self.selected_square == coords:  # if player clicks same square twice ie he's trying to deselect
                        self.selected_square = list()
                        self.playerclick = list()
                        self.selected_box = None
                        # print('4')
                    else:
                        self.selected_square = coords
                        self.playerclick = [self.selected_square]
                        self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                        # for i in self.moves_manager.legal_moves:
                        #    print(i.x, i.y, end="i.x, i.y")

                elif self.grid[coords[0]][coords[1]].piece.color != my_color:
                    if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                        # print(self.moves_manager.selected_piece)
                        print("1")


                        message = {'ID': 60, 'UserID': self.Interface.username, 'RoomID': self.Interface.client.room_id,
                                   'Start': self.playerclick[0],#Rutvik
                                   'Stop': coords, 'MoveNo': self.moves_manager.moves_count,
                                   'Turn': "white" if self.my_piece_color == "Black" else "black",'Checkmate':False,'Forfeit':False,'Stalemate':False,'Left':False}
                        # send the move message to all other users
                        self.Interface.client.sock.send(pickle.dumps(message))
                        self.opponent_turn = True
                        self.my_turn = False
                        self.move(self.grid[self.playerclick[0][0]][self.playerclick[0][1]].piece, coords, self.grid,
                                  self.position_adjustment['type{}'.format(self.piece_type)][
                                      self.moves_manager.adjustment_dictionary_name])
                        
                        #print("My pawns")
                        #for move in self.moves_manager.pieces['pawn']:
                        #    print(move.position,end = " ")
                        #print("Enemy pawns")
                        #for move in self.moves_manager.enemy_pieces['pawn']:
                        #    print(move.position,end = " ")

                        # print('6')
                        self.selected_square = list()
                        self.playerclick = list()
                        #############################print(self.moves_manager.checks, end = " ")
                        self.whiteToMove = not self.whiteToMove
                        if self.whiteToMove:
                            self.moves_manager.moves_count += 1
                    else:
                        self.selected_square = list()
                        self.playerclick = list()
                        self.selected_box = None


            else:
                if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                    # print(self.moves_manager.selected_piece)
                    print("2")
                    message = {'ID': 60, 'UserID': self.Interface.username, 'RoomID': self.Interface.client.room_id,
                               'Start': self.playerclick[0],#Rutvik
                               'Stop': coords, 'MoveNo': self.moves_manager.moves_count,
                               'Turn': "white" if self.my_piece_color == "Black" else "black",'Checkmate':False,'Forfeit':False,'Stalemate':False,'Left':False}
                    # send the move message to all other users
                    self.Interface.client.sock.send(pickle.dumps(message))
                    self.opponent_turn = True
                    self.my_turn = False
                    self.move(self.grid[self.playerclick[0][0]][self.playerclick[0][1]].piece, coords, self.grid,
                              self.position_adjustment['type{}'.format(self.piece_type)][
                                  self.moves_manager.adjustment_dictionary_name])

                    #print("My pawns")
                    #    for move in self.moves_manager.pieces['pawn']:
                    #        print(move.position,end = " ")               
                    #print("Enemy pawns")
                    #for move in self.moves_manager.enemy_pieces['pawn']:
                    #    print(move.position,end = " ")

                    # print('7')
                    self.selected_square = list()
                    self.playerclick = list()
                    self.whiteToMove = not self.whiteToMove
                    if self.whiteToMove:
                        self.moves_manager.moves_count += 1
                else:
                    self.selected_square = list()
                    self.playerclick = list()
                    self.selected_box = None

            print("Black -- legal moves",self.moves_manager.legal_moves)

        elif self.my_turn:
            self.selected_box = None
            self.selected_square = []
            self.playerclick = list()
            self.selected_square = list()
            self.moves_manager.legal_moves = []
            self.moves_manager.selected_piece = None
            # print('8')

        print(len(self.opponentclick),self.selected_square,coords,self.opponent_turn)
        if self.opponent_turn and len(self.opponentclick) == 0:  # player clicks on first square
            #print("True 1")
            if self.grid[coords[0]][coords[1]].is_empty == False:  # if the square selected is not empty
                self.selected_square = coords
                print("selected sq",self.selected_square)
                self.opponentclick.append(self.selected_square)
                # print(self.playerclick)
                # print('1')

        elif self.opponent_turn and len(self.opponentclick) == 1:  # player clicks on second square
            #print("True 2")
            if self.grid[coords[0]][coords[1]].is_empty == False:  # if selected square is not empty
                if self.grid[coords[0]][coords[1]].piece.color == my_color:
                    # print(self.moves_manager.selected_piece)
                    self.opponent_turn =False
                    self.my_turn = True
                    print("From opponent move:",self.opponent_turn)
                    adjustment_name = self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.color[0].upper()+ self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.name[0].upper() + self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.name[1:]
                    self.move(self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece, coords, self.grid,
                              self.position_adjustment['type{}'.format(self.piece_type)][
                                  adjustment_name])

                        # print('6')
                    self.selected_square = list()
                    self.opponentclick = list()
                    

            else:
                    # print(self.moves_manager.selected_piece)
                print("3")
                self.opponent_turn =False
                self.my_turn = True
                print("From opponent move:",self.opponent_turn)
                adjustment_name = self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.color[0].upper() + self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.name[0].upper() + self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece.name[1:]
                self.move(self.grid[self.opponentclick[0][0]][self.opponentclick[0][1]].piece, coords, self.grid,
                          self.position_adjustment['type{}'.format(self.piece_type)][
                              adjustment_name])

                # print('7')
                self.selected_square = list()
                self.playerclick = list()
                #self.whiteToMove = not self.whiteToMove
                #if self.whiteToMove:
                #    self.moves_manager.moves_count += 1

        elif self.opponent_turn:
            self.selected_box = None
            self.opponentclick = list()
            self.selected_square = list()
            self.moves_manager.legal_moves = []
            self.moves_manager.selected_piece = None
            # print('8')

    def highlight_selected_box(self):
        if self.selected_box:
            pygame.draw.rect(self.screen, (0, 255, 0),
                             [self.selected_box.xstart, self.selected_box.ystart, self.selected_box.width,
                              self.selected_box.height], 3)

    def highlight_legal_moves(self):
        if self.selected_box:
            if self.moves_manager.legal_moves:
                for i in self.moves_manager.legal_moves:
                    pygame.draw.rect(self.screen, (0, 255, 0), [i.xstart, i.ystart, i.width, i.height], 4)

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def chess_notation(self, piece, destination, board):
        if piece.color == 'white':
            print(self.moves_manager.moves_count, end=" ")
        if piece.name == 'pawn':
            if board[destination[0]][destination[1]].is_empty == True:
                return self.rank_file(destination[0], destination[1])
            else:
                return self.cols_to_files[piece.position[0]] + "x" + self.rank_file(destination[0], destination[1])
        elif piece.name == 'knight':
            if board[destination[0]][destination[1]].is_empty == True:
                return "N" + self.rank_file(destination[0], destination[1])
            else:
                return "Nx" + self.rank_file(destination[0], destination[1])
        elif piece.name == 'king':
            if board[destination[0]][destination[1]].is_empty == True:
                if self.my_piece_color == 'White':
                    if (piece.position == [7, 4] and destination == [7, 6]):
                        return "0-0"
                    elif (piece.position == [7, 4] and destination == [7, 2]):
                        return "0-0-0"
                elif self.my_piece_color == 'Black':
                    if (piece.position == [7, 3] and destination == [7, 1]):
                        return "0-0"
                    elif (piece.position == [7, 3] and destination == [7, 5]):
                        return "0-0-0"
                else:
                    return piece.name[:1].upper() + self.rank_file(destination[0], destination[1])
            else:
                return piece.name[:1].upper() + "x" + self.rank_file(destination[0], destination[1])
        else:
            if board[destination[0]][destination[1]].is_empty == True:
                return piece.name[:1].upper() + self.rank_file(destination[0], destination[1])
            else:
                return piece.name[:1].upper() + "x" + self.rank_file(destination[0], destination[1])

    def rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def get_move_type(self, source, destination):
        # print(source,destination)
        # type  value
        # [+,+] - 1
        # [+,-] - 2
        # [-,+] - 3
        # [-,-] - 4
        # [+,0] - 5
        # [0,+] - 6
        # [-,0] - 7
        # [0,-] - 8
        if destination[0] < source[0] and destination[1] > source[1]:
            return 1
        elif destination[0] > source[0] and destination[1] > source[1]:
            return 2
        elif destination[0] < source[0] and destination[1] < source[1]:
            return 3
        elif destination[0] > source[0] and destination[1] < source[1]:
            return 4
        elif destination[0] == source[0] and destination[1] > source[1]:
            return 5
        elif destination[0] < source[0] and destination[1] == source[1]:
            return 6
        elif destination[0] == source[0] and destination[1] < source[1]:
            return 7
        elif destination[0] > source[0] and destination[1] == source[1]:
            return 8

    def update_castling_rights(self, moved_piece):
        if not self.my_turn:
            if moved_piece.color == 'white':
                if moved_piece.name == 'king':
                    self.currentCastleRights.wks = False
                    self.currentCastleRights.wqs = False

                elif moved_piece.name == 'rook':
                    if moved_piece.position[0] == 7 and moved_piece.position[1] == 0:
                        self.currentCastleRights.wqs = False
                    elif moved_piece.position[0] == 7 and moved_piece.position[1] == 7:
                        self.currentCastleRights.wks = False

            else:
                if moved_piece.name == 'king':
                    self.currentCastleRights.bks = False
                    self.currentCastleRights.bqs = False

                elif moved_piece.name == 'rook':
                    if moved_piece.position[0] == 7 and moved_piece.position[1] == 0:
                        self.currentCastleRights.bks = False
                    elif moved_piece.position[0] == 7 and moved_piece.position[1] == 7:
                        self.currentCastleRights.bqs = False


        else:
            if moved_piece.color == 'white':
                if moved_piece.name == 'king':
                    self.currentCastleRights.wks = False
                    self.currentCastleRights.wqs = False

                elif moved_piece.name == 'rook':
                    if moved_piece.position[0] == 0 and moved_piece.position[1] == 0:
                        self.currentCastleRights.wks = False
                    elif moved_piece.position[0] == 0 and moved_piece.position[1] == 7:
                        self.currentCastleRights.wqs = False

            else:
                if moved_piece.name == 'king':
                    self.currentCastleRights.bks = False
                    self.currentCastleRights.bqs = False

                elif moved_piece.name == 'rook':
                    if moved_piece.position[0] == 7 and moved_piece.position[1] == 0:
                        self.currentCastleRights.bqs = False
                    elif moved_piece.position[0] == 0 and moved_piece.position[1] == 7:
                        self.currentCastleRights.bks = False



    def move(self, piece, destination, board, adjustment):
        global moved_piece,captured_piece_num,captured_piece
        #self.moves_manager.enpassant_captured_piece = None
        # self.moves_manager.enpassant_sq = list()
        # get start and stop positions
        #print("Piece capture:",self.grid[destination[0]][destination[1]].piece,self.grid[destination[0]][destination[1]].is_empty)
        move_type = self.get_move_type(piece.position, destination)
        # print(move_type)
        start = [board[piece.position[0]][piece.position[1]].xstart + adjustment[0],
                 board[piece.position[0]][piece.position[1]].ystart + adjustment[1]]

        stop = [board[destination[0]][destination[1]].xstart + adjustment[0],
                board[destination[0]][destination[1]].ystart + adjustment[1] + 1]

        # print(self.chess_notation(piece, destination, board), end = " ")
        moved_piece = piece
        self.update_castling_rights(moved_piece)

        # pawn promotion condition
        print(piece,destination)

        if (piece.name == 'pawn' and piece.color == self.my_piece_color.lower() and piece.position[0] == 1 and destination[0] == 0) or (
                piece.name == 'pawn' and piece.color != self.my_piece_color.lower() and piece.position[0] == 6 and destination[
            0] == 7
        ):
            self.moves_manager.promotion = True

        # enpassant condition generation
        #self.moves_manager.enpassant = False
        #if moved_piece.name == 'pawn' and abs(moved_piece.position[0] - destination[0]) == 2:
        #    self.moves_manager.enpassant_sq = list()
        #    if moved_piece.position[1] + 1 <= 7:
        #        if self.grid[destination[0]][destination[1] + 1].is_empty == False:
        #            pic = self.grid[destination[0]][destination[1] + 1].piece
        #            if pic.name == 'pawn' and pic.color != moved_piece.color:
        #                self.moves_manager.enpassant = True
        #                self.moves_manager.enpassant_sq.append([pic.position, destination, [
        #                    moved_piece.position[0] - pic.position[0], moved_piece.position[1] - pic.position[1]]])
        #    if moved_piece.position[1] + 1 >= 0:
        #        if self.grid[destination[0]][destination[1] - 1].is_empty == False:
        #            pic = self.grid[destination[0]][destination[1] - 1].piece
        #            if pic.name == 'pawn' and pic.color != moved_piece.color:
        #                self.moves_manager.enpassant = True
        #                self.moves_manager.enpassant_sq.append([pic.position, destination, [
        #                    moved_piece.position[0] - pic.position[0], moved_piece.position[1] - pic.position[1]]])

        # setting capture in enpassant
        # if piece.name == 'pawn' and self.grid[destination[0]][destination[1]].is_empty == True and [abs(
        #         piece.position[0] - destination[0]), abs(piece.position[1] - destination[1])] == [1, 1]:
        #     self.moves_manager.enpassant_captured_piece = self.grid[self.moves_manager.enpassant_sq[0][1][0]][
        #         self.moves_manager.enpassant_sq[0][1][1]].piece
        #     captured_piece = self.moves_manager.enpassant_captured_piece
        #     # print(captured_piece)
        #     if captured_piece.color == 'white':
        #         for i in range(len(self.moves_manager.pieces[captured_piece.name])):
        #             if self.moves_manager.pieces[captured_piece.name][i].position == self.moves_manager.enpassant_sq[0][
        #                 1]:
        #                 captured_piece_num = i
        #                 # self.moves_manager.pieces[captured_piece.name][i].position = [-1,-1]
        #                 break

        #     else:
        #         for i in range(len(self.moves_manager.enemy_pieces[captured_piece.name])):
        #             if self.moves_manager.enemy_pieces[captured_piece.name][i].position == \
        #                     self.moves_manager.enpassant_sq[0][1]:
        #                 captured_piece_num = i
        #                 # self.moves_manager.enemy_pieces[captured_piece.name][i].position = [-1, -1]
        #                 break

        #    self.captured_pieces[captured_piece.color[:1] + captured_piece.name] += 1

        #    self.moves_manager.enpassant_sq = list()

        # set the current box of grid to empty
        self.grid[piece.position[0]][piece.position[1]].is_empty = True

        if self.grid[destination[0]][
            destination[1]].is_empty == False:  # destination square non-empty means definitely contains black piece
            captured_piece = self.grid[destination[0]][destination[1]].piece
            #print("capture condition:",self.captured_piece)
            '''
            setting position of captured piece to [-1,-1] because 
            [-1,-1] doesn't exist on the grid and so does the captured piece
            '''
            if not self.my_turn:
                for i in range(len(self.moves_manager.enemy_pieces[captured_piece.name])):
                    if self.moves_manager.enemy_pieces[captured_piece.name][i].position == destination:
                        captured_piece_num = i
                        #            #self.moves_manager.enemy_pieces[captured_piece.name][i].position = [-1, -1]
                        break
            else:
                for i in range(len(self.moves_manager.pieces[captured_piece.name])):
                    if self.moves_manager.pieces[captured_piece.name][i].position == destination:
                        captured_piece_num = i
                        #            #self.moves_manager.enemy_pieces[captured_piece.name][i].position = [-1, -1]
                        break

            #print(self.captured_piece)

            self.captured_pieces[captured_piece.color[:1] + captured_piece.name] += 1

        #else:
        #    captured_piece = self.moves_manager.enpassant_captured_piece
        # print(captured_piece)
        # '''
        self.grid[destination[0]][destination[1]].piece = piece

        # moving rook while castling
        if piece.name == 'king' and not self.my_turn:
            if self.my_piece_color == 'White':
                if piece.position == [7, 4]:
                    if destination == [7, 6]:  # white king-side castling
                        castling_rook = self.grid[7][7].piece
                        self.grid[7][7].is_empty = True
                        self.grid[7][5].is_empty = False
                        self.grid[7][5].piece = castling_rook
                        self.grid[7][5].piece.position = [7, 5]
                        for i in range(len(self.moves_manager.pieces['rook'])):
                            if self.moves_manager.pieces['rook'][i].position == [7, 7]:
                                self.moves_manager.pieces['rook'][i].position = [7, 5]
                                break
                    elif destination == [7, 2]:  # white queen-side castling
                        castling_rook = self.grid[7][0].piece
                        self.grid[7][0].is_empty = True
                        self.grid[7][3].is_empty = False
                        self.grid[7][3].piece = castling_rook
                        self.grid[7][3].piece.position = [7, 3]
                        for i in range(len(self.moves_manager.pieces['rook'])):
                            if self.moves_manager.pieces['rook'][i].position == [7, 0]:
                                self.moves_manager.pieces['rook'][i].position = [7, 3]
                                break
            else:
                if piece.position == [7, 3]:
                    if destination == [7, 1]:  # black king-side castling
                        castling_rook = self.grid[7][0].piece
                        self.grid[7][0].is_empty = True
                        self.grid[7][2].is_empty = False
                        self.grid[7][2].piece = castling_rook
                        self.grid[7][2].piece.position = [7, 2]
                        for i in range(len(self.moves_manager.pieces['rook'])):
                            if self.moves_manager.pieces['rook'][i].position == [7, 0]:
                                self.moves_manager.pieces['rook'][i].position = [7, 2]
                                break
                    elif destination == [7, 5]:  # black queen-side castling
                        castling_rook = self.grid[7][7].piece
                        self.grid[7][7].is_empty = True
                        self.grid[7][4].is_empty = False
                        self.grid[7][4].piece = castling_rook
                        self.grid[7][4].piece.position = [7, 4]
                        for i in range(len(self.moves_manager.pieces['rook'])):
                            if self.moves_manager.pieces['rook'][i].position == [7, 7]:
                                self.moves_manager.pieces['rook'][i].position = [7, 4]
                                break

        else:
            if self.my_piece_color == 'White':
                if piece.position == [0, 4]:
                    if destination == [0, 6]:  # opponent's king-side castling
                        castling_rook = self.grid[0][7].piece
                        self.grid[0][7].is_empty = True
                        self.grid[0][5].is_empty = False
                        self.grid[0][5].piece = castling_rook
                        self.grid[0][5].piece.position = [0, 5]
                        for i in range(len(self.moves_manager.enemy_pieces['rook'])):
                            if self.moves_manager.enemy_pieces['rook'][i].position == [0, 7]:
                                self.moves_manager.enemy_pieces['rook'][i].position = [0, 5]
                                break
                    elif destination == [0, 2]:  # opponent's queen-side castling
                        castling_rook = self.grid[0][0].piece
                        self.grid[0][0].is_empty = True
                        self.grid[0][3].is_empty = False
                        self.grid[0][3].piece = castling_rook
                        self.grid[0][3].piece.position = [0, 3]
                        for i in range(len(self.moves_manager.enemy_pieces['rook'])):
                            if self.moves_manager.enemy_pieces['rook'][i].position == [0, 0]:
                                self.moves_manager.enemy_pieces['rook'][i].position = [0, 3]
                                break
            else:
                if piece.position == [0, 3]:
                    if destination == [0, 1]:  # opponent's king-side castling
                        castling_rook = self.grid[0][0].piece
                        self.grid[0][0].is_empty = True
                        self.grid[0][2].is_empty = False
                        self.grid[0][2].piece = castling_rook
                        self.grid[0][2].piece.position = [0, 2]
                        for i in range(len(self.moves_manager.enemy_pieces['rook'])):
                            if self.moves_manager.enemy_pieces['rook'][i].position == [0, 0]:
                                self.moves_manager.enemy_pieces['rook'][i].position = [0, 2]
                                break
                    elif destination == [0, 5]:  # opponent's queen-side castling
                        castling_rook = self.grid[0][7].piece
                        self.grid[0][7].is_empty = True
                        self.grid[0][4].is_empty = False
                        self.grid[0][4].piece = castling_rook
                        self.grid[0][4].piece.position = [0, 4]
                        for i in range(len(self.moves_manager.enemy_pieces['rook'])):
                            if self.moves_manager.enemy_pieces['rook'][i].position == [0, 7]:
                                self.moves_manager.enemy_pieces['rook'][i].position = [0, 4]
                                break

        # unlock the piece so that update_pieces function does not show it on screen when it is moving
        piece.locked = False
        # moving piece
        while True:
            # keep updating the screen and pieces while moving piece
            self.update(pygame.mouse.get_pos())
            self.update_pieces()
            self.Interface.print_messages()
            # add animation conditions for different pieces

            # diagonal up right
            if move_type == 1 and piece.name in ['pawn', 'bishop', 'queen', 'king']:
                if start[0] <= stop[0] and start[1] >= stop[1]:
                    start[0] += 6
                    start[1] -= 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # diagonal down right
            elif move_type == 2 and piece.name in ['pawn', 'bishop', 'queen', 'king']:
                if start[0] <= stop[0] and start[1] <= stop[1]:
                    start[0] += 6
                    start[1] += 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # diagonal up left
            elif move_type == 3 and piece.name in ['pawn', 'bishop', 'queen', 'king']:
                if start[0] >= stop[0] and start[1] >= stop[1]:
                    start[0] -= 6
                    start[1] -= 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # diagonal down left
            elif move_type == 4 and piece.name in ['pawn', 'bishop', 'queen', 'king']:
                if start[0] >= stop[0] and start[1] <= stop[1]:
                    start[0] -= 6
                    start[1] += 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # straight upward
            elif move_type == 6 and piece.name in ['king', 'pawn', 'queen', 'rook']:
                if start[1] >= stop[1]:
                    start[1] -= 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # straight downward
            elif move_type == 8 and piece.name in ['king', 'pawn', 'queen', 'rook']:
                if start[1] <= stop[1]:
                    start[1] += 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            elif move_type == 5 and piece.name in ['king', 'queen', 'rook']:
                if start[0] <= stop[0]:
                    start[0] += 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    piece.locked = True
                    break

            elif move_type == 7 and piece.name in ['king', 'queen', 'rook']:
                if start[0] >= stop[0]:
                    start[0] -= 6
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    piece.locked = True
                    break

            ########################################### Movement of Knights ########################################################
            # upwards right
            elif move_type == 1 and "knight" == piece.name:
                if start[0] <= stop[0] and start[1] >= stop[1]:
                    if abs(piece.position[0] - destination[0]) == 2 and abs(
                            piece.position[1] - destination[1]) == 1:
                        start[0] += 2
                        start[1] -= 4
                    else:
                        start[0] += 4
                        start[1] -= 2
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

                # downward right
            elif move_type == 2 and "knight" == piece.name:
                if start[0] <= stop[0] and start[1] <= stop[1]:
                    if abs(piece.position[0] - destination[0]) == 1 and abs(piece.position[1] - destination[1]) == 2:
                        start[0] += 4
                        start[1] += 2
                    else:
                        start[0] += 2
                        start[1] += 4
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

            # upward left
            elif move_type == 3 and "knight" == piece.name:
                if start[0] >= stop[0] and start[1] >= stop[1]:
                    if abs(piece.position[0] - destination[0]) == 1 and abs(piece.position[1] - destination[1]) == 2:
                        start[0] -= 4
                        start[1] -= 2
                    else:
                        start[0] -= 2
                        start[1] -= 4
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break


            # downward left
            elif move_type == 4 and "knight" == piece.name:
                if start[0] >= stop[0] and start[1] <= stop[1]:
                    if abs(piece.position[0] - destination[0]) == 1 and abs(piece.position[1] - destination[1]) == 2:
                        start[0] -= 4
                        start[1] += 2
                    else:
                        start[0] -= 2
                        start[1] += 4
                    self.screen.blit(piece.image, (start[0], start[1]))
                    pygame.display.flip()
                else:
                    piece.position = destination
                    # self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                    # self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                    # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                    piece.locked = True
                    break

        if self.moves_manager.promotion:
            promotedpiece = 'Queen'
            #promoted_piece = Queen / Rook / Bishop / Knight
            if self.grid[destination[0]][destination[1]].is_empty == False:
                self.grid[destination[0]][destination[1]].piece.is_alive = False

            if not self.my_turn:
                #Queen promoted from my_turn condition
                #Promoted queen's color
                Promoted_Piece = Piece('queen', destination, 'white')
                if self.my_piece_color == 'Black':
                    Promoted_Piece.color = 'black'
                Promoted_Piece.image = self.white_pieces_images[promotedpiece]
                Promoted_Piece.pos_adjustment = self.position_adjustment['type3'][
                self.my_piece_color[0] + promotedpiece]
                self.moves_manager.pieces[promotedpiece.lower()].append(Promoted_Piece)
            else:
                Promoted_Piece = Piece('queen', destination, 'white')
                Promoted_Piece.image = self.black_pieces_images[promotedpiece]
                Promoted_Piece.pos_adjustment = self.position_adjustment['type3'][
                    self.enemy_piece_color[0] + promotedpiece]
                if self.my_piece_color == 'White':
                    Promoted_Piece.color = 'black'
                self.moves_manager.enemy_pieces[promotedpiece.lower()].append(Promoted_Piece)

            '''
                        if self.my_piece_color == 'White':
                Promoted_Piece.image = self.white_pieces_images[promotedpiece]
                Promoted_Piece.pos_adjustment = self.position_adjustment['type3'][self.my_piece_color[0] + promotedpiece]
                self.moves_manager.pieces[promotedpiece.lower()].append(Promoted_Piece)
            elif self.my_piece_color == 'Black':
                Promoted_Piece.image = self.black_pieces_images[promotedpiece]
                Promoted_Piece.pos_adjustment = self.position_adjustment['type3'][self.my_piece_color[0] + promotedpiece]
                Promoted_Piece.color = 'black'
                self.moves_manager.pieces[promotedpiece.lower()].append(Promoted_Piece)
            '''
            #print(Promoted_Piece)
            #self.moves_manager.promotion = True
            self.grid[piece.position[0]][piece.position[1]].is_empty = True
            #self.update_pieces()
            self.grid[destination[0]][destination[1]].piece = Promoted_Piece
            #Promoted_Queen.locked = True
            #self.screen.blit(Promoted_Queen.image, (self.grid[destination[0]][destination[1]].xstart + Promoted_Queen.pos_adjustment[0],
            # self.grid[destination[0]][destination[1]].ystart + Promoted_Queen.pos_adjustment[1]))
            #self.update_pieces()
            #pygame.display.flip()

        #print(captured_piece)
        if captured_piece:

            # if captured_piece.color == 'white':
            #    self.moves_manager.pieces[captured_piece.name][captured_piece_num].is_alive = False
            # else:
            #    self.moves_manager.enemy_pieces[captured_piece.name][captured_piece_num].is_alive = False

            #print("In actual capturing",captured_piece)
            if not self.my_turn:
                self.moves_manager.enemy_pieces[captured_piece.name][captured_piece_num].is_alive = False
            else:
                self.moves_manager.pieces[captured_piece.name][captured_piece_num].is_alive = False

            adjustment = self.position_adjustment['type{}'.format(self.piece_type)][
                captured_piece.color[0].upper() + captured_piece.name[0].upper() + captured_piece.name[1:]]
            start = [board[piece.position[0]][piece.position[1]].xstart + adjustment[0],
                     board[piece.position[0]][piece.position[1]].ystart + adjustment[1]]
            if captured_piece.name == "pawn" and captured_piece.color == "white":
                stop = [1110, 110]

            elif captured_piece.name == "pawn" and captured_piece.color == "black":
                print("Captured black pawn")
                stop = [1110, 208]

            elif captured_piece.name == "rook" and captured_piece.color == "white":
                stop = [1190, 109]

            elif captured_piece.name == "rook" and captured_piece.color == "black":
                stop = [1190, 206]

            elif captured_piece.name == "queen" and captured_piece.color == "white":
                stop = [1430, 106]

            elif captured_piece.name == "queen" and captured_piece.color == "black":
                stop = [1430, 201]

            elif captured_piece.name == "bishop" and captured_piece.color == "white":
                stop = [1275, 107]

            elif captured_piece.name == "bishop" and captured_piece.color == "black":
                stop = [1275, 203]

            elif captured_piece.name == "knight" and captured_piece.color == "white":
                stop = [1355, 105]

            elif captured_piece.name == "knight" and captured_piece.color == "black":
                stop = [1355, 203]

            dest = [int((stop[0] - self.Interface.xstart) // (self.Interface.boardwidth // 8)),
                    int((stop[1] - self.Interface.ystart) // (self.Interface.boardheight // 8))]

            # print(dest,captured_piece.position)
            if captured_piece.position[0] < dest[1]:
                move_type = "downright"
            elif captured_piece.position[0] == dest[1]:
                move_type = "straight_right"
            else:
                move_type = "upright"

            print("Move type",move_type)
            while True:
                self.screen.fill((255, 255, 255))
                self.update(pygame.mouse.get_pos())
                self.update_pieces()
                self.Interface.print_messages()
                # print(start,stop)
                if move_type == "upright":
                    if start[0] <= stop[0] and start[1] >= stop[1]:
                        start[0] += abs(captured_piece.position[1] - dest[0])+2
                        start[1] -= abs(captured_piece.position[0] - dest[1])+2
                        self.screen.blit(captured_piece.image, (start[0], start[1]))
                        pygame.display.flip()
                    else:
                        break

                elif move_type == "downright":
                    if start[0] <= stop[0] and start[1] <= stop[1]:
                        start[0] += abs(captured_piece.position[1] - dest[0])+2
                        start[1] += abs(captured_piece.position[0] - dest[1])+2
                        self.screen.blit(captured_piece.image, (start[0], start[1]))
                        pygame.display.flip()
                    else:
                        break

                elif move_type == "straight_right":
                    if start[0] <= stop[0]:
                        start[0] += abs(captured_piece.position[1] - dest[0])+2
                        self.screen.blit(captured_piece.image, (start[0], start[1]))
                        pygame.display.flip()
                    else:
                        break

            # print(captured_piece)
        '''
        if captured_piece is not None:
            if captured_piece.color == 'white':
                for i in range(len(self.moves_manager.pieces[captured_piece.name])):
                    if captured_piece.position == self.moves_manager.pieces[captured_piece.name][
                        i].position and self.moves_manager.pieces[captured_piece.name][i].is_alive == False:
                        self.moves_manager.pieces[captured_piece.name].remove(self.moves_manager.pieces[captured_piece.name][
                        i])
                        break
            elif captured_piece.color == 'black':
                for i in range(len(self.moves_manager.enemy_pieces[captured_piece.name])):
                    if captured_piece.position == self.moves_manager.enemy_pieces[captured_piece.name][
                        i].position and self.moves_manager.enemy_pieces[captured_piece.name][i].is_alive == False:
                        self.moves_manager.enemy_pieces[captured_piece.name].remove(self.moves_manager.enemy_pieces[captured_piece.name][
                        i])
                        break
        '''

        if self.moves_manager.promotion:
            self.update_pieces()
            self.screen.blit(Promoted_Piece.image,
                             (self.grid[destination[0]][destination[1]].xstart + Promoted_Piece.pos_adjustment[0],
                              self.grid[destination[0]][destination[1]].ystart + Promoted_Piece.pos_adjustment[1]))

            pygame.display.flip()

        self.moves_manager.promotion = False
        self.moves_manager.selected_piece = None
        self.moves_manager.legal_moves = []
        self.selected_box = None
        self.grid[destination[0]][destination[1]].is_empty = False
        captured_piece = None
        captured_piece_num = None

    def update_castle(self):
        return self.currentCastleRights

    def update_wtm(self):
        return self.whiteToMove

    def decode_messages(self):
        while True:
            try:
                message = self.Interface.client.board_messages.pop()
                if message['ID'] == 60:
                    if message['Start']:
                        start = message['Start']
                        start = [7-start[0],7-start[1]]

                    if message['Stop']:
                        stop = message['Stop']
                        stop = [7 - stop[0], 7 - stop[1]]

                    #print(start,stop)

                    if message['Turn']:
                        self.whiteToMove = True if (
                                    message['Turn'] == "white" and self.my_piece_color == "White") else False
                    
                    try:
                        self.moves_manager.moves_count += 1
                    except:
                        pass

                    try:
                        piece = self.grid[start[0]][start[1]].piece
                    except:
                        pass
                    #print("count:",self.moves_manager.moves_count)
                    try:
                        self.opponentclick = []
                        self.opponent_click = start
                        self.opponent_coords = stop
                    except:
                        pass

                    if bool(message['Checkmate']):
                        self.opponent_checkmate = True

                    elif bool(message['Forfeit']):
                        self.opponent_forfeited = True

                    elif bool(message['Stalemate']):
                        self.stalemate = True

                    elif bool(message['Left']):
                        self.opponent_left = True 

            except:
                pass

    # graphical
    def get_captured_pieces_numbers(self):
        num = FONT.render("0", True, RED)
        rects = [num.get_rect() for i in range(10)]
        rects[0].center = (1170, 183)
        rects[1].center = (1255, 183)
        rects[2].center = (1337, 183)
        rects[3].center = (1420, 183)
        rects[4].center = (1503, 183)
        rects[5].center = (1170, 281)
        rects[6].center = (1255, 281)
        rects[7].center = (1337, 281)
        rects[8].center = (1420, 281)
        rects[9].center = (1503, 281)
        pieces = ['wpawn', 'wrook', 'wbishop', 'wknight', 'wqueen', 'bpawn', 'brook', 'bbishop', 'bknight', 'bqueen']
        for i in range(len(pieces)):
            num = FONT.render(str(self.captured_pieces[pieces[i]]), True, RED)
            self.captured_pieces_count[pieces[i]] = [num, rects[i]]

    def get_axes(self):

        a = AXIS_COORD_FONT.render("a", True, BLACK)
        b = AXIS_COORD_FONT.render("b", True, BLACK)
        c = AXIS_COORD_FONT.render("c", True, BLACK)
        d = AXIS_COORD_FONT.render("d", True, BLACK)
        e = AXIS_COORD_FONT.render("e", True, BLACK)
        f = AXIS_COORD_FONT.render("f", True, BLACK)
        g = AXIS_COORD_FONT.render("g", True, BLACK)
        h = AXIS_COORD_FONT.render("h", True, BLACK)
        self.x_axis_coords = {"a": [a, a.get_rect()], "b": [b, b.get_rect()], "c": [c, c.get_rect()],
                              "d": [d, d.get_rect()],
                              "e": [e, e.get_rect()], "f": [f, f.get_rect()], "g": [g, g.get_rect()],
                              "h": [h, h.get_rect()]}
        self.x_axis_coords["a"][1].center = (315, 773)
        self.x_axis_coords["b"][1].center = (412, 773)
        self.x_axis_coords["c"][1].center = (509, 773)
        self.x_axis_coords["d"][1].center = (606, 773)
        self.x_axis_coords["e"][1].center = (703, 773)
        self.x_axis_coords["f"][1].center = (800, 773)
        self.x_axis_coords["g"][1].center = (897, 773)
        self.x_axis_coords["h"][1].center = (994, 773)

        one = AXIS_COORD_FONT.render("1", True, BLACK)
        two = AXIS_COORD_FONT.render("2", True, BLACK)
        three = AXIS_COORD_FONT.render("3", True, BLACK)
        four = AXIS_COORD_FONT.render("4", True, BLACK)
        five = AXIS_COORD_FONT.render("5", True, BLACK)
        six = AXIS_COORD_FONT.render("6", True, BLACK)
        seven = AXIS_COORD_FONT.render("7", True, BLACK)
        eight = AXIS_COORD_FONT.render("8", True, BLACK)
        self.y_axis_coords = {"one": [one, one.get_rect()], "two": [two, two.get_rect()],
                              "three": [three, three.get_rect()], "four": [four, four.get_rect()],
                              "five": [five, five.get_rect()], "six": [six, six.get_rect()],
                              "seven": [seven, seven.get_rect()], "eight": [eight, eight.get_rect()]}

        self.y_axis_coords["one"][1].center = (315, 700)
        self.y_axis_coords["two"][1].center = (315, 603)
        self.y_axis_coords["three"][1].center = (315, 506)
        self.y_axis_coords["four"][1].center = (315, 409)
        self.y_axis_coords["five"][1].center = (315, 312)
        self.y_axis_coords["six"][1].center = (315, 215)
        self.y_axis_coords["seven"][1].center = (315, 118)
        self.y_axis_coords["eight"][1].center = (315, 21)

    def update(self, pos):

        # Board - Border
        pygame.draw.rect(self.screen, BLACK, [self.Interface.xstart, self.Interface.ystart, self.Interface.boardwidth,
                                              self.Interface.boardheight], 3)
        # Settings Panel - Border
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.panel_xstart, self.Interface.panel_ystart, self.Interface.panelwidth,
                          self.Interface.panelheight], 2)
        # Captured Pieces - Border
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.killed_xstart, self.Interface.killed_ystart, self.Interface.killed_box_width,
                          self.Interface.killed_box_height], 2)
        # Chat box - Border
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.chatbox_xstart, self.Interface.chatbox_ystart, self.Interface.chatbox_width,
                          self.Interface.chatbox_height], 2)
        # Player 1 - Border
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.game_info_box1_coords[0], self.Interface.game_info_box1_coords[1],
                          self.Interface.game_info_box1_width, self.Interface.game_info_box1_height], 3)
        # Player 2 - Border
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.game_info_box2_coords[0], self.Interface.game_info_box2_coords[1],
                          self.Interface.game_info_box2_width, self.Interface.game_info_box2_height], 3)
        # Board
        self.Interface.draw_chess_board()
        # Settings Panel
        pygame.draw.rect(self.screen, (0, 102, 50), [self.Interface.panel_xstart + 2, self.Interface.panel_ystart + 2,
                                                     self.Interface.panelwidth - 2.5, self.Interface.panelheight - 2.5])
        # Captured Pieces
        pygame.draw.rect(self.screen, GREEN, [self.Interface.killed_xstart + 2, self.Interface.killed_ystart + 2,
                                              self.Interface.killed_box_width - 2.5,
                                              self.Interface.killed_box_height - 2.5])
        # Chat box
        pygame.draw.rect(self.screen, (23, 28, 38),
                         [self.Interface.chatbox_xstart + 2, self.Interface.chatbox_ystart + 2.5,
                          self.Interface.chatbox_width - 2.5, self.Interface.chatbox_height - 2.5])

        # Chat box text bar - Border
        #if self.Interface.chat_panel.selected == "chat":
        pygame.draw.rect(self.screen, WHITE,
                         [self.Interface.messsage_input_xstart, self.Interface.messsage_input_ystart,
                          self.Interface.messsage_input_width, self.Interface.messsage_input_height], 2)
        # Chat box text bar
        pygame.draw.rect(self.screen, BLACK,
                         [self.Interface.messsage_input_xstart + 2, self.Interface.messsage_input_ystart + 2,
                          self.Interface.messsage_input_width - 3, self.Interface.messsage_input_height - 3])
        if self.Interface.cursor_blink():
            pygame.draw.line(self.screen, WHITE,
                             (self.Interface.cursor_coord[0][0], self.Interface.cursor_coord[0][1]),
                             (self.Interface.cursor_coord[1][0], self.Interface.cursor_coord[1][1]), 2)

        # Captured pieces
        self.screen.blit(self.white_pieces_images['Pawn'], (1110, 110))
        self.screen.blit(self.white_pieces_images['Rook'], (1190, 109))
        self.screen.blit(self.white_pieces_images['Bishop'], (1275, 107))
        self.screen.blit(self.white_pieces_images['Knight'], (1355, 105))
        self.screen.blit(self.white_pieces_images['Queen'], (1430, 106))
        self.screen.blit(self.black_pieces_images['Pawn'], (1110, 208))
        self.screen.blit(self.black_pieces_images['Rook'], (1190, 206))
        self.screen.blit(self.black_pieces_images['Bishop'], (1275, 203))
        self.screen.blit(self.black_pieces_images['Knight'], (1355, 203))
        self.screen.blit(self.black_pieces_images['Queen'], (1430, 201))

        pygame.draw.circle(self.screen, BLACK, (1170, 281), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1170, 281), 10)
        pygame.draw.circle(self.screen, BLACK, (1255, 281), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1255, 281), 10)
        pygame.draw.circle(self.screen, BLACK, (1337, 281), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1337, 281), 10)
        pygame.draw.circle(self.screen, BLACK, (1420, 281), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1420, 281), 10)
        pygame.draw.circle(self.screen, BLACK, (1503, 281), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1503, 281), 10)

        pygame.draw.circle(self.screen, BLACK, (1170, 183), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1170, 183), 10)
        pygame.draw.circle(self.screen, BLACK, (1255, 183), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1255, 183), 10)
        pygame.draw.circle(self.screen, BLACK, (1337, 183), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1337, 183), 10)
        pygame.draw.circle(self.screen, BLACK, (1420, 183), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1420, 183), 10)
        pygame.draw.circle(self.screen, BLACK, (1503, 183), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1503, 183), 10)

        self.screen.blit(self.captured_pieces_count['wpawn'][0], self.captured_pieces_count['wpawn'][1])
        self.screen.blit(self.captured_pieces_count['wrook'][0], self.captured_pieces_count['wrook'][1])
        self.screen.blit(self.captured_pieces_count['wbishop'][0], self.captured_pieces_count['wbishop'][1])
        self.screen.blit(self.captured_pieces_count['wknight'][0], self.captured_pieces_count['wknight'][1])
        self.screen.blit(self.captured_pieces_count['wqueen'][0], self.captured_pieces_count['wqueen'][1])

        self.screen.blit(self.captured_pieces_count['bpawn'][0], self.captured_pieces_count['bpawn'][1])
        self.screen.blit(self.captured_pieces_count['brook'][0], self.captured_pieces_count['brook'][1])
        self.screen.blit(self.captured_pieces_count['bbishop'][0], self.captured_pieces_count['bbishop'][1])
        self.screen.blit(self.captured_pieces_count['bknight'][0], self.captured_pieces_count['bknight'][1])
        self.screen.blit(self.captured_pieces_count['bqueen'][0], self.captured_pieces_count['bqueen'][1])

        #self.Interface.chat_panel.mount(self.Interface.chatbox_xstart, self.Interface.chatbox_ystart)

        for coord in self.x_axis_coords:
            self.screen.blit(self.x_axis_coords[coord][0], self.x_axis_coords[coord][1])
        for coord in self.y_axis_coords:
            self.screen.blit(self.y_axis_coords[coord][0], self.y_axis_coords[coord][1])

        pygame.draw.rect(self.screen, (0, 0, 0), [1115, 20, 140, 53], 2)
        pygame.draw.rect(self.screen, (0, 0, 0), [1275, 20, 100, 53], 2)
        pygame.draw.rect(self.screen, (0, 0, 0), [1395, 20, 110, 53], 2)
        pygame.draw.rect(self.screen, (255, 255, 255), [1117, 22, 137, 50])
        pygame.draw.rect(self.screen, (255, 255, 255), [1277, 22, 97, 50])
        pygame.draw.rect(self.screen, (255, 255, 255), [1397, 22, 107, 50])

        # focusing buttons
        if pos[0] <= 1255 and pos[0] >= 1115 and pos[1] <= 73 and pos[1] >= 20:
            pygame.draw.rect(self.screen, (94, 118, 128), [1117, 22, 137, 50])
        elif pos[0] <= 1375 and pos[0] >= 1275 and pos[1] <= 73 and pos[1] >= 20:
            pygame.draw.rect(self.screen, (94, 118, 128), [1277, 22, 97, 50])
        elif pos[0] <= 1505 and pos[0] >= 1395 and pos[1] <= 73 and pos[1] >= 20:
            pygame.draw.rect(self.screen, (94, 118, 128), [1397, 22, 107, 50])

        if self.main_menu.settings_object.music:
                self.screen.blit(self.music_on_button, (1125, 35))
        else:
            self.screen.blit(self.music_off_button,(1120,35))
        self.screen.blit(self.forfeit_button, (1285, 35))
        self.screen.blit(self.leave_button, (1415, 35))

        self.screen.blit(self.myprofimg,(15,407))
        self.screen.blit(self.enemyprofimg,(15,10))

        self.screen.blit(self.enemyname,(50,349))

    def __del__(self):
        print("Game object deleted")

