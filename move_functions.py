from functions import *

class CastleRights:
    def __init__(self, wks, wqs, bks, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

class Moves_manager:
    def __init__(self, game):
        self.game = game
        self.pieces	 = {}
        self.enemy_pieces = {}
        self.legal_moves = list()
        self.selected_piece = None
        self.adjustment_dictionary_name = None
        self.wking_loc = list()
        self.bking_loc = list()
        self.currentCastleRights = self.game.update_castle()
        self.whiteToMove = self.game.whiteToMove
        self.possibleMoves = list()
        self.in_check = False
        self.pins = [] #squares pinned and the direction it's pinned from (list of lists)
        self.checks = [] #squares where enemy is applying a check
        self.rook_moves = list()
        self.knight_moves = list()
        self.bishop_moves = list()
        self.queen_moves = list()
        self.white_pawn_moves = list()
        self.black_pawn_moves = list()
        self.king_moves = list()
        self.castle_moves = list()
        self.checkmate = False
        self.stalemate = False
        self.moves_count = 1

    def squareUnderAttack(self, coords, my_color, board):

        #self.whiteToMove = not self.whiteToMove

        if my_color == 'white':
            enemy_color = 'black'
        else:
            enemy_color = 'white'
        #print(board[1][1].piece.name)
        for i in range(8):
            for j in range(8):
                if board[i][j].is_empty == False:
                    #print(i, j)
                    Piece = board[i][j].piece
                    if Piece.color == enemy_color:
                        if Piece.name == "pawn" :
                            #in case of pawn, no use calling get_pawn_moves. instead, collect pawn.position from moves_manager.pieces
                            #and putcondition of diagonal attack of pawn
                            if enemy_color == 'black':
                                #self.possibleMoves = list()
                                #self.get_black_pawn_moves(Piece, board)
                                if len(self.enemy_pieces['pawn']) > 0:
                                    for pawn in self.enemy_pieces['pawn']:
                                        self.possibleMoves.append(
                                            [pawn.position, [pawn.position[0] + 1, pawn.position[1] + 1], pawn, None])
                                        self.possibleMoves.append(
                                            [pawn.position, [pawn.position[0] + 1, pawn.position[1] - 1], pawn, None])
                            else:
                                #self.possibleMoves = list()
                                #self.get_white_pawn_moves(Piece, board)
                                if len(self.pieces['pawn']) > 0:
                                    for pawn in self.pieces['pawn']:
                                        self.possibleMoves.append(
                                            [pawn.position, [pawn.position[0] - 1, pawn.position[1] + 1], pawn, None])
                                        self.possibleMoves.append(
                                            [pawn.position, [pawn.position[0] - 1, pawn.position[1] - 1], pawn, None])
                        elif Piece.name == "rook":
                            #self.possibleMoves = list()
                            self.get_rook_moves(Piece, board)
                        elif Piece.name == "bishop":
                            #self.possibleMoves = list()
                            self.get_bishop_moves(Piece, board)
                        elif Piece.name == "knight":
                            #self.possibleMoves = list()
                            self.get_knight_moves(Piece, board)
                        elif Piece.name == "queen":
                            #self.possibleMoves = list()
                            self.get_queen_moves(Piece, board)

                        moves = self.possibleMoves

                        if len(moves) > 0:
                            for k in range(len(moves)):
                                if moves[k][1] == coords:
                                    return True
        return False



    def get_castling_moves(self, board):
        #self.selected_piece = piece
        #self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[0].upper() + self.selected_piece.name[1:]
        #self.castle_moves = list()
        if self.whiteToMove:
            piece = self.pieces['king'][0]
        else:
            piece = self.enemy_pieces['king'][0]
        if self.whiteToMove:
            if self.currentCastleRights.wks == True:
                # print("1")
                #print(piece.position, piece.color)
                if board[piece.position[0]][piece.position[1] + 1].is_empty == True and board[piece.position[0]][
                    piece.position[1] + 2].is_empty == True and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] + 1], 'white', board)) and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] + 2], 'white', board)):
                    self.castle_moves.append(board[piece.position[0]][piece.position[1] + 2])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0], piece.position[1] + 2], piece,
                         None])
            if self.currentCastleRights.wqs == True:
                #print(piece.position, piece.color)
                if board[piece.position[0]][piece.position[1] - 1].is_empty == True and board[piece.position[0]][
                    piece.position[1] - 2].is_empty == True and board[piece.position[0]][
                    piece.position[1] - 3].is_empty == True and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] - 1], 'white', board)) and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] - 2], 'white', board)):
                    self.castle_moves.append(board[piece.position[0]][piece.position[1] - 2])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0], piece.position[1] - 2], piece,
                         None])

        else:
            if self.currentCastleRights.bks == True:
                # print("1")
                if board[piece.position[0]][piece.position[1] + 1].is_empty == True and board[piece.position[0]][
                    piece.position[1] + 2].is_empty == True and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] + 1], 'black', board)) and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] + 2], 'black', board)):
                    self.castle_moves.append(board[piece.position[0]][piece.position[1] + 2])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0], piece.position[1] + 2], piece,
                         None])
            if self.currentCastleRights.bqs == True:
                if board[piece.position[0]][piece.position[1] - 1].is_empty == True and board[
                    piece.position[0]][piece.position[1] - 2].is_empty == True and board[
                    piece.position[0]][piece.position[1] - 3].is_empty == True and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] - 1], 'black', board)) and (not self.squareUnderAttack([
                    piece.position[0], piece.position[1] - 2], 'black', board)):
                    self.castle_moves.append(board[piece.position[0]][piece.position[1] - 2])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0], piece.position[1] - 2], piece,
                         None])

        #return self.castle_moves

    def check_pins_and_checks(self, board):
        start_row = []
        start_col = []
        if self.whiteToMove:
            my_color = 'white'
            enemy_color = 'black'
            king_coords = self.pieces['king'][0].position
            self.wking_loc = king_coords
        else:
            my_color = 'black'
            enemy_color = 'white'
            king_coords = self.enemy_pieces['king'][0].position
            self.bking_loc = king_coords
        # check outwards from king for pins and checks, keep track of pins
        directions = [[-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = []  #reset possible pins
            start_row = king_coords[0]
            start_col = king_coords[1]
            # print(start_row, start_col)
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = board[end_row][end_col].piece
                    if board[end_row][end_col].is_empty == False:
                        if end_piece.color == my_color and end_piece.name != "king":
                            if possible_pin == []:  #first my_piece which could be pinned
                                possible_pin = [[end_row, end_col], [direction[0], direction[1]]]
                                #print(possible_pin)
                            else:  #Second my_piece is in the same direction.
                                 break   #So no check or pin from this direction

                        elif end_piece.color == enemy_color:
                            enemy_type = end_piece.name
                            if (0 <= j <= 3 and enemy_type == "rook") or (4 <= j <= 7 and enemy_type == "bishop") or (
                                    i == 1 and enemy_type == "pawn" and ((enemy_color == "white" and 6 <= j <= 7) or (
                                    enemy_color == 'black' and 4 <= j <= 5))) or (enemy_type == "queen") or (
                                    i == 1 and enemy_type == "king"):
                                if possible_pin == []:  #Check because no piece is blocking
                                    self.in_check = True
                                    if [[end_row, end_col], [direction[0], direction[1]]] not in self.checks:
                                        self.checks.append([[end_row, end_col], [direction[0], direction[1]]])
                                    break
                                else:  #Pin because piece is blocking
                                    if possible_pin not in self.pins:
                                        self.pins.append(possible_pin)
                                    break
                            else:  #enemy_piece not applying checks
                                break
                else:
                    break  #off board

        #check for knight checks
        knight_moves = [[-2, -1], [-2, 1], [-1, 2], [1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                if not board[end_row][end_col].is_empty:
                    end_piece = board[end_row][end_col].piece
                    if end_piece.color == enemy_color and end_piece.name == "knight":  #enemy knight attaking king
                        self.in_check = True
                        self.checks.append([[end_row, end_col], [move[0], move[1]]])

    def get_king_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.check_pins_and_checks(board)

        possible_moves = [[-1, 0], [-1, 1], [0, 1], [1, 1],
                          [1, 0], [1, -1], [0, -1], [-1, -1]]

        for pos in possible_moves:
            if (0 <= piece.position[0] + pos[0] <= 7) and (0 <= piece.position[1] + pos[1] <= 7):
                if board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].is_empty == True:
                    if not self.squareUnderAttack([piece.position[0] + pos[0], piece.position[1] + pos[1]], piece.color, board):
                        self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                        self.possibleMoves.append(
                        [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece,
                         None])
                # captures
                else:
                    captured_piece = board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece
                    if self.selected_piece.color == 'white': #white king captures black piece
                        if  not self.squareUnderAttack([piece.position[0] + pos[0], piece.position[1] + pos[1]], piece.color, board):
                            if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'black') and (
                                board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                                self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                                self.possibleMoves.append(
                                [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece, captured_piece])
                            #self.get_castling_moves(self.king_moves, board, piece)
                    else: #black king captures white piece
                        if not self.squareUnderAttack([piece.position[0] + pos[0], piece.position[1] + pos[1]], piece.color, board):
                            if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'white') and (
                                board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                                self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                                self.possibleMoves.append(
                                [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece,
                                 captured_piece])
        #self.get_castling_moves(board)

    def get_knight_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.check_pins_and_checks(board)
        for i in range(len(self.pins)):
            if piece.position == self.pins[i][0]:
                return []

        possible_moves = [[-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        for pos in possible_moves:
            if (piece.position[0] + pos[0] >= 0) and (piece.position[1] + pos[1] >= 0) and (
                    piece.position[0] + pos[0] <= 7) and (piece.position[1] + pos[1] <= 7):

                if board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].is_empty:
                    self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece,
                         None])
                # captures
                else:
                    captured_piece = board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece
                    if self.selected_piece.color == 'white':
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'black'):# and (
                            #board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                            self.possibleMoves.append(
                                [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece,
                                 captured_piece])
                    else:
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'white'):# and (
                            #board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                            self.possibleMoves.append(
                                [piece.position, [piece.position[0] + pos[0], piece.position[1] + pos[1]], piece,
                                 captured_piece])


    def get_rook_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        piece_pinned = False
        pin_direction = []

        self.check_pins_and_checks(board)
        for i in range(len(self.pins) - 1, -1, -1):
            if piece.position == self.pins[i][0]:
                piece_pinned = True
                pin_direction = self.pins[i][1]
                if board[piece.position[0]][piece.position[1]] != "queen":
                    self.pins.remove(self.pins[i])
                break

        directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        for direction in directions:
            for i in range(1, 8):
                end_row = piece.position[0] + direction[0] * i
                end_col = piece.position[1] + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == [-direction[0], -direction[1]]:
                        if board[end_row][end_col].is_empty == True:
                            self.rook_moves.append(board[end_row][end_col])
                            self.possibleMoves.append(
                                [piece.position, [end_row, end_col], piece,
                                 None])
                        #captures
                        else:
                            if self.selected_piece.color == "white":
                                captured_piece = board[end_row][end_col].piece
                                if board[end_row][end_col].piece.color == "black":# and board[end_row][
                                    #end_col].piece.name != "king":
                                    self.rook_moves.append(board[end_row][end_col])
                                    self.possibleMoves.append(
                                        [piece.position, [end_row, end_col], piece,
                                         captured_piece])
                                    break
                                elif board[end_row][end_col].piece.color == "white":
                                    break
                            else:
                                captured_piece = board[end_row][end_col].piece
                                if board[end_row][end_col].piece.color == "white":# and board[end_row][
                                    #end_col].piece.name != "king":
                                    self.rook_moves.append(board[end_row][end_col])
                                    self.possibleMoves.append(
                                        [piece.position, [end_row, end_col], piece,
                                         captured_piece])
                                    break
                                elif board[end_row][end_col].piece.color == 'black':
                                    break


    def get_bishop_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        piece_pinned = False
        pin_direction = []

        self.check_pins_and_checks(board)
        for i in range(len(self.pins) - 1, -1, -1):
            if piece.position == self.pins[i][0]:
                piece_pinned = True
                pin_direction = self.pins[i][1]
                self.pins.remove(self.pins[i])
                break

        directions = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

        for direction in directions:
            for i in range(1, 8):
                end_row = piece.position[0] + direction[0] * i
                end_col = piece.position[1] + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    if not piece_pinned or pin_direction == direction or pin_direction == [-direction[0],
                                                                                           -direction[1]]:
                        if board[end_row][end_col].is_empty == True:
                            self.bishop_moves.append(board[end_row][end_col])
                            self.possibleMoves.append(
                                [piece.position, [end_row, end_col], piece,
                                 None])
                        else:
                            if self.selected_piece.color == "white":
                                captured_piece = board[end_row][end_col].piece
                                if board[end_row][end_col].piece.color == "black":# and board[end_row][
                                    #end_col].piece.name != "king":
                                    self.bishop_moves.append(board[end_row][end_col])
                                    self.possibleMoves.append(
                                        [piece.position, [end_row, end_col], piece,
                                         captured_piece])
                                    break
                                elif board[end_row][end_col].piece.color == "white":
                                    break
                            else:
                                captured_piece = board[end_row][end_col].piece
                                if board[end_row][end_col].piece.color == "white":# and board[end_row][
                                    #end_col].piece.name != "king":
                                    self.bishop_moves.append(board[end_row][end_col])
                                    self.possibleMoves.append(
                                        [piece.position, [end_row, end_col], piece,
                                         captured_piece])
                                    break
                                elif board[end_row][end_col].piece.color == "black":
                                    break

    def get_queen_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.queen_moves = self.get_rook_moves(piece, board)
        temp = self.get_bishop_moves(piece, board)
        if temp is not None:
            for i in temp:
                self.queen_moves.append(i)

    def get_white_pawn_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        piece_pinned = False
        pin_direction = []

        self.check_pins_and_checks(board)
        for i in range(len(self.pins) - 1, -1, -1):
            if piece.position == self.pins[i][0]:
                piece_pinned = True
                pin_direction = self.pins[i][1]
                self.pins.remove(self.pins[i])
                break

        if piece.position[0] == 6:
            if not piece_pinned or pin_direction == [-1, 0]:
                if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                    self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] - 1, piece.position[1]], piece,
                         None])
                if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                    if (board[piece.position[0] - 2][piece.position[1]].is_empty == True):
                        self.white_pawn_moves.append(board[piece.position[0] - 2][piece.position[1]])
                        self.possibleMoves.append(
                            [piece.position, [piece.position[0] - 2, piece.position[1]], piece,
                             None])
            # captures
            if piece.position[0] - 1 >= 0 and piece.position[1] + 1 <= 7:  # captures towards right
                if not piece_pinned or pin_direction == [-1, 1]:
                    if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                        captured_piece = board[piece.position[0] - 1][piece.position[1] + 1].piece
                        if (board[piece.position[0] - 1][piece.position[1] + 1].piece.color == 'black'):# and (
                                #board[piece.position[0] - 1][piece.position[1] + 1].piece.name != 'king'):
                            self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] - 1, piece.position[1] + 1], piece,
                                     captured_piece])
            if piece.position[0] - 1 >= 0 and piece.position[1] - 1 >= 0:  # captures towards left
                if not piece_pinned or pin_direction == [-1, -1]:
                    if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                        captured_piece = board[piece.position[0] - 1][piece.position[1] - 1].piece
                        if (board[piece.position[0] - 1][piece.position[1] - 1].piece.color == 'black'):# and (
                                #board[piece.position[0] - 1][piece.position[1] - 1].piece.name != 'king'):
                            self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] - 1, piece.position[1] - 1], piece,
                                     captured_piece])

        elif piece.position[0] in [5, 4, 3, 2]:
            if not piece_pinned or pin_direction == [-1, 0]:
                if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                    self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] - 1, piece.position[1]], piece,
                         None])

            # captures
            if piece.position[0] - 1 >= 0 and piece.position[1] + 1 <= 7:  # captures towards right
                if not piece_pinned or pin_direction == [-1, 1]:
                    if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                        captured_piece = board[piece.position[0] - 1][piece.position[1] + 1].piece
                        if (board[piece.position[0] - 1][piece.position[1] + 1].piece.color == 'black'):# and (
                                #board[piece.position[0] - 1][piece.position[1] + 1].piece.name != 'king'):
                            self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] - 1, piece.position[1] + 1], piece,
                                     captured_piece])

            if piece.position[0] - 1 >= 0 and piece.position[1] - 1 >= 0:
                if not piece_pinned or pin_direction == [-1, -1]:
                    if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                        captured_piece = board[piece.position[0] - 1][piece.position[1] - 1].piece
                        if (board[piece.position[0] - 1][piece.position[1] - 1].piece.color == 'black'):# and (
                                #board[piece.position[0] - 1][piece.position[1] - 1].piece.name != 'king'):
                            self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])
                            self.possibleMoves.append(
                                [piece.position, [piece.position[0] - 1, piece.position[1] - 1], piece,
                                captured_piece])

        # promotion to be added
        elif piece.position[0] == 1:
            if not piece_pinned or pin_direction == [-1, 0]:
                if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                    self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] - 1, piece.position[1]], piece,
                         None])

            # captures and promotes
            if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                if (board[piece.position[0] - 1][piece.position[1] + 1].piece.color == 'black') and (
                        board[piece.position[0] - 1][piece.position[1] + 1].piece.name != 'king'):
                    promotions = ['queen', 'rook', 'bishop', 'knight']
                    for i in promotions:
                        piece.name = i
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
            if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                if (board[piece.position[0] - 1][piece.position[1] - 1].piece.color == 'black') and (
                        board[piece.position[0] - 1][piece.position[1] - 1].piece.name != 'king'):
                    promotions = ['queen', 'rook', 'bishop', 'knight']
                    for i in promotions:
                        piece.name = i
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])

    def get_black_pawn_moves(self, piece, board):
        #self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        piece_pinned = False
        pin_direction = []

        self.check_pins_and_checks(board)
        for i in range(len(self.pins) - 1, -1, -1):
            if piece.position == self.pins[i][0]:
                piece_pinned = True
                pin_direction = self.pins[i][1]
                self.pins.remove(self.pins[i])
                break

        if piece.position[0] == 1:
            if not piece_pinned or pin_direction == [1, 0]:
                if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                    self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
                    self.possibleMoves.append([piece.position, [piece.position[0] + 1, piece.position[1]], piece, None])
                if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                    if (board[piece.position[0] + 2][piece.position[1]].is_empty == True):
                        self.black_pawn_moves.append(board[piece.position[0] + 2][piece.position[1]])
                        self.possibleMoves.append(
                            [piece.position, [piece.position[0] + 2, piece.position[1]], piece, None])

            # captures
            #print(piece.position)
            if piece.position[0] + 1 <= 7 and piece.position[1] + 1 <= 7:
                if not piece_pinned or pin_direction == [1, 1]:
                    if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                        captured_piece = board[piece.position[0] + 1][piece.position[1] + 1].piece
                        if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white'):# and (
                                #board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                            self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] + 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] + 1, piece.position[1] + 1], piece, captured_piece])
            if piece.position[0] + 1 <= 7 and piece.position[1] - 1 >= 0: # captures towards left
                if not piece_pinned or pin_direction == [1, -1]:
                    if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                        captured_piece = board[piece.position[0] + 1][piece.position[1] - 1].piece
                        if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white'):# and (
                                #board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                            self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] - 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] + 1, piece.position[1] - 1], piece,
                                     captured_piece])

        elif piece.position[0] in [5, 4, 3, 2]:
            if not piece_pinned or pin_direction == [1, 0]:
                if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                    self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] + 1, piece.position[1]], piece, None])

            # captures
            if piece.position[0] + 1 <= 7 and piece.position[1] + 1 <= 7: # captures towards right
                if not piece_pinned or pin_direction == [1, 1]:
                    if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                        captured_piece = board[piece.position[0] + 1][piece.position[1] + 1].piece
                        if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white'):# and (
                                #board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                            self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] + 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] + 1, piece.position[1] + 1], piece,
                                     captured_piece])
            if piece.position[0] + 1 <= 7 and piece.position[1] - 1 >= 0: # captures towards left
                if not piece_pinned or pin_direction == [1, -1]:
                    if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                        captured_piece = board[piece.position[0] + 1][piece.position[1] - 1].piece
                        if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white'):# and (
                                #board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                            self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] - 1])
                            self.possibleMoves.append(
                                    [piece.position, [piece.position[0] + 1, piece.position[1] - 1], piece,
                                     captured_piece])

        # promotion to be added
        elif piece.position[0] == 6:
            if not piece_pinned or pin_direction == [1, 0]:
                if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                    #promotions = ['queen', 'rook', 'bishop', 'knight']
                    #for i in promotions:
                    #    piece.name = i
                    self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
                    self.possibleMoves.append(
                        [piece.position, [piece.position[0] + 1, piece.position[1]], piece,
                         None])
            # captures and promotes
            if piece.position[0] + 1 <= 7 and piece.position[1] + 1 <= 7: # captures towards right
                if not piece_pinned or pin_direction == [1, 1]:
                    if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                        captured_piece = board[piece.position[0] + 1][piece.position[1] + 1].piece
                        if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white'):# and (
                                #board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                            promotions = ['queen', 'rook', 'bishop', 'knight']
                            for i in promotions:
                                piece.name = i
                                self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] + 1])
                                self.possibleMoves.append(
                                    [piece.position, [piece.position[0] + 1, piece.position[1] + 1], piece,
                                     captured_piece])
            if piece.position[0] + 1 <= 7 and piece.position[1] - 1 >= 0:  # captures towards left
                if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                    captured_piece = board[piece.position[0] + 1][piece.position[1] - 1].piece
                    if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white'):# and (
                            #board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                        #promotion = input()
                        #for i in promotions:
                            #piece.name = i
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] - 1])
                        self.possibleMoves.append(
                            [piece.position, [piece.position[0] + 1, piece.position[1] - 1], piece,
                            captured_piece])

    def get_possible_moves(self, board):
        #no of lines can be minimized using eval or locals. do it later.
        self.check_pins_and_checks(board)
        if self.whiteToMove:
            if len(self.pieces['king']) > 0:
                for i in self.pieces['king']:
                    self.get_king_moves(i, board)
            if len(self.pieces['pawn']) > 0:
                for i in self.pieces['pawn']:
                    self.get_white_pawn_moves(i, board)
            if len(self.pieces['bishop']) > 0:
                for i in self.pieces['bishop']:
                    self.get_bishop_moves(i, board)
            if len(self.pieces['rook']) > 0:
                for i in self.pieces['rook']:
                    self.get_rook_moves(i, board)
            if len(self.pieces['queen']) > 0:
                for i in self.pieces['queen']:
                    self.get_queen_moves(i, board)
            if len(self.pieces['knight']) > 0:
                for i in self.pieces['knight']:
                    #print(i, i.name, i.position, i.color)
                    self.get_knight_moves(i, board)
            #self.get_castling_moves(self.enemy_pieces['king'][0], board)

        else:
            if len(self.enemy_pieces['king']) > 0:
                for i in self.enemy_pieces['king']:
                    self.get_king_moves(i, board)
            if len(self.enemy_pieces['pawn']) > 0:
                for i in self.enemy_pieces['pawn']:
                    self.get_black_pawn_moves(i, board)
            if len(self.enemy_pieces['knight']) > 0:
                for i in self.enemy_pieces['knight']:
                    self.get_knight_moves(i, board)
            if len(self.enemy_pieces['bishop']) > 0:
                for i in self.enemy_pieces['bishop']:
                    self.get_bishop_moves(i, board)
            if len(self.enemy_pieces['rook']) > 0:
                for i in self.enemy_pieces['rook']:
                    self.get_rook_moves(i, board)
            if len(self.enemy_pieces['queen']) > 0:
                for i in self.enemy_pieces['queen']:
                    self.get_queen_moves(i, board)

            #self.get_castling_moves(self.enemy_pieces['king'][0], board)

    def get_legal_moves(self, piece, board):
        self.selected_piece = piece
        #reseting the variables mentioned below
        self.possibleMoves = list()
        self.legal_moves = list()
        self.rook_moves = list()
        self.knight_moves = list()
        self.bishop_moves = list()
        self.queen_moves = list()
        self.white_pawn_moves = list()
        self.black_pawn_moves = list()
        self.castle_moves = list()
        self.king_moves = list()
        self.in_check = False
        self.pins = list()
        self.checks = list()
        # self.adjustment_dictionary_name = self.selected_piece.color[0].upper()+self.selected_piece.name[0].upper()+self.selected_piece.name[1:]
        #print(self.is_king_in_check(board))
        self.check_pins_and_checks(board)
        if self.whiteToMove:
            kingsq = self.wking_loc
            king = self.pieces['king'][0]
        else:
            kingsq = self.bking_loc
            king = self.enemy_pieces['king'][0]
            # board[kingsq[0]][kingsq[1]].piece
        if self.in_check:
            if len(self.checks) == 1: #single check, hence it can be blocked or king can be moved
                self.get_possible_moves(board)
                moves = self.possibleMoves
                #print(self.checks)
                check_row = self.checks[0][0][0]
                check_col = self.checks[0][0][1]
                #print(check_row, check_col)
                piece_checking = board[check_row][check_col].piece
                valid_squares = [] #squares that pieces can move to (apart from king moves)
                if piece_checking.name == 'knight':
                    valid_squares = [[check_row, check_col]]
                else:
                    for i in range(8):
                        valid_square = [kingsq[0] + self.checks[0][1][0] * i,
                                        kingsq[1] + self.checks[0][1][1] * i]
                        valid_squares.append(valid_square) #if piece_checking = bishop, valid_squares will contain all coordinates
                                                            #between king and bishop(excluding bishop and including king)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i][2].name != 'king':
                        if not moves[i][1] in valid_squares: #remove those moves whose destination is not in valid squares
                            moves.remove(moves[i])
                        elif moves[i][2].color != king.color: #even piece_checking's color moves were included in moves, so need to remove them.
                            moves.remove(moves[i])
                #for move in moves:
                #    print(move[0], move[1], move[2].name, move[2].color, move[3] , end = " ")
                #print("\n")
                if len(moves) > 0:
                    for i in range(len(moves)):
                        if moves[i][2] == piece:
                            self.legal_moves.append(board[moves[i][1][0]][moves[i][1][1]])
                elif len(moves) == 0:
                    self.checkmate = True
                    print("CheckMate!!!!!")

            else: #double check
                self.get_king_moves(board[kingsq[0]][kingsq[1]].piece, board)
                moves = self.possibleMoves

                if len(moves) > 0:
                    for i in range(len(moves)):
                        if moves[i][2] == piece:
                            self.legal_moves.append(board[moves[i][1][0]][moves[i][1][1]])
                elif len(moves) == 0:
                    self.checkmate = True
                    print("CheckMate!!!!!")

        else:
            self.get_possible_moves(board)
            moves = self.possibleMoves

            if len(moves) > 0:
                for i in range(len(moves)):
                    if moves[i][2] == piece:
                        self.legal_moves.append(board[moves[i][1][0]][moves[i][1][1]]) #appending board[destination[0]][destination[1]]
            self.possibleMoves = list()
            self.get_castling_moves(board)
            castling_moves = self.possibleMoves
            if len(castling_moves) > 0:
                for i in range(len(castling_moves)):
                    if castling_moves[i][2] == piece:
                        self.legal_moves.append(board[castling_moves[i][1][0]][castling_moves[i][1][1]])

            if len(moves) == 0:
                self.stalemate = True
                print("Stalemate!!!!")
