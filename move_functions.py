from functions import *
class Moves_manager:
    def __init__(self):
        self.pieces	 = {}
        self.legal_moves = list()
        self.selected_piece = None
        self.adjustment_dictionary_name = None

    def get_legal_moves(self,piece,board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper()+self.selected_piece.name[0].upper()+self.selected_piece.name[1:]
        if piece.name == 'pawn' and piece.color == 'white':
            
            if piece.position[0] == 6:
                if (board[piece.position[0]-1][piece.position[1]].is_empty == True):
                    self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])
                if (board[piece.position[0]-2][piece.position[1]].is_empty == True):
                    self.legal_moves.append(board[piece.position[0]-2][piece.position[1]])
                    
                #captures
                if board[piece.position[0]-1][piece.position[1]+1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]+1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]+1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
                if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]-1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]-1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])
                    
            elif piece.position[0] in [5, 4, 3, 2]:
                if (board[piece.position[0]-1][piece.position[1]].is_empty == True):
                    self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])
                    
                #captures
                if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]+1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]+1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 1])
                if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]-1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]-1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 1])
            
            #promotion to be added
            elif piece.position[0] == 1:
                if (board[piece.position[0] - 1][piece.position[1]].is_empty == True):
                    promotions = ['queen', 'rook', 'bishop', 'knight']
                    for i in promotions:
                        piece.name = i
                        self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])
                #captures and promotes
                if board[piece.position[0] - 1][piece.position[1] + 1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]+1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]+1].piece.name != 'king'):
                        promotions = ['queen', 'rook', 'bishop', 'knight']
                        for i in promotions:
                            piece.name = i
                            self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])
                if board[piece.position[0] - 1][piece.position[1] - 1].is_empty == False:
                    if (board[piece.position[0]-1][piece.position[1]-1].piece.color == 'black') and (board[piece.position[0]-1][piece.position[1]-1].piece.name != 'king'):
                        promotions = ['queen', 'rook', 'bishop', 'knight']
                        for i in promotions:
                            piece.name = i
                            self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])

        elif piece.name == 'knight':

            #print(piece.position)
            self.legal_moves = list()
            if piece.position[0] - 1 >= 0 and piece.position[1] + 2 <= 7:

                if board[piece.position[0] - 1][piece.position[1] + 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 2])
                #captures
                else:
                    if (board[piece.position[0] - 1][piece.position[1] + 2].piece.color == 'black') and (board[piece.position[0] - 1][piece.position[1] + 2].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 2])

            if piece.position[0] - 1 >= 0 and piece.position[1] - 2 >= 0:
                if board[piece.position[0] - 1][piece.position[0] - 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 2])
                #captures
                else:
                    if (board[piece.position[0] - 1][piece.position[0] - 2].piece.color == 'black') and (board[piece.position[0] - 1][piece.position[0] -2].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 2])

            if piece.position[0] + 1 <= 7 and piece.position[1] + 2 <= 7:
                if board[piece.position[0] + 1][piece.position[0] + 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] + 2])
                #captures
                else:
                    if (board[piece.position[0] + 1][piece.position[0] + 2].piece.color == 'black') and (board[piece.position[0] + 1][piece.position[0] + 2].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] + 2])

            if piece.position[0] + 1 <= 7 and piece.position[1] - 2 >= 0:
                if board[piece.position[0] + 1][piece.position[0] - 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] - 2])
                #captures
                else:
                    if (board[piece.position[0] + 1][piece.position[0] - 2].piece.color == 'black') and (board[piece.position[0] + 1][piece.position[0] - 2].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] - 2])

            if piece.position[0] + 2 <= 7 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] + 2][piece.position[0] + 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] + 1])
                #captures
                else:
                    if (board[piece.position[0] + 2][piece.position[0] + 1].piece.color == 'black') and (board[piece.position[0] + 2][piece.position[0] + 1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] + 1])

            if piece.position[0] + 2 <= 7 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] + 2][piece.position[0] - 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] - 1])
                #captures
                else:
                    if (board[piece.position[0] + 2][piece.position[0] - 1].piece.color == 'black') and (board[piece.position[0] + 2][piece.position[0] - 1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] - 1])

            if piece.position[0] - 2 >= 0 and piece.position[1] + 1 <= 7:
                #print(piece.position)
                #print(board[piece.position[0] - 2][piece.position[1]])
                if board[piece.position[0] - 2][piece.position[1] +1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] + 1])
                #captures
                else:
                    if (board[piece.position[0] - 2][piece.position[0] + 1].piece.color == 'black') and (board[piece.position[0] - 2][piece.position[0] + 1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] + 1])

            if piece.position[0] - 2 >= 0 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] - 2][piece.position[0] - 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] - 1])
                #captures
                else:
                    if (board[piece.position[0] - 2][piece.position[0] -1].piece.color == 'black') and (board[piece.position[0] - 2][piece.position[0] -1].piece.name != 'king'):
                        self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] - 1])

        elif piece.name == 'rook':
            self.legal_moves = list()
            if piece.position[0] != 7:
                for i in range(piece.position[0] + 1, 8):
                    if (board[i][piece.position[1]].is_empty == True):
                        self.legal_moves.append(board[i][piece.position[1]])

                    #captures
                    else:
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][piece.position[1]].piece.name != 'king'):
                            self.legal_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break

            if piece.position[0] != 0:
                for i in range(piece.position[0] - 1, -1, -1):
                    if (board[i][piece.position[1]].is_empty == True) :
                        self.legal_moves.append(board[i][piece.position[1]])

                    #captures
                    else:
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][piece.position[1]].piece.name != 'king'):
                            self.legal_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break

            if piece.position[1] != 7:
                for i in range(piece.position[1] + 1, 8):
                    if (board[piece.position[0]][i].is_empty == True):
                        self.legal_moves.append(board[piece.position[0]][i])

                    #captures
                    else:
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][i].piece.name != 'king'):
                            self.legal_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break
            if piece.position[1] != 0:
                for i in range(piece.position[1] - 1, -1, -1):
                    if (board[piece.position[0]][i].is_empty == True):
                        self.legal_moves.append(board[piece.position[0]][i])

                    #captures
                    else:
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][i].piece.name != 'king'):
                            self.legal_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break

        elif piece.name == 'queen':
            self.legal_moves = list()
            if piece.position[0] != 7:
                for i in range(piece.position[0] + 1, 8):
                    if (board[i][piece.position[1]].is_empty == True):
                        self.legal_moves.append(board[i][piece.position[1]])

                    #captures
                    else:
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][piece.position[1]].piece.name != 'king'):
                            self.legal_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break

            if piece.position[0] != 0:
                for i in range(piece.position[0] - 1, -1, -1):
                    if (board[i][piece.position[1]].is_empty == True) :
                        self.legal_moves.append(board[i][piece.position[1]])

                    #captures
                    else:
                        if (board[i][piece.position[1]].piece.color == 'black' and board[i][piece.position[1]].piece.name != 'king'):
                            self.legal_moves.append(board[i][piece.position[1]])
                            break
                        elif board[i][piece.position[1]].piece.color == 'white':
                            break

            if piece.position[1] != 7:
                for i in range(piece.position[1] + 1, 8):
                    if (board[piece.position[0]][i].is_empty == True):
                        self.legal_moves.append(board[piece.position[0]][i])

                    #captures
                    else:
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][i].piece.name != 'king'):
                            self.legal_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break

            if piece.position[1] != 0:
                for i in range(piece.position[1] - 1, -1, -1):
                    if (board[piece.position[0]][i].is_empty == True):
                        self.legal_moves.append(board[piece.position[0]][i])

                    #captures
                    else:
                        if (board[piece.position[0]][i].piece.color == 'black' and board[piece.position[0]][i].piece.name != 'king'):
                            self.legal_moves.append(board[piece.position[0]][i])
                            break
                        elif board[piece.position[0]][i].piece.color == 'white':
                            break

            if piece.position[0] != 7 and piece.position[1] != 7:
                i = piece.position[0] + 1
                j = piece.position[1] + 1

                while i <= 7 and j <= 7:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i += 1
                        j += 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 0 and piece.position[1] != 0:
                i = piece.position[0] - 1
                j = piece.position[1] - 1

                while i >= 0 and j >= 0:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i -= 1
                        j -= 1
                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 0 and piece.position[1] != 7:
                i = piece.position[0] - 1
                j = piece.position[1] + 1

                while i >= 0 and j <= 7:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i -= 1
                        j += 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 7 and piece.position[1] != 0:
                i = piece.position[0] + 1
                j = piece.position[1] - 1

                while i <= 7 and j >= 0:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i += 1
                        j -= 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

        elif piece.name == 'bishop':
            if piece.position[0] != 7 and piece.position[1] != 7:
                i = piece.position[0] + 1
                j = piece.position[1] + 1

                while i <= 7 and j <= 7:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i += 1
                        j += 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 0 and piece.position[1] != 0:
                i = piece.position[0] - 1
                j = piece.position[1] - 1

                while i >= 0 and j >= 0:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i -= 1
                        j -= 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 0 and piece.position[1] != 7:
                i = piece.position[0] - 1
                j = piece.position[1] + 1

                while i >= 0 and j <= 7:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i -= 1
                        j += 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break

            if piece.position[0] != 7 and piece.position[1] != 0:
                i = piece.position[0] + 1
                j = piece.position[1] - 1

                while i <= 7 and j >= 0:
                    if (board[i][j].is_empty == True):
                        self.legal_moves.append(board[i][j])
                        i += 1
                        j -= 1

                    #captures
                    else:
                        if (board[i][j].piece.color == 'black' and board[i][j].piece.name != 'king'):
                            self.legal_moves.append(board[i][j])
                            break
                        elif board[i][j].piece.color == 'white':
                            break



        else:
            self.legal_moves = list()