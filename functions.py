import pygame
from pygame.locals import *
from time import *
import sys
from threading import Thread
from socket import *
import time
import random
from chat_panel import *

captured_piece = None
moved_piece = None

selected_square = list()
playerclick = list()
whiteToMove = True

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

    def __init__(self, width, height, screen=None):
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
        self.max_message_length = 25
        self.old_messages = []
        self.first_msg = 0
        self.last_msg = 0
        self.server = '65.0.204.13'
        self.port = 12000
        self.username = "Hrishi"

    # self.connect_to_server()
    # self.receive_thread = Thread(target=self.receive_messages)
    # self.receive_thread.start()

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
        self.killed_box_height = self.height * (31 / 100)

    def generate_chatbox(self):
        self.chatbox_xstart = self.xend + self.width * (0.97 / 100)
        self.chatbox_ystart = self.killed_ystart + self.killed_box_height + self.width * (0.97 / 100)
        self.chatbox_width = self.panelwidth
        self.chatbox_height = self.boardheight + self.ystart - self.chatbox_ystart
        self.chat_panel = Chat_panel(self.screen, [self.chatbox_xstart, self.chatbox_ystart, self.chatbox_width,
                                                   self.chatbox_height])

    def draw_chess_board(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    pygame.draw.rect(self.screen, COLOR3,
                                     [self.grid[i][j].xstart, self.grid[i][j].ystart, self.boxwidth, self.boxheight])
                else:
                    pygame.draw.rect(self.screen, COLOR4,
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
                    self.message_text = FONT.render(self.message, True, BLACK)
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
                    msg = self.username + ":" + self.message
                    # self.send_message(msg)
                    text = FONT.render(self.message, True, BLACK)
                    rect = text.get_rect()
                    username = FONT.render("Me:", True, random.choice([RED, GREEN, LIGHTBLUE, LIGHTNAVY]))
                    uname_rect = username.get_rect()
                    self.chat_buffer_graphic.append(([username, uname_rect], [text, rect]))
                    self.message = ""
                    self.cursor_position = 0
                    self.cursor_coord = [[self.messsage_input_xstart + self.width * (0.3 / 100),
                                          self.messsage_input_ystart + self.height * (0.6 / 100)],
                                         [self.messsage_input_xstart + self.width * (0.3 / 100),
                                          self.messsage_input_ystart + self.height * (4.4 / 100)]]
                    self.last_msg += 1
                    if self.last_msg >= 10:
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
                    self.message_text = FONT.render(self.message, True, BLACK)
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

    # Networking part
    def connect_to_server(self):
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            print("Socket successfully created")
        except error as err:
            print("socket creation failed with error %s" % (err))
        self.sock.connect((self.server, self.port))
        self.sock.send(self.username.encode())

    def get_username_and_message(self, message):
        username = ""
        msg = ""
        if ":" not in message:
            return None, message
        for i in message:
            if i != ":":
                username += i
            else:
                break
        msg = message[len(username) + 1:]
        return username, msg

    def receive_messages(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    username, message = self.get_username_and_message(message)
                    if message and username:
                        self.chat_buffer_text.append(message)
                        username = FONT.render(username + ":", True, random.choice([RED, GREEN, LIGHTBLUE, LIGHTNAVY]))
                        uname_rect = username.get_rect()
                        message = FONT.render(message, True, BLACK)
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
                self.sock.close()
                break

    def send_message(self, message):
        try:
            self.sock.send(message.encode())
        except:
            print("Error sending message!!")
            self.sock.close()


class piece:
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


class game:

    def __init__(self, Interface, screen, sfac, piece_type):
        self.white_pieces_images = {}
        self.black_pieces_images = {}
        self.captured_pieces = {'wpawn': 0, 'wrook': 0, 'wknight': 0, 'wbishop': 0, 'wqueen': 0,
                                'bpawn': 0, 'brook': 0, 'bknight': 0, 'bbishop': 0, 'bqueen': 0}
        self.captured_pieces_count = {}
        self.piece_type = piece_type
        self.grid = Interface.grid
        self.Interface = Interface
        self.whiteToMove = True
        self.enemy_pieces = {}
        self.selected_box = None
        self.screen = screen
        self.pieces_scaling_factor = sfac
        self.moves_manager = None
        self.get_captured_pieces_numbers()
        self.position_adjustment = {
            'type1': {'WPawn': (0, 0), 'WRook': (0, 0),
                      'WKnight': (0, 0), 'W_Bishop': (0, 0),
                      'WQueen': (0, 0), 'WKing': (0, 0),
                      'BPawn': (0, 0), 'BRook': (0, 0),
                      'BKnight': (0, 0), 'B_Bishop': (0, 0),
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

    def load_pieces(self):
        piece = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Pawn']
        for i in piece:
            self.white_pieces_images[i] = pygame.image.load(f'Media/pieces type {self.piece_type}/W{i}.png')

        if self.pieces_scaling_factor:
            for piece in self.white_pieces_images:
                self.white_pieces_images[piece] = pygame.transform.scale(self.white_pieces_images[piece],
                                                                         self.pieces_scaling_factor)
        for i in piece:
            self.black_pieces_images[i] = pygame.image.load(f'Media/pieces type {self.piece_type}/B{i}.png')

        if self.pieces_scaling_factor:
            for piece in self.black_pieces_images:
                self.black_pieces_images[piece] = pygame.transform.scale(self.black_pieces_images[piece],
                                                                         self.pieces_scaling_factor)

    def init_my_pieces(self):
        pawns = [piece('pawn', [6, 0], "white"), piece('pawn', [6, 1], "white"), piece('pawn', [6, 2], "white"),
                 piece('pawn', [6, 3], "white"), piece('pawn', [6, 4], "white"), piece('pawn', [6, 5], "white"),
                 piece('pawn', [6, 6], "white"), piece('pawn', [6, 7], "white")]
        for pawn in pawns:
            pawn.image = self.white_pieces_images['Pawn']
            pawn.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WPawn']
        self.moves_manager.pieces['pawn'] = pawns
        for i in range(8):
            self.grid[6][i].piece = pawns[i]

        rooks = [piece('rook', [7, 0], "white"), piece('rook', [7, 7], "white")]
        for rook in rooks:
            rook.image = self.white_pieces_images['Rook']
            rook.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WRook']
        self.moves_manager.pieces['rook'] = rooks
        self.grid[7][0].piece = rooks[0]
        self.grid[7][7].piece = rooks[1]

        bishops = [piece('bishop', [7, 2], "white"), piece('bishop', [7, 5], "white")]
        for bishop in bishops:
            bishop.image = self.white_pieces_images['Bishop']
            bishop.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WBishop']
        self.moves_manager.pieces['bishop'] = bishops
        self.grid[7][2].piece = bishops[0]
        self.grid[7][5].piece = bishops[1]

        knights = [piece('knight', [7, 1], "white"), piece('knight', [7, 6], "white")]
        for knight in knights:
            knight.image = self.white_pieces_images['Knight']
            knight.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WKnight']
        self.moves_manager.pieces['knight'] = knights
        self.grid[7][1].piece = knights[0]
        self.grid[7][6].piece = knights[1]

        king = piece('king', [7, 4], "white")
        king.image = self.white_pieces_images['King']
        king.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WKing']
        self.moves_manager.pieces['king'] = [king]
        self.grid[7][4].piece = king

        queen = piece('queen', [7, 3], "white")
        queen.image = self.white_pieces_images['Queen']
        queen.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['WQueen']
        self.moves_manager.pieces['queen'] = [queen]
        self.grid[7][3].piece = queen

        for i in range(6, 8):
            for j in range(0, 8):
                self.grid[i][j].is_empty = False

        for i in range(2, 6):
            for j in range(0, 8):
                self.grid[i][j].is_empty = True

    def init_opponent_pieces(self):
        pawns = [piece('pawn', [1, 0], "black"), piece('pawn', [1, 1], "black"), piece('pawn', [1, 2], "black"),
                 piece('pawn', [1, 3], "black"), piece('pawn', [1, 4], "black"), piece('pawn', [1, 5], "black"),
                 piece('pawn', [1, 6], "black"), piece('pawn', [1, 7], "black")]
        for pawn in pawns:
            pawn.image = self.black_pieces_images['Pawn']
            pawn.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BPawn']
        self.moves_manager.enemy_pieces['pawn'] = pawns
        for i in range(8):
            self.grid[1][i].piece = pawns[i]

        rooks = [piece('rook', [0, 0], "black"), piece('rook', [0, 7], "black")]
        for rook in rooks:
            rook.image = self.black_pieces_images['Rook']
            rook.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BRook']
        self.moves_manager.enemy_pieces['rook'] = rooks
        self.grid[0][0].piece = rooks[0]
        self.grid[0][7].piece = rooks[1]

        bishops = [piece('bishop', [0, 2], "black"), piece('bishop', [0, 5], "black")]
        for bishop in bishops:
            bishop.image = self.black_pieces_images['Bishop']
            bishop.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BBishop']
        self.moves_manager.enemy_pieces['bishop'] = bishops
        self.grid[0][2].piece = bishops[0]
        self.grid[0][5].piece = bishops[1]

        knights = [piece('knight', [0, 1], "black"), piece('knight', [0, 6], "black")]
        for knight in knights:
            knight.image = self.black_pieces_images['Knight']
            knight.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BKnight']
        self.moves_manager.enemy_pieces['knight'] = knights
        self.grid[0][1].piece = knights[0]
        self.grid[0][6].piece = knights[1]

        king = piece('king', [0, 4], "black")
        king.image = self.black_pieces_images['King']
        king.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BKing']
        self.moves_manager.enemy_pieces['king'] = [king]
        self.grid[0][4].piece = king

        queen = piece('queen', [0, 3], "black")
        queen.image = self.black_pieces_images['Queen']
        queen.pos_adjustment = self.position_adjustment['type{}'.format(self.piece_type)]['BQueen']
        self.moves_manager.enemy_pieces['queen'] = [queen]
        self.grid[0][3].piece = queen

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
                self.screen.blit(piece.image, (
                self.grid[piece.position[0]][piece.position[1]].xstart + piece.pos_adjustment[0],
                self.grid[piece.position[0]][piece.position[1]].ystart + piece.pos_adjustment[1]))

    # as of now, both white and black pieces can move as per some basic rules.

    def handle_click_event(self, coords):
        global playerclick, selected_square, whiteToMove
        self.selected_box = self.grid[coords[0]][coords[1]]
        #print(self.squareUnderAttack(coords, self.grid))
        # if white to move
        if whiteToMove:
            if len(playerclick) == 0: #player clicks on first square
                if self.grid[coords[0]][coords[1]].is_empty == False: #if the square selected is not empty
                    if self.grid[coords[0]][coords[1]].piece.color == 'white': #white selects white piece
                        selected_square = coords
                        playerclick.append(selected_square)
                        #print('1')
                        self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                    elif (self.grid[coords[0]][coords[1]].piece.color == 'black'):#white selects empty square or blackpiece
                        self.selected_box = None
                        playerclick = list()
                        selected_square = list()
                        #print('2')
                else:#if square selected is empty
                    self.selected_box = None
                    playerclick = list()
                    selected_square = list()
                    #print('3')
            elif len(playerclick) == 1: #player clicks on second square
                if self.grid[coords[0]][coords[1]].is_empty == False: #if selected square is not empty
                    if self.grid[coords[0]][coords[1]].piece.color == 'white': #if selected square contains white piece
                        if selected_square == coords: #if white player clicks same square twice ie he's trying to deselect
                            selected_square = list()
                            playerclick = list()
                            self.selected_box = None
                            #print('4')
                        else:
                            selected_square = coords
                            playerclick = [selected_square]
                            #print('5')
                            self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                    elif self.grid[coords[0]][coords[1]].piece.color == 'black':
                        if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                            #print(self.moves_manager.selected_piece)
                            self.move(self.moves_manager.selected_piece, coords, self.grid,
                                  self.position_adjustment['type{}'.format(self.piece_type)][
                                      self.moves_manager.adjustment_dictionary_name])
                            #print('6')
                            selected_square = list()
                            playerclick = list()
                            whiteToMove = not whiteToMove
                        else:
                            selected_square = list()
                            playerclick = list()
                            self.selected_box = None

                else:
                    if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                        #print(self.moves_manager.selected_piece)
                        self.move(self.moves_manager.selected_piece, coords, self.grid,
                                  self.position_adjustment['type{}'.format(self.piece_type)][
                                      self.moves_manager.adjustment_dictionary_name])
                        #print('7')
                        selected_square = list()
                        playerclick = list()
                        whiteToMove = not whiteToMove
                    else:
                        selected_square = list()
                        playerclick = list()
                        self.selected_box = None

            else:
                self.selected_box = None
                playerclick = list()
                selected_square = list()
                self.moves_manager.legal_moves = []
                self.moves_manager.selected_piece = None
                #print('8')

        #if black to move
        else:
            if len(playerclick) == 0:
                if self.grid[coords[0]][coords[1]].is_empty == False:
                    if self.grid[coords[0]][coords[1]].piece.color == 'black':
                        selected_square = coords
                        playerclick.append(selected_square)
                        self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                    elif (self.grid[coords[0]][
                                  coords[1]].piece.color == 'white'):
                        self.selected_box = None
                        playerclick = list()
                        selected_square = list()
                else:
                    self.selected_box = None
                    playerclick = list()
                    selected_square = list()
            elif len(playerclick) == 1:
                if self.grid[coords[0]][coords[1]].is_empty == False:
                    if self.grid[coords[0]][coords[1]].piece.color == 'black':
                        if selected_square == coords:
                            selected_square = list()
                            playerclick = list()
                            self.selected_box = None
                        else:
                            selected_square = coords
                            playerclick = [selected_square]
                            self.moves_manager.get_legal_moves(self.grid[coords[0]][coords[1]].piece, self.grid)
                    elif self.grid[coords[0]][coords[1]].piece.color == 'white':
                        if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                            self.move(self.moves_manager.selected_piece, coords, self.grid,
                                  self.position_adjustment['type{}'.format(self.piece_type)][
                                      self.moves_manager.adjustment_dictionary_name])
                            selected_square = list()
                            playerclick = list()
                            whiteToMove = not whiteToMove
                        else:
                            selected_square = list()
                            playerclick = list()
                            self.selected_box = None

                else:
                    if coords in [[i.x, i.y] for i in self.moves_manager.legal_moves]:
                        self.move(self.moves_manager.selected_piece, coords, self.grid,
                                  self.position_adjustment['type{}'.format(self.piece_type)][
                                      self.moves_manager.adjustment_dictionary_name])
                        whiteToMove = not whiteToMove
                        selected_square = list()
                        playerclick = list()
                    else:
                        selected_square = list()
                        playerclick = list()
                        self.selected_box = None

            else:
                self.selected_box = None
                playerclick = list()
                selected_square = list()
                self.moves_manager.legal_moves = []
                self.moves_manager.selected_piece = None


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

    def chess_notation(self, piece, destination):
        return self.rank_file(piece.position[0], piece.position[1]) +  self.rank_file(destination[0], destination[1])

    def rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def move(self, piece, destination, board, adjustment):
        global moved_piece, captured_piece
        # get start and stop positions
        start = [board[piece.position[0]][piece.position[1]].xstart + adjustment[0],
                 board[piece.position[0]][piece.position[1]].ystart + adjustment[1]]

        stop = [board[destination[0]][destination[1]].xstart + adjustment[0],
                board[destination[0]][destination[1]].ystart + adjustment[1] + 1]

        print(self.chess_notation(piece, destination))
        moved_piece = piece
        # set the current box of grid to empty
        self.grid[piece.position[0]][piece.position[1]].is_empty = True

        if self.grid[destination[0]][destination[1]].is_empty == False: #destination square non-empty means definitely contains black piece
            captured_piece = self.grid[destination[0]][destination[1]].piece
            '''
            setting position of captured piece to [-1,-1] because 
            [-1,-1] doesn't exist on the grid and so does the captured piece
            '''
            if captured_piece.color == 'white':
                for i in range(len(self.moves_manager.pieces[captured_piece.name])):
                    if self.moves_manager.pieces[captured_piece.name][i].position == destination:
                        self.moves_manager.pieces[captured_piece.name][i].is_alive = False
                        self.moves_manager.pieces[captured_piece.name][i].position = [-1,-1]
                        break

            else:
                for i in range(len(self.moves_manager.enemy_pieces[captured_piece.name])):
                    if self.moves_manager.enemy_pieces[captured_piece.name][i].position == destination:
                        self.moves_manager.enemy_pieces[captured_piece.name][i].is_alive = False
                        self.moves_manager.enemy_pieces[captured_piece.name][i].position = [-1, -1]
                        break

            self.captured_pieces[captured_piece.color[:1] + captured_piece.name] += 1

        else:
            captured_piece = None
        #'''
        self.grid[destination[0]][destination[1]].piece = piece

        # unlock the piece so that update_pieces function does not show it on screen when it is moving
        piece.locked = False

        # moving piece
        while True:
            # keep updating the screen and pieces while moving piece
            self.update()
            self.update_pieces()
            self.Interface.print_messages()
            #add animation conditions for different pieces
            if start[1] > stop[1]:
                start[1] -= 2
                self.screen.blit(piece.image, (start[0], start[1]))
                pygame.display.flip()
            else:
                piece.position = destination
                self.moves_manager.wking_loc = self.moves_manager.pieces['king'][0].position
                self.moves_manager.bking_loc = self.moves_manager.enemy_pieces['king'][0].position
                # print(self.moves_manager.wking_loc, self.moves_manager.bking_loc)
                piece.locked = True
                break

        self.moves_manager.selected_piece = None
        self.moves_manager.legal_moves = []
        self.selected_box = None
        self.grid[destination[0]][destination[1]].is_empty = False

    # graphical
    def get_captured_pieces_numbers(self):
        num = FONT.render("0", True, RED)
        rects = [num.get_rect() for i in range(10)]
        rects[0].center = (1170, 200)
        rects[1].center = (1255, 200)
        rects[2].center = (1337, 200)
        rects[3].center = (1420, 200)
        rects[4].center = (1503, 200)
        rects[5].center = (1170, 330)
        rects[6].center = (1255, 330)
        rects[7].center = (1337, 330)
        rects[8].center = (1420, 330)
        rects[9].center = (1503, 330)
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

    def update(self):

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
        pygame.draw.rect(self.screen, (0,255,0), [self.Interface.panel_xstart + 2, self.Interface.panel_ystart + 2,
                                                  self.Interface.panelwidth - 2.5, self.Interface.panelheight - 2.5])
        # Captured Pieces
        pygame.draw.rect(self.screen, GREEN, [self.Interface.killed_xstart + 2, self.Interface.killed_ystart + 2,
                                              self.Interface.killed_box_width - 2.5,
                                              self.Interface.killed_box_height - 2.5])
        # Chat box
        pygame.draw.rect(self.screen, WHITE, [self.Interface.chatbox_xstart + 2, self.Interface.chatbox_ystart + 2,
                                              self.Interface.chatbox_width - 2.5, self.Interface.chatbox_height - 3])
        # Chat box text bar
        # pygame.draw.rect(self.screen,WHITE,[self.Interface.messsage_input_xstart+2,self.Interface.messsage_input_ystart+2,self.Interface.messsage_input_width-2.5,self.Interface.messsage_input_height-2.5])
        # Chat box text bar - Border
        if self.Interface.chat_panel.selected == "chat":
            pygame.draw.rect(self.screen, BLACK,
                             [self.Interface.messsage_input_xstart, self.Interface.messsage_input_ystart,
                              self.Interface.messsage_input_width, self.Interface.messsage_input_height], 2)
            if self.Interface.cursor_blink():
                pygame.draw.line(self.screen, BLACK,
                                 (self.Interface.cursor_coord[0][0], self.Interface.cursor_coord[0][1]),
                                 (self.Interface.cursor_coord[1][0], self.Interface.cursor_coord[1][1]), 2)

        # Captured pieces
        self.screen.blit(self.white_pieces_images['Pawn'], (1110, 127))
        self.screen.blit(self.white_pieces_images['Rook'], (1190, 125))
        self.screen.blit(self.white_pieces_images['Bishop'], (1275, 124))
        self.screen.blit(self.white_pieces_images['Knight'], (1355, 122))
        self.screen.blit(self.white_pieces_images['Queen'], (1430, 123))
        self.screen.blit(self.black_pieces_images['Pawn'], (1110, 257))
        self.screen.blit(self.black_pieces_images['Rook'], (1190, 255))
        self.screen.blit(self.black_pieces_images['Bishop'], (1275, 252))
        self.screen.blit(self.black_pieces_images['Knight'], (1355, 252))
        self.screen.blit(self.black_pieces_images['Queen'], (1430, 250))

        pygame.draw.circle(self.screen, BLACK, (1170, 330), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1170, 330), 10)
        pygame.draw.circle(self.screen, BLACK, (1255, 330), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1255, 330), 10)
        pygame.draw.circle(self.screen, BLACK, (1337, 330), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1337, 330), 10)
        pygame.draw.circle(self.screen, BLACK, (1420, 330), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1420, 330), 10)
        pygame.draw.circle(self.screen, BLACK, (1503, 330), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1503, 330), 10)

        pygame.draw.circle(self.screen, BLACK, (1170, 200), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1170, 200), 10)
        pygame.draw.circle(self.screen, BLACK, (1255, 200), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1255, 200), 10)
        pygame.draw.circle(self.screen, BLACK, (1337, 200), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1337, 200), 10)
        pygame.draw.circle(self.screen, BLACK, (1420, 200), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1420, 200), 10)
        pygame.draw.circle(self.screen, BLACK, (1503, 200), 12, 3)
        pygame.draw.circle(self.screen, WHITE, (1503, 200), 10)

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

        self.Interface.chat_panel.mount(self.Interface.chatbox_xstart, self.Interface.chatbox_ystart)

        for coord in self.x_axis_coords:
            self.screen.blit(self.x_axis_coords[coord][0], self.x_axis_coords[coord][1])
        for coord in self.y_axis_coords:
            self.screen.blit(self.y_axis_coords[coord][0], self.y_axis_coords[coord][1])


# def update_captured_pieces(self):
