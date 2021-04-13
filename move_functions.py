from functions import *
class Moves_manager:
    def __init__(self):
        self.pieces	 = {}
        self.enemy_pieces = {}
        self.legal_moves = list()
        self.selected_piece = None
        self.adjustment_dictionary_name = None
        self.wking_loc = list()
        self.bking_loc = list()

    def get_king_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.king_moves = list()
        possible_moves = [[-1, 0], [-1, 1], [0, 1], [1, 1],
                          [1, 0], [1, -1], [0, -1], [-1, -1]]
        #modification needed for including castling, checks, checkmate, stalemate
        for pos in possible_moves:
            if (piece.position[0] + pos[0] >= 0) and (piece.position[1] + pos[1] >= 0) and (
                    piece.position[0] + pos[0] <= 7) and (piece.position[1] + pos[1] <= 7):
                if board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].is_empty == True:
                    self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'black') and (
                            board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                    else:
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'white') and (
                            board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.king_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
        return self.king_moves


    def get_knight_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.knight_moves = list()
        possible_moves = [[-1, 2], [-1, -2], [1, 2], [1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        for pos in possible_moves:
            if (piece.position[0] + pos[0] >= 0) and (piece.position[1] + pos[1] >= 0) and (
                    piece.position[0] + pos[0] <= 7) and (piece.position[1] + pos[1] <= 7):

                if board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].is_empty == True:
                    self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'black') and (
                            board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])
                    else:
                        if (board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.color == 'white') and (
                            board[piece.position[0] + pos[0]][piece.position[1] + pos[1]].piece.name != 'king'):
                            self.knight_moves.append(board[piece.position[0] + pos[0]][piece.position[1] + pos[1]])


        return self.knight_moves

    def get_rook_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.rook_moves = list()
        if piece.position[0] != 7:
            for i in range(piece.position[0] + 1, 8):
                if (board[i][piece.position[1]].is_empty == True):
                    self.rook_moves.append(board[i][piece.position[1]])

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][
                            piece.position[1]].piece.name != 'king'):
                            self.rook_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break
                    else:
                        if (board[i][piece.position[1]].piece.color == 'white' and board[i][
                            piece.position[1]].piece.name != 'king'):
                            self.rook_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'black':
                            break

        if piece.position[0] != 0:
            for i in range(piece.position[0] - 1, -1, -1):
                if (board[i][piece.position[1]].is_empty == True):
                    self.rook_moves.append(board[i][piece.position[1]])

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][
                            piece.position[1]].piece.name != 'king'):
                            self.rook_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break
                    else:
                        if (board[i][piece.position[1]].piece.color == 'white' and board[i][
                            piece.position[1]].piece.name != 'king'):
                            self.rook_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'black':
                            break


        if piece.position[1] != 7:
            for i in range(piece.position[1] + 1, 8):
                if (board[piece.position[0]][i].is_empty == True):
                    self.rook_moves.append(board[piece.position[0]][i])

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][
                            i].piece.name != 'king'):
                            self.rook_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break
                    else:
                        if (board[piece.position[0]][i].piece.color == 'white' and board[
                            piece.position[0]][i].piece.name != 'king'):
                            self.rook_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'black':
                            break
        if piece.position[1] != 0:
            for i in range(piece.position[1] - 1, -1, -1):
                if (board[piece.position[0]][i].is_empty == True):
                    self.rook_moves.append(board[piece.position[0]][i])

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][
                            i].piece.name != 'king'):
                            self.rook_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break
                    else:
                        if (board[piece.position[0]][i].piece.color == 'white' and board[piece.position[0]][
                            i].piece.name != 'king'):
                            self.rook_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'black':
                            break

        return self.rook_moves

    def get_bishop_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.bishop_moves = list()

        if piece.position[0] != 7 and piece.position[1] != 7:
            i = piece.position[0] + 1
            j = piece.position[1] + 1

            while i <= 7 and j <= 7:
                if (board[i][j].is_empty == True):
                    self.bishop_moves.append(board[i][j])
                    i += 1
                    j += 1

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break
                    else:
                        if (board[i][j].piece.color == 'white' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'black':
                            break


        if piece.position[0] != 0 and piece.position[1] != 0:
            i = piece.position[0] - 1
            j = piece.position[1] - 1

            while i >= 0 and j >= 0:
                if (board[i][j].is_empty == True):
                    self.bishop_moves.append(board[i][j])
                    i -= 1
                    j -= 1

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break
                    else:
                        if (board[i][j].piece.color == 'white' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'black':
                            break

        if piece.position[0] != 0 and piece.position[1] != 7:
            i = piece.position[0] - 1
            j = piece.position[1] + 1

            while i >= 0 and j <= 7:
                if (board[i][j].is_empty == True):
                    self.bishop_moves.append(board[i][j])
                    i -= 1
                    j += 1

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break
                    else:
                        if (board[i][j].piece.color == 'white' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'black':
                            break

        if piece.position[0] != 7 and piece.position[1] != 0:
            i = piece.position[0] + 1
            j = piece.position[1] - 1

            while i <= 7 and j >= 0:
                if (board[i][j].is_empty == True):
                    self.bishop_moves.append(board[i][j])
                    i += 1
                    j -= 1

                # captures
                else:
                    if self.selected_piece.color == 'white':
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break
                    else:
                        if (board[i][j].piece.color == 'white' and board[i][j].piece.name != 'king'):
                            self.bishop_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'black':
                            break
        return self.bishop_moves

    def get_queen_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.queen_moves = self.get_rook_moves(piece, board)
        temp = self.get_bishop_moves(piece, board)
        if temp is not None:
            for i in temp:
                self.queen_moves.append(i)
        return self.queen_moves

    def get_white_pawn_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.white_pawn_moves = list()

        if piece.position[0] == 6:
            if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
            if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                if (board[piece.position[0] - 2][piece.position[1]].is_empty == True):
                    self.white_pawn_moves.append(board[piece.position[0] - 2][piece.position[1]])

            # captures
            if piece.position[0] - 1 >= 0 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0] - 1][piece.position[1] + 1].piece.color == 'black') and (
                        board[piece.position[0] - 1][piece.position[1] + 1].piece.name != 'king'):
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
            if piece.position[0] - 1 >= 0 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0] - 1][piece.position[1] - 1].piece.color == 'black') and (
                        board[piece.position[0] - 1][piece.position[1] - 1].piece.name != 'king'):
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])

        elif piece.position[0] in [5, 4, 3, 2]:
            if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])

            # captures
            if piece.position[0] - 1 >= 0 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0] - 1][piece.position[1] + 1].piece.color == 'black') and (
                            board[piece.position[0] - 1][piece.position[1] + 1].piece.name != 'king'):
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
            if piece.position[0] - 1 >= 0 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0] - 1][piece.position[1] - 1].piece.color == 'black') and (
                            board[piece.position[0] - 1][piece.position[1] - 1].piece.name != 'king'):
                        self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])

        # promotion to be added
        elif piece.position[0] == 1:
            if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                promotions = ['queen', 'rook', 'bishop', 'knight']
                for i in promotions:
                    piece.name = i
                    self.white_pawn_moves.append(board[piece.position[0] - 1][piece.position[1]])
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
        return self.white_pawn_moves

    def get_black_pawn_moves(self, piece, board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper() + self.selected_piece.name[
            0].upper() + self.selected_piece.name[1:]

        self.black_pawn_moves = list()

        if piece.position[0] == 1:
            if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
            if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                if (board[piece.position[0] + 2][piece.position[1]].is_empty == True):
                    self.black_pawn_moves.append(board[piece.position[0] + 2][piece.position[1]])

            # captures
            #print(piece.position)
            if piece.position[0] + 1 <= 7 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white') and (
                            board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] + 1])
            if piece.position[0] + 1 <= 7 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white') and (
                            board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] - 1])

        elif piece.position[0] in [5, 4, 3, 2]:
            if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])

            # captures
            if piece.position[0] + 1 <= 7 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white') and (
                            board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] + 1])
            if piece.position[0] + 1 <= 7 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white') and (
                            board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1] - 1])

        # promotion to be added
        elif piece.position[0] == 6:
            if (board[piece.position[0] + 1][piece.position[1]].is_empty == True):
                promotions = ['queen', 'rook', 'bishop', 'knight']
                for i in promotions:
                    piece.name = i
                    self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
            # captures and promotes
            if board[piece.position[0] + 1][piece.position[1] + 1].is_empty == False:
                if (board[piece.position[0] + 1][piece.position[1] + 1].piece.color == 'white') and (
                        board[piece.position[0] + 1][piece.position[1] + 1].piece.name != 'king'):
                    promotions = ['queen', 'rook', 'bishop', 'knight']
                    for i in promotions:
                        piece.name = i
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
            if board[piece.position[0] + 1][piece.position[1] - 1].is_empty == False:
                if (board[piece.position[0] + 1][piece.position[1] - 1].piece.color == 'white') and (
                        board[piece.position[0] + 1][piece.position[1] - 1].piece.name != 'king'):
                    promotions = ['queen', 'rook', 'bishop', 'knight']
                    for i in promotions:
                        piece.name = i
                        self.black_pawn_moves.append(board[piece.position[0] + 1][piece.position[1]])
        return self.black_pawn_moves

    def get_legal_moves(self,piece,board):
        self.selected_piece = piece
        #self.adjustment_dictionary_name = self.selected_piece.color[0].upper()+self.selected_piece.name[0].upper()+self.selected_piece.name[1:]
        #self.pin_and_check(board)
        if piece.name == 'pawn' and piece.color == 'white':
            self.legal_moves = self.get_white_pawn_moves(piece, board)

        elif piece.name == 'pawn' and piece.color == 'black':
            self.legal_moves = self.get_black_pawn_moves(piece, board)

        elif piece.name == 'knight':
            self.legal_moves = self.get_knight_moves(piece, board)

        elif piece.name == 'rook':
            self.legal_moves = self.get_rook_moves(piece, board)

        elif piece.name == 'queen':
            self.legal_moves = self.get_queen_moves(piece, board)

        elif piece.name == 'bishop':
            self.legal_moves = self.get_bishop_moves(piece, board)

        elif piece.name == 'king':
            self.legal_moves = self.get_king_moves(piece, board)

        else:
            self.legal_moves = list()