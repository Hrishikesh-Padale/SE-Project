class Moves_manager:
    def __init__(self):
        self.pieces	 = {}
        self.legal_moves = []
        self.selected_piece = None
        self.adjustment_dictionary_name = None

    def get_legal_moves(self,piece,board):
        self.selected_piece = piece
        self.adjustment_dictionary_name = self.selected_piece.color[0].upper()+self.selected_piece.name[0].upper()+self.selected_piece.name[1:]
        self.legal_moves = list()
        if piece.name == 'pawn':
            if piece.is_at_start:
                self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])
                self.legal_moves.append(board[piece.position[0]-2][piece.position[1]])
                piece.is_at_start = False
            else:
                self.legal_moves.append(board[piece.position[0]-1][piece.position[1]])

        elif piece.name == 'knight':
            if piece.position[0] - 1 >= 0 and piece.position[1] + 2 <= 7:
                if board[piece.position[0] - 1][piece.position[0] + 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 2])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] + 2])

            elif piece.position[0] - 1 >= 0 and piece.position[1] - 2 >= 0:
                if board[piece.position[0] - 1][piece.position[0] - 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 2])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] - 1][piece.position[1] - 2])

            elif piece.position[0] + 1 <= 7 and piece.position[1] + 2 <= 7:
                if board[piece.position[0] + 1][piece.position[0] + 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] + 2])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] + 2])

            elif piece.position[0] + 1 <= 7 and piece.position[1] - 2 >= 0:
                if board[piece.position[0] + 1][piece.position[0] - 2].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] - 2])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] + 1][piece.position[1] - 2])

            elif piece.position[0] + 2 <= 7 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] + 2][piece.position[0] + 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] + 1])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] + 1])

            elif piece.position[0] + 2 <= 7 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] + 2][piece.position[0] - 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] - 1])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] + 2][piece.position[1] - 1])

            elif piece.position[0] - 2 >= 0 and piece.position[1] + 1 <= 7:
                if board[piece.position[0] - 2][piece.position[0] + 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] + 1])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] + 1])

            elif piece.position[0] - 2 >= 0 and piece.position[1] - 1 >= 0:
                if board[piece.position[0] - 2][piece.position[0] - 1].is_empty == True:
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] - 1])
                if piece.color == 'black' and piece.name != 'king':
                    self.legal_moves.append(board[piece.position[0] - 2][piece.position[1] - 1])