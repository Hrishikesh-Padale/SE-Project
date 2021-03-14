class Moves_manager:
	def __init__(self):
		self.pieces	 = {}
		self.legal_moves = []
		self.selected_piece = None
		self.adjustment_dictionary_name = None

	def get_legal_moves(self,piece,board):
		self.selected_piece = piece
		self.adjustment_dictionary_name = self.selected_piece.color[0].upper()+self.selected_piece.name[0].upper()+self.selected_piece.name[1:]
		if piece.name == 'pawn':
			self.legal_moves=[board[piece.position[0]-1][piece.position[1]],board[piece.position[0]-2][piece.position[1]]]
		else:
			self.legal_moves = []

																			

