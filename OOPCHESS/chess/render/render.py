import pygame

from chess.moves.moves import ChessPosition

class InputRender:
	def render(self, game_state):
		raise NotImplementedError

	def print_line(self, string):
		raise NotImplementedError

class WindowRender(InputRender):

	BLACK = (50, 50, 50)
	WHITE = (200 ,200, 200)

	def __init__(self):
		pygame.init()
		self._screen = pygame.display.set_mode([1000, 1000])

		self._clock = pygame.time.Clock()

		self._squares = []
		self._input = []

		self._message = ''
		self._message_start_time = 0
		self._message_duration = 2000

	def render(self, game_state):
		
		n = game_state.board_size

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

			if event.type == pygame.MOUSEBUTTONUP:
				self._handle_input(pygame.mouse.get_pos(), n)

		self._screen.fill((0, 0, 0))

		if((pygame.time.get_ticks() - self._message_start_time) < self._message_duration):
			font = pygame.font.Font('freesansbold.ttf', 32)
			text = font.render(self._message, True, (200, 0 ,0))
			textRect = text.get_rect()
			textRect.center = (self._screen.get_width() / 2, self._screen.get_height() * 0.95)
			self._screen.blit(text, textRect)

		board = pygame.draw.rect(self._screen, 
								(133, 129, 127), 
								pygame.Rect(self._screen.get_width() * 0.1, self._screen.get_height() * 0.1, self._screen.get_width() * 0.8, self._screen.get_height() * 0.8))

		squares = pygame.draw.rect(self._screen, 
								(0, 0, 0), 
								pygame.Rect(board.left + board.w * 0.05, board.top + board.h * 0.05, board.width * 0.9, board.height * 0.9))

		

		if game_state is None:
			pass
		else:
			self._squares = []
			for i in range(n):
				for j in range(n):

					if((i+j)%2==0):
						color = WindowRender.WHITE
					else: 
						color = WindowRender.BLACK

					square_size = squares.w / n

					square = pygame.draw.rect(self._screen,
							color,
							pygame.Rect(squares.left + square_size * j, squares.top + square_size * i, square_size, square_size))

					self._squares.append(square)

					for piece in game_state.pieces:
						if(piece.position.x_coord==j and piece.position.y_coord==(n-1-i)):
							image = pygame.image.load(f"chess/render/images/{piece.piece_type()}{piece.color}.png")
							image = pygame.transform.scale(image, (square_size, square_size))
							image = image.convert_alpha()


							self._screen.blit(image, (square.left, square.top))
							break

		pygame.display.flip()
		self._clock.tick(60)

	def _handle_input(self, mouse_position, board_size):
		
		for index, square in enumerate(self._squares):
			if(square.left < mouse_position[0] and square.right > mouse_position[0] and square.top < mouse_position[1] and square.bottom > mouse_position[1]):
				row = 8 - (index // board_size)
				column = (index % board_size) + 1
				if len(self._input) == 2:
					return
				
				self._input.append((row, column))

	def get_input(self):
		if(len(self._input) != 2):
			return ""

		from_position = self._input[0]
		to_position = self._input[1]

		from_column = from_position[1]
		to_column = to_position[1]

		from_column = chr(ord("a") + from_column -1)
		to_column = chr(ord("a") + to_column -1)

		self._input = []
		return f"{from_column}{from_position[0]} {to_column}{to_position[0]}"


	def print_line(self, string):
		self._message_start_time = pygame.time.get_ticks()
		self._message = string



class ConsoleRender(InputRender):
	def render(self, game):
		for i in reversed(range(0, game.board_size)):
			self._draw_board_line(i, game.pieces, game.board_size)
		self._draw_bottom_line(game.board_size)

	def print_line(self, string):
		print(string)

	def _draw_time_line(self, countdown_white, countdown_black):
		print("Time remaining: {}s W / B {}s".format(countdown_white, countdown_black))

	def _draw_board_line(self, line_number, pieces, board_size):
		empty_square = " "
		white_square_prefix = "\u001b[47m"
		black_square_prefix = "\u001b[40m"
		reset_suffix = "\u001b[0m"
		black_first_offset = line_number % 2

		legend = "{:<2} ".format(line_number + 1)
		print(legend, end='')
		for i in range(0, board_size):
			is_black = (i + black_first_offset) % 2
			prefix = black_square_prefix if is_black else white_square_prefix
			contents = empty_square
			curr_position = ChessPosition(i, line_number)
			for piece in pieces:
				if curr_position == piece.position:
					contents = piece.symbol()
			square_str = prefix + contents + reset_suffix
			print(square_str, end='')
		print()

	def _draw_bottom_line(self, board_size):
		vertical_legend_offset = 3
		line = " " * vertical_legend_offset
		for i in range(0, board_size):
			line += chr(ord("a") + i)
		print(line)
