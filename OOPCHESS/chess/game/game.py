from copy import deepcopy
from chess.pieces.piece import Piece
from chess.render.render import *
from chess.moves.moves import *
from chess.board.board import ChessBoard

class ChessGameState:
	def __init__(self, pieces, board_size):
		self.pieces = pieces
		self.board_size = board_size


class ChessGame:
	STATUS_WHITE_MOVE = "white_move"
	STATUS_BLACK_MOVE = "black_move"
	STATUS_WHITE_VICTORY = "white_victory"
	STATUS_BLACK_VICTORY = "black_victory"

	def __init__(self, renderer: InputRender = None):
		self._finished = False
		self._board = ChessBoard()
		self._renderer = renderer
		self._status = ChessGame.STATUS_WHITE_MOVE

	def run(self):
		self._renderer.render(self.get_game_state())
		while not self._finished:
			input = self._renderer.get_input()

			command = self._parse_command(input)
			if command is None:
				pass
			elif not self._try_move(command):
				self._renderer.print_line("Invalid command, please re-enter.")
			else:
				self._board.execute_move(command)			
				if self._status == ChessGame.STATUS_WHITE_MOVE:
					self._status = ChessGame.STATUS_BLACK_MOVE
				elif self._status == ChessGame.STATUS_BLACK_MOVE:
					self._status = ChessGame.STATUS_WHITE_MOVE

			self._renderer.render(self.get_game_state())
	
	def _try_move(self, command: MoveCommand):
		board_copy = deepcopy(self._board)
		src_piece = board_copy.get_piece(command.src)
		if src_piece is None:
			return False
		if (self._status == ChessGame.STATUS_WHITE_MOVE and src_piece.color == Piece.BLACK) or \
				(self._status == ChessGame.STATUS_BLACK_MOVE and src_piece.color == Piece.WHITE):
			return False
		if command.dst not in src_piece.get_moveable_positions(board_copy) and \
				command.dst not in src_piece.get_threatened_positions(board_copy):
			return False
		board_copy.execute_move(command)
		for piece in board_copy.pieces:
			if self._status == ChessGame.STATUS_WHITE_MOVE and \
					board_copy.white_king_position in piece.get_threatened_positions(board_copy):
				return False
			elif self._status == ChessGame.STATUS_BLACK_MOVE and \
					board_copy.black_king_position in piece.get_threatened_positions(board_copy):
				return False
		return True

	def _parse_command(self, input_):
		#input_ = input()
		return MoveCommand.from_string(input_)

	def get_game_state(self):
		return ChessGameState(self._board.pieces, self._board.size)